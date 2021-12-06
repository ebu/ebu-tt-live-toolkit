from pytest_bdd import when, scenarios, parsers
from pytest import fixture

scenarios('features/validation/sequence_id_num.feature')


@fixture
def seq_id():
    return ''

@when(parsers.parse('it has sequence identifier {seq_id}'))
@when(parsers.parse('it has sequence identifier'))
def when_sequence_id(seq_id, template_dict):
    template_dict['sequence_id'] = seq_id


@fixture
def seq_n():
    return ''

@when(parsers.parse('it has sequence number {seq_n}'))
@when(parsers.parse('it has sequence number'))
def when_sequence_number(seq_n, template_dict):
    template_dict['sequence_num'] = seq_n
