from abc import abstractmethod, abstractproperty
from ebu_tt_live.utils import AutoRegisteringABCMeta, AbstractStaticMember, validate_types_only

# Interfaces
# ==========


class INode(object, metaclass=AutoRegisteringABCMeta):
    """
    This is the foundation of all nodes that take part in the processing of subtitle documents.
    The Node should deal with subtitles in a high level interface,
    which is an instance of :class:`<ebu_tt_live.documents.SubtitleDocument>`. That is the interface which should
    be used to communicate with the carriage mechanism. See :class:`<ebu_tt_live.carriage.ICarriageMechanism>`
    """

    @abstractmethod
    def process_document(self, document, **kwargs):
        """
        The central hook that is meant to implement the main functionality of the node.
        A node must implement this method.

        :param kwargs: Extra parameters
        :param document: Can be XML, Document object...etc. depending on the carriage implementation

        """
        raise NotImplementedError()


class IProducerNode(INode):

    _provides = AbstractStaticMember(validate_types_only)

    @abstractmethod
    def resume_producing(self):
        """
        This allows the node to be triggered by events, such as a timer.
        """

    @classmethod
    def provides(cls):
        """
        Data type provided
        :return:
        """
        if isinstance(cls._provides, AbstractStaticMember):
            raise TypeError('Classmethod relies on abstract property: \'_provides\'')
        return cls._provides

    @abstractproperty
    def producer_carriage(self):
        """
        Carriage mechanism accessor
        :return:
        """

    @abstractmethod
    def register_producer_carriage(self, producer_carriage):
        """
        Output carriage mechanism registration
        :param producer_carriage:
        """


class IConsumerNode(INode):

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

    @abstractproperty
    def consumer_carriage(self):
        """
        Carriage mechanism accessor
        :return:
        """

    @abstractmethod
    def register_consumer_carriage(self, consumer_carriage):
        """
        Input carriage mechanism registration
        :param consumer_carriage:
        """
