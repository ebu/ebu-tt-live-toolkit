from ebu_tt_live.node.delay import FixedDelayNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from mock import MagicMock
from pytest_bdd import scenarios, given, when, then

scenarios('features/timing/delay.feature')


@given('it has body begin time <body_begin>')
def given_body_begin(body_begin, test_context, gen_document):
    gen_document.binding.body.begin = body_begin
    test_context['doc'] = gen_document


@when('the delay node delays it by <delay>')
def when_delay(delay, test_context, gen_document):

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    carriage = MagicMock()

    delay_float = LimitedClockTimingType(delay).timedelta.total_seconds()

    delay_node = FixedDelayNode(
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
    # test_context['doc'] = gen_document


@then('the delay node outputs the document at <delayed_avail_time>')
def then_availability_time(delayed_avail_time, test_context):
    delayed_avail_time_float = LimitedClockTimingType(delayed_avail_time).timedelta
    assert test_context['doc'].availability_time == delayed_avail_time_float


@then('the updated body begin time is <updated_body_begin>')
def then_updated_body_begin_time(test_context, updated_body_begin):
    assert test_context['doc'].binding.body.begin == updated_body_begin
