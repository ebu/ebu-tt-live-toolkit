from pytest_bdd import scenarios, when, parsers
from pytest import fixture

scenarios('features/validation/smpte_constraints.feature')


@fixture
def time_base():
    return None

@when(parsers.parse('it has timeBase {time_base}'))
@when(parsers.parse('it has timeBase'))
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@fixture
def frame_rate():
    return None

@when(parsers.parse('it has frameRate {frame_rate}'))
@when(parsers.parse('it has frameRate'))
def when_frame_rate(frame_rate, template_dict):
    template_dict['frame_rate'] = frame_rate


@fixture
def frame_rate_multiplier():
    return None

@when(parsers.parse('it has frameRateMultiplier {frame_rate_multiplier}'))
@when(parsers.parse('it has frameRateMultiplier'))
def when_frame_rate_multiplier(frame_rate_multiplier, template_dict):
    template_dict['frame_rate_multiplier'] = frame_rate_multiplier


@fixture
def drop_mode():
    return None

@when(parsers.parse('it has dropMode {drop_mode}'))
@when(parsers.parse('it has dropMode'))
def when_drop_mode(drop_mode, template_dict):
    template_dict['drop_mode'] = drop_mode


@fixture
def marker_mode():
    return None

@when(parsers.parse('it has markerMode {marker_mode}'))
@when(parsers.parse('it has markerMode'))
def when_marker_mode(marker_mode, template_dict):
    template_dict['marker_mode'] = marker_mode
