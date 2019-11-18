from pytest_bdd import scenarios, when, then, given, parsers
from ebu_tt_live.errors import ExtentMissingError
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
import xml.etree.ElementTree as ET
import pytest

scenarios('features/styles/ebuttd_style_references.feature')
scenarios('features/unit_conversion/ebuttd_colour_conversion.feature')
scenarios('features/unit_conversion/ebuttd_line_height_conversion.feature')
scenarios('features/unit_conversion/ebuttd_origin_extent_conversion.feature')
scenarios('features/validation/lengthtype_constraints.feature')


@when(parsers.parse('the document has a cell resolution of "{cell_resolution}"'))
def when_document_has_cell_resolution(template_dict, cell_resolution):
    template_dict['cell_resolution'] = cell_resolution


@when(parsers.parse('the document has an extent of "{extent}"'))
def when_document_has_extent(template_dict, extent):
    template_dict['extent'] = extent


@when('the document does not specify an extent')
def when_doc_has_no_extent():
    #Do nothing, default behaviour is no extent
    pass


@when(parsers.parse('it contains style "{style_name}"'))
def when_it_contains_style(test_context, template_dict, style_name):
    if 'styles' not in template_dict:
        template_dict['styles'] = list()
    style = {"id": style_name}
    template_dict['styles'].append(style)
    test_context[style_name] = style


@when(parsers.parse('style "{style_name}" has attribute "{attribute}" set to "{ebu_tt_live_value}"'))
@when(parsers.parse('style "{style_name}" has attribute "{attribute}" set to <ebu_tt_live_value>'))
@when(parsers.parse('style "{style_name}" has attribute <attribute> set to <ebu_tt_live_value>'))
def when_style_has_attribute(test_context, style_name, attribute, ebu_tt_live_value):
    test_context[style_name][attribute] = ebu_tt_live_value


@when(parsers.parse('style "{style_name}" has attribute "{attribute}" set to <lineHeight>'))
def when_style_has_line_height_attribute(test_context, style_name, attribute, lineHeight):
    test_context[style_name][attribute] = lineHeight


@when(parsers.parse('style "{style_name}" has attribute "{attribute}" set to <fontSize>'))
def when_style_has_fontSize_attribute(test_context, style_name, attribute, fontSize):
    test_context[style_name][attribute] = fontSize


@when(parsers.parse('it contains some text with style "{style_name}"'))
def when_text_has_style(template_dict, style_name):
    template_dict['text_style'] = style_name


@when(parsers.parse('it contains some text with region "{region_name}"'))
def when_text_has_region(template_dict, region_name):
    template_dict['text_region'] = region_name


@when(parsers.parse('it contains region "{region_id}"'))
def when_it_contains_region(test_context, template_dict, region_id):
    if 'regions' not in template_dict:
        template_dict['regions'] = list()
    region = {"id": region_id}
    template_dict['regions'].append(region)
    test_context[region_id] = region


@when(parsers.parse('region "{region_id}" has attribute "{attribute}" set to "{value}"'))
@when(parsers.parse('region "{region_id}" has attribute <attribute> set to "{value}"'))
@when(parsers.parse('region "{region_id}" has attribute <attribute> set to <value>'))
def when_region_has_attribute(test_context, region_id, attribute, value):
    test_context[region_id][attribute] = value


@then(parsers.parse('the ebu_tt_d document contains style "{style_name}" with attribute "{attribute}" set to "{ebu_tt_d_value}"'))
@then(parsers.parse('the ebu_tt_d document contains style "{style_name}" with attribute "{attribute}" set to <ebu_tt_d_value>'))
def then_converted_document_has_style(test_context, style_name, attribute, ebu_tt_d_value):
    ebuttd_document = test_context['ebuttd_document']
    tree = ET.fromstring(ebuttd_document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}head/'
                            '{http://www.w3.org/ns/ttml}styling/'
                            '{http://www.w3.org/ns/ttml}style[@{http://www.w3.org/XML/1998/namespace}id="%s"]' % style_name)
    assert len(elements) == 1
    assert elements[0].get('{http://www.w3.org/ns/ttml#styling}%s' % attribute) == ebu_tt_d_value

@then(parsers.parse('the ebu_tt_d document contains style <style_id> with attribute "{attribute}" set to <ebu_tt_d_value>'))
def then_converted_document_has_style_with_attribute_and_value(test_context, style_id, attribute, ebu_tt_d_value):
    ebuttd_document = test_context['ebuttd_document']
    tree = ET.fromstring(ebuttd_document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}head/'
                            '{http://www.w3.org/ns/ttml}styling/'
                            '{http://www.w3.org/ns/ttml}style[@{http://www.w3.org/XML/1998/namespace}id="%s"]' % style_id)
    assert len(elements) == 1
    assert elements[0].get('{http://www.w3.org/ns/ttml#styling}%s' % attribute) == ebu_tt_d_value

@then(parsers.parse('the ebu_tt_d document contains region "{region_id}" with attribute "{attribute}" set to "{value}"'))
def then_converted_document_has_region_with_styling_attribute(test_context, region_id, attribute, value):
    ebuttd_document = test_context['ebuttd_document']
    tree = ET.fromstring(ebuttd_document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}head/'
                            '{http://www.w3.org/ns/ttml}layout/'
                            '{http://www.w3.org/ns/ttml}region[@{http://www.w3.org/XML/1998/namespace}id="%s"]' % region_id)
    assert len(elements) == 1
    assert elements[0].get('{http://www.w3.org/ns/ttml#styling}%s' % attribute) == value


@then(parsers.parse('the ebu_tt_d document contains style "{style_id}" without a "{attribute}" attribute'))
def then_converted_document_has_style_without_attribute(test_context, style_id, attribute):
    ebuttd_document = test_context['ebuttd_document']
    tree = ET.fromstring(ebuttd_document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}head/'
                            '{http://www.w3.org/ns/ttml}styling/'
                            '{http://www.w3.org/ns/ttml}style[@{http://www.w3.org/XML/1998/namespace}id="%s"]' % style_id)
    assert len(elements) == 1
    assert elements[0].get('{http://www.w3.org/ns/ttml#styling}%s' % attribute) == None

@then('document has an ExtentMissingError')
def invalid_doc(template_file, template_dict):

    xml_file = template_file.render(template_dict)
    try:
        EBUTT3Document.create_from_xml(xml_file)
    except Exception as exc:
        assert isinstance(exc, ExtentMissingError)    
    else:
        pytest.fail('No exception thrown')
        assert False

 