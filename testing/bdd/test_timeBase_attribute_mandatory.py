from pytest_bdd import when, scenarios


scenarios('features/validation/timeBase_attribute_mandatory.feature')


@when('it has ttp:timeBase attribute <time_base>')
def when_sequence_id(time_base, template_dict):
    template_dict['time_base'] = time_base
