from ebu_tt_live.documents import EBUTT3Document
from pyxb import SimpleTypeValueError
from pytest_bdd import given, then, scenario
from .common import load_template
import pytest


@scenario(
    'features/validation/templating_example.feature',
    'From xml to binding (wrongs)',
    example_converters=dict(xml_file=str, seqID=str, seqN=str)
)
def test_from_xml_to_binding():
    pass


@given('a xml file <xml_file>')
def template_file(xml_file):
    return load_template(xml_file)


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
