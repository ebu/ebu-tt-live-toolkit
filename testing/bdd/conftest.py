import os
import unittest
from pytest_bdd import given, then
from jinja2 import Environment, FileSystemLoader
from ebu_tt_live.documents import EBUTT3Document



@given('a xml file <xml_file>')
def template_file(xml_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template(xml_file)

@then(
    'document is valid'
)
def valid_doc(template_file, time_base, frame_rate=None):
    xml_file = template_file.render(time_base=time_base, frame_rate=frame_rate)
    document = EBUTT3Document.create_from_xml(xml_file)
    assert isinstance(document, EBUTT3Document)
