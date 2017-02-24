from ebu_tt_live.node.delay import RetimingDelayNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document
from mock import MagicMock
from pytest_bdd import scenarios, given, when, then
import pytest

scenarios('features/timing/retimingDelayNode.feature')


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


@given('it has span2 begin time <span2_begin>')
def given_span2_begin(span2_begin, template_dict):
    template_dict['span2_begin'] = span2_begin


@given('it has span2 end time <span2_end>')
def given_span2_end(span2_end, template_dict):
    template_dict['span2_end'] = span2_end


@given('it has <sequence_id_1>')
def given_original_sequence_id(template_dict, sequence_id_1):
    template_dict['sequence_identifier'] = sequence_id_1


@given('it has <authoring_delay>')
def given_authoring_delay(template_dict, authoring_delay):
    template_dict['authoring_delay'] = authoring_delay


@when('the retiming delay node delays it by <delay>')
def when_retiming_delay(delay, test_context, gen_document):

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    carriage = MagicMock(spec=IProducerCarriage)
    carriage.expects.return_value = EBUTT3Document

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


@then('the retiming delay node with <produced_sequence> will reject it')
def then_retiming_delay_node_rejects(gen_document, produced_sequence):
    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    carriage = MagicMock(spec=IProducerCarriage)
    carriage.expects.return_value = EBUTT3Document

    delay_float = 5.0

    delay_node = RetimingDelayNode(
        node_id='simple-delay-node',
        carriage_impl=carriage,
        reference_clock=reference_clock,
        fixed_delay=delay_float,
        document_sequence=produced_sequence,
    )
    with pytest.raises(Exception):
        delay_node.process_document(gen_document)


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


@then('the updated span computed begin time is <updated_span_begin>')
def then_updated_span_computed_begin_time(test_context, updated_span_begin):
    if updated_span_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[0].computed_begin_time == LimitedClockTimingType(updated_span_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[0].computed_begin_time is None


@then('the updated span computed end time is <updated_span_end>')
def then_updated_span_computed_end_time(test_context, updated_span_end):
    if updated_span_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[0].computed_end_time == LimitedClockTimingType(updated_span_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[0].computed_end_time is None


@then('the updated span2 computed begin time is <updated_span2_begin>')
def then_updated_span2_computed_begin_time(test_context, updated_span2_begin):
    if updated_span2_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[1].computed_begin_time == LimitedClockTimingType(updated_span2_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[1].computed_begin_time is None


@then('the updated span2 computed end time is <updated_span2_end>')
def then_updated_span2_computed_end_time(test_context, updated_span2_end):
    if updated_span2_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[1].computed_end_time == LimitedClockTimingType(updated_span2_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[1].computed_end_time is None


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
        assert test_context['doc'].binding.body.end == updated_body_end
    else:
        assert test_context['doc'].binding.body.end is None


@then('the updated div specified begin time is <updated_div_begin>')
def then_updated_div_specified_begin_time(test_context, updated_div_begin):
    if updated_div_begin != '':
        assert test_context['doc'].binding.body.div[0].begin == updated_div_begin
    else:
        assert test_context['doc'].binding.body.div[0].begin is None


@then('the updated div specified end time is <updated_div_end>')
def then_updated_div_specified_end_time(test_context, updated_div_end):
    if updated_div_end != '':
        assert test_context['doc'].binding.body.div[0].end == updated_div_end
    else:
        assert test_context['doc'].binding.body.div[0].end is None


@then('the updated p specified begin time is <updated_p_begin>')
def then_updated_p_specified_begin_time(test_context, updated_p_begin):
    if updated_p_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].begin == updated_p_begin
    else:
        assert test_context['doc'].binding.body.div[0].p[0].begin is None


@then('the updated p specified end time is <updated_p_end>')
def then_updated_p_specified_end_time(test_context, updated_p_end):
    if updated_p_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].end == updated_p_end
    else:
        assert test_context['doc'].binding.body.div[0].p[0].end is None


@then('the updated span specified begin time is <updated_span_begin>')
def then_updated_span_specified_begin_time(test_context, updated_span_begin):
    if updated_span_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[0].begin == updated_span_begin
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[0].begin is None


@then('the updated span specified end time is <updated_span_end>')
def then_updated_span_specified_end_time(test_context, updated_span_end):
    if updated_span_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[0].end == updated_span_end
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[0].end is None


@then('the updated span2 specified begin time is <updated_span2_begin>')
def then_updated_span2_specified_begin_time(test_context, updated_span2_begin):
    if updated_span2_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[1].begin == updated_span2_begin
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[1].begin is None


@then('the updated span2 specified end time is <updated_span2_end>')
def then_updated_span2_specified_end_time(test_context, updated_span2_end):
    if updated_span2_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[1].end == updated_span2_end
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[1].end is None


@then('the updated document has <sequence_id_2>')
def then_updated_seq_id(test_context, sequence_id_2):
    assert test_context['doc'].sequence_identifier == sequence_id_2


@then('the updated document has <authoring_delay>')
def then_updated_auth_delay(test_context, authoring_delay):
    if authoring_delay:
        assert test_context['doc'].binding.authoringDelay == authoring_delay
    else:
        assert test_context['doc'].binding.authoringDelay is None
