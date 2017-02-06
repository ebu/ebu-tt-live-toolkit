from ebu_tt_live.node.distributing import DistributingNode
from ebu_tt_live.carriage.interface import IConsumerCarriage, IProducerCarriage

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


@when('it processes the document')
def when_processes_document(distributing_node, test_context, template_file):
    xml_file = template_file.render()
    test_context['document'] = xml_file
    distributing_node.process_document(xml_file)


@then('the emitted document is identical to the received one')
def then_emitted_document_identical(distributing_node, test_context):
    from ebu_tt_live.utils import compare_xml
    prod_carriage = distributing_node.producer_carriage
    assert prod_carriage.emit_data.call_count == 1
    assert compare_xml(test_context['document'], prod_carriage.emit_data.call_args[0][0])

