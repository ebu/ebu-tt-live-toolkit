from ebu_tt_live.node.delay import RetimingDelayNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from mock import MagicMock
from pytest_bdd import scenarios, given, when, then

scenarios('features/timing/delay.feature')


@given('it has body begin time <body_begin>')
def given_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@given('it has body end time <body_end>')
def given_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@given('it has body duration <body_dur>')
def given_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur


@given('it has div begin time <div_begin>')
def given_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin


@given('it has div end time <div_end>')
def given_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end


@given('it has p begin time <p_begin>')
def given_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin


@given('it has p end time <p_end>')
def given_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end


@given('it has span begin time <span_begin>')
def given_span_begin(span_begin, template_dict):
    template_dict['span_begin'] = span_begin


@given('it has span end time <span_end>')
def given_span_end(span_end, template_dict):
    template_dict['span_end'] = span_end


@when('the delay node delays it by <delay>')
def when_delay(delay, test_context, gen_document):

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    carriage = MagicMock()

    delay_float = LimitedClockTimingType(delay).timedelta.total_seconds()

    delay_node = RetimingDelayNode(
        node_id='simple-delay-node',
        carriage_impl=carriage,
        reference_clock=reference_clock,
        fixed_delay=delay_float,
        document_sequence='delayed_sequence',
    )
    delay_node.process_document(gen_document)
    # As long as you operate on a document produced by the given statement you do not have to do this step unless
    # you wanted to be compatible with some pre-existing implemented when statements expecting the
    # document in the test_context fixture.
    test_context['doc'] = gen_document


@then('the delay node outputs the document at <delayed_avail_time>')
def then_availability_time(delayed_avail_time, test_context):
    delayed_avail_time_float = LimitedClockTimingType(delayed_avail_time).timedelta
    assert test_context['doc'].availability_time == delayed_avail_time_float

# functions for computed times


@then('the updated body computed begin time is <updated_body_begin>')
def then_updated_body_computed_begin_time(test_context, updated_body_begin):
    if updated_body_begin != '':
        assert test_context['doc'].binding.body.computed_begin_time == LimitedClockTimingType(updated_body_begin).timedelta
    else:
        assert test_context['doc'].binding.body.computed_begin_time is None


@then('the updated body computed end time is <updated_body_end>')
def then_updated_body_computed_end_time(test_context, updated_body_end):
    if updated_body_end != '':
        assert test_context['doc'].binding.body.computed_end_time == LimitedClockTimingType(updated_body_end).timedelta
    else:
        assert test_context['doc'].binding.body.computed_end_time is None


@then('the updated div computed begin time is <updated_div_begin>')
def then_updated_div_computed_begin_time(test_context, updated_div_begin):
    if updated_div_begin != '':
        assert test_context['doc'].binding.body.div[0].computed_begin_time == LimitedClockTimingType(updated_div_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].computed_begin_time is None


@then('the updated div computed end time is <updated_div_end>')
def then_updated_div_computed_end_time(test_context, updated_div_end):
    if updated_div_end != '':
        assert test_context['doc'].binding.body.div[0].computed_end_time == LimitedClockTimingType(updated_div_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].computed_end_time is None


@then('the updated p computed begin time is <updated_p_begin>')
def then_updated_p_computed_begin_time(test_context, updated_p_begin):
    if updated_p_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].computed_begin_time == LimitedClockTimingType(updated_p_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].computed_begin_time is None


@then('the updated p computed end time is <updated_p_end>')
def then_updated_p_computed_end_time(test_context, updated_p_end):
    if updated_p_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].computed_end_time == LimitedClockTimingType(updated_p_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].computed_end_time is None

# functions for specified times


@then('the updated body specified begin time is <updated_body_begin>')
def then_updated_body_specified_begin_time(test_context, updated_body_begin):
    if updated_body_begin != '':
        assert test_context['doc'].binding.body.begin == updated_body_begin
    else:
        assert test_context['doc'].binding.body.begin is None


@then('the updated body specified end time is <updated_body_end>')
def then_updated_body_specified_end_time(test_context, updated_body_end):
    if updated_body_end != '':
        assert test_context['doc'].binding.body.computed_end_time == LimitedClockTimingType(updated_body_end).timedelta
    else:
        assert test_context['doc'].binding.body.computed_end_time is None


@then('the updated div specified begin time is <updated_div_begin>')
def then_updated_div_specified_begin_time(test_context, updated_div_begin):
    if updated_div_begin != '':
        assert test_context['doc'].binding.body.div[0].computed_begin_time == LimitedClockTimingType(updated_div_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].computed_begin_time is None


@then('the updated div specified end time is <updated_div_end>')
def then_updated_div_specified_end_time(test_context, updated_div_end):
    if updated_div_end != '':
        assert test_context['doc'].binding.body.div[0].computed_end_time == LimitedClockTimingType(updated_div_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].computed_end_time is None


@then('the updated p specified begin time is <updated_p_begin>')
def then_updated_p_specified_begin_time(test_context, updated_p_begin):
    if updated_p_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].computed_begin_time == LimitedClockTimingType(updated_p_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].computed_begin_time is None


@then('the updated p specified end time is <updated_p_end>')
def then_updated_p_specified_end_time(test_context, updated_p_end):
    if updated_p_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].computed_end_time == LimitedClockTimingType(updated_p_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].computed_end_time is None