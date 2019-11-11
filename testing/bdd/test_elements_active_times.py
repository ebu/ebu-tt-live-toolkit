from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType
from pytest_bdd import scenarios, when, then

scenarios('features/timing/elements_active_times.feature')
scenarios('features/timing/elements_active_times_empty_body.feature')

@when('it has timeBase <time_base>')
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when('it has sequenceIdentifier <sequence_identifier>')
def when_seq_id(sequence_identifier, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier


@when('it has sequenceNumber <sequence_number>')
def when_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number

@when('it is available at <availability_time>')
def when_doc_available(test_context, availability_time, template_dict):
    if availability_time:
        template_dict['availability_time'] = FullClockTimingType(availability_time).timedelta


@then('body active begin time is <body_active_begin>')
def then_body_active_begin(test_context, body_active_begin):
    computed_begin = test_context['document'].binding.body.computed_begin_time
    if body_active_begin == "undefined":
        assert computed_begin is None
    else:
        body_active_begin_timedelta = FullClockTimingType(body_active_begin).timedelta
        assert body_active_begin_timedelta == computed_begin


@then('body active end time is <body_active_end>')
def then_body_active_end(test_context, body_active_end):
    computed_end = test_context['document'].binding.body.computed_end_time
    if body_active_end == "undefined":
        assert computed_end is None
    else:
        body_active_end_timedelta = FullClockTimingType(body_active_end).timedelta
        assert body_active_end_timedelta == computed_end


@then('div active begin time is <div_active_begin>')
def then_div_active_begin(test_context, div_active_begin):
    computed_begin = test_context['document'].binding.body.orderedContent()[0].value.computed_begin_time

    if div_active_begin == "undefined":
        assert computed_begin is None
    else:
        div_active_begin_timedelta = FullClockTimingType(div_active_begin).timedelta
        assert div_active_begin_timedelta == computed_begin


@then('div active end time is <div_active_end>')
def then_div_active_end(test_context, div_active_end):
    computed_end = test_context['document'].binding.body.orderedContent()[0].value.computed_end_time
    if div_active_end == "undefined":
        assert computed_end is None
    else:
        div_active_end_timedelta = FullClockTimingType(div_active_end).timedelta
        assert div_active_end_timedelta == computed_end


@then('p active begin time is <p_active_begin>')
def then_p_active_begin(test_context, p_active_begin):
    computed_begin = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.computed_begin_time
    if p_active_begin == "undefined":
        assert computed_begin is None
    else:
        p_active_begin_timedelta = FullClockTimingType(p_active_begin).timedelta
        assert p_active_begin_timedelta == computed_begin


@then('p active end time is <p_active_end>')
def then_p_active_end(test_context, p_active_end):
    computed_end = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.computed_end_time
    if p_active_end == "undefined":
        assert computed_end is None
    else:
        p_active_end_timedelta = FullClockTimingType(p_active_end).timedelta
        assert p_active_end_timedelta == computed_end


@then('span1 active begin time is <span1_active_begin>')
def then_span1_active_begin(test_context, span1_active_begin):
    computed_begin = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.orderedContent()[1].value.computed_begin_time
    if span1_active_begin == "undefined":
        assert computed_begin is None
    else:
        span1_active_begin_timedelta = FullClockTimingType(span1_active_begin).timedelta
        assert span1_active_begin_timedelta == computed_begin


@then('span1 active end time is <span1_active_end>')
def then_span1_active_end(test_context, span1_active_end):
    computed_end = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.orderedContent()[1].value.computed_end_time
    if span1_active_end == "undefined":
        assert computed_end is None
    else:
        span1_active_end_timedelta = FullClockTimingType(span1_active_end).timedelta
        assert span1_active_end_timedelta == computed_end


@then('span2 active begin time is <span2_active_begin>')
def then_span2_active_begin(test_context, span2_active_begin):
    computed_begin = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.orderedContent()[3].value.computed_begin_time
    if span2_active_begin == "undefined":
        assert computed_begin is None
    else:
        span2_active_begin_timedelta = FullClockTimingType(span2_active_begin).timedelta
        assert span2_active_begin_timedelta == computed_begin


@then('span2 active end time is <span2_active_end>')
def then_span2_active_end(test_context, span2_active_end):
    computed_end = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.orderedContent()[3].value.computed_end_time
    if span2_active_end == "undefined":
        assert computed_end is None
    else:
        span2_active_end_timedelta = FullClockTimingType(span2_active_end).timedelta
        assert span2_active_end_timedelta == computed_end
