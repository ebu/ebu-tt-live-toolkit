
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
