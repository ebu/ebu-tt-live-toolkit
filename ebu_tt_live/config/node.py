from .common import ConfigurableComponent, Namespace, converters, RequiredConfig
from .clocks import clock_by_type
from .carriage import carriage_by_type
from ebu_tt_live import documents
from ebu_tt_live.example_data import get_example_data
import ebu_tt_live.node as processing_node
from itertools import cycle
from ebu_tt_live.utils import tokenize_english_document


class NodeBase(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('id', default='generic_node')


class SimpleConsumer(NodeBase):
    required_config = Namespace()
    required_config.add_option('id', default='simple-consumer')
    required_config.input = input_section = Namespace()
    input_section.add_option('type', default='websocket-input', from_string_converter=carriage_by_type)


class SimpleProducer(NodeBase):
    required_config = Namespace()
    required_config.add_option('id', default='simple-producer')
    required_config.add_option('show_time', default=False)
    required_config.add_option('sequence_identifier', default='TestSequence1')
    required_config.output = output_section = Namespace()
    output_section.add_option('type', default='websocket-output', from_string_converter=carriage_by_type)
    required_config.clock = clock_section = Namespace()
    clock_section.add_option('type', default='local', from_string_converter=clock_by_type)

    clock = None
    output = None

    def __init__(self, config, local_config):
        super(SimpleProducer, self).__init__(config, local_config)
        self.clock = local_config.clock.type(config, local_config.clock)
        sequence = documents.EBUTT3DocumentSequence(
            sequence_identifier=local_config.sequence_identifier,
            lang='en-GB',
            reference_clock=self.clock.component
        )
        self.output = local_config.output.type(config, local_config.output)

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

        self.component = processing_node.SimpleProducer(
            node_id='simple-producer',
            document_sequence=sequence,
            carriage_impl=self.output.component,
            input_blocks=subtitle_tokens
        )


def nodes_by_name(node_name):
    if node_name == 'simple-consumer':
        return SimpleConsumer
    elif node_name == 'simple-producer':
        return SimpleProducer
    else:
        raise Exception('No such node {}'.format(node_name))


class UniversalNode(RequiredConfig):
    required_config = Namespace()
    required_config.node = node = Namespace()
    node.add_option('type', default='simple-consumer', from_string_converter=nodes_by_name)
