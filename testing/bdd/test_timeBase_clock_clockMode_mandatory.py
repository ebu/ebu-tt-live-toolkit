from pytest_bdd import when, scenarios, parsers
from pytest import fixture


scenarios('features/validation/timeBase_clock_clockMode_mandatory.feature')


@when(parsers.parse('it has ttp:timeBase attribute {time_base}'))
def when_has_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@fixture
def clock_mode():
    return ''

@when(parsers.parse('it has ttp:clockMode attribute {clock_mode}'))
@when(parsers.parse('it has ttp:clockMode attribute'))
def when_has_clock_mode(clock_mode, template_dict):
    template_dict['clock_mode'] = clock_mode
