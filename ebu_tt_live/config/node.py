from .common import ConfigurableComponent, Namespace, converters
from .clocks import clock_for_type
from ebu_tt_live import documents
from ebu_tt_live.example_data import get_example_data
from ebu_tt_live import node as processing_node
from itertools import cycle
from ebu_tt_live.utils import tokenize_english_document


class NodeBase(ConfigurableComponent):
    required_config = Namespace()
    required_config.add_option('id', default='generic_node')


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
    def configure(cls, config, local_config):
        reference_clock = local_config.clock.type.configure(config, local_config.clock)
        sequence = documents.EBUTT3DocumentSequence(
            sequence_identifier=local_config.sequence_identifier,
            lang='en-GB',
            reference_clock=reference_clock
        )
        output_carriage = local_config.output.type.configure(config, local_config.output)

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

        simple_producer = processing_node.SimpleProducer(
            node_id='simple-producer',
            document_sequence=sequence,
            carriage_impl=output_carriage,
            input_blocks=subtitle_tokens
        )

        return simple_producer