from pytest_bdd import given, scenarios


scenarios('features/validation/sequence_id_num.feature')


@given('it has sequence identifier <seq_id>')
def given_sequence_id(seq_id, template_dict):
    template_dict['sequence_id'] = seq_id


@given('it has sequence number <seq_n>')
def given_sequence_number(seq_n, template_dict):
    template_dict['sequence_num'] = seq_n
