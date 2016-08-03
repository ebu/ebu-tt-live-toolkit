from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType, LimitedClockTimingType
from pytest_bdd import scenarios, then, when, parsers

scenarios('features/timing/resolved_times.feature')


def timestr_to_timedelta(time_str, time_base):
    if time_base == 'clock':
        return LimitedClockTimingType(time_str).timedelta
    elif time_base == 'media':
        return FullClockTimingType(time_str).timedelta
    elif time_base == 'smpte':
        raise NotImplementedError('SMPTE needs implementation')


@when('we create a new document')
def when_new_doc(template_dict):
    template_dict = dict()


@when('it has timeBase <time_base>')
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when('it has sequenceIdentifier <sequence_identifier>')
def when_seq_id(sequence_identifier, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier


@when(parsers.parse('it has predefined sequenceNumber {sequence_number}'))
def when_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number


@when('it has doc1 body begin time <doc1_begin>')
def when_doc1_body_begin(doc1_begin, template_dict):
    template_dict['body_begin'] = doc1_begin


@when('it has doc1 body end time <doc1_end>')
def when_doc1_body_end(doc1_end, template_dict):
    template_dict['body_end'] = doc1_end


@when('it has doc1 body duration <doc1_dur>')
def when_doc1_body_dur(doc1_dur, template_dict):
    template_dict['body_dur'] = doc1_dur


@when('it has doc2 body begin time <doc2_begin>')
def when_doc2_body_begin(doc2_begin, template_dict):
    template_dict['body_begin'] = doc2_begin


@when('it has doc2 body end time <doc2_end>')
def when_doc2_body_end(doc2_end, template_dict):
    template_dict['body_end'] = doc2_end


@when('it has doc2 body duration <doc2_dur>')
def when_doc2_body_dur(doc2_dur, template_dict):
    template_dict['body_dur'] = doc2_dur


@when('it has doc3 body begin time <doc3_begin>')
def when_doc3_body_begin(doc3_begin, template_dict):
    template_dict['body_begin'] = doc3_begin


@when('it has doc3 body end time <doc3_end>')
def when_doc3_body_end(doc3_end, template_dict):
    template_dict['body_end'] = doc3_end


@when('it has doc3 body duration <doc3_dur>')
def when_doc3_body_dur(doc3_dur, template_dict):
    template_dict['body_dur'] = doc3_dur


@when('doc1 is added to the sequence with availability time <doc1_avail_time>')
def when_doc1_added_to_seq(doc1_avail_time, template_file, template_dict, sequence):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.availability_time = timestr_to_timedelta(doc1_avail_time, sequence.reference_clock.time_base)
    sequence.add_document(document)


@when('doc2 is added to the sequence with availability time <doc2_avail_time>')
def when_doc2_added_to_seq(doc2_avail_time, template_file, template_dict, sequence):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.availability_time = timestr_to_timedelta(doc2_avail_time, sequence.reference_clock.time_base)
    sequence.add_document(document)


@when('doc3 is added to the sequence with availability time <doc3_avail_time>')
def when_doc3_added_to_seq(doc3_avail_time, template_file, template_dict, sequence):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.availability_time = timestr_to_timedelta(doc3_avail_time, sequence.reference_clock.time_base)
    sequence.add_document(document)


@then('doc1 has resolved begin time <r_begin_doc1>')
def valid_resolved_begin_time_doc1(r_begin_doc1, sequence):
    resolved_begin_timedelta = timestr_to_timedelta(r_begin_doc1, sequence.reference_clock.time_base)
    assert sequence.docs[0].resolved_begin_time == resolved_begin_timedelta


@then('doc1 has resolved end time <r_end_doc1>')
def valid_resolved_end_time_doc1(r_end_doc1, sequence):
    if r_end_doc1:
        resolved_end_timedelta = timestr_to_timedelta(r_end_doc1, sequence.reference_clock.time_base)
    else:
        resolved_end_timedelta = None
    assert sequence.docs[0].resolved_end_time == resolved_end_timedelta


@then('doc2 has resolved begin time <r_begin_doc2>')
def valid_resolved_begin_time_doc2(r_begin_doc2, sequence):
    resolved_begin_timedelta = timestr_to_timedelta(r_begin_doc2, sequence.reference_clock.time_base)
    assert sequence.docs[1].resolved_begin_time == resolved_begin_timedelta


@then('doc2 has resolved end time <r_end_doc2>')
def valid_resolved_end_time_doc2(r_end_doc2, sequence):
    if r_end_doc2:
        resolved_end_timedelta = timestr_to_timedelta(r_end_doc2, sequence.reference_clock.time_base)
    else:
        resolved_end_timedelta = None
    assert sequence.docs[1].resolved_end_time == resolved_end_timedelta


@then('doc3 has resolved begin time <r_begin_doc3>')
def valid_resolved_begin_time_doc3(r_begin_doc3, sequence):
    resolved_begin_timedelta = timestr_to_timedelta(r_begin_doc3, sequence.reference_clock.time_base)
    assert sequence.docs[2].resolved_begin_time == resolved_begin_timedelta


@then('doc3 has resolved end time <r_end_doc3>')
def valid_resolved_end_time_doc3(r_end_doc3, sequence):
    if r_end_doc3:
        resolved_end_timedelta = timestr_to_timedelta(r_end_doc3, sequence.reference_clock.time_base)
    else:
        resolved_end_timedelta = None
    assert sequence.docs[2].resolved_end_time == resolved_end_timedelta
