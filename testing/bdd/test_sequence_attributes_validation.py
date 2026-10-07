from pytest_bdd import scenarios, when

from testing.bdd.conftest import legacy_name

scenarios('features/validation/sequence_id_num.feature')


@when(**legacy_name(name='it has sequence identifier <seq_id>'))
def when_sequence_id(seq_id, template_dict):
    template_dict['sequence_id'] = seq_id


@when(**legacy_name(name='it has sequence number <seq_n>'))
def when_sequence_number(seq_n, template_dict):
    template_dict['sequence_num'] = seq_n
