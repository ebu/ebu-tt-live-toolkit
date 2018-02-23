from .common import ConfigurableComponent, Namespace
from ebu_tt_live.carriage.direct import DirectCarriageImpl
from ebu_tt_live.carriage.websocket import WebsocketProducerCarriage, WebsocketConsumerCarriage
from ebu_tt_live.carriage import filesystem
from ebu_tt_live.utils import HTTPProxyConfig
from ebu_tt_live.strings import ERR_CONF_PROXY_CONF_VALUE, ERR_NO_SUCH_COMPONENT
from ebu_tt_live.errors import ConfigurationError
from ebu_tt_live.strings import CFG_FILENAME_PATTERN, CFG_MESSAGE_PATTERN
import urlparse
import re

# Memory carriage mechanism configurators
# ===========================================
class DirectCommon(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('id', default='default')

    _components = {}

    def __init__(self, config, local_config, **kwargs):
        super(DirectCommon, self).__init__(
            config=config,
            local_config=local_config,
            **kwargs
        )
        self.backend.register_component_start(self)

    @classmethod
    def configure_component(cls, config, local_config, **kwargs):
        instance = cls(config=config, local_config=local_config)
        component = cls._components.get(local_config.id, None)

        if component is None:
            instance.component = DirectCarriageImpl()
            cls._components[local_config.id] = instance.component
        else:
            instance.component = component

        return instance


class DirectInput(DirectCommon):
    pass


class DirectOutput(DirectCommon):
    pass


# File-based carriage mechanism configurators
# ===========================================
class FilesystemOutput(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option(
        'folder',
        default='./export',
        doc='The output folder/directory. Folder is created if it does not exist. Existing files are overwritten.'
    )
    required_config.add_option(
        'filename_pattern',
        default=CFG_FILENAME_PATTERN,
        doc='File name pattern. It needs to contain {counter} format parameter.'
    )
    required_config.add_option(
        'message_filename_pattern',
        default=CFG_MESSAGE_PATTERN,
        doc='File name pattern. It needs to contain {counter} format parameter.'
    )
    required_config.add_option(
        'rotating_buf',
        default=0,
        doc='Rotating buffer size. This will keep the last N number of files created in the folder or all if N is zero.'
    )
    required_config.add_option(
        'suppress_manifest',
        default=False,
        doc='Suppress output of a manifest file (default false)'
    )
    
    def __init__(self, config, local_config):
        super(FilesystemOutput, self).__init__(config, local_config)
        self.component = filesystem.FilesystemProducerImpl(
            dirpath=self.config.folder,
            file_name_pattern=self.config.filename_pattern,
            message_file_name_pattern=self.config.message_filename_pattern,
            circular_buf_size=self.config.rotating_buf,
            suppress_manifest=self.config.suppress_manifest)



class FilesystemInput(ConfigurableComponent):

    required_config = Namespace()
    required_config.add_option('manifest_file', doc='The timing manifest file for importing files')
    required_config.add_option(
        'tail',
        doc='Keep the manifest open and wait for new input much like UNIX\'s tail -f command'
    )
    _fs_reader = None

    def __init__(self, config, local_config):
        super(FilesystemInput, self).__init__(config, local_config)
        self.component = filesystem.FilesystemConsumerImpl()
        self._fs_reader = filesystem.FilesystemReader(
            manifest_path=self.config.manifest_file,
            do_tail=self.config.tail,
            custom_consumer=self.component
        )
        self.backend.register_component_start(self)

    def start(self):
        self._fs_reader.resume_reading()


# Websocket carriage mechanism configurators
# ==========================================
def str_to_url_converter(value):
    parsed = urlparse.urlparse(value)
    return parsed


def parse_url_list(value):
    parsed_value = []
    if value is not None:
        for item in value:
            parsed_value.append(str_to_url_converter(item))
    return parsed_value

proxy_regex = re.compile(r'^((?P<protocol>.+?)://)?(?P<host>[^:]+?):(?P<port>[0-9]+)$')


def parse_proxy_address(value):
    result = None
    match = proxy_regex.match(value)
    if match:
        # Ignoring the protocol part for now as it is only a http proxy
        result = HTTPProxyConfig(
            host=match.group('host'),
            port=int(match.group('port'))
        )
    elif value:
        # In this case something was provided that isn't a falsy value but the parsing failed.
        raise ConfigurationError(
            ERR_CONF_PROXY_CONF_VALUE.format(
                value=value
            )
        )
    return result


class WebsocketLegacyBase(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('uri', default='ws://localhost:9001', from_string_converter=str_to_url_converter)


class WebsocketLegacyOutput(WebsocketLegacyBase):

    _backend_producer = None
    _looping_call = None

    def __init__(self, config, local_config):
        super(WebsocketLegacyOutput, self).__init__(config, local_config)
        self.component = WebsocketProducerCarriage()
        self.backend.register_component_start(self)

    def start(self):
        self._backend_producer = self.backend.wsl_backend_producer(uri=self.config.uri, custom_producer=self.component)


class WebsocketLegacyInput(WebsocketLegacyBase):

    _backend_consumer = None
    required_config = Namespace()
    required_config.add_option(
        'proxy',
        doc='HTTP proxy in format ADDR:PORT',
        default=None,
        from_string_converter=parse_proxy_address
    )

    def __init__(self, config, local_config):
        super(WebsocketLegacyInput, self).__init__(config, local_config)
        self.component = WebsocketConsumerCarriage()
        self.backend.register_component_start(self)

    def start(self):
        self._backend_consumer = self.backend.wsl_backend_consumer(uri=self.config.uri, custom_consumer=self.component)


class WebsocketBase(ConfigurableComponent):

    required_config = Namespace()
    required_config.add_option(
        'listen',
        default=None,
        doc='Socket to listen on i.e: ws://ADDR:PORT',
        from_string_converter=str_to_url_converter
    )
    required_config.add_option('connect', default=[], doc='List of connections to make')
    required_config.add_option(
        'proxy',
        doc='HTTP proxy in format ADDR:PORT',
        default=None,
        from_string_converter=parse_proxy_address
    )


class WebsocketOutput(WebsocketBase):

    required_config = Namespace()
    _backend_producer = None

    def __init__(self, config, local_config):
        super(WebsocketOutput, self).__init__(config, local_config)
        # from_string_converter does not work for lists in configman :( Doing it manually here
        self.config.connect = parse_url_list(self.config.connect)
        self.component = WebsocketProducerCarriage()
        self.backend.register_component_start(self)

    def start(self):
        self._backend_producer = self.backend.ws_backend_producer(
            custom_producer=self.component,
            listen=self.config.listen,
            connect=self.config.connect,
            proxy=self.config.proxy
        )


class WebsocketInput(WebsocketBase):

    required_config = Namespace()
    _backend_consumer = None

    def __init__(self, config, local_config):
        super(WebsocketInput, self).__init__(config, local_config)
        # from_string_converter does not work for lists in configman :( Doing it manually here
        self.config.connect = parse_url_list(self.config.connect)
        self.component = WebsocketConsumerCarriage()
        self.backend.register_component_start(self)

    def start(self):
        self._backend_consumer = self.backend.ws_backend_consumer(
            custom_consumer=self.component,
            listen=self.config.listen,
            connect=self.config.connect,
            proxy=self.config.proxy
        )


producer_carriage_by_type = {
    'websocket': WebsocketOutput,
    'websocket-legacy': WebsocketLegacyOutput,
    'filesystem': FilesystemOutput,
    'direct': DirectOutput
}


def get_producer_carriage(carriage_type):
    try:
        return producer_carriage_by_type[carriage_type]
    except KeyError:
        raise ConfigurationError(
            ERR_NO_SUCH_COMPONENT.format(
                type_name=carriage_type
            )
        )


consumer_carriage_by_type = {
    'websocket': WebsocketInput,
    'websocket-legacy': WebsocketLegacyInput,
    'direct': DirectInput,
    'filesystem':  FilesystemInput
}


def get_consumer_carriage(carriage_type):
    try:
        return consumer_carriage_by_type[carriage_type]
    except KeyError:
        raise ConfigurationError(
            ERR_NO_SUCH_COMPONENT.format(
                type_name=carriage_type
            )
        )
