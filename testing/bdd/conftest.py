from pytest_bdd import when, given, then, parsers
from jinja2 import Environment, FileSystemLoader
from ebu_tt_live.documents import EBUTT3Document, EBUTT3DocumentSequence, EBUTTDDocument
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType, LimitedClockTimingType, CellFontSizeType, lineHeightType
from datetime import timedelta
import pytest
import os
import unittest


@given(parsers.parse('an xml file {xml_file}'), target_fixture='template_file')
def template_file(xml_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(xml_file)

@given(parsers.parse('a first xml file {xml_file_1}'), target_fixture='template_file_one')
def template_file_one(xml_file_1):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(xml_file_1)

@then(parsers.parse('a second xml file {xml_file_2}'))
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

@given(parsers.parse('a sequence {sequence_identifier} with timeBase {time_base}'), target_fixture='sequence')
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
def valid_doc(template_file_one, template_dict):
    xml_file_1 = template_file_one.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file_1)
    assert isinstance(document, EBUTT3Document)

@then('the second document is valid')
def valid_doc(template_file_two, template_dict):
    xml_file_2 = template_file_two.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file_2)
    assert isinstance(document, EBUTT3Document)

@then('document is invalid')
def invalid_doc(template_file, template_dict):
    xml_file = template_file.render(template_dict)
    with pytest.raises(Exception):
        EBUTT3Document.create_from_xml(xml_file)


@given('the document is generated', target_fixture='gen_document')
def gen_document(template_file, template_dict):
    # TODO: This is legacy and to be removed when tests are refactored
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.validate()
    return document

@when('the document is generated')
def when_doc_generated(test_context, template_dict, template_file):
    # This is a more standard-compliant way to do this
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    test_context['document'] = document


@given('the first document is generated', target_fixture='gen_first_document')
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

@pytest.fixture
def computed_begin():
    return None

@then(parsers.parse('it has computed begin time {computed_begin}'))
@then(parsers.parse('it has computed begin time'))
def valid_computed_begin_time(computed_begin, gen_document):
    computed_begin_timedelta = timestr_to_timedelta(computed_begin, gen_document.time_base)
    assert gen_document.computed_begin_time == computed_begin_timedelta

@pytest.fixture
def computed_end():
    return None

@then(parsers.parse('it has computed end time {computed_end}'))
@then(parsers.parse('it has computed end time'))
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


@pytest.fixture
def computed_value():
    return ''

@then(parsers.parse('the computed {style_attribute} in {elem_id} is {computed_value}'))
@then(parsers.parse('the computed {style_attribute} in {elem_id} is'))
def then_computed_style_value_is(style_attribute, elem_id, computed_value, test_context):
    document = test_context['document']
    elem = document.get_element_by_id(elem_id)
    if computed_value == '':
        assert elem.computed_style.get_attribute_value(style_attribute) is None
    else:
        assert elem.computed_style.get_attribute_value(style_attribute) == computed_style_attribute_casting[style_attribute](computed_value)


@given(parsers.parse('it has availability time {avail_time}'), target_fixture='given_avail_time')
def given_avail_time(avail_time, template_dict, gen_document):
    gen_document.availability_time = timestr_to_timedelta(avail_time, gen_document.time_base)


@pytest.fixture
def template_dict():
    return dict()


@pytest.fixture
def test_context():
    return dict()
