from abc import ABCMeta, abstractmethod, abstractproperty

# Interfaces
# ==========


class ICarriageMechanism(object):
    """
    Basic interface for the carrige mechanisms
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def register_node(self, node):
        """
        Link the processing node to the carriage mechanism
        :param node:
        :return:
        """

    @abstractproperty
    def node(self):
        """
        Node getter
        :return:
        """


class IProducerCarriage(ICarriageMechanism):
    """
    Node that emits documents to an output interface, usually some network socket.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def emit_data(self, data, **kwargs):
        """
        Implement protocol specific postprocessing here.
        :param **kwargs: Extra parameters to send down
        :param data:
        :return:
        """

    @abstractmethod
    def resume_producing(self):
        """
        This makes sure that the producers can be pulled. This is good for timer or manual triggering
        :return:
        """


class IConsumerCarriage(ICarriageMechanism):
    """
    Node that receives documents and processes them.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_new_data(self, data, **kwargs):
        """
        Implement protocol specific preprocessing here.
        :param **kwargs: Extra parameters to send down
        :return:
        """

# Abstract classes
# ================


class __AbstractCarriage(ICarriageMechanism):
    """
    Protocol specific bindings that connects the business logic to the carriage mechanism.
    This is meant to be used in a dependency injection fashion. Carriage mechanism can be anything from a network socket
    through file system to a tape. This implementation is meant to receive
    """
    _node = None

    def register_node(self, node):
        self._node = node

    @property
    def node(self):
        return self._node


class AbstractProducerCarriage(IProducerCarriage, __AbstractCarriage):

    def resume_producing(self):
        self.node.resume_producing()


class AbstractConsumerCarriage(IConsumerCarriage, __AbstractCarriage):
    pass


class AbstractCombinedCarriage(AbstractConsumerCarriage, AbstractProducerCarriage):
    pass
