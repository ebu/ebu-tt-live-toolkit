from pytest_bdd import scenarios, when

scenarios('features/validation/referenceClockIdentifier_constraints.feature')


@when('it has timeBase <time_base>')
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when('it has clock mode <clock_mode>')
def when_clock_mode(clock_mode, template_dict):
    template_dict['clock_mode'] = clock_mode


@when('it has reference clock identifier <ref_clock_id>')
def when_ref_clock_id(ref_clock_id, template_dict):
    template_dict['ref_clock_id'] = ref_clock_id
