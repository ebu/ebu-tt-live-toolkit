from abc import abstractmethod, abstractproperty
from ebu_tt_live.utils import AutoRegisteringABCMeta, AbstractStaticMember, validate_types_only

# Interfaces
# ==========


class ICarriageMechanism(object, metaclass=AutoRegisteringABCMeta):
    """
    Basic interface for the carrige mechanisms
    """


class IProducerCarriage(ICarriageMechanism):
    """
    Carriage mechanism interface for producer nodes.
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

        :param node: The node to connect to.

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

        :param kwargs: Extra parameters to send down
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
    Carriage mechanism interface for consumer nodes.
    """

    _provides = AbstractStaticMember(validate_types_only)

    @classmethod
    def provides(cls):
        """
        Data type provided

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

        :param kwargs: Extra parameters to send down

        """
