from pytest_bdd import scenarios, given

scenarios('features/validation/referenceClockIdentifier_constraints.feature')


@given('it has timeBase <time_base>')
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@given('it has clock mode <clock_mode>')
def given_clock_mode(clock_mode, template_dict):
    template_dict['clock_mode'] = clock_mode


@given('it has reference clock identifier <ref_clock_id>')
def given_ref_clock_id(ref_clock_id, template_dict):
    template_dict['ref_clock_id'] = ref_clock_id
