from ebu_tt_live.node.delay import BufferDelayNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from mock import MagicMock
from pytest_bdd import scenarios, given, when, then


scenarios('features/timing/bufferDelayNode.feature')


# functions for scenario: BufferDelayNode delays emission by no less than the delay period

@given('the buffer delay node delays it by <delay_offset>')
def given_buffer_delay(delay_offset, test_context, gen_document):

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    carriage = MagicMock()

    delay_float = LimitedClockTimingType(delay_offset).timedelta.total_seconds()

    buffer_delay_node = BufferDelayNode(
        node_id='simple-delay-node',
        carriage_impl=carriage,
        reference_clock=reference_clock,
        fixed_delay=delay_float,
        document_sequence='delayed_sequence',
    )

    buffer_delay_node.process_document(gen_document)
    test_context['doc'] = gen_document


@given('the document is emitted')
def given_document_emitted(test_context):
    test_context['doc'].emission = ''  # TODO: fill in this value


@then('the delta between emission and availability time is greater or equal to <delay_offset>')
def then_delta_should_be_correct(delay_offset, test_context):

    delay_timedelta = LimitedClockTimingType(delay_offset).timedelta

    assert test_context['doc'].emission - test_context['doc'].availability_time >= delay_timedelta
