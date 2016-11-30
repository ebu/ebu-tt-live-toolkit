import types
import logging
import weakref
from abc import abstractmethod, abstractproperty
from ebu_tt_live.utils import AutoRegisteringABCMeta, AbstractStaticMember

log = logging.getLogger(__name__)

# Interfaces
# ==========


def _types_only(value, member_name, class_name):
    if not isinstance(value, tuple):
        value = (value,)
    for item in value:
        if not isinstance(item, (type, types.ClassType)):
            raise TypeError(
                'Abstract static member: \'{}.{}\' is not a types or class'.format(
                    class_name,
                    member_name
                )
            )


class IDocumentDataAdapter(object):
    """
    This adapter is used to do various conversions on the payload between the carriage and the node
    """
    __metaclass__ = AutoRegisteringABCMeta

    __impl_registry = {}
    _expects = AbstractStaticMember(_types_only)
    _provides = AbstractStaticMember(_types_only)

    @classmethod
    def auto_register_impl(cls, impl_class):
        impl_expects = impl_class.expects()
        provides_map = cls.__impl_registry.setdefault(impl_expects, weakref.WeakValueDictionary())
        impl_provides = impl_class.provides()
        if impl_provides in provides_map.keys():
            log.warning(
                '({} -> {}) adapter already registered: {}. Ignoring: {} '.format(
                    impl_expects,
                    impl_provides,
                    provides_map[impl_provides],
                    impl_class
                )
            )
        else:
            log.debug(
                'Registering ({} -> {}) adapter: {}'.format(
                    impl_expects,
                    impl_provides,
                    impl_class
                )
            )
            provides_map[impl_provides] = impl_class

    @classmethod
    def get_registered_impl(cls, expects, provides):
        impl_class = cls.__impl_registry.get(expects, {}).get(provides, None)
        if impl_class is None:
            raise ValueError('No such adapter found for ({} -> {})'.format(
                expects, provides
            ))
        return impl_class

    @classmethod
    def expects(cls):
        """
        Data type expected
        :return:
        """
        if isinstance(cls._expects, AbstractStaticMember):
            raise TypeError('Classmethod relies on abstract property: \'_expects\'')
        return cls._expects

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
    def convert_data(self, data, **kwargs):
        """
        Subclasses must implement this method
        :param data:
        :param kwargs: Extra parameters
        :return:
        """
        raise NotImplementedError()
