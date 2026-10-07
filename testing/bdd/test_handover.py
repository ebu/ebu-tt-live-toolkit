
from unittest.mock import MagicMock

import pytest
from pytest_bdd import given, scenarios, then, when

from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.node import handover as handover_node
from testing.bdd.conftest import legacy_name

scenarios('features/handover/handover_algorithm.feature')
scenarios('features/handover/handover.feature')


@given(
    'a handover node with the following details:',
    target_fixture='given_handover_node')
# def given_handover_node(authors_group_identifier, sequence_identifier):
def _(datatable):
    keys = datatable[0]
    assert 'node' not in keys
    values = datatable[1]
    data = dict(zip(keys, values))

    carriage = MagicMock(spec=IProducerCarriage)
    carriage.expects.return_value = EBUTT3Document
    instance = handover_node.HandoverNode(
        node_id='testHandoverNode',
        authors_group_identifier=data['authors_group_identifier'],
        sequence_identifier=data['sequence_identifier'],
        producer_carriage=carriage
    )
    data['node'] = instance
    return data


@when(**legacy_name(name='it has <sequence_identifier1> and <sequence_number1>'))
def when_sequence_id_and_num_1(sequence_identifier1, sequence_number1, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier1
    template_dict['sequence_number'] = sequence_number1


@when(**legacy_name(name='it has <sequence_identifier2> and <sequence_number2>'))
def when_sequence_id_and_num_2(sequence_identifier2, sequence_number2, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier2
    template_dict['sequence_number'] = sequence_number2


@when(**legacy_name(name='it has authors group identifier <authors_group_identifier>'))
def when_authors_group_id(template_dict, given_handover_node, authors_group_identifier):
    # pytest-bdd isn't providing the value from the data table so override it
    # <authors_group_identifier> was provided in the earlier data table
    template_dict['authors_group_identifier'] = \
        given_handover_node['authors_group_identifier']
    # print(f"it has <authors_group_identifier> with authors_group_identifier = '{authors_group_identifier}'")
    # print(f"template_dict = {template_dict}")
    # print(f"given_handover_node = {given_handover_node}")


@when(**legacy_name(name='it has new authors group identifier <authors_group_identifier>'))
def when_authors_group_id1(template_dict, authors_group_identifier):
    # print(f'when it has new authors group identifier <authors_group_identifier> with value "{authors_group_identifier}')
    template_dict['authors_group_identifier'] = authors_group_identifier


@when(**legacy_name(name='it has authors group control token <authors_group_control_token1>'))
def when_authors_group_token1(template_dict, authors_group_control_token1):
    # print(f'when it has <authors_group_control_token1> with value "{authors_group_control_token1}')
    template_dict['authors_group_control_token'] = authors_group_control_token1


@when('new document is created')
def new_doc_created(template_dict):
    # print('new document is created')
    template_dict.clear()


@when('handover node processes document')
def new_document(test_context, given_handover_node):
    given_handover_node['node'].process_document(test_context['document'])


@then(**legacy_name(name='handover node emits <emitted_documents> documents'))
def then_handover_node_emits(given_handover_node, emitted_documents):
    # print("then_handover_node_emits()")
    # print(f"given_handover_node = {given_handover_node}")
    assert given_handover_node['node'].producer_carriage.emit_data.call_count == int(emitted_documents)


@then('handover node errors when processing document')
def then_handover_node_errors(given_handover_node, test_context):
    with pytest.raises(Exception):  # noqa: B017
        given_handover_node['node'].process_document(test_context['document'])


@then(**legacy_name(name='the emitted documents belong to <sequence_identifier> and use consecutive sequence numbering from 1'))
def then_handover_node_produces_sequence(given_handover_node, sequence_identifier):
    # pytest-bdd isn't providing the value from the data table so override it
    sequence_identifier = given_handover_node['sequence_identifier']
    counter = 1
    for pos_args, kw_args in given_handover_node['node'].producer_carriage.emit_data.call_args_list:
        assert kw_args['data'].sequence_identifier == sequence_identifier
        assert kw_args['data'].sequence_number == counter
        counter += 1


@then(**legacy_name(name='the emitted documents specify a token and have <authors_group_identifier>'))
def then_handover_parameter_passthrough(given_handover_node, authors_group_identifier):
    # pytest-bdd isn't providing the value from the data table so override it
    authors_group_identifier = given_handover_node['authors_group_identifier']
    for pos_args, kw_args in given_handover_node['node'].producer_carriage.emit_data.call_args_list:
        assert kw_args['data'].authors_group_identifier == authors_group_identifier
        assert kw_args['data'].authors_group_control_token is not None


@then(**legacy_name(name='the emitted documents have <authors_group_selected_sequence_identifiers>'))
def then_authors_group_selected_sequence_id(given_handover_node, authors_group_selected_sequence_identifiers):
    # NOTE: The comma is a valid sequenceIdentifier character but we use it as a divisor in the test. Make sure
    # the tests use sequence identifiers without commas.
    # seq_ids = map(lambda x: x.strip(), authors_group_selected_sequence_identifiers.split(','))
    if authors_group_selected_sequence_identifiers is None:
        seq_ids = []
    else:
        seq_ids = [x.strip() for x in authors_group_selected_sequence_identifiers.split(',')]
    for index, call_args in enumerate(given_handover_node['node'].producer_carriage.emit_data.call_args_list):
        pos_args, kw_args = call_args
        assert kw_args['data'].authors_group_selected_sequence_identifier == seq_ids[index]
