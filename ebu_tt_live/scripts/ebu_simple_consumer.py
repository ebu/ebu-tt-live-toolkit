import logging
from argparse import ArgumentParser
from .common import create_loggers
from ebu_tt_live.clocks.local import LocalMachineClock
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from twisted.internet import reactor


log = logging.getLogger('ebu_simple_consumer')
parser = ArgumentParser()

parser.add_argument('-c', '--config', dest='config', metavar='CONFIG')

items = [1,2,3,4,5,6,7]


class ClientNodeProtocol(WebSocketClientProtocol):

    def onOpen(self):
        self.sendMessage('Hello')

    def onMessage(self, payload, isBinary):

        log.info(payload)


def main():
    args = parser.parse_args()
    create_loggers()
    log.info('This is a Simple Consumer example')

    factory = WebSocketClientFactory('ws://localhost:9000')
    factory.protocol = ClientNodeProtocol

    connectWS(factory=factory)

    reactor.run()
