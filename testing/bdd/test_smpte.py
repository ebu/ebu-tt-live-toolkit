from pytest_bdd import scenarios, given

scenarios('features/validation/smpte_constraints.feature')


@given('it has timeBase <time_base>')
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@given('it has frameRate <frame_rate>')
def given_frame_rate(frame_rate, template_dict):
    template_dict['frame_rate'] = frame_rate


@given('it has frameRateMultiplier <frame_rate_multiplier>')
def given_frame_rate_multiplier(frame_rate_multiplier, template_dict):
    template_dict['frame_rate_multiplier'] = frame_rate_multiplier


@given('it has dropMode <drop_mode>')
def given_drop_mode(drop_mode, template_dict):
    template_dict['drop_mode'] = drop_mode


@given('it has markerMode <marker_mode>')
def given_marker_mode(marker_mode, template_dict):
    template_dict['marker_mode'] = marker_mode
