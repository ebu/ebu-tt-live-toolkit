from abc import ABCMeta, abstractmethod
import six

# Interfaces
# ==========


class IDocumentDataAdapter(six.with_metaclass(ABCMeta)):
    """
    This adapter is used to do various conversions on the payload between the carriage and the node
    """

    @abstractmethod
    def convert_data(self, data, **kwargs):
        """
        Subclasses must implement this method
        :param data:
        :param kwargs: Extra parameters
        :return:
        """
        raise NotImplementedError()
