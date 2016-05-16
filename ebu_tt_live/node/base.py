
class Node(object):
    """
    This is the foundation of all nodes that take part in the processing of subtitle documents
    """

    _node_id = None

    def __init__(self, node_id):
        self._node_id = node_id

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


class ProducerNode(Node):
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


class ConsumerNode(Node):
    """
    Node that receives documents and processes them.
    """

    def on_new_data(self, data):
        """
        Implement protocol specific preprocessing here.
        :return:
        """
        raise NotImplementedError()


class TransferNode(ConsumerNode, ProducerNode):
    """
    Node that receives and also emits documents by combining the Producer and Consumer tasks.
    """
    pass
