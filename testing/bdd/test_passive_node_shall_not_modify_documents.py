from ebu_tt_live.node.distributing import DistributingNode
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.node.delay import BufferDelayNode
from ebu_tt_live.utils import compare_xml
from mock import MagicMock
from pytest_bdd import given, when, then, scenarios
import six


scenarios('features/nodes/passive_nodes_shall_not_modify_document.feature')


@given('a distributing node')
def distributing_node():
    reference_clock = MagicMock()
    prod_carriage = MagicMock(spec=IProducerCarriage)
    prod_carriage.expects.return_value = six.text_type
    node = DistributingNode(
        'test_distributing',
        producer_carriage=prod_carriage,
        reference_clock=reference_clock
    )
    return node


@given('a buffer delay node')
def buffer_delay_node():
    reference_clock = MagicMock()
    prod_carriage = MagicMock(spec=IProducerCarriage)
    prod_carriage.expects.return_value = six.text_type
    node = BufferDelayNode(
        'test_buffer_delay',
        producer_carriage=prod_carriage,
        reference_clock=reference_clock,
        fixed_delay=5.0
    )
    return node


@when('it delays the document')
def when_delays_document(buffer_delay_node, test_context, template_file):
    xml_file = template_file.render()
    test_context['document'] = xml_file
    buffer_delay_node.process_document(xml_file)


@then('the delayed document is identical to the received one')
def then_delayed_document_identical(buffer_delay_node, test_context):
    prod_carriage = buffer_delay_node.producer_carriage
    assert prod_carriage.emit_data.call_count == 1
    assert compare_xml(test_context['document'], prod_carriage.emit_data.call_args[1]['data'])  # kwargs call differs from positional call


@when('it processes the document')
def when_processes_document(distributing_node, test_context, template_file):
    xml_file = template_file.render()
    test_context['document'] = xml_file
    distributing_node.process_document(xml_file)


@then('the emitted document is identical to the received one')
def then_emitted_document_identical(distributing_node, test_context):
    prod_carriage = distributing_node.producer_carriage
    assert prod_carriage.emit_data.call_count == 1
    assert compare_xml(test_context['document'], prod_carriage.emit_data.call_args[1]['data'])
