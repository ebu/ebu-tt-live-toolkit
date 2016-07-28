from pytest_bdd import given, then
from jinja2 import Environment, FileSystemLoader
from ebu_tt_live.documents import EBUTT3Document
from datetime import timedelta
import pytest
import os
import unittest


@given('an xml file <xml_file>')
def template_file(xml_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(xml_file)


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
    return document


def timestr_to_timedelta(time_str, time_base):
    time_base = template_dict['time_base']
    if time_base == 'clock' or time_base == 'media':
        hours, minutes, rest = time_str.split(":")
        seconds, milliseconds = rest.split(".")
        avail_timed = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
        return avail_timed


@then('it has resolved begin time <resolved_begin>')
def valid_resolved_begin_time(resolved_begin, gen_doc):
    resolved_begin_timedelta = timestr_to_timedelta(resolved_begin, gen_doc.time_base)
    assert gen_doc.resolved_begin_time == resolved_begin_timedelta


@then('it has resolved end time <resolved_end>')
def valid_resolved_end_time(resolved_end, gen_doc):
    resolved_end_timedelta = timestr_to_timedelta(resolved_end, gen_doc.time_base)
    assert gen_doc.resolved_end_time == resolved_end_timedelta


@pytest.fixture
def template_dict():
    return dict()
