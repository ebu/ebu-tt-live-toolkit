from pytest_bdd import given, scenarios


scenarios('features/validation/timeBase_attribute_mandatory.feature')


@given('it has ttp:timeBase attribute <time_base>')
def given_sequence_id(time_base, template_dict):
    template_dict['time_base'] = time_base
