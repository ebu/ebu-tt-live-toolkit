from pytest_bdd import scenarios, when

from testing.bdd.conftest import legacy_name

scenarios('features/validation/timeBase_attribute_mandatory.feature')


@when(**legacy_name('it has ttp:timeBase attribute <time_base>'))
def when_has_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base
