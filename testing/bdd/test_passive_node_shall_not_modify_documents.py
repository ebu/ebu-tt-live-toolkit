from ebu_tt_live.node.distributing import DistributingNode
from ebu_tt_live.carriage.base import ProducerCarriageImpl
from ebu_tt_live.documents import EBUTT3Document
from mock import MagicMock
from pytest_bdd import given, when, then, scenarios


scenarios('features/nodes/passive_nodes_shall_not_modify_document.feature')


class TestCarriage(ProducerCarriageImpl):

    _last_emitted_document = None

    def emit_document(self, document):
        self._last_emitted_document = document

    @property
    def last_emitted_document(self):
        return self._last_emitted_document


@given('a distributing node')
def distributing_node(test_context):
    carriage_impl = TestCarriage()
    reference_clock = MagicMock()
    node = DistributingNode('test_distributing', carriage_impl, reference_clock)
    # This will be useful the day we have other passive nodes to test, we will
    # simply need to add a `given` method and not change any other steps.
    # Without that, the name of the variable containing the node would depend
    # on the `given` step and would complicate following steps for no reason.
    test_context['node'] = node
    return node


@when('it processes the document')
def when_processes_document(test_context, template_file):
    xml_file = template_file.render()
    document = EBUTT3Document.create_from_xml(xml_file)
    test_context['document'] = document
    test_context['node'].process_document(document)


@then('the emitted document is identical to the received one')
def then_emitted_document_identical(test_context):
    emitted_document = test_context['node']._carriage_impl.last_emitted_document
    assert emitted_document.get_xml() == test_context['document'].get_xml()
