from pytest_bdd import when, scenarios, then, parsers
from pytest import fixture
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.bindings import ebuttdt
from ebu_tt_live.documents.converters import EBUTT3EBUTTDConverter
from ebu_tt_live.documents.ebuttd import EBUTTDDocument
from datetime import timedelta


scenarios('features/styles/ebuttd_fontsize_conversion.feature')
scenarios('features/styles/style_attribute_simple.feature')
scenarios('features/styles/style_attribute_inherited.feature')
scenarios('features/styles/lineHeight.feature')


@when(parsers.parse('it has a cell resolution of {cell_resolution}'))
def when_cell_resolution(template_dict, cell_resolution):
    template_dict['cell_resolution'] = cell_resolution


@fixture
def extent():
    return None

@when(parsers.parse('it has extent of {extent}'))
@when(parsers.parse('it has extent of'))
def when_extent(template_dict, extent):
    template_dict['extent'] = extent


@fixture
def S1_value():
    return ''

@when(parsers.parse('it contains style S1 with {style_attribute} value {S1_value}'))
@when(parsers.parse('it contains style S1 with {style_attribute} value'))
def when_s1_attr_value(template_dict, style_attribute, S1_value):
    template_dict['S1_value'] = S1_value
    template_dict['style_attribute'] = style_attribute


@fixture
def S2_value():
    return ''

@when(parsers.parse('it contains style S2 with {style_attribute} value {S2_value}'))
@when(parsers.parse('it contains style S2 with {style_attribute} value'))
def when_s2_attr_value(template_dict, style_attribute, S2_value):
    template_dict['S2_value'] = S2_value
    template_dict['style_attribute'] = style_attribute


@fixture
def S3_value():
    return ''

@when(parsers.parse('it contains style S3 with {style_attribute} value {S3_value}'))
@when(parsers.parse('it contains style S3 with {style_attribute} value'))
def when_s3_attr_value(template_dict, style_attribute, S3_value):
    template_dict['S3_value'] = S3_value
    template_dict['style_attribute'] = style_attribute


@fixture
def S4_value():
    return ''

@when(parsers.parse('it contains style S4 with {style_attribute} value {S4_value}'))
@when(parsers.parse('it contains style S4 with {style_attribute} value'))
def when_s4_attr_value(template_dict, style_attribute, S4_value):
    template_dict['S4_value'] = S4_value
    template_dict['style_attribute'] = style_attribute


@fixture
def R1_value():
    return ''

@when(parsers.parse('R1 contains {style_attribute} value {R1_value}'))
@when(parsers.parse('R1 contains {style_attribute} value'))
def when_r1_attr_value(template_dict, style_attribute, R1_value):
    template_dict['R1_value'] = R1_value
    template_dict['style_attribute'] = style_attribute


@fixture
def S1_value2():
    return ''

@when(parsers.parse('S1 contains {style_attribute2} value {S1_value2}'))
@when(parsers.parse('S1 contains {style_attribute2} value'))
def when_s1_attr2_value(template_dict, style_attribute2, S1_value2):
    template_dict['S1_value2'] = S1_value2
    template_dict['style_attribute2'] = style_attribute2


@fixture
def S2_value2():
    return ''

@when(parsers.parse('S2 contains {style_attribute2} value {S2_value2}'))
@when(parsers.parse('S2 contains {style_attribute2} value'))
def when_s2_attr2_value(template_dict, style_attribute2, S2_value2):
    template_dict['S2_value2'] = S2_value2
    template_dict['style_attribute2'] = style_attribute2


@fixture
def S3_value2():
    return ''

@when(parsers.parse('S3 contains {style_attribute2} value {S3_value2}'))
@when(parsers.parse('S3 contains {style_attribute2} value'))
def when_s3_attr2_value(template_dict, style_attribute2, S3_value2):
    template_dict['S3_value2'] = S3_value2
    template_dict['style_attribute2'] = style_attribute2


@fixture
def S4_value2():
    return ''

@when(parsers.parse('S4 contains {style_attribute2} value {S4_value2}'))
@when(parsers.parse('S4 contains {style_attribute2} value'))
def when_s4_attr2_value(template_dict, style_attribute2, S4_value2):
    template_dict['S4_value2'] = S4_value2
    template_dict['style_attribute2'] = style_attribute2


@when(parsers.parse('it contains style S5 with {style_attribute} value {S5_value}'))
def when_s5_attr_value(template_dict, style_attribute, S5_value):
    template_dict['S5_value'] = S5_value
    template_dict['style_attribute'] = style_attribute


@when(parsers.parse('it contains style S6 with {style_attribute} value {S6_value}'))
def when_s6_attr_value(template_dict, style_attribute, S6_value):
    template_dict['S6_value'] = S6_value
    template_dict['style_attribute'] = style_attribute


@when(parsers.parse('the document is converted to EBUTTD with {local_time_mapping}'))
def when_document_converted(test_context, local_time_mapping):
    media_clock = MediaClock()
    media_clock.adjust_time(timedelta(), ebuttdt.LimitedClockTimingType(local_time_mapping).timedelta)
    ebuttd_converter = EBUTT3EBUTTDConverter(
        media_clock=media_clock
    )
    converted_bindings = ebuttd_converter.convert_document(test_context['document'].binding)
    ebuttd_document = EBUTTDDocument.create_from_raw_binding(converted_bindings)
    test_context['ebuttd_document'] = ebuttd_document
    # TODO: Add the proper assertions
    ebuttd_document.get_xml()
