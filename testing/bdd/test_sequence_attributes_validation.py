from ebu_tt_live.documents import EBUTT3Document, EBUTT3DocumentSequence
from ebu_tt_live.clocks.local import LocalMachineClock
from pytest_bdd import given, when, then, scenarios
import pytest


scenarios('features/validation/sequence_id_num.feature')


@when('it has sequence identifier <seq_id>')
def when_sequence_id(seq_id, template_dict):
    template_dict['sequence_id'] = seq_id


@when('it has sequence number <seq_n>')
def when_sequence_number(seq_n, template_dict):
    template_dict['sequence_num'] = seq_n


@given('a test sequence')
def sequence(template_dict):
    ref_clock = LocalMachineClock()
    sequence = EBUTT3DocumentSequence('testSeq', ref_clock, 'en-GB')
    template_dict['sequence_id'] = 'testSeq'
    return sequence


@when('it has sequence number <doc1_seqnum>')
def when_doc1_has_seqnum(doc1_seqnum, template_dict):
    template_dict['sequence_num'] = doc1_seqnum


@when('doc1 is added to the sequence')
def when_doc1_added_to_sequence(sequence, template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    sequence.add_document(document)


@when('we create a new document')
def when_create_new_document(template_dict):
    template_dict['sequence_num'] = None


@when('it has sequence number <doc2_seqnum>')
def when_doc2_has_seqnum(doc2_seqnum, template_dict):
    template_dict['sequence_num'] = doc2_seqnum


@then('adding doc2 to the sequence results in an error')
def then_adding_doc2_error(sequence, template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    with pytest.raises(Exception):
        sequence.add_document(document)


@then('adding doc2 to the sequence does not raise any error')
def then_adding_doc2_success(sequence, template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    sequence.add_document(document)
