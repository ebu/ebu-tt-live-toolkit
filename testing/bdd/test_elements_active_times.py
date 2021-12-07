from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType
from pytest_bdd import scenarios, when, then, parsers
from pytest import fixture

scenarios('features/timing/elements_active_times.feature')
scenarios('features/timing/elements_active_times_empty_body.feature')


@when(parsers.parse('it has timeBase {time_base}'))
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when(parsers.parse('it has sequenceIdentifier {sequence_identifier}'))
def when_seq_id(sequence_identifier, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier


@when(parsers.parse('it has sequenceNumber {sequence_number}'))
def when_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number


@fixture
def body_begin():
    return None

@when(parsers.parse('it has body begin time {body_begin}'))
@when(parsers.parse('it has body begin time'))
def when_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@fixture
def body_dur():
    return None

@when(parsers.parse('it has body duration {body_dur}'))
@when(parsers.parse('it has body duration'))
def when_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur


@fixture
def body_end():
    return None

@when(parsers.parse('it has body end time {body_end}'))
@when(parsers.parse('it has body end time'))
def when_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@fixture
def div_begin():
    return None

@when(parsers.parse('it has div begin time {div_begin}'))
@when(parsers.parse('it has div begin time'))
def when_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin


@fixture
def div_end():
    return None

@when(parsers.parse('it has div end time {div_end}'))
@when(parsers.parse('it has div end time'))
def when_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end


@fixture
def p_begin():
    return None

@when(parsers.parse('it has p begin time {p_begin}'))
@when(parsers.parse('it has p begin time'))
def when_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin


@fixture
def p_end():
    return None

@when(parsers.parse('it has p end time {p_end}'))
@when(parsers.parse('it has p end time'))
def when_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end


@fixture
def span1_begin():
    return None

@when(parsers.parse('it has span1 begin time {span1_begin}'))
@when(parsers.parse('it has span1 begin time'))
def when_span1_begin(span1_begin, template_dict):
    template_dict['span1_begin'] = span1_begin


@fixture
def span1_end():
    return None

@when(parsers.parse('it has span1 end time {span1_end}'))
@when(parsers.parse('it has span1 end time'))
def when_span1_end(span1_end, template_dict):
    template_dict['span1_end'] = span1_end


@fixture
def span2_begin():
    return None

@when(parsers.parse('it has span2 begin time {span2_begin}'))
@when(parsers.parse('it has span2 begin time'))
def when_span2_begin(span2_begin, template_dict):
    template_dict['span2_begin'] = span2_begin


@fixture
def span2_end():
    return None

@when(parsers.parse('it has span2 end time {span2_end}'))
@when(parsers.parse('it has span2 end time'))
def when_span2_end(span2_end, template_dict):
    template_dict['span2_end'] = span2_end


@fixture
def availability_time():
    return None

@when(parsers.parse('it is available at {availability_time}'))
@when(parsers.parse('it is available at'))
def when_doc_available(test_context, availability_time):
    if availability_time:
        test_context['document'].availability_time = FullClockTimingType(availability_time).timedelta


@then(parsers.parse('body active begin time is {body_active_begin}'))
def then_body_active_begin(test_context, body_active_begin):
    computed_begin = test_context['document'].binding.body.computed_begin_time
    if body_active_begin == "undefined":
        assert computed_begin is None
    else:
        body_active_begin_timedelta = FullClockTimingType(body_active_begin).timedelta
        assert body_active_begin_timedelta == computed_begin


@then(parsers.parse('body active end time is {body_active_end}'))
def then_body_active_end(test_context, body_active_end):
    computed_end = test_context['document'].binding.body.computed_end_time
    if body_active_end == "undefined":
        assert computed_end is None
    else:
        body_active_end_timedelta = FullClockTimingType(body_active_end).timedelta
        assert body_active_end_timedelta == computed_end


@then(parsers.parse('div active begin time is {div_active_begin}'))
def then_div_active_begin(test_context, div_active_begin):
    computed_begin = test_context['document'].binding.body.orderedContent()[0].value.computed_begin_time

    if div_active_begin == "undefined":
        assert computed_begin is None
    else:
        div_active_begin_timedelta = FullClockTimingType(div_active_begin).timedelta
        assert div_active_begin_timedelta == computed_begin


@then(parsers.parse('div active end time is {div_active_end}'))
def then_div_active_end(test_context, div_active_end):
    computed_end = test_context['document'].binding.body.orderedContent()[0].value.computed_end_time
    if div_active_end == "undefined":
        assert computed_end is None
    else:
        div_active_end_timedelta = FullClockTimingType(div_active_end).timedelta
        assert div_active_end_timedelta == computed_end


@then(parsers.parse('p active begin time is {p_active_begin}'))
def then_p_active_begin(test_context, p_active_begin):
    computed_begin = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.computed_begin_time
    if p_active_begin == "undefined":
        assert computed_begin is None
    else:
        p_active_begin_timedelta = FullClockTimingType(p_active_begin).timedelta
        assert p_active_begin_timedelta == computed_begin


@then(parsers.parse('p active end time is {p_active_end}'))
def then_p_active_end(test_context, p_active_end):
    computed_end = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.computed_end_time
    if p_active_end == "undefined":
        assert computed_end is None
    else:
        p_active_end_timedelta = FullClockTimingType(p_active_end).timedelta
        assert p_active_end_timedelta == computed_end


@then(parsers.parse('span1 active begin time is {span1_active_begin}'))
def then_span1_active_begin(test_context, span1_active_begin):
    computed_begin = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.orderedContent()[1].value.computed_begin_time
    if span1_active_begin == "undefined":
        assert computed_begin is None
    else:
        span1_active_begin_timedelta = FullClockTimingType(span1_active_begin).timedelta
        assert span1_active_begin_timedelta == computed_begin


@then(parsers.parse('span1 active end time is {span1_active_end}'))
def then_span1_active_end(test_context, span1_active_end):
    computed_end = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.orderedContent()[1].value.computed_end_time
    if span1_active_end == "undefined":
        assert computed_end is None
    else:
        span1_active_end_timedelta = FullClockTimingType(span1_active_end).timedelta
        assert span1_active_end_timedelta == computed_end


@then(parsers.parse('span2 active begin time is {span2_active_begin}'))
def then_span2_active_begin(test_context, span2_active_begin):
    computed_begin = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.orderedContent()[3].value.computed_begin_time
    if span2_active_begin == "undefined":
        assert computed_begin is None
    else:
        span2_active_begin_timedelta = FullClockTimingType(span2_active_begin).timedelta
        assert span2_active_begin_timedelta == computed_begin


@then(parsers.parse('span2 active end time is {span2_active_end}'))
def then_span2_active_end(test_context, span2_active_end):
    computed_end = test_context['document'].binding.body.orderedContent()[0].value.orderedContent()[0].value.orderedContent()[3].value.computed_end_time
    if span2_active_end == "undefined":
        assert computed_end is None
    else:
        span2_active_end_timedelta = FullClockTimingType(span2_active_end).timedelta
        assert span2_active_end_timedelta == computed_end
