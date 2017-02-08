from ebu_tt_live.node.delay import BufferDelayNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from ebu_tt_live.carriage.filesystem import FilesystemProducerImpl
from ebu_tt_live.adapters.node_carriage import ProducerNodeCarriageAdapter
from ebu_tt_live.adapters import document_data
from pytest_bdd import scenarios, given, when, then

scenarios('features/timing/bufferDelayNode.feature')

# functions for scenario: BufferDelayNode delays emission by no less than the delay period

@given('the buffer delay node delays it by <delay_offset>')
def given_buffer_delay(delay_offset, test_context, gen_document):

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'

    gen_document.availability_time = LimitedClockTimingType('00:00:00.0').timedelta

    # the first delay node applies no delay
    carriage_delay1 = FilesystemProducerImpl('testing/initial', reference_clock)
    delay_float1 = LimitedClockTimingType('00:00:00.0').timedelta.total_seconds()

    buffer_delay_node1 = BufferDelayNode(
        node_id='simple-delay-node',
        producer_carriage=None,
        reference_clock=reference_clock,
        fixed_delay=delay_float1
    )

    ProducerNodeCarriageAdapter(
        producer_node=buffer_delay_node1,
        producer_carriage=carriage_delay1
    )

    buffer_delay_node1.process_document(gen_document.get_xml())

    # the second delay node applies a delay of delay_offset
    carriage_delay2 = FilesystemProducerImpl('testing/buffer', reference_clock)
    delay_float2 = LimitedClockTimingType(delay_offset).timedelta.total_seconds()

    buffer_delay_node2 = BufferDelayNode(
        node_id='simple-delay-node',
        producer_carriage=None,
        reference_clock=reference_clock,
        fixed_delay=delay_float2
    )

    ProducerNodeCarriageAdapter(
        producer_node=buffer_delay_node2,
        producer_carriage=carriage_delay2
    )

    buffer_delay_node2.process_document(gen_document.get_xml())
    test_context['doc'] = gen_document


@given('the document is emitted')
def given_document_emitted(test_context):

    # read the availability time from the manifest file stored in initial/tmp
    manifest_path = 'testing/initial/manifest_delayTest.txt'
    avail_time = ''

    with open(manifest_path, 'r') as f:
        for last_line in f:
            avail_time, _ = last_line.split(',')

    test_context['doc'].avail_time = avail_time

    # read the emission time from the manifest file stored in buffer/tmp
    manifest_path = 'testing/buffer/manifest_delayTest.txt'
    emission_time = ''

    with open(manifest_path, 'r') as f:
        for last_line in f:
            emission_time, _ = last_line.split(',')

    test_context['doc'].emission = emission_time


@then('the delta between emission and availability time is greater or equal to <delay_offset>')
def then_delta_should_be_correct(delay_offset, test_context):

    delay_timedelta = LimitedClockTimingType(delay_offset).timedelta
    avail_timedelta = LimitedClockTimingType(test_context['doc'].avail_time).timedelta
    emission_timedelta = LimitedClockTimingType(test_context['doc'].emission).timedelta

    assert emission_timedelta - avail_timedelta >= delay_timedelta
