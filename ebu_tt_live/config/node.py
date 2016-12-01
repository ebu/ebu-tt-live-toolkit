from .common import ConfigurableComponent, Namespace, converters, RequiredConfig
from .clocks import clock_by_type
from .carriage import producer_carriage_by_type, consumer_carriage_by_type
from ebu_tt_live import documents
from ebu_tt_live.example_data import get_example_data
import ebu_tt_live.node as processing_node
from itertools import cycle
from ebu_tt_live.utils import tokenize_english_document
from .adapters import ProducerNodeCarriageAdapter


class NodeBase(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('id', default='generic_node')


class SimpleConsumer(NodeBase):
    required_config = Namespace()
    required_config.add_option('id', default='simple-consumer')
    required_config.input = input_section = Namespace()
    input_section.add_option('type', default='websocket', from_string_converter=consumer_carriage_by_type)


class SimpleProducer(NodeBase):
    required_config = Namespace()
    required_config.add_option('id', default='simple-producer')
    required_config.add_option('show_time', default=False)
    required_config.add_option('sequence_identifier', default='TestSequence1')
    required_config.output = Namespace()
    required_config.output.carriage = Namespace()
    required_config.output.carriage.add_option(
        'type', default='websocket', from_string_converter=producer_carriage_by_type
    )
    required_config.output.add_option('adapters')
    required_config.clock = Namespace()
    required_config.clock.add_option('type', default='local', from_string_converter=clock_by_type)

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

        self.output = local_config.output
        self.output.carriage = local_config.output.carriage.type(config, local_config.output.carriage)

        self.component = processing_node.SimpleProducer(
            node_id='simple-producer',
            document_sequence=sequence,
            producer_carriage=None,
            input_blocks=subtitle_tokens
        )

        self.output.adapters = ProducerNodeCarriageAdapter(
            config=config,
            local_config=local_config.output.adapters,
            producer=self.component,
            carriage=self.output.carriage.component
        )



def nodes_by_type(node_name):
    if node_name == 'simple-consumer':
        return SimpleConsumer
    elif node_name == 'simple-producer':
        return SimpleProducer
    else:
        raise Exception('No such node {}'.format(node_name))


class UniversalNode(RequiredConfig):
    required_config = Namespace()
    required_config.node = node = Namespace()
    node.add_option('type', default='simple-consumer', from_string_converter=nodes_by_type)
