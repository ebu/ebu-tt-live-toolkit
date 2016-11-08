from ebu_tt_live.node.delay import FixedDelayNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.carriage.twisted import TwistedConsumerImpl
from pytest_bdd import scenarios, when, then

scenarios('features/timing/delay.feature')


@when('the delay node delays it by <delay>')
def when_delay(delay, test_context, document):

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    consumer_impl = TwistedConsumerImpl()

    delay_node = FixedDelayNode(
        node_id='simple-delay-node',
        carriage_impl=consumer_impl,
        reference_clock=reference_clock,
        fixed_delay=delay,
        document_sequence='delayed_sequence',
    )
    delay_node.process_document(document)
    test_context['doc'] = document


@then('the delay node outputs the document at <delayed_avail_time>')
def then_availability_time(delayed_avail_time, test_context):
    assert test_context['doc'].availability_time == delayed_avail_time

