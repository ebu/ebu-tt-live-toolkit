from pytest_bdd import when, scenarios, parsers
from pytest import fixture

scenarios('features/validation/timeBase_attribute_mandatory.feature')


@fixture
def time_base():
    return ''

@when(parsers.parse('it has ttp:timeBase attribute {time_base}'))
@when(parsers.parse('it has ttp:timeBase attribute'))
def when_has_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base
