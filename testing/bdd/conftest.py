import os

import pytest
from jinja2 import Environment, FileSystemLoader
from pytest_bdd import given, parsers, then, when

from ebu_tt_live.bindings._ebuttdt import (
    CellFontSizeType,
    FullClockTimingType,
    LimitedClockTimingType,
    lineHeightType,
)
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.documents import (
    EBUTT3Document,
    EBUTT3DocumentSequence,
    EBUTTDDocument,
)

# Utility functions


def empty_to_none(value):
    """
    A converter that returns None for empty strings, used in legacy_name()
    """
    return None if value.strip() == "" else value


def legacy_name(
        name: str) -> dict:
    """
    Utility function to map a legacy style name with <field> parameters
    into a parsers.re with converters, to be able to handle null values.

    To use, replace the name or parser arg with
    **legacy_name(name="the step <name>") in a step definition.
    There's no need to use this where there are no <field>s.

    Inspired by (but better than!)
    https://pytest-bdd.readthedocs.io/en/latest/#handling-empty-example-cells
    - in older versions of pytest-bdd steps like this were decoded for you,
    but in someone's wisdom that functionality was removed. A key issue with
    its removal was that to handle empty values as None you'd need to have
    two step definitions that were almost the same, and get them in the right
    order. Using this avoids that issue.
    """
    # Gather the variables and
    # convert from "the <x> and the <y>" to
    # parsers.re("the [<]?(?P<{x}>[^<>]*)[>]? and the [<]?(?P<{y}>[^<>]*)[>]?")
    variables: list[str] = []
    start_pos: int = name.find('<') + 1
    while start_pos != 0:
        end_pos = name.find('>', start_pos)
        if end_pos == -1:
            break
        variable = name[start_pos:end_pos]
        variables.append(variable)

        start_pos = name.find('<', end_pos) + 1

    for variable in variables:
        name = name.replace(
            f'<{variable}>',
            f'[<]?(?P<{variable}>[^<>]*)[>]?')

    return {
        "name": parsers.re(name=name),
        "converters": {v: empty_to_none for v in variables}
        }


@given(
    **legacy_name(name='an xml file <xml_file>'),
    target_fixture='template_file')
@given(
    name=parsers.parse(name='an xml file {xml_file}'),
    target_fixture='template_file')
def template_file(xml_file: str):
    xml_file = xml_file.strip('"')
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(
        loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
        trim_blocks=True)
    return j2_env.get_template(xml_file)


@given(name='it has the following template variables')
@when(name='it has the following template variables')
def template_file_with_variables(datatable, template_dict):
    keys = datatable[0]
    values = [empty_to_none(value=v) for v in datatable[1]]
    # remove keys where the value is None
    for i in range(len(keys)-1, 0, -1):
        if values[i] is None:
            del values[i]
            del keys[i]
    data = dict(zip(keys, values))
    template_dict.update(data)


@given(
    **legacy_name(name='a first xml file <xml_file_1>'),
    target_fixture='template_file_one')
def template_file_one(xml_file_1):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(
        loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
        trim_blocks=True)
    return j2_env.get_template(xml_file_1)


@then(
    **legacy_name(name='a second xml file <xml_file_2>'),
    target_fixture='template_file_two')
def template_file_two(xml_file_2):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(
        loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
        trim_blocks=True)
    return j2_env.get_template(xml_file_2)


# Calling fixtures directly is deprecated, this solution described at
# https://docs.pytest.org/en/latest/deprecations.html#calling-fixtures-directly
# seems to work, creating a named fixture rather than defining the "then"
# step as a fixture directly.
@pytest.fixture(name='template_file_two')
def template_file_two_fixture(xml_file_2):
    return template_file_two(xml_file_2)

# NOTE: Some of the code below includes handling of SMPTE time base, which was
# removed from version 1.0 of the specification.


@given(
    **legacy_name(
        name='a sequence with the following identifier and timeBase'),
    target_fixture='sequence')
def sequence(datatable):
    keys = datatable[0]
    values = datatable[1]
    data = dict(zip(keys, values))
    sequence_identifier = data['sequence_identifier']
    time_base = data['time_base']
    ref_clock = None
    if time_base == 'clock':
        ref_clock = LocalMachineClock()
    elif time_base == 'media':
        ref_clock = MediaClock()
    elif time_base == 'smpte':
        raise NotImplementedError()
    sequence = EBUTT3DocumentSequence(
        sequence_identifier,
        ref_clock,
        'en-GB',
        verbose=True)
    return sequence


@then('document is valid')
def valid_doc(template_file, template_dict):
    xml_file = template_file.render(template_dict)
    # print(f"xml_file: \n{xml_file}")
    document = EBUTT3Document.create_from_xml(xml_file)
    assert isinstance(document, EBUTT3Document)


@then('the first document is valid')
def valid_first_doc(template_file_one, template_dict):
    xml_file_1 = template_file_one.render(template_dict)
    # print(f"xml_file_1: \n{xml_file_1}")
    document = EBUTT3Document.create_from_xml(xml_file_1)
    assert isinstance(document, EBUTT3Document)


@then('the second document is valid')
def valid_second_doc(template_file_two, template_dict):
    xml_file_2 = template_file_two.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file_2)
    assert isinstance(document, EBUTT3Document)


@then('document is invalid')
def invalid_doc(template_file, template_dict):
    xml_file = template_file.render(template_dict)
    # print(f"xml_file: \n{xml_file}")
    with pytest.raises(Exception):  # noqa: B017
        EBUTT3Document.create_from_xml(xml_file)


@given('the document is generated', target_fixture='gen_document')
def gen_document(template_file, template_dict):
    # TODO: This is legacy and to be removed when tests are refactored
    # print('the document is generated')
    # print('template dict: {}'.format(template_dict))
    xml_file = template_file.render(template_dict)
    # print('xml_file:')
    # print(xml_file)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.validate()
    return document


@when('the document is generated')
def when_doc_generated(test_context, template_dict, template_file):
    # This is a more standard-compliant way to do this
    # print('when the document is generated')
    # print('template dict: {}'.format(template_dict))
    xml_file = template_file.render(template_dict)
    # print('xml_file:')
    # print(xml_file)
    document = EBUTT3Document.create_from_xml(xml_file)
    test_context['document'] = document


@given('the first document is generated', target_fixture='gen_first_document')
def gen_first_document(test_context, template_dict, template_file_one):
    xml_file_1 = template_file_one.render(template_dict)
    document1 = EBUTT3Document.create_from_xml(xml_file_1)
    test_context['document1'] = document1
    document1.validate()
    return document1


@then('the second document is generated', target_fixture='gen_second_document')
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
def gen_second_document_fixture(
        test_context,
        template_dict,
        template_file_two):
    return gen_second_document(test_context, template_dict, template_file_two)


@then('EBUTTD document is valid')
def then_ebuttd_document_valid(test_context):
    ebuttd_document = test_context['ebuttd_document']
    ebuttd_document.validate()
    assert isinstance(ebuttd_document, EBUTTDDocument)


def timestr_to_timedelta(time_str, time_base):
    # print(f"timestr_to_timedelta time_str={time_str} time_base={time_base}")
    if time_base == 'clock':
        return LimitedClockTimingType(time_str).timedelta
    elif time_base == 'media':
        return FullClockTimingType(time_str).timedelta
    elif time_base == 'smpte':
        raise NotImplementedError('SMPTE needs implementation')


@then(**legacy_name(name='it has computed begin time <computed_begin>'))
def valid_computed_begin_time(computed_begin, gen_document):
    computed_begin_timedelta = timestr_to_timedelta(
        computed_begin,
        gen_document.time_base)
    assert gen_document.computed_begin_time == computed_begin_timedelta


@then(**legacy_name(name='it has computed end time <computed_end>'))
def valid_computed_end_time(computed_end, gen_document):
    if computed_end:
        computed_end_timedelta = timestr_to_timedelta(
            computed_end,
            gen_document.time_base)
    else:
        computed_end_timedelta = None
    assert gen_document.computed_end_time == computed_end_timedelta


# @then(parsers.parse('it has computed end time '))
# def valid_indefinite_computed_end_time(gen_document):
#     required_end_timedelta = None
#     assert gen_document.computed_end_time == required_end_timedelta


computed_style_attribute_casting = {
    'tts:fontSize': CellFontSizeType,
    'tts:direction': str,  # String is good enough PyXB is smart and figures
                           # out the types for us
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


@then(**legacy_name(
    name='the computed <style_attribute> in <elem_id> is <computed_value>'))
def then_computed_style_value_is(
        style_attribute, elem_id, computed_value, test_context):
    document = test_context['document']
    elem = document.get_element_by_id(elem_id)
    if computed_value:
        assert elem.computed_style.get_attribute_value(style_attribute) == \
            computed_style_attribute_casting[style_attribute](computed_value)
    else:
        assert elem.computed_style.get_attribute_value(style_attribute) is None


@given(
    **legacy_name(name='it has availability time <avail_time>'),
    target_fixture='given_avail_time')
def given_avail_time(avail_time, template_dict, gen_document):
    gen_document.availability_time = timestr_to_timedelta(
        avail_time,
        gen_document.time_base)


@pytest.fixture
def template_dict():
    return {}


@pytest.fixture
def test_context():
    return {}
