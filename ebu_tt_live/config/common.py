import re
import six
import logging
import time
from configman import RequiredConfig, Namespace, converters
from ebu_tt_live.strings import ERR_CONF_ONE_BACKEND_ONLY
from ebu_tt_live.errors import ConfigurationError

runtime_template_regex = re.compile(ur'[*]{2}.*?[*]{2}')
converters = converters

log = logging.getLogger(__name__)


class ConfigurableComponent(RequiredConfig):

    required_config = Namespace()

    config = None
    component = None  # To store the component itself inside its configurator
    _backend = None  # Static variable holding the backend

    def __init__(self, config, local_config, backend=None):
        self.config = local_config

        if backend is not None:
            if self.backend is not None:
                raise ConfigurationError(
                    ERR_CONF_ONE_BACKEND_ONLY.format(
                        backend1=self.backend,
                        backend2=backend
                    )
                )
            else:
                ConfigurableComponent._backend = backend
        elif self.backend is not None:
            # Register configurator instance
            self.backend.register_configurator(self)

    @property
    def backend(self):
        return ConfigurableComponent._backend

    @classmethod
    def configure_component(cls, config, local_config, **kwargs):
        """
        This is a class method to either return an instance that already exists or create one.
        :param config:
        :param local_config:
        :param kwargs: Extra parameters
        :return: Instance of ConfigurableComponent
        """
        return cls(config=config, local_config=local_config)

    @classmethod
    def _resolve_runtime_variable_match(cls, matchobj):
        # Give this function to re.sub to do the replacement for you
        var_loc = matchobj.group(0).replace(u'**', u'')
        var_loc = var_loc.split(u'.')
        node_id, attr_names = var_loc[0], var_loc[1:]
        node = current_app.get_node(node_id)
        result = node
        for attr_name in attr_names:
            temp_result = getattr(result, attr_name)
            while temp_result is None:
                log.warning('Variable should not be None. Trying to wait for deferred.')
                time.sleep(2)
                temp_result = getattr(result, attr_name)
            result = temp_result

        if not isinstance(result, six.text_type):
            result = six.text_type(result)
        return result

    @classmethod
    def resolve_runtime_variables(cls, str_parameter):
        return runtime_template_regex.sub(
            repl=cls._resolve_runtime_variable_match,
            string=str_parameter
        )

    def start(self):
        pass

    def stop(self):
        pass

# This variable stores the current application
current_app = None


def install_app(app_obj):
    global current_app
    current_app = app_obj
    return current_app
