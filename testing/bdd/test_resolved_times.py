from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType, LimitedClockTimingType
from pytest_bdd import scenarios, then, when, parsers
from pytest import fixture


scenarios('features/timing/resolved_times.feature')
scenarios('features/timing/resolved_times_no_body.feature')

#NOTE: contains SMPTE time base. SMPTE was removed from the specification in version 1.0.

def timestr_to_timedelta(time_str, time_base):
    if time_base == 'clock':
        return LimitedClockTimingType(time_str).timedelta
    elif time_base == 'media':
        return FullClockTimingType(time_str).timedelta
    elif time_base == 'smpte':
        raise NotImplementedError('SMPTE needs implementation')

@when('we create a new document')
def when_new_doc(template_dict):
    template_dict.clear()


@when(parsers.parse('it has timeBase {time_base}'))
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when(parsers.parse('it has sequenceIdentifier {sequence_identifier}'))
def when_seq_id(sequence_identifier, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier


@when(parsers.parse('it has predefined sequenceNumber {sequence_number}'))
def when_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number


@fixture
def doc1_no_body():
    return None

@when(parsers.parse('it has doc1 body {doc1_no_body}'))
@when(parsers.parse('it has doc1 body'))
def when_doc1_body(doc1_no_body, template_dict):
    template_dict['body'] = doc1_no_body


@fixture
def doc1_begin():
    return None

@when(parsers.parse('it has doc1 body begin time {doc1_begin}'))
@when(parsers.parse('it has doc1 body begin time'))
def when_doc1_body_begin(doc1_begin, template_dict):
    template_dict['body_begin'] = doc1_begin


@fixture
def doc1_end():
    return None

@when(parsers.parse('it has doc1 body end time {doc1_end}'))
@when(parsers.parse('it has doc1 body end time'))
def when_doc1_body_end(doc1_end, template_dict):
    template_dict['body_end'] = doc1_end


@fixture
def doc1_dur():
    return None

@when(parsers.parse('it has doc1 body duration {doc1_dur}'))
@when(parsers.parse('it has doc1 body duration'))
def when_doc1_body_dur(doc1_dur, template_dict):
    template_dict['body_dur'] = doc1_dur


@fixture
def doc2_no_body():
    return None

@when(parsers.parse('it has doc2 body {doc2_no_body}'))
@when(parsers.parse('it has doc2 body'))
def when_doc2_body(doc2_no_body, template_dict):
    template_dict['body'] = doc2_no_body


@fixture
def doc2_begin():
    return None

@when(parsers.parse('it has doc2 body begin time {doc2_begin}'))
@when(parsers.parse('it has doc2 body begin time'))
def when_doc2_body_begin(doc2_begin, template_dict):
    template_dict['body_begin'] = doc2_begin


@fixture
def doc2_end():
    return None

@when(parsers.parse('it has doc2 body end time {doc2_end}'))
@when(parsers.parse('it has doc2 body end time'))
def when_doc2_body_end(doc2_end, template_dict):
    template_dict['body_end'] = doc2_end


@fixture
def doc2_dur():
    return None

@when(parsers.parse('it has doc2 body duration {doc2_dur}'))
@when(parsers.parse('it has doc2 body duration'))
def when_doc2_body_dur(doc2_dur, template_dict):
    template_dict['body_dur'] = doc2_dur


@fixture
def doc3_no_body():
    return None

@when(parsers.parse('it has doc3 body {doc3_no_body}'))
@when(parsers.parse('it has doc3 body'))
def when_doc3_body(doc3_no_body, template_dict):
    template_dict['body'] = doc3_no_body


@fixture
def doc3_begin():
    return None

@when(parsers.parse('it has doc3 body begin time {doc3_begin}'))
@when(parsers.parse('it has doc3 body begin time'))
def when_doc3_body_begin(doc3_begin, template_dict):
    template_dict['body_begin'] = doc3_begin


@fixture
def doc3_end():
    return None

@when(parsers.parse('it has doc3 body end time {doc3_end}'))
@when(parsers.parse('it has doc3 body end time'))
def when_doc3_body_end(doc3_end, template_dict):
    template_dict['body_end'] = doc3_end


@fixture
def doc3_dur():
    return None

@when(parsers.parse('it has doc3 body duration {doc3_dur}'))
@when(parsers.parse('it has doc3 body duration'))
def when_doc3_body_dur(doc3_dur, template_dict):
    template_dict['body_dur'] = doc3_dur


@when(parsers.parse('doc1 is added to the sequence with availability time {doc1_avail_time}'))
def when_doc1_added_to_seq(doc1_avail_time, template_file, template_dict, sequence, test_context):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.availability_time = timestr_to_timedelta(doc1_avail_time, sequence.reference_clock.time_base)
    sequence.add_document(document)
    test_context['doc1'] = document


@when(parsers.parse('doc2 is added to the sequence with availability time {doc2_avail_time}'))
def when_doc2_added_to_seq(doc2_avail_time, template_file, template_dict, sequence, test_context):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.availability_time = timestr_to_timedelta(doc2_avail_time, sequence.reference_clock.time_base)
    sequence.add_document(document)
    test_context['doc2'] = document


@when(parsers.parse('doc3 is added to the sequence with availability time {doc3_avail_time}'))
def when_doc3_added_to_seq(doc3_avail_time, template_file, template_dict, sequence, test_context):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.availability_time = timestr_to_timedelta(doc3_avail_time, sequence.reference_clock.time_base)
    sequence.add_document(document)
    test_context['doc3'] = document


@then(parsers.parse('doc1 has resolved begin time {r_begin_doc1}'))
def valid_resolved_begin_time_doc1(r_begin_doc1, sequence, test_context):
    resolved_begin_timedelta = timestr_to_timedelta(r_begin_doc1, sequence.reference_clock.time_base)
    assert test_context['doc1'].resolved_begin_time == resolved_begin_timedelta


@fixture
def r_end_doc1():
    return None

@then(parsers.parse('doc1 has resolved end time {r_end_doc1}'))
@then(parsers.parse('doc1 has resolved end time'))
def valid_resolved_end_time_doc1(r_end_doc1, sequence, test_context):
    if r_end_doc1:
        resolved_end_timedelta = timestr_to_timedelta(r_end_doc1, sequence.reference_clock.time_base)
    else:
        resolved_end_timedelta = None
    assert test_context['doc1'].resolved_end_time == resolved_end_timedelta


@then(parsers.parse('doc2 has resolved begin time {r_begin_doc2}'))
def valid_resolved_begin_time_doc2(r_begin_doc2, sequence, test_context):
    resolved_begin_timedelta = timestr_to_timedelta(r_begin_doc2, sequence.reference_clock.time_base)
    assert test_context['doc2'].resolved_begin_time == resolved_begin_timedelta


@then(parsers.parse('doc2 has resolved end time {r_end_doc2}'))
def valid_resolved_end_time_doc2(r_end_doc2, sequence, test_context):
    if r_end_doc2:
        resolved_end_timedelta = timestr_to_timedelta(r_end_doc2, sequence.reference_clock.time_base)
    else:
        resolved_end_timedelta = None
    assert test_context['doc2'].resolved_end_time == resolved_end_timedelta


@then(parsers.parse('doc3 has resolved begin time {r_begin_doc3}'))
def valid_resolved_begin_time_doc3(r_begin_doc3, sequence, test_context):
    resolved_begin_timedelta = timestr_to_timedelta(r_begin_doc3, sequence.reference_clock.time_base)
    assert test_context['doc3'].resolved_begin_time == resolved_begin_timedelta


@fixture
def r_end_doc3():
    return None

@then(parsers.parse('doc3 has resolved end time {r_end_doc3}'))
@then(parsers.parse('doc3 has resolved end time'))
def valid_resolved_end_time_doc3(r_end_doc3, sequence, test_context):
    if r_end_doc3:
        resolved_end_timedelta = timestr_to_timedelta(r_end_doc3, sequence.reference_clock.time_base)
    else:
        resolved_end_timedelta = None
    assert test_context['doc3'].resolved_end_time == resolved_end_timedelta


@then('doc2 has resolved_end < resolved_begin and is skipped')
def then_doc2_skipped(test_context):
    document = test_context['doc2']
    assert document.resolved_end_time < document.resolved_begin_time
    assert document.discarded


@then('doc1 and doc2 have resolved_end < resolved_begin and are skipped')
def then_doc1_doc2_skipped(sequence, test_context):
    document1 = test_context['doc1']
    document2 = test_context['doc2']
    assert document1.resolved_end_time < document1.resolved_begin_time
    assert document1.discarded
    assert document2.resolved_end_time < document2.resolved_begin_time
    assert document2.discarded
