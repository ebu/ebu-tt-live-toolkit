from pytest_bdd import when, given, then
from jinja2 import Environment, FileSystemLoader
from ebu_tt_live.documents import EBUTT3Document, EBUTT3DocumentSequence, EBUTTDDocument
from ebu_tt_live.documents.converters import EBUTT3EBUTTDConverter
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.node.denester import DenesterNode
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType, LimitedClockTimingType, CellFontSizeType, lineHeightType
from datetime import timedelta
import pytest
import os
import unittest

denester_node = DenesterNode(
    node_id = "denester_node"
);

@given('an xml file <xml_file>')
def template_file(xml_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(xml_file)

@given('a first xml file <xml_file_1>')
def template_file_one(xml_file_1):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(xml_file_1)

@then('a second xml file <xml_file_2>')
def template_file_two(xml_file_2):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(xml_file_2)

# Calling fixtures directly is deprecated, this solution described at
# https://docs.pytest.org/en/latest/deprecations.html#calling-fixtures-directly
# seems to work, creating a named fixture rather than defining the "then"
# step as a fixture directly.
@pytest.fixture(name='template_file_two')
def template_file_two_fixture(xml_file_2):
    return template_file_two(xml_file_2)
    
# NOTE: Some of the code below includes handling of SMPTE time base, which was removed from version 1.0 of the specification.

@given('a sequence <sequence_identifier> with timeBase <time_base>')
def sequence(sequence_identifier, time_base):
    ref_clock = None
    if time_base == 'clock':
        ref_clock = LocalMachineClock()
    elif time_base == 'media':
        ref_clock = MediaClock()
    elif time_base == 'smpte':
        raise NotImplementedError()
    sequence = EBUTT3DocumentSequence(sequence_identifier, ref_clock, 'en-GB', verbose=True)
    return sequence


@then('document is valid')
def valid_doc(template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    assert isinstance(document, EBUTT3Document)

@then('the first document is valid')
def valid_doc_1(template_file_one, template_dict):
    xml_file_1 = template_file_one.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file_1)
    assert isinstance(document, EBUTT3Document)

@then('the second document is valid')
def valid_doc_2(template_file_two, template_dict):
    xml_file_2 = template_file_two.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file_2)
    assert isinstance(document, EBUTT3Document)

@then('document is invalid')
def invalid_doc(template_file, template_dict):
    xml_file = template_file.render(template_dict)
    with pytest.raises(Exception):
        EBUTT3Document.create_from_xml(xml_file)


@given('the document is generated')
def gen_document(template_file, template_dict):
    # TODO: This is legacy and to be removed when tests are refactored
    xml_file = template_file.render(template_dict)
    if 'availability_time' in template_dict:
        document = EBUTT3Document.create_from_xml(xml_file, template_dict['availability_time'])
    else:
        document = EBUTT3Document.create_from_xml(xml_file)
    document.validate()
    return document

@when('the document is generated')
def when_doc_generated(test_context, template_dict, template_file):
    # This is a more standard-compliant way to do this
    xml_file = template_file.render(template_dict)
    if 'availability_time' in template_dict:
        document = EBUTT3Document.create_from_xml(xml_file, template_dict['availability_time'])
    else:
        document = EBUTT3Document.create_from_xml(xml_file)
    test_context['document'] = document


@given('the first document is generated')
def gen_first_document(test_context, template_dict, template_file_one):
    xml_file_1 = template_file_one.render(template_dict)
    document1 = EBUTT3Document.create_from_xml(xml_file_1)
    test_context['document1'] = document1
    document1.validate()
    return document1

@then('the second document is generated')
def gen_second_document(test_context, template_dict, template_file_two):
    xml_file_2 = template_file_two.render(template_dict)
    document2 = EBUTT3Document.create_from_xml(xml_file_2)
    test_context['document2'] = document2
    document2.validate()
    return document2

# Calling fixtures directly is deprecated, this solution described at
# https://docs.pytest.org/en/latest/deprecations.html#calling-fixtures-directly
# seems to work, creating a named fixture rather than defining the "then"
# step as a fixture directly.
@pytest.fixture(name='gen_second_document')
def gen_second_document_fixture(test_context, template_dict, template_file_two):
    return gen_second_document(test_context, template_dict, template_file_two)

@when('the EBU-TT-Live document is denested')
def convert_to_ebuttd(test_context):
    test_context["document"] = denester_node.process_document(test_context["document"])

@when('the EBU-TT-Live document is converted to EBU-TT-D')
def convert_to_ebuttd(test_context):
    ebuttd_converter = EBUTT3EBUTTDConverter(None)
    doc_xml = test_context["document"].get_xml()
    ebutt3_doc = EBUTT3Document.create_from_xml(doc_xml)
    converted_bindings = ebuttd_converter.convert_document(ebutt3_doc.binding)
    ebuttd_document = EBUTTDDocument.create_from_raw_binding(converted_bindings)
    test_context['ebuttd_document'] = ebuttd_document

@then('EBUTTD document is valid')
def then_ebuttd_document_valid(test_context):
    ebuttd_document = test_context['ebuttd_document']
    ebuttd_document.validate()
    assert isinstance(ebuttd_document, EBUTTDDocument)

def timestr_to_timedelta(time_str, time_base):
    if time_base == 'clock':
        return LimitedClockTimingType(time_str).timedelta
    elif time_base == 'media':
        return FullClockTimingType(time_str).timedelta
    elif time_base == 'smpte':
        raise NotImplementedError('SMPTE needs implementation')


@then('it has computed begin time <computed_begin>')
def valid_computed_begin_time(computed_begin, gen_document):
    computed_begin_timedelta = timestr_to_timedelta(computed_begin, gen_document.time_base)
    assert gen_document.computed_begin_time == computed_begin_timedelta

@when('it has body begin time <body_begin>')
def when_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin

@when('it has body duration <body_dur>')
def when_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur

@when('it has body end time <body_end>')
def when_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end

@when('it has div begin time <div_begin>')
def when_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin

@when('it has div end time <div_end>')
def when_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end

@when('it has p begin time <p_begin>')
def when_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin

@when('it has p end time <p_end>')
def when_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end

@when('it has p1 begin time <p1_begin>')
def when_p1_begin(p1_begin, template_dict):
    template_dict['p1_begin'] = p1_begin

@when('it has p1 end time <p1_end>')
def when_p1_end(p1_end, template_dict):
    template_dict['p1_end'] = p1_end

@when('it has span1 begin time <span1_begin>')
def when_span1_begin(span1_begin, template_dict):
    template_dict['span1_begin'] = span1_begin

@when('it has nestedSpan begin time <nestedSpan_begin>')
def when_nestedSpan_begin(nestedSpan_begin, template_dict):
    template_dict['nestedSpan_begin'] = nestedSpan_begin

@when('it has nestedSpan end time <nestedSpan_end>')
def when_nestedSpan_end(nestedSpan_end, template_dict):
    template_dict['nestedSpan_end'] = nestedSpan_end

@when('it has span1 end time <span1_end>')
def when_span1_end(span1_end, template_dict):
    template_dict['span1_end'] = span1_end

@when('it has span2 begin time <span2_begin>')
def when_span2_begin(span2_begin, template_dict):
    template_dict['span2_begin'] = span2_begin

@when('it has span2 end time <span2_end>')
def when_span2_end(span2_end, template_dict):
    template_dict['span2_end'] = span2_end

@when('it has span3 begin time <span3_begin>')
def when_span2_begin(span3_begin, template_dict):
    template_dict['span3_begin'] = span3_begin

@when('it has span3 end time <span3_end>')
def when_span3_end(span3_end, template_dict):
    template_dict['span3_end'] = span3_end

@when('it has div_region <div_region>')
def when_div_region(div_region, template_dict):
    template_dict['div_region'] = div_region

@when('it has p1_region <p1_region>')
def when_p1_region(p1_region, template_dict):
    template_dict['p1_region'] = p1_region

@when('it has p2_region <p2_region>')
def when_p2_region(p2_region, template_dict):
    template_dict['p2_region'] = p2_region

@then('it has computed end time <computed_end>')
def valid_computed_end_time(computed_end, gen_document):
    if computed_end:
        computed_end_timedelta = timestr_to_timedelta(computed_end, gen_document.time_base)
    else:
        computed_end_timedelta = None
    assert gen_document.computed_end_time == computed_end_timedelta


computed_style_attribute_casting = {
    'tts:fontSize': CellFontSizeType,
    'tts:direction': str,  # String is good enough PyXB is smart and figures out the types for us
    'tts:color': str,
    'tts:fontFamily': str,
    'tts:fontStyle': str,
    'tts:fontWeight': str,
    'ebutts:linePadding': str,
    'ebutts:multiRowAlign': str,
    'tts:textAlign': str,
    'tts:textDecoration': str,
    'tts:wrapOption': str,
    'tts:backgroundColor': str,
    'tts:padding': str,
    'tts:unicodeBidi': str,
    'tts:lineHeight': lineHeightType.Factory
}


@then('the computed <style_attribute> in <elem_id> is <computed_value>')
def then_computed_style_value_is(style_attribute, elem_id, computed_value, test_context):
    document = test_context['document']
    elem = document.get_element_by_id(elem_id)
    if computed_value == '':
        assert elem.computed_style.get_attribute_value(style_attribute) is None
    else:
        assert elem.computed_style.get_attribute_value(style_attribute) == computed_style_attribute_casting[style_attribute](computed_value)


@given('it has availability time <avail_time>')
def given_avail_time(avail_time, template_dict, gen_document):
    gen_document.availability_time = timestr_to_timedelta(avail_time, gen_document.time_base)


@pytest.fixture
def template_dict():
    return dict()


@pytest.fixture
def test_context():
    return dict()
