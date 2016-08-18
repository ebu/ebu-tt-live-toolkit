from pytest_bdd import when, scenarios


scenarios('features/validation/sequence_id_num.feature')


@when('it has sequence identifier <seq_id>')
def when_sequence_id(seq_id, template_dict):
    template_dict['sequence_id'] = seq_id


@when('it has sequence number <seq_n>')
def when_sequence_number(seq_n, template_dict):
    template_dict['sequence_num'] = seq_n
