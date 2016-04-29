
from zope.interface import implementer
from zope.interface import Interface


class IEBUTT3Reader(Interface):

    def load_xml(self):
        pass


class IEBUTT3Writer(Interface):

    def get_xml(self):
        pass


class ICommonReader(Interface):

    def load_document(self):
        pass


class ICommonWriter(Interface):

    def get_document(self):
        pass
