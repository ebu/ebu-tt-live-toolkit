
from configman import RequiredConfig, ConfigurationManager, Namespace, environment, ConfigFileFutureProxy, \
    command_line, converters
from itertools import cycle
from ebu_tt_live.scripts.common import tokenize_english_document
from ebu_tt_live import node
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl, TwistedProducerImpl
from ebu_tt_live.twisted import websocket
from ebu_tt_live.example_data import get_example_data
from ebu_tt_live import documents, clocks


class ConfigurableComponent(object):

    @classmethod
    def configure(cls, config, local_config):
        instance = cls()
        instance.config = local_config
        return instance


class LocalMachineClock(RequiredConfig, ConfigurableComponent):
    required_config = Namespace()

    @classmethod
    def create_from_config(cls, local_config):
        return clocks.local.LocalMachineClock()


def clock_for_type(clock_type):
    if clock_type == 'local':
        return LocalMachineClock


class FileOutput(RequiredConfig, ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('folder', default='./export')


class WebsocketBase(RequiredConfig):
    required_config = Namespace()
    required_config.add_option('uri', default='ws://localhost:9001')
    required_config.add_option('channel', default='TestSequence1')


class WebsocketOutput(WebsocketBase, ConfigurableComponent):

    @classmethod
    def create_from_config(cls, local_config):
        out_carriage = TwistedProducerImpl()
        out_carriage.twisted_channel = local_config.channel

        factory = websocket.BroadcastServerFactory(local_config.uri)
        factory.protocol = websocket.StreamingServerProtocol
        factory.listen()


class WebsocketInput(WebsocketBase, ConfigurableComponent):
    pass


class NodeBase(RequiredConfig, ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('id', default='base_node')


class SimpleConsumer(NodeBase):
    required_config = Namespace()
    required_config.add_option('id', default='simple-consumer')
    required_config.input = input_section = Namespace()
    input_section.add_option('type', default='WebsocketInput', from_string_converter=converters.class_converter)


class SimpleProducer(NodeBase):
    required_config = Namespace()
    required_config.add_option('id', default='simple-producer')
    required_config.add_option('show_time', default=False)
    required_config.add_option('sequence_identifier', default='TestSequence1')
    required_config.output = output_section = Namespace()
    output_section.add_option('type', default='WebsocketOutput', from_string_converter=converters.class_converter)
    required_config.clock = clock_section = Namespace()
    clock_section.add_option('type', default='local', from_string_converter=clock_for_type)

    @classmethod
    def create_from_config(cls, local_config):
        reference_clock = local_config.clock.type.create_from_config(local_config.clock)
        sequence = documents.EBUTT3DocumentSequence(
            sequence_identifier=local_config.sequence_identifier,
            lang='en-GB',
            reference_clock=reference_clock
        )
        output_carriage = local_config.output.type.create_from_config(local_config.output)

        if local_config.show_time:
            subtitle_tokens = None  # Instead of text we provide the availability time as content.
        else:
            # Let's read our example conversation
            full_text = get_example_data('simple_producer.txt')
            # if do_export:
            #     subtitle_tokens = iter(tokenize_english_document(full_text))
            # else:
            #     # This makes the source cycle infinitely.
            subtitle_tokens = cycle(tokenize_english_document(full_text))

        simple_producer = node.SimpleProducer(
            node_id='simple-producer',
            document_sequence=sequence,
            carriage_impl=output_carriage,
            input_blocks=subtitle_tokens
        )

        return simple_producer


class UniversalNode(RequiredConfig):
    required_config = Namespace()
    required_config.node = node = Namespace()
    node.add_option('type', default='SimpleConsumer', from_string_converter=converters.class_converter)


def main():
    cm = ConfigurationManager(
        definition_source=[
            UniversalNode.get_required_config()
        ],
        values_source_list=[
            ConfigFileFutureProxy,
            command_line
        ]
    )
    config = cm.get_config()

    #node = config.node.type.create_from_config(config.node)

    node = config.node.type.configure(config, config.node)
    print node


if __name__ == '__main__':
    main()
