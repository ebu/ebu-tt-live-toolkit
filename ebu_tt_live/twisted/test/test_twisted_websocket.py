# coding=utf8
from twisted.trial.unittest import TestCase
from twisted.test import proto_helpers
from ebu_tt_live.twisted.websocket import BroadcastServerFactory, BroadcastServerProtocol, \
    BroadcastClientFactory, BroadcastClientProtocol, TwistedWSConsumer, TwistedWSPushProducer
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from mock import MagicMock
from ebu_tt_live.node.interface import IProducerNode, IConsumerNode
import pytest

from twisted.internet import task
import twisted.internet.base
twisted.internet.base.DelayedCall.debug = True


class _NewWSCommon(object):

    def _create_server(self, *args, **kwargs):
        self.sfactory = BroadcastServerFactory(*args, **kwargs)
        self.sproto = BroadcastServerProtocol()
        self.sproto.factory = self.sfactory
        self.sproto.failHandshake = MagicMock()
        self.str = proto_helpers.StringTransportWithDisconnection()
        self.sproto.transport = self.str
        self.str.protocol = self.sproto

    def _create_client(self, *args, **kwargs):
        self.cfactory = BroadcastClientFactory(*args, **kwargs)
        self.cproto = BroadcastClientProtocol()
        self.cproto.factory = self.cfactory
        self.cproto.failHandshake = MagicMock()
        self.ctr = proto_helpers.StringTransportWithDisconnection()
        self.cproto.transport = self.ctr
        self.ctr.protocol = self.cproto

    def _connect(self):
        self.sproto.connectionMade()
        self.cproto.connectionMade()

        # Process incoming request
        self.sproto.dataReceived(self.ctr.value())
        self.ctr.clear()
        # Process response
        self.cproto.dataReceived(self.str.value())
        self.str.clear()

        # At this point handshake is supposed to be done
        self.assertEqual(self.sproto.state, self.sproto.STATE_OPEN)
        self.sproto.failHandshake.assert_not_called()
        self.assertEqual(self.cproto.state, self.cproto.STATE_OPEN)
        self.cproto.failHandshake.assert_not_called()

    def _disconnect(self):
        # Do closing handshake
        self.cproto.sendClose()
        self.sproto.dataReceived(self.ctr.value())
        self.ctr.clear()
        self.cproto.dataReceived(self.str.value())
        self.str.clear()

        # Verify transmission success
        # The server should have closed the socket by now
        self.assertEqual(self.sproto.state, self.sproto.STATE_CLOSED)
        self.assertTrue(self.sproto.wasClean)
        self.assertFalse(self.str.connected)
        # And the client needs some help here
        self.ctr.loseConnection()
        self.assertEqual(self.cproto.state, self.cproto.STATE_CLOSED)
        self.assertTrue(self.cproto.wasClean)


class TestProdServerToConsClientProtocols(_NewWSCommon, TestCase):

    def setUp(self):
        self.prod = MagicMock()
        self.cons = MagicMock()
        self.sequence_identifier = 'TestSeq01'

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_server_prod_client_cons_success(self):
        self._create_server(url='ws://localhost:9005', producer=self.prod)
        self._create_client(
            url='ws://localhost:9005/{}/subscribe'.format(
                self.sequence_identifier
            ),
            consumer=self.cons
        )

        # This step is supposed to be done by the mocked out twisted consumer on connection registration
        self.cproto.consumer = self.cons

        self._connect()

        self.cons.register.assert_called_with(self.cproto)
        self.prod.register.assert_called_with(self.sproto)
        self.assertEqual(self.cproto.action, 'subscribe')
        self.assertEqual(self.sproto.action, 'subscribe')

        # At this point we are supposed to be able to send data through
        doc = b'dummy message'
        self.sproto.sendSequenceMessage(
            sequence_identifier=self.sequence_identifier,
            payload=doc
        )

        self.cons.write.assert_not_called()

        # Do the transport step
        self.cproto.dataReceived(self.str.value())
        self.str.clear()
        self.sproto.dataReceived(self.ctr.value())
        self.ctr.clear()

        # This should be a successful reception of the data frame
        self.cons.write.assert_called_with(doc, sequence_identifier=self.sequence_identifier)

        # Bring a clean disconnect
        self._disconnect()

        # Check protocol de-registration
        self.cons.unregister.assert_called_with(self.cproto)
        self.prod.unregister.assert_called_with(self.sproto)

        # And that is our success case here

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_server_prod_client_cons_wrong_sequence_error(self):
        # This test emulates the data parsing raising the UnexpectedSequenceIdentifierError
        def fail_parsing(data, **kwargs):
            raise UnexpectedSequenceIdentifierError()

        self.cons.write.side_effect = fail_parsing

        self._create_server(url='ws://localhost:9005', producer=self.prod)
        self._create_client(
            url='ws://localhost:9005/{}/subscribe'.format(
                self.sequence_identifier
            ),
            consumer=self.cons
        )

        # This step is supposed to be done by the mocked out twisted consumer on connection registration
        self.cproto.consumer = self.cons

        self._connect()

        self.cons.register.assert_called_with(self.cproto)
        self.prod.register.assert_called_with(self.sproto)
        self.assertEqual(self.cproto.action, 'subscribe')
        self.assertEqual(self.sproto.action, 'subscribe')

        # At this point we are supposed to be able to send data through
        doc = b'dummy message'
        self.sproto.sendSequenceMessage(
            sequence_identifier=self.sequence_identifier,
            payload=doc
        )

        self.cons.write.assert_not_called()

        # Do the transport step
        self.cproto.dataReceived(self.str.value())
        self.str.clear()
        self.sproto.dataReceived(self.ctr.value())
        self.ctr.clear()

        # Now the exception should be raised and the connection should be broken

        self.cons.write.assert_called()
        self.assertEqual(self.cproto.state, self.sproto.STATE_CLOSED)
        self.assertFalse(self.cproto.wasClean)

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_consumer_send_data_error(self):
        self._create_server(url='ws://localhost:9005', producer=self.prod)
        self._create_client(
            url='ws://localhost:9005/{}/subscribe'.format(
                self.sequence_identifier
            ),
            consumer=self.cons
        )

        # This step is supposed to be done by the mocked out twisted consumer on connection registration
        self.cproto.consumer = self.cons

        self._connect()

        # When data arrives from consumer to server
        self.sproto.dataReceived(b'consumers should not send data')

        # This must have triggered the connection to be dropped
        self.assertEqual(self.sproto.state, self.sproto.STATE_CLOSED)
        self.assertFalse(self.sproto.wasClean)

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_producer_to_producer_error(self):
        self._create_server(url='ws://localhost:9005', producer=self.prod)
        self._create_client(
            url='ws://localhost:9005/{}/publish'.format(
                self.sequence_identifier
            ),
            consumer=self.cons
        )

        # This is meant to fail handshake so wait for AssertionError here
        self.assertRaises(AssertionError, self._connect)

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_url_encoded_components(self):
        # This test is about getting percent encoded characters work in sequenceId or hostname
        sequence_id = 'sequence/ünicödé?/Name'
        self._create_server(url='ws://localhost:9006', producer=self.prod)
        self._create_client(
            url='ws://localhost:9006/sequence%2F%C3%BCnic%C3%B6d%C3%A9%3F%2FName/subscribe',
            consumer=self.cons
        )

        self.cproto.consumer = self.cons

        self._connect()

        self.assertEqual(sequence_id, self.cproto._sequence_identifier)
        self.assertEqual(sequence_id, self.sproto._sequence_identifier)

    def tearDown(self):
        self.ctr.loseConnection()
        self.str.loseConnection()


class TestConsServerToProdClientProtocols(_NewWSCommon, TestCase):

    def setUp(self):
        self.prod = MagicMock()
        self.cons = MagicMock()
        self.sequence_identifier = 'TestSeq01'

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_serv_cons_client_prod_success(self):

        self._create_server(
            url='ws://localhost:9005',
            consumer=self.cons
        )

        self._create_client(
            url='ws://localhost:9005/{}/publish'.format(
                self.sequence_identifier
            ),
            producer=self.prod
        )

        self.sproto.consumer = self.cons

        self._connect()

        self.cons.register.assert_called_with(self.sproto)
        self.prod.register.assert_called_with(self.cproto)
        self.assertEqual(self.sproto.action, 'publish')
        self.assertEqual(self.cproto.action, 'publish')

        # Sending data
        doc = b'producer client sample'
        self.cproto.sendSequenceMessage(
            sequence_identifier=self.sequence_identifier,
            payload=doc
        )

        self.sproto.dataReceived(self.ctr.value())
        self.ctr.clear()
        self.cproto.dataReceived(self.str.value())
        self.str.clear()

        self.cons.write.assert_called_with(doc, sequence_identifier=self.sequence_identifier)

        # Let's do a clean disconnect

        self._disconnect()

        # Check de-registration
        self.cons.unregister.assert_called_with(self.sproto)
        self.prod.unregister.assert_called_with(self.cproto)

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_serv_cons_client_prod_wrong_sequence_error(self):
        def fail_parsing(data, **kwargs):
            raise UnexpectedSequenceIdentifierError()

        self.cons.write.side_effect = fail_parsing

        self._create_server(
            url='ws://localhost:9005',
            consumer=self.cons
        )

        self._create_client(
            url='ws://localhost:9005/{}/publish'.format(
                self.sequence_identifier
            ),
            producer=self.prod
        )

        self.sproto.consumer = self.cons

        self._connect()

        self.cons.register.assert_called_with(self.sproto)
        self.prod.register.assert_called_with(self.cproto)
        self.assertEqual(self.sproto.action, 'publish')
        self.assertEqual(self.cproto.action, 'publish')

        # Sending data
        doc = b'producer client sample'
        self.cproto.sendSequenceMessage(
            sequence_identifier=self.sequence_identifier,
            payload=doc
        )

        self.sproto.dataReceived(self.ctr.value())
        self.ctr.clear()
        self.cproto.dataReceived(self.str.value())
        self.str.clear()

        # The connection should be broken by now

        self.assertEqual(self.sproto.state, self.sproto.STATE_CLOSED)
        self.assertFalse(self.sproto.wasClean)

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_consumer_to_consumer_error(self):
        self._create_server(
            url='ws://localhost:9005',
            consumer=self.cons
        )

        self._create_client(
            url='ws://localhost:9005/{}/subscribe'.format(
                self.sequence_identifier
            ),
            producer=self.prod
        )

        self.sproto.consumer = self.cons

        # This is not meant to survive the handshake
        self.assertRaises(AssertionError, self._connect)

    @pytest.mark.xfail(reason="Twisted deferred testing needs to be reworked.")
    def test_consumer_send_data_error(self):
        self._create_server(
            url='ws://localhost:9005',
            consumer=self.cons
        )

        self._create_client(
            url='ws://localhost:9005/{}/publish'.format(
                self.sequence_identifier
            ),
            producer=self.prod
        )

        self.sproto.consumer = self.cons

        self._connect()

        self.cproto.dataReceived(b'consumers should not send data')

        # This should make the connection kick the bucket
        self.assertEqual(self.cproto.state, self.cproto.STATE_CLOSED)
        self.assertFalse(self.cproto.wasClean)


class TestWSProducerCarriage(TestCase):

    def setUp(self):
        self.producer = MagicMock()

        self.protocol1 = MagicMock()
        self.protocol2 = MagicMock()

        self.carriage = TwistedWSPushProducer(
            custom_producer=self.producer
        )

        # Create a mock connection
        self.carriage.register(self.protocol1)
        self.carriage.register(self.protocol2)

        self.sequence_identifier = 'testSeq1'

    def test_successful_broadcast(self):

        doc = b'test_data'
        self.carriage.emit_data(
            sequence_identifier=self.sequence_identifier,
            data=doc
        )
        self.protocol1.sendSequenceMessage.assert_called_with(
            sequence_identifier=self.sequence_identifier,
            payload=doc
        )
        self.protocol2.sendSequenceMessage.assert_called_with(
            sequence_identifier=self.sequence_identifier,
            payload=doc
        )

        self.protocol1.reset_mock()
        self.protocol2.reset_mock()

        self.carriage.unregister(self.protocol2)

        self.carriage.emit_data(
            sequence_identifier=self.sequence_identifier,
            data=doc
        )
        self.protocol1.sendSequenceMessage.assert_called_with(
            sequence_identifier=self.sequence_identifier,
            payload=doc
        )
        # However protocol2 should be empty
        self.protocol2.sendSequenceMessage.assert_not_called()

    def test_delayed_broadcast(self):
        doc = b'delayed test data'
        delay = 5.0
        clock = task.Clock()
        self.carriage._callLater = clock.callLater
        deferred = self.carriage.emit_data(
            sequence_identifier=self.sequence_identifier,
            data=doc,
            delay=delay
        )

        self.protocol1.sendSequenceMessage.assert_not_called()
        clock.advance(4)

        self.protocol1.sendSequenceMessage.assert_not_called()
        clock.advance(2)

        self.protocol1.sendSequenceMessage.assert_called_with(
            sequence_identifier=self.sequence_identifier,
            payload=doc
        )

    def test_interface_implementation(self):
        self.carriage.resumeProducing()
        self.producer.resume_producing.assert_called_once()

        # These are NOP at the moment
        self.carriage.stopProducing()
        self.carriage.pauseProducing()


class TestWSConsumerCarriage(TestCase):

    def setUp(self):
        self.consumer = MagicMock()

        self.protocol1 = MagicMock()
        self.protocol2 = MagicMock()

        self.carriage = TwistedWSConsumer(
            custom_consumer=self.consumer
        )

        self.carriage.register(self.protocol1)
        self.carriage.register(self.protocol2)

    def test_successful_reception(self):

        doc = b'document reception test'

        self.assertEqual(self.protocol1.consumer, self.carriage)
        self.assertEqual(self.protocol2.consumer, self.carriage)

        self.carriage.write(data=doc)

        self.consumer.on_new_data.assert_called_with(doc)

        self.carriage.unregister(self.protocol1)
        self.assertIsNone(self.protocol1.consumer)

    def test_interface_implementation(self):

        # TODO: Figure out if this pass is appropriate
        self.carriage.registerProducer(MagicMock(), True)
        self.carriage.unregisterProducer()

    def tearDown(self):
        pass


class TestWSProtocolCarriageIntegration(TestCase):
    pass
