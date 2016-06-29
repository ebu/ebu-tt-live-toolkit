from ebu_tt_live.documents import EBUTT3Document
from pyxb import SimpleTypeValueError
from pytest_bdd import given, then, scenario
import pytest


@scenario(
    'features/validation/sequence_id_num.feature',
    'Invalid Sequence head attributes',
    example_converters=dict(xml_file=str, seq_id=str, seq_n=str)
)
def test_from_xml_to_binding():
    pass


@given('it has sequence identifier <seq_id>')
def sequence_id(seq_id):
    return seq_id


@given('it has sequence number <seq_n>')
def sequence_number(seq_n):
    return seq_n


@then('document is invalid')
def is_invalid(template_file, sequence_id, sequence_number):
    xml = template_file.render(sequenceIdentifier=sequence_id, sequenceNumber=sequence_number)
    with pytest.raises(SimpleTypeValueError):
        EBUTT3Document.create_from_xml(xml)
