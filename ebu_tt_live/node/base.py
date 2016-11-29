from abc import ABCMeta, abstractmethod, abstractproperty

# Interfaces
# ==========


class INode(object):
    """
    This is the foundation of all nodes that take part in the processing of subtitle documents.
    The Node should deal with subtitles in a high level interface,
    which is an instance of :class:`<ebu_tt_live.documents.SubtitleDocument>`. That is the interface which should
    be used to communicate with the carriage machanism. See :class:`<ebu_tt_live.carriage.ICarriage>`
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_document(self, document, **kwargs):
        """
        The central hook that is meant to implement the main functionality of the node.
        A node must implement this method.
        :param **kwargs: Extra parameters
        :param document: Can be XML, Document object...etc. depending on the carriage implementation
        :return:
        """
        raise NotImplementedError()


class IProducerNode(INode):
    __metaclass__ = ABCMeta

    @abstractproperty
    def provides(self):
        """
        :return: Interface of the data the producer produces
        """


class IConsumerNode(INode):
    __metaclass__ = ABCMeta

    @abstractproperty
    def expects(self):
        """
        :return: Interface of the data the consumer consumes
        """


class __AbstractNode(INode):

    _node_id = None
    _carriage_impl = None

    def __init__(self, node_id, carriage_impl):
        self._node_id = node_id
        self._carriage_impl = carriage_impl
        self._carriage_impl.register(node=self)

    def __repr__(self):
        return '<{name}, ID:{id} at {address} >'.format(
            name=self.__class__,
            id=self._node_id,
            address=hex(id(self))
        )

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, value):
        self._node_id = value


class AbstractProducerNode(IProducerNode, __AbstractNode):
    pass


class AbstractConsumerNode(IConsumerNode, __AbstractNode):
    pass


class AbstractCombinedNode(AbstractProducerNode, AbstractConsumerNode):
    pass
