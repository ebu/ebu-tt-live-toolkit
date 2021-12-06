from ebu_tt_live.documents import EBUTT3Document, EBUTT3DocumentSequence
from pytest_bdd import given, when, then, scenarios, parsers
import pytest


scenarios('features/validation/sequence_identical_timing_model.feature')


# We cannot use a sequence fixture here like in other sequence tests because
# the sequence is created later from the first document and assigning a fixture
# after its creation function is not possible. So we store the documents in an
# array and create the sequence in the final thens
@given('a test sequence', target_fixture='doc_list')
def doc_list(template_dict):
    doc_list = []
    return doc_list


@when(parsers.parse('it has sequenceNumber {sequence_number}'))
def when_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number


@pytest.fixture
def time_base1():
    return None

@when(parsers.parse('it has timeBase {time_base1}'))
@when(parsers.parse('it has timeBase'))
def when_time_base1(time_base1, template_dict):
    template_dict['time_base'] = time_base1


@pytest.fixture
def clock_mode1():
    return None

@when(parsers.parse('it has clockMode {clock_mode1}'))
@when(parsers.parse('it has clockMode'))
def when_clock_mode1(clock_mode1, template_dict):
    template_dict['clock_mode'] = clock_mode1


@pytest.fixture
def frame_rate1():
    return None

@when(parsers.parse('it has frameRate {frame_rate1}'))
@when(parsers.parse('it has frameRate'))
def when_frame_rate1(frame_rate1, template_dict):
    template_dict['frame_rate'] = frame_rate1


@pytest.fixture
def frame_rate_multiplier1():
    return None

@when(parsers.parse('it has frameRateMultiplier {frame_rate_multiplier1}'))
@when(parsers.parse('it has frameRateMultiplier'))
def when_frame_rate_multiplier1(frame_rate_multiplier1, template_dict):
    template_dict['frame_rate_multiplier'] = frame_rate_multiplier1


@pytest.fixture
def drop_mode1():
    return None

@when(parsers.parse('it has dropMode {drop_mode1}'))
@when(parsers.parse('it has dropMode'))
def when_drop_mode1(drop_mode1, template_dict):
    template_dict['drop_mode'] = drop_mode1


@pytest.fixture
def marker_mode1():
    return None

@when(parsers.parse('it has markerMode {marker_mode1}'))
@when(parsers.parse('it has markerMode'))
def when_marker_mode1(marker_mode1, template_dict):
    template_dict['marker_mode'] = marker_mode1


@when('doc1 is added to the sequence')
def when_doc1_added_to_sequence(doc_list, template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    doc_list.append(document)


@when('we create a new document')
def when_create_new_document(template_dict):
    template_dict['sequence_num'] = None


@pytest.fixture
def time_base2():
    return None

@when(parsers.parse('it has timeBase2 {time_base2}'))
@when(parsers.parse('it has timeBase2'))
def when_time_base2(time_base2, template_dict):
    template_dict['time_base'] = time_base2


@pytest.fixture
def clock_mode2():
    return None

@when(parsers.parse('it has clockMode2 {clock_mode2}'))
@when(parsers.parse('it has clockMode2'))
def when_clock_mode2(clock_mode2, template_dict):
    template_dict['clock_mode'] = clock_mode2


@pytest.fixture
def frame_rate2():
    return None

@when(parsers.parse('it has frameRate2 {frame_rate2}'))
@when(parsers.parse('it has frameRate2'))
def when_frame_rate2(frame_rate2, template_dict):
    template_dict['frame_rate'] = frame_rate2


@pytest.fixture
def frame_rate_multiplier2():
    return None

@when(parsers.parse('it has frameRateMultiplier2 {frame_rate_multiplier2}'))
@when(parsers.parse('it has frameRateMultiplier2'))
def when_frame_rate_multiplier2(frame_rate_multiplier2, template_dict):
    template_dict['frame_rate_multiplier'] = frame_rate_multiplier2


@pytest.fixture
def drop_mode2():
    return None

@when(parsers.parse('it has dropMode2 {drop_mode2}'))
@when(parsers.parse('it has dropMode2'))
def when_drop_mode2(drop_mode2, template_dict):
    template_dict['drop_mode'] = drop_mode2


@pytest.fixture
def marker_mode2():
    return None

@when(parsers.parse('it has markerMode2 {marker_mode2}'))
@when(parsers.parse('it has markerMode2'))
def when_marker_mode2(marker_mode2, template_dict):
    template_dict['marker_mode'] = marker_mode2


@pytest.fixture
def doc2_seqnum():
    return None

@when(parsers.parse('it has sequenceNumber2 {doc2_seqnum}'))
@when(parsers.parse('it has sequenceNumber2'))
def when_doc2_has_seqnum(doc2_seqnum, template_dict):
    template_dict['sequence_num'] = doc2_seqnum


@then('adding doc2 to the sequence results in an error')
def then_adding_doc2_error(doc_list, template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    sequence = EBUTT3DocumentSequence.create_from_document(doc_list[0])
    with pytest.raises(Exception):
        sequence.add_document(document)


@then('adding doc2 to the sequence does not raise any error')
def then_adding_doc2_success(doc_list, template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    sequence = EBUTT3DocumentSequence.create_from_document(doc_list[0])
    sequence.add_document(document)
