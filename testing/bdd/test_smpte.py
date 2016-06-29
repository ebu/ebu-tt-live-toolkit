from pytest_bdd import scenarios, given

scenarios('features/validation/smpte_constraints.feature')


@given('it has timeBase <time_base>')
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@given('it has frameRate <frame_rate>')
def given_frame_rate(frame_rate, template_dict):
    template_dict['frame_rate'] = frame_rate
