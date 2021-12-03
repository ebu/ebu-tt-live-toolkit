from pytest_bdd import scenarios, when, parsers
from pytest import fixture

scenarios('features/validation/referenceClockIdentifier_constraints.feature')


@fixture
def clock_mode():
    return None

@when(parsers.parse('it has timeBase {time_base}'))
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@fixture
def clock_mode():
    return None

@when(parsers.parse('it has clock mode {clock_mode}'))
@when(parsers.parse('it has clock mode'))
def when_clock_mode(clock_mode, template_dict):
    template_dict['clock_mode'] = clock_mode


@fixture
def ref_clock_id():
    return None

@when(parsers.parse('it has reference clock identifier {ref_clock_id}'))
@when(parsers.parse('it has reference clock identifier'))
def when_ref_clock_id(ref_clock_id, template_dict):
    template_dict['ref_clock_id'] = ref_clock_id
