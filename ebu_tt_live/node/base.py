
class Node(object):
    """
    This is the foundation of all nodes that take part in the processing of subtitle documents.
    The Node should deal with subtitles in a high level interface,
    which is an instance of :class:`<ebu_tt_live.documents.SubtitleDocument>`. That is the interface which should
    be used to communicate with the carriage machanism. See :class:`<CarriageImpl>`
    """

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

    def process_document(self, document):
        """
        The central hook that is meant to implement the main functionality of the node.
        A node must implement this method.
        :param document:
        :return:
        """
        raise NotImplementedError()


class CarriageImpl(object):
    """
    Protocol specific bindings that connects the business logic to the carriage mechanism.
    This is meant to use in a dependency injection fashion. Carriage mechanism can be anything from a network socket
    through file system to a tape. This implementation is meant to receive
    """
    _node = None

    def register(self, node):
        self._node = node


class ProducerCarriageImpl(CarriageImpl):
    """
    Node that emits documents to an output interface, usually some network socket.
    """

    def emit_document(self, document):
        """
        Implement protocol specific postprocessing here.
        :param document:
        :return:
        """
        raise NotImplementedError()


class ConsumerCarriageImpl(CarriageImpl):
    """
    Node that receives documents and processes them.
    """

    def on_new_data(self, data):
        """
        Implement protocol specific preprocessing here.
        :return:
        """
        raise NotImplementedError()


class CombinedCarriageImpl(ConsumerCarriageImpl, ProducerCarriageImpl):
    """
    Node that receives and also emits documents by combining the Producer and Consumer tasks.
    """
    pass
