from pytest_bdd import scenarios, when

scenarios('features/validation/smpte_constraints.feature')


@when('it has timeBase <time_base>')
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when('it has frameRate <frame_rate>')
def when_frame_rate(frame_rate, template_dict):
    template_dict['frame_rate'] = frame_rate


@when('it has frameRateMultiplier <frame_rate_multiplier>')
def when_frame_rate_multiplier(frame_rate_multiplier, template_dict):
    template_dict['frame_rate_multiplier'] = frame_rate_multiplier


@when('it has dropMode <drop_mode>')
def when_drop_mode(drop_mode, template_dict):
    template_dict['drop_mode'] = drop_mode


@when('it has markerMode <marker_mode>')
def when_marker_mode(marker_mode, template_dict):
    template_dict['marker_mode'] = marker_mode
