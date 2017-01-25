from ebu_tt_live.node.delay import BufferDelayNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from ebu_tt_live.carriage.filesystem import FilesystemProducerImpl
from pytest_bdd import scenarios, given, when, then


scenarios('features/timing/bufferDelayNode.feature')


# functions for scenario: BufferDelayNode delays emission by no less than the delay period

@given('the buffer delay node delays it by <delay_offset>')
def given_buffer_delay(delay_offset, test_context, gen_document):

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    carriage = FilesystemProducerImpl('testing/tmp', reference_clock)

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

    # read the emission time from the manifest file stored in testing/tmp
    manifest_path = 'testing/tmp/manifest_delayTest.txt'
    emission_time = ''

    with open(manifest_path, 'r') as f:
        for last_line in f:
            emission_time, _ = last_line.split(',')

    test_context['doc'].emission = emission_time


@then('the delta between emission and availability time is greater or equal to <delay_offset>')
def then_delta_should_be_correct(delay_offset, test_context):

    delay_timedelta = LimitedClockTimingType(delay_offset).timedelta
    emission_timedelta = LimitedClockTimingType(test_context['doc'].emission).timedelta

    assert emission_timedelta - test_context['doc'].availability_time >= delay_timedelta
