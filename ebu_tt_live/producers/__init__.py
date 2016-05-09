
from zope.interface import Interface


class IContentProducer(Interface):

    def register_consumer(self, consumer):
        raise NotImplementedError()
