
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketServerFactory, WebSocketServerProtocol, \
    listenWS, WebSocketClientFactory, connectWS

from twisted.internet import interfaces, reactor
from twisted.python import url as twisted_url
from zope.interface import implementer
from logging import getLogger
import json
import six
from ebu_tt_live.strings import ERR_WS_INVALID_ACTION, ERR_WS_NOT_CONSUMER, ERR_WS_NOT_PRODUCER, \
    ERR_WS_RECEIVE_VIA_PRODUCER, ERR_WS_SEND_VIA_CONSUMER

from .base import IBroadcaster


log = getLogger(__name__)


class UserInputServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        try:
            self.factory.write(payload)
        except Exception as e:
            self.sendMessage("ERROR: " + str(e))
            return
        self.sendMessage('SUCCESS')

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)

    def sendMessage(self, payload, isBinary=False, fragmentSize=None, sync=False, doNotCompress=False):
        super(UserInputServerProtocol, self).sendMessage(
            payload=payload,
            isBinary=isBinary,
            fragmentSize=fragmentSize,
            sync=sync,
            doNotCompress=doNotCompress
        )


@implementer(IBroadcaster, interfaces.IConsumer)
class UserInputServerFactory(WebSocketServerFactory):
    _consumer = None
    _clients = None

    def __init__(self, url, consumer):
        super(UserInputServerFactory, self).__init__(url, protocols=[13])
        self._consumer = consumer
        self._consumer.registerProducer(self, True)
        self._clients = []

    def write(self, data):
        self._consumer.write(data)

    def resumeProducing(self):
        pass

    def register(self, client):
        if client not in self._clients:
            log.info("registered client {}".format(client.peer))
            self._clients.append(client)

    def unregister(self, client):
        if client in self._clients:
            log.info("unregistered client {}".format(client.peer))
            self._clients.remove(client)

    def listen(self):
        listenWS(self)


class EBUWebsocketProtocolMixin(object):
    """
    This mixin exists because the WS protocol suggested in EBU-3370s1 is agnostic of client-server relationship
    in the sense that data can be streamed from client to server or the other way around. Based on which action
    a server/client is doing different functions should be available. This class holds the common logic.
    """

    _sequence_identifier = None
    _action = None
    _path_format = u'{sequence_identifier}/{action}'
    _valid_actions = [
        'publish',
        'subscribe'
    ]
    _consumer = None

    @property
    def consumer(self):
        return self._consumer

    @consumer.setter
    def consumer(self, value):
        # TODO: Some checks here
        self._consumer = value

    def _parse_path(self, full_url):
        if not isinstance(full_url, six.text_type):
            full_url = six.text_type(full_url)
        result = twisted_url.URL.fromText(full_url).asIRI()
        sequence_identifier, action = result.path
        return sequence_identifier, action

    def _write_to_consumer(self, data):
        # Consumer mode
        # TODO: This can error in multiple ways
        self.consumer.write(data)

    def _send_sequence_message(
            self, sequence_identifier, payload, isBinary=False, fragmentSize=None, sync=False, doNotCompress=False
        ):
        if sequence_identifier == self._sequence_identifier:
            self.sendMessage(
                payload=payload,
                isBinary=isBinary,
                fragmentSize=fragmentSize,
                sync=sync,
                doNotCompress=doNotCompress
            )
            log.info("message sent to {}".format(self.peer))

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if value not in self._valid_actions:
            raise ValueError(
                ERR_WS_INVALID_ACTION.format(
                    action=value
                )
            )
        self._action = value


@implementer(interfaces.IPushProducer)
class TwistedWSPushProducer(object):
    """
    This is a Twisted Push producer. The concept is related to twisted and it is not the same as our producer
    and consumer nodes.
    """

    _custom_producer = None
    _connections = None
    _callLater = reactor.callLater
    real_port_number = None

    def __init__(self, custom_producer):
        self._custom_producer = custom_producer
        self._custom_producer.register_backend_producer(self)
        self._connections = []

    def emit_data(self, sequence_identifier, data, delay=None):
        if delay is not None:
            deferred = self._callLater(delay, self._do_write, sequence_identifier, data)
            return deferred
        else:
            self._do_write(sequence_identifier, data)
            return True

    def register(self, connection):
        self._connections.append(connection)

    def unregister(self, connection):
        self._connections.remove(connection)

    def _do_write(self, sequence_identifier, data):
        log.info("broadcasting message...")
        for conn in self._connections:
            conn.sendSequenceMessage(
                sequence_identifier=sequence_identifier,
                payload=data.encode("utf-8")
            )

    def resumeProducing(self):
        self._custom_producer.resume_producing()

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


@implementer(interfaces.IConsumer)
class TwistedWSConsumer(object):
    """
    This class wraps the protocol objects.
    """
    _custom_consumer = None
    real_port_number = None

    def __init__(self, custom_consumer):
        self._custom_consumer = custom_consumer

    def register(self, connection):
        connection.consumer = self

    def unregister(self, connection):
        connection.consumer = None

    def write(self, data):
        self._custom_consumer.on_new_data(data)

    def registerProducer(self, producer, streaming):
        pass

    def unregisterProducer(self):
        pass


class BroadcastServerProtocol(EBUWebsocketProtocolMixin, WebSocketServerProtocol):

    def onOpen(self):
        try:
            # Not that well documented in twisted but this being only a path segment gets picked up fine
            self._sequence_identifier, self.action = self._parse_path(
                full_url=self.http_request_path
            )
        except ValueError as err:
            log.error(err)
            self.dropConnection()
        except Exception as err:
            log.exception(err)
            self.dropConnection()

        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if self.action == 'publish':
            self._write_to_consumer(payload)
        else:
            log.error(ERR_WS_RECEIVE_VIA_PRODUCER)
            self.dropConnection(abort=True)

    def sendSequenceMessage(
            self, sequence_identifier, payload, isBinary=False, fragmentSize=None, sync=False, doNotCompress=False
    ):
        if self.action == 'subscribe':
            self._send_sequence_message(
                sequence_identifier=sequence_identifier,
                payload=payload,
                isBinary=isBinary,
                fragmentSize=fragmentSize,
                sync=sync,
                doNotCompress=doNotCompress
            )
        else:
            log.error(ERR_WS_SEND_VIA_CONSUMER)
            self.dropConnection(abort=True)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastFactoryCommon(object):
    _consumer = None
    _producer = None

    @property
    def producer(self):
        return self._producer

    @producer.setter
    def producer(self, value):
        if value is not None:
            # Overwriting a producer without explicit removal is not supported
            if self._producer is not None:
                raise ValueError
        else:
            # At removal make sure the producer is stopped.
            self._stop_producer()
        self._producer = value

    def _stop_producer(self):
        pass

    @property
    def consumer(self):
        return self._consumer

    @consumer.setter
    def consumer(self, value):
        if value is not None:
            if self._consumer is not None:
                raise ValueError
        self._consumer = value


class BroadcastServerFactory(BroadcastFactoryCommon, WebSocketServerFactory):

    real_port_number = None

    def __init__(self, url=None, producer=None, consumer=None):
        super(BroadcastServerFactory, self).__init__(url, protocols=[13])
        self.producer = producer
        self.consumer = consumer

    def _stop_producer(self):
        if self._producer is not None:
            self._producer.stopProducing()

    def register(self, client):
        if client.action == 'subscribe':
            if self.producer is None:
                # TODO: Here a message would be useful
                log.error(ERR_WS_NOT_PRODUCER)
                client.dropConnection()
            else:
                self.producer.register(client)
        elif client.action == 'publish':
            if self.consumer is None:
                log.error(ERR_WS_NOT_CONSUMER)
                client.dropConnection()
            else:
                self.consumer.register(client)

    def unregister(self, client):
        if client.action == 'subscribe':
            self._producer.unregister(client)
        if client.action == 'publish':
            self._consumer.unregister(client)

    def stopFactory(self):
        self._stop_producer()

    def listen(self):
        listener = listenWS(self)
        self.real_port_number = listener.getHost().port
        if self.producer:
            self.producer.real_port_number = self.real_port_number
        if self.consumer:
            self.consumer.real_port_number = self.real_port_number


class BroadcastClientProtocol(EBUWebsocketProtocolMixin, WebSocketClientProtocol):

    def onOpen(self):
        try:
            self._sequence_identifier, self.action = self._parse_path(self.factory.url)
        except ValueError as err:
            log.error(err)
            self.dropConnection()
        except Exception as err:
            log.exception(err)
            self.dropConnection()

        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if self.action == 'subscribe':
            self._write_to_consumer(payload)
        else:
            log.error(ERR_WS_RECEIVE_VIA_PRODUCER)

    def sendSequenceMessage(
            self, sequence_identifier, payload, isBinary=False, fragmentSize=None, sync=False, doNotCompress=False
    ):
        if self.action == 'publish':
            self._send_sequence_message(
                sequence_identifier=sequence_identifier,
                payload=payload,
                isBinary=isBinary,
                fragmentSize=fragmentSize,
                sync=sync,
                doNotCompress=doNotCompress
            )
        else:
            log.error(ERR_WS_SEND_VIA_CONSUMER)
            self.dropConnection(abort=True)

    def connectionLost(self, reason):
        WebSocketClientProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastClientFactory(BroadcastFactoryCommon, WebSocketClientFactory):

    def __init__(self, url, consumer=None, producer=None, *args, **kwargs):
        super(BroadcastClientFactory, self).__init__(url=url, *args, **kwargs)
        self.producer = producer
        self.consumer = consumer

    def register(self, client):
        if client.action == 'subscribe':
            if self.consumer is None:
                log.error(ERR_WS_NOT_CONSUMER)
                client.dropConnection()
            else:
                self.consumer.register(client)
        elif client.action == 'publish':
            if self.producer is None:
                log.error(ERR_WS_NOT_PRODUCER)
                client.dropConnection()
            else:
                self.producer.register(client)

    def unregister(self, client):
        if client.action == 'subscribe' and self.consumer:
            self.consumer.unregister(client)
        elif client.action == 'publish' and self.producer:
            self.producer.unregister(client)

    def connect(self):
        log.info('Connecting to {}'.format(self.url))
        connectWS(self)


# Here comes the legacy ws protocol
# =================================
@implementer(interfaces.IPullProducer)
class TwistedPullProducer(object):

    _custom_producer = None
    _consumer = None

    def __init__(self, consumer, custom_producer):
        self._custom_producer = custom_producer
        self._consumer = consumer
        self._consumer.registerProducer(self, False)
        self._custom_producer.register_twisted_producer(self)

    def emit_data(self, channel, data, delay=None):
        if delay is not None:
            reactor.callLater(delay, self._consumer.write, channel, data)
        else:
            self._consumer.write(channel, data)

    def resumeProducing(self):
        self._custom_producer.resume_producing()

    def stopProducing(self):
        pass


@implementer(interfaces.IConsumer)
class TwistedConsumer(object):

    _custom_consumer = None
    _producer = None

    def __init__(self, custom_consumer):
        self._custom_consumer = custom_consumer

    def registerProducer(self, producer, streaming):
        self._producer = producer
        if streaming:
            self._producer.resumeProducing()

    def unregisterProducer(self):
        self._producer.stopProducing()
        self._producer = None

    def write(self, data):
        self._custom_consumer.on_new_data(data)


class LegacyBroadcastServerProtocol(WebSocketServerProtocol):

    _channels = None

    def onOpen(self):
        self.factory.register(self)
        self._channels = set()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            try:
                data = json.loads(payload)
                if 'subscribe' in data:
                    log.info('{} subscibes to {}'.format(self.peer, data['subscribe']))
                    self._channels.add(data['subscribe'])
                if 'unsubscribe' in data:
                    log.info('{} unsubscribes from {}'.format(self.peer, data['unsubscribe']))
                    self._channels.remove(data['unsubscribe'])
            except Exception:
                pass

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def sendMessageOnChannel(self, channel, payload, isBinary=False, fragmentSize=None, sync=False,
                             doNotCompress=False):
        if channel in self._channels:
            super(LegacyBroadcastServerProtocol, self).sendMessage(
                payload=payload,
                isBinary=isBinary,
                fragmentSize=fragmentSize,
                sync=sync,
                doNotCompress=doNotCompress
            )
            log.info("message sent to {}".format(self.peer))


@implementer(IBroadcaster, interfaces.IConsumer)
class LegacyBroadcastServerFactory(WebSocketServerFactory):
    _clients = None
    _producer = None
    _push_producer = None

    def __init__(self, url):
        super(LegacyBroadcastServerFactory, self).__init__(url, protocols=[13])
        self._clients = []

    def registerProducer(self, producer, streaming):
        self._producer = producer
        self._push_producer = streaming

    def unregisterProducer(self):
        self._producer.stopProducing()
        self._producer = None

    def write(self, channel, data):
        self.broadcast(channel, data)

    def register(self, client):
        if client not in self._clients:
            log.info("registered client {}".format(client.peer))
            self._clients.append(client)

    def unregister(self, client):
        if client in self._clients:
            log.info("unregistered client {}".format(client.peer))
            self._clients.remove(client)

    def pull(self):
        if self._producer:
            self._producer.resumeProducing()

    def broadcast(self, channel, msg):
        log.info("broadcasting message...")

        for c in self._clients:
            c.sendMessageOnChannel(channel, msg.encode("utf-8"), isBinary=False, doNotCompress=False, sync=False)

    def stopFactory(self):
        self.unregisterProducer()

    def listen(self):
        listenWS(self)


class LegacyBroadcastClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        for channel in self.factory.channels:
            self.subscribeChannel(channel)

    def subscribeChannel(self, channel):
        data = {
            'subscribe': channel
        }
        self.sendMessage(json.dumps(data))

    def unsubscribeChannel(self, channel):
        data = {
            'unsubscribe': channel
        }
        self.sendMessage(json.dumps(data))

    def onMessage(self, payload, isBinary):
        self.factory.dataReceived(payload)


@implementer(interfaces.IPushProducer)
class LegacyBroadcastClientFactory(WebSocketClientFactory):

    _channels = None
    _consumer = None
    _stopped = None

    def __init__(self, url, consumer, channels=None, *args, **kwargs):
        super(LegacyBroadcastClientFactory, self).__init__(url=url, *args, **kwargs)

        if not channels:
            self._channels = []
        else:
            self._channels = channels

        self._consumer = consumer
        self._consumer.registerProducer(self, True)
        self._stopped = True

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, value):
        self._channels = value

    def dataReceived(self, data):
        self._consumer.write(data)

    def stopProducing(self):
        self._stopped = True

    def resumeProducing(self):
        self._stopped = False

    def pauseProducing(self):
        self._stopped = True

    def connect(self):
        log.info('Connecting to {}'.format(self.url))
        connectWS(self)
