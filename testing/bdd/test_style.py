from pytest_bdd import when, scenarios, then, parsers
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.bindings import ebuttdt
from ebu_tt_live.documents.converters import EBUTT3EBUTTDConverter
from ebu_tt_live.documents.ebuttd import EBUTTDDocument
from datetime import timedelta


scenarios('features/styles/ebuttd_fontsize_conversion.feature')
scenarios('features/styles/ebuttd_fontsize_inheritance.feature')
scenarios('features/styles/ebuttd_fontsize_same_style_ref.feature')
scenarios('features/styles/style_attribute_simple.feature')
scenarios('features/styles/style_attribute_inherited.feature')
scenarios('features/styles/lineHeight.feature')


@when('it has a cell resolution of <cell_resolution>')
@when(parsers.parse('it has a cell resolution of "{cell_resolution}"'))
def when_cell_resolution(template_dict, cell_resolution):
    template_dict['cell_resolution'] = cell_resolution


@when('it has extent of <extent>')
@when(parsers.parse('it has extent of "{extent}"'))
def when_extent(template_dict, extent):
    template_dict['extent'] = extent


@when('it has region fontSize of <region_fontSize>')
@when(parsers.parse('it has region fontSize of "{region_fontSize}"'))
def when_region_fontSize(template_dict, region_fontSize):
    template_dict['region_fontSize'] = region_fontSize


@when('it has div fontSize of <div_fontSize>')
@when(parsers.parse('it has div fontSize of "{div_fontSize}"'))
def when_div_fontSize(template_dict, div_fontSize):
    template_dict['div_fontSize'] = div_fontSize


@when('it has p fontSize of <p_fontSize>')
@when(parsers.parse('it has p fontSize of "{p_fontSize}"'))
def when_p_fontSize(template_dict, p_fontSize):
    template_dict['p_fontSize'] = p_fontSize


@when('it contains style S1 with <style_attribute> value <S1_value>')
def when_s1_attr_value(template_dict, style_attribute, S1_value):
    template_dict['S1_value'] = S1_value
    template_dict['style_attribute'] = style_attribute


@when('it contains style S2 with <style_attribute> value <S2_value>')
def when_s2_attr_value(template_dict, style_attribute, S2_value):
    template_dict['S2_value'] = S2_value
    template_dict['style_attribute'] = style_attribute


@when('it contains style S3 with <style_attribute> value <S3_value>')
def when_s3_attr_value(template_dict, style_attribute, S3_value):
    template_dict['S3_value'] = S3_value
    template_dict['style_attribute'] = style_attribute


@when('it contains style S4 with <style_attribute> value <S4_value>')
def when_s4_attr_value(template_dict, style_attribute, S4_value):
    template_dict['S4_value'] = S4_value
    template_dict['style_attribute'] = style_attribute


@when('R1 contains <style_attribute> value <R1_value>')
def when_r1_attr_value(template_dict, style_attribute, R1_value):
    template_dict['R1_value'] = R1_value
    template_dict['style_attribute'] = style_attribute


@when('S1 contains <style_attribute2> value <S1_value2>')
def when_s1_attr2_value(template_dict, style_attribute2, S1_value2):
    template_dict['S1_value2'] = S1_value2
    template_dict['style_attribute2'] = style_attribute2


@when('S2 contains <style_attribute2> value <S2_value2>')
def when_s2_attr2_value(template_dict, style_attribute2, S2_value2):
    template_dict['S2_value2'] = S2_value2
    template_dict['style_attribute2'] = style_attribute2


@when('S3 contains <style_attribute2> value <S3_value2>')
def when_s3_attr2_value(template_dict, style_attribute2, S3_value2):
    template_dict['S3_value2'] = S3_value2
    template_dict['style_attribute2'] = style_attribute2


@when('S4 contains <style_attribute2> value <S4_value2>')
def when_s4_attr2_value(template_dict, style_attribute2, S4_value2):
    template_dict['S4_value2'] = S4_value2
    template_dict['style_attribute2'] = style_attribute2


@when('it contains style S5 with <style_attribute> value <S5_value>')
def when_s5_attr_value(template_dict, style_attribute, S5_value):
    template_dict['S5_value'] = S5_value
    template_dict['style_attribute'] = style_attribute


@when('it contains style S6 with <style_attribute> value <S6_value>')
def when_s6_attr_value(template_dict, style_attribute, S6_value):
    template_dict['S6_value'] = S6_value
    template_dict['style_attribute'] = style_attribute


@when('the document is converted to EBUTTD with <local_time_mapping>')
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


@then('the EBUTTD has region fontSize <ttd_region_fontSize>')
def then_EBUTTD_has_region_fontSize(test_context, ttd_region_fontSize):
    ttd_doc = test_context['ebuttd_document']
    region = ttd_doc.get_element_by_id('R1')
    fontSize = region.specified_style.get_attribute_value('fontSize')
    if ttd_region_fontSize == '':
        assert fontSize is None
    else:
        assert fontSize == ttd_region_fontSize


@then('the EBUTTD has div fontSize <ttd_div_fontSize>')
def then_EBUTTD_has_div_fontSize(test_context, ttd_div_fontSize):
    ttd_doc = test_context['ebuttd_document']
    div = ttd_doc.get_element_by_id('div1')
    fontSize = div.specified_style.get_attribute_value('fontSize')
    if ttd_div_fontSize == '':
        assert fontSize is None
    else:
        assert fontSize == ttd_div_fontSize


@then('the EBUTTD has div lineHeight of <ttd_div_lineHeight>')
def then_EBUTTD_has_div_lineHeight(test_context, ttd_div_lineHeight):
    ttd_doc = test_context['ebuttd_document']
    div = ttd_doc.get_element_by_id('div1')
    lineHeight = div.specified_style.get_attribute_value('lineHeight')
    if ttd_div_lineHeight == '':
        assert lineHeight is None
    else:
        assert lineHeight == ttd_div_lineHeight


@then('the EBUTTD has p fontSize of <ttd_p_fontSize>')
def then_EBUTTD_has_p_fontSize(test_context, ttd_p_fontSize):
    ttd_doc = test_context['ebuttd_document']
    p = ttd_doc.get_element_by_id('p1')
    fontSize = p.specified_style.get_attribute_value('fontSize')
    if ttd_p_fontSize == '':
        assert fontSize is None
    else:
        assert fontSize == ttd_p_fontSize


@then('the EBUTTD has p lineHeight of <ttd_p_lineHeight>')
def then_EBUTTD_has_p_lineHeight(test_context, ttd_p_lineHeight):
    ttd_doc = test_context['ebuttd_document']
    p = ttd_doc.get_element_by_id('p1')
    lineHeight = p.specified_style.get_attribute_value('lineHeight')
    if ttd_p_lineHeight == '':
        assert lineHeight is None
    else:
        assert lineHeight == ttd_p_lineHeight
