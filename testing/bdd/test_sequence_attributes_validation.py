from ebu_tt_live.documents import EBUTT3Document
from pyxb import ValidationError
from pytest_bdd import given, then, scenarios
import pytest


scenarios('features/validation/sequence_id_num.feature')


@given('it has sequence identifier <seq_id>')
def sequence_id(seq_id):
    return seq_id


@given('it has sequence number <seq_n>')
def sequence_number(seq_n):
    return seq_n


@then('document is invalid')
def invalid_doc(template_file, sequence_id=None, sequence_number=None):
    xml = template_file.render(sequence_id=sequence_id, sequence_num=sequence_number)
    print xml
    with pytest.raises(ValidationError):
        EBUTT3Document.create_from_xml(xml)


@then('document is valid')
def valid_doc(template_file, sequence_id=None, sequence_number=None):
    xml = template_file.render(sequence_id=sequence_id, sequence_num=sequence_number)
    document = EBUTT3Document.create_from_xml(xml)
    assert isinstance(document, EBUTT3Document)
