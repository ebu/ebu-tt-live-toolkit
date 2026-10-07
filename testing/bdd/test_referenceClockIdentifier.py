from pytest_bdd import scenarios, when

from testing.bdd.conftest import legacy_name

scenarios('features/validation/referenceClockIdentifier_constraints.feature')


@when(**legacy_name(name='it has timeBase <time_base>'))
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when(**legacy_name(name='it has clock mode <clock_mode>'))
def when_clock_mode(clock_mode, template_dict):
    template_dict['clock_mode'] = clock_mode


@when(**legacy_name(name='it has reference clock identifier <ref_clock_id>'))
def when_ref_clock_id(ref_clock_id, template_dict):
    template_dict['ref_clock_id'] = ref_clock_id
