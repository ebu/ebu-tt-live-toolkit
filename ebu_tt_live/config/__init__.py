"""
This subpackage is meant to contain configuration directives of validation and normalization as well as defaults.
The current plan is to use mozilla/configman package. Ultimately there is one goal there. Avoid any
runtime errors because of a broken configuration value being used at a later stage in execution at which point due to
not having been validated would cause the system to break. Validation and normalization eliminates this problem
completely. This means At startup time we can be sure that all of the configuration values match the requirements
of successful operation.

Further on there is the requirement of the code to be independent from the configurator. The code needs to be
written in a way that the modules are self-contained and only expect their dependencies to have a particular interface
but not knowing about the details of their configuration. Therefore in the modules dependency injection is used. In
turn however these configurator classes are here to make sure the configuration is possible via a single structured
configuration file or environment variables or command line argument overrides.

The mozilla/configman package gives a modular way of writing a complex configuration factory that is
controllable by file, environment and command line arguments. This gives great flexibility as the configuration of
the individual modules can be self-contained as much as possible yet it is possible to have system-wide configuration
parameters, such as a HTTP proxy.
"""

from configman import RequiredConfig, ConfigurationManager, ConfigFileFutureProxy, \
    command_line
from .backend import UniversalBackend
from .node import UniversalNodes

__all__ = [
    'common', 'backend', 'node'
]

current_app = None


def create_app(**kwargs):
    global current_app
    current_app = AppConfig(**kwargs)
    return current_app


class AppConfig(RequiredConfig):

    _config = None
    _backend = None
    _nodes = None

    def __init__(self, **kwargs):
        cm_args = {
            "definition_source": [
                UniversalNodes.get_required_config(),
                UniversalBackend.get_required_config()
            ],
            "values_source_list": [
                ConfigFileFutureProxy,
                command_line
            ]
        }
        cm_args.update(kwargs)
        cm = ConfigurationManager(
            **cm_args
        )
        config = cm.get_config()

        self._backend = config.backend.type.configure_component(config, config.backend)
        self._nodes = config.nodes.type.configure_component(config, config.nodes)
        self._config = config

        global current_app
        current_app = self

    def start(self):

        self._backend.start()

