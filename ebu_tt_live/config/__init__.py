"""
This subpackage is meant to contain configuration directives of validation and and normalization as well as defaults.
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

The mozilla/configman package seems to give a modular way of writing a complex configuration factory that is
controllable by file, environment and command line arguments. This gives great flexibility as the configuration of
the individual modules can be self-contained as much as possible yet it is possible to have system-wide configuration
parameters, such as a HTTP proxy.
"""


__all__ = [
    'common', 'backend', 'node'
]

from . import common
from . import backend
from . import node
import configman


current_app = None


def create_app(**kwargs):
    global current_app
    current_app = AppConfig(**kwargs)


class AppConfig(configman.RequiredConfig):

    _config = None
    _backend = None
    _nodes = None

    def __init__(self, **kwargs):
        default_config = {
            'definition_source':  [
                node.UniversalNode.get_required_config(),
                backend.UniversalBackend.get_required_config()
            ],
            'values_source_list': [
                configman.ConfigFileFutureProxy,
                configman.command_line
            ]
        }
        default_config.update(kwargs)
        config = configman.configuration(**default_config)
        self.config = config

        global current_app
        current_app = instance

    required_config = configman.Namespace()
    required_config.backend = backend.UniversalBackend
    required_config.add_aggregation('nodes')
