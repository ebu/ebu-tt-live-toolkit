from abc import abstractmethod, abstractproperty
from ebu_tt_live.utils import AutoRegisteringABCMeta, AbstractStaticMember, validate_types_only

# Interfaces
# ==========


class ICarriageMechanism(object):
    """
    Basic interface for the carrige mechanisms
    """
    __metaclass__ = AutoRegisteringABCMeta


class IProducerCarriage(ICarriageMechanism):
    """
    Node that emits documents to an output interface, usually some network socket.
    """

    _expects = AbstractStaticMember(validate_types_only)

    @classmethod
    def expects(cls):
        """
        Data type expected
        :return:
        """
        if isinstance(cls._expects, AbstractStaticMember):
            raise TypeError('Classmethod relies on abstract property: \'_expects\'')
        return cls._expects

    @abstractmethod
    def register_producer_node(self, node):
        """
        Register the producer node in the carriage mechanism
        :param node:
        :return:
        """

    @abstractproperty
    def producer_node(self):
        """
        Node accessor
        :return:
        """

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

    _provides = AbstractStaticMember(validate_types_only)

    @classmethod
    def provides(cls):
        """
        Data type expected
        :return:
        """
        if isinstance(cls._provides, AbstractStaticMember):
            raise TypeError('Classmethod relies on abstract property: \'_provides\'')
        return cls._provides

    @abstractmethod
    def register_consumer_node(self, node):
        """
        Register the consumer node in the carriage mechanism
        :param node:
        :return:
        """

    @abstractproperty
    def consumer_node(self):
        """
        Node accessor
        :return:
        """

    @abstractmethod
    def on_new_data(self, data, **kwargs):
        """
        Implement protocol specific preprocessing here.
        :param **kwargs: Extra parameters to send down
        :return:
        """
