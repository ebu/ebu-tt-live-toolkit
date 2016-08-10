from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType
from pytest_bdd import scenarios, when, then

scenarios('features/timing/elements_active_times.feature')


@when('it has timeBase <time_base>')
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when('it has sequenceIdentifier <sequence_identifier>')
def when_seq_id(sequence_identifier, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier


@when('it has sequenceNumber <sequence_number>')
def when_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number


@when('it has body begin time <body_begin>')
def when_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@when('it has body end time <body_end>')
def when_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@when('it has div begin time <div_begin>')
def when_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin


@when('it has div end time <div_end>')
def when_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end


@when('it has p begin time <p_begin>')
def when_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin


@when('it has p end time <p_end>')
def when_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end


@when('it has span1 begin time <span1_begin>')
def when_span1_begin(span1_begin, template_dict):
    template_dict['span1_begin'] = span1_begin


@when('it has span1 end time <span1_end>')
def when_span1_end(span1_end, template_dict):
    template_dict['span1_end'] = span1_end


@when('it has span2 begin time <span2_begin>')
def when_span2_begin(span2_begin, template_dict):
    template_dict['span2_begin'] = span2_begin


@when('it has span2 end time <span2_end>')
def when_span2_end(span2_end, template_dict):
    template_dict['span2_end'] = span2_end


@when('the document is generated')
def when_doc_generated(test_context, template_dict, template_file):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    test_context['document'] = document


# I don't know through which interface I will get the active times yet so it is
# then functions are not complete.
@then('body active begin time is <body_active_begin>')
def then_body_active_begin(test_context, body_active_begin):
    if body_active_begin == "undefined":
        pass
    else:
        body_active_begin_timedelta = FullClockTimingType(body_active_begin).timedelta
        pass


@then('body active end time is <body_active_end>')
def then_body_active_end(test_context, body_active_end):
    if body_active_end == "undefined":
        pass
    else:
        body_active_end_timedelta = FullClockTimingType(body_active_end).timedelta
        pass


@then('div active begin time is <div_active_begin>')
def then_div_active_begin(test_context, div_active_begin):
    if div_active_begin == "undefined":
        pass
    else:
        div_active_begin_timedelta = FullClockTimingType(div_active_begin).timedelta
        pass


@then('div active end time is <div_active_end>')
def then_div_active_end(test_context, div_active_end):
    if div_active_end == "undefined":
        pass
    else:
        div_active_end_timedelta = FullClockTimingType(div_active_end).timedelta
        pass


@then('p active begin time is <p_active_begin>')
def then_p_active_begin(test_context, p_active_begin):
    if p_active_begin == "undefined":
        pass
    else:
        p_active_begin_timedelta = FullClockTimingType(p_active_begin).timedelta
        pass


@then('p active end time is <p_active_end>')
def then_p_active_end(test_context, p_active_end):
    if p_active_end == "undefined":
        pass
    else:
        p_active_end_timedelta = FullClockTimingType(p_active_end).timedelta
        pass


@then('span1 active begin time is <span1_active_begin>')
def then_span1_active_begin(test_context, span1_active_begin):
    if span1_active_begin == "undefined":
        pass
    else:
        span1_active_begin_timedelta = FullClockTimingType(span1_active_begin).timedelta
        pass


@then('span1 active end time is <span1_active_end>')
def then_span1_active_end(test_context, span1_active_end):
    if span1_active_end == "undefined":
        pass
    else:
        span1_active_end_timedelta = FullClockTimingType(span1_active_end).timedelta
        pass


@then('span2 active begin time is <span2_active_begin>')
def then_span2_active_begin(test_context, span2_active_begin):
    if span2_active_begin == "undefined":
        pass
    else:
        span2_active_begin_timedelta = FullClockTimingType(span2_active_begin).timedelta
        pass


@then('span2 active end time is <span2_active_end>')
def then_span2_active_end(test_context, span2_active_end):
    if span2_active_end == "undefined":
        pass
    else:
        span2_active_end_timedelta = FullClockTimingType(span2_active_end).timedelta
        pass
