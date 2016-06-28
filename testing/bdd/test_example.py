from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings import CreateFromDocument
from pyxb import SimpleTypeValueError
from pytest_bdd import given, then, scenario
import pytest
from jinja2 import Environment, FileSystemLoader
import os


@scenario(
    'features/templating_example.feature',
    'From xml to binding (wrongs)',
    example_converters=dict(xml_file=str, seqID=str, seqN=str)
)
def test_from_xml_to_binding():
    pass


@given('an xml file <xml_file>')
def template_file(xml_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(os.path.join(cur_dir, 'templates')),
                         trim_blocks=True)
    return j2_env.get_template('base.xml')


@given('it has sequence identifier <seqID>')
def sequenceID(seqID):
    return seqID


@given('it has sequence number <seqN>')
def sequenceN(seqN):
    return seqN


@then('the document is invalid')
def is_invalid(template_file, seqID, sequenceN):
    xml = template_file.render(sequenceIdentifier=seqID, sequenceNumber=sequenceN)
    with pytest.raises(SimpleTypeValueError):
        EBUTT3Document.create_from_xml(xml)
