from .common import ConfigurableComponent, Namespace
from ebu_tt_live.carriage.direct import DirectCarriageImpl
from ebu_tt_live.carriage.websocket import WebsocketProducerCarriage, WebsocketConsumerCarriage
from ebu_tt_live.carriage import filesystem
import urlparse


def producer_carriage_by_type(carriage_type):
    if carriage_type == 'websocket':
        return WebsocketOutput
    elif carriage_type == 'websocket-legacy':
        return WebsocketLegacyOutput
    elif carriage_type == 'filesystem':
        return FilesystemOutput
    elif carriage_type == 'filesystem-simple':
        return SimpleFilesystemOutput
    elif carriage_type == 'direct':
        return DirectOutput
    else:
        raise Exception('No such component: {}'.format(carriage_type))


def consumer_carriage_by_type(carriage_type):
    if carriage_type == 'websocket':
        return WebsocketInput
    elif carriage_type == 'websocket-legacy':
        return WebsocketLegacyInput
    elif carriage_type == 'direct':
        return DirectInput
    elif carriage_type == 'filesystem':
        return FilesystemInput
    else:
        raise Exception('No such component: {}'.format(carriage_type))


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
class FileOutputCommon(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option(
        'folder',
        default='./export',
        doc='The output folder/directory. Folder is created if it does not exist. Existing files are overwritten.'
    )


class FilesystemOutput(FileOutputCommon):

    def __init__(self, config, local_config):
        super(FilesystemOutput, self).__init__(config, local_config)
        self.component = filesystem.FilesystemProducerImpl(dirpath=config.folder)


class SimpleFilesystemOutput(FileOutputCommon):
    # This does not create a manifest file
    required_config = Namespace()
    required_config.add_option(
        'filename_pattern',
        default='export-{counter}.xml',
        doc='File name pattern. It needs to contain {counter} format parameter.'
    )
    required_config.add_option(
        'rotating_buf',
        default=0,
        doc='Rotating buffer size. This will keep the last N number of files created in the folder.'
    )

    def __init__(self, config, local_config):
        super(SimpleFilesystemOutput, self).__init__(config, local_config)
        if config.rotating_buf:
            self.component = filesystem.RotatingFolderExport(
                dir_path=config.folder,
                file_name_pattern=config.filename_pattern,
                circular_buf_size=config.rotating_buf
            )
        else:
            self.component = filesystem.SimpleFolderExport(
                dir_path=config.folder,
                file_name_pattern=config.filename_pattern
            )


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
            manifest_path=config.manifest_file,
            do_tail=config.tail,
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
    required_config.add_option('proxy', doc='HTTP proxy in format ADDR:PORT')

    def __init__(self, config, local_config):
        super(WebsocketLegacyInput, self).__init__(config, local_config)
        self.component = WebsocketConsumerCarriage()
        self.backend.register_component_start(self)

    def start(self):
        self._backend_consumer = self.backend.wsl_backend_consumer(uri=self.config.uri, custom_consumer=self.component)


class WebsocketBase(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('listen', default='ws://localhost:9001', doc='Socket to listen on i.e: ws://ADDR:PORT', from_string_converter=str_to_url_converter)
    required_config.add_option('client', default=[], doc='List of connections to make')


class WebsocketOutput(WebsocketBase):

    required_config = Namespace()
    required_config.add_option('proxy', doc='HTTP proxy in format ADDR:PORT')


class WebsocketInput(WebsocketBase):

    required_config = Namespace()
    required_config.add_option('proxy', doc='HTTP proxy in format ADDR:PORT')
