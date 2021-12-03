from ebu_tt_live.node.deduplicator import DeDuplicatorNode
from ebu_tt_live.node.base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings import style_type, region_type
from ebu_tt_live.carriage.interface import IProducerCarriage, IConsumerCarriage
from mock import MagicMock
from pytest_bdd import scenarios, when, then, given, parsers
import six
import pytest

scenarios('features/deduplicator/deduplicator.feature')


@given('a deduplicator node', target_fixture='given_deduplicator_node')
def given_deduplicator_node():
    carriage = MagicMock(spec=IProducerCarriage)
    carriage.expects.return_value = EBUTT3Document

    instance = DeDuplicatorNode(
        node_id='testDeDuplicatorNode',
        sequence_identifier='testDeDuplicated1',
        producer_carriage=carriage
    )
    return instance


@when('the document is processed')
def when_document_processed(given_deduplicator_node, gen_document, test_context):
    given_deduplicator_node.process_document(gen_document)
    test_context['doc'] = gen_document
    given_deduplicator_node.producer_carriage.reset_mock()

@when('the first document is processed')
def when_first_document_processed(given_deduplicator_node, gen_first_document, test_context):
    given_deduplicator_node.process_document(gen_first_document)
    test_context['doc1'] = gen_first_document
    given_deduplicator_node.producer_carriage.reset_mock()

@then('the second document is processed')
def when_second_document_processed(given_deduplicator_node, gen_second_document, test_context):
    given_deduplicator_node.process_document(gen_second_document)
    test_context['doc2'] = gen_second_document
    given_deduplicator_node.producer_carriage.reset_mock()

@then(parsers.parse('the output document has {style_out_num} styles'))
def then_document_has_styles(style_out_num, test_context):
    if test_context['doc'].binding.head.styling is not None:
        new_style_list = test_context['doc'].binding.head.styling.style
        assert int(style_out_num) == len(new_style_list)

@then(parsers.parse('the first output document has {style_out_num_1} styles'))
def then_first_document_has_styles(style_out_num_1, test_context):
    if test_context['doc1'].binding.head.styling is not None:
        new_style_list_1 = test_context['doc1'].binding.head.styling.style
        assert int(style_out_num_1) == len(new_style_list_1)

@then(parsers.parse('the second output document has {style_out_num_2} styles'))
def then_second_document_has_styles(style_out_num_2, test_context):
    if test_context['doc2'].binding.head.styling is not None:
        new_style_list_2 = test_context['doc2'].binding.head.styling.style
        assert int(style_out_num_2) == len(new_style_list_2)

@then(parsers.parse('it has {region_out_num} regions'))
def then_document_has_regions(region_out_num, test_context):
    if test_context['doc'].binding.head.layout is not None:
        new_region_list = test_context['doc'].binding.head.layout.region
        assert int(region_out_num) == len(new_region_list)

@then(parsers.parse('the first output document has {region_out_num_1} regions'))
def then_first_document_has_regions(region_out_num_1, test_context):
    if test_context['doc1'].binding.head.layout is not None:
        new_region_list_1 = test_context['doc1'].binding.head.layout.region
        assert int(region_out_num_1) == len(new_region_list_1)

@then(parsers.parse('the second output document has {region_out_num_2} regions'))
def then_second_document_has_regions(region_out_num_2, test_context):
    if test_context['doc2'].binding.head.layout is not None:
        new_region_list_2 = test_context['doc2'].binding.head.layout.region
        assert int(region_out_num_2) == len(new_region_list_2)
