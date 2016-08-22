import os

import pytest
from ebu_tt_live.bindings.ebutt_live import ebuttdt
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.documents import EBUTT3Document, EBUTT3DocumentSequence
from jinja2 import Environment, FileSystemLoader
from pytest_bdd import given, then


@given('an xml file <xml_file>')
def template_file(xml_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(xml_file)


@given('a sequence <sequence_identifier> with timeBase <time_base>')
def sequence(sequence_identifier, time_base):
    ref_clock = None
    if time_base == 'clock':
        ref_clock = LocalMachineClock()
    elif time_base == 'media':
        ref_clock = MediaClock()
    elif time_base == 'smpte':
        raise NotImplementedError()
    sequence = EBUTT3DocumentSequence(sequence_identifier, ref_clock, 'en-GB')
    return sequence


@then('document is valid')
def valid_doc(template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    assert isinstance(document, EBUTT3Document)


@then('document is invalid')
def invalid_doc(template_file, template_dict):
    xml_file = template_file.render(template_dict)
    with pytest.raises(Exception):
        EBUTT3Document.create_from_xml(xml_file)


@given('the document is generated')
def gen_document(template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.validate()
    return document


def timestr_to_timedelta(time_str, time_base):
    if time_base == 'clock':
        return ebuttdt.FullClockTimingType(time_str).timedelta
    elif time_base == 'media':
        return ebuttdt.FullClockTimingType(time_str).timedelta
    elif time_base == 'smpte':
        raise NotImplementedError('SMPTE needs implementation')


@then('it has computed begin time <computed_begin>')
def valid_computed_begin_time(computed_begin, gen_document):
    computed_begin_timedelta = timestr_to_timedelta(computed_begin, gen_document.time_base)
    assert gen_document.computed_begin_time == computed_begin_timedelta


@then('it has computed end time <computed_end>')
def valid_computed_end_time(computed_end, gen_document):
    if computed_end:
        computed_end_timedelta = timestr_to_timedelta(computed_end, gen_document.time_base)
    else:
        computed_end_timedelta = None
    assert gen_document.computed_end_time == computed_end_timedelta


@given('it has availability time <avail_time>')
def given_avail_time(avail_time, template_dict, gen_document):
    gen_document.availability_time = timestr_to_timedelta(avail_time, template_dict['time_base'])


@pytest.fixture
def template_dict():
    return dict()


@pytest.fixture
def test_context():
    return dict()
