from ebu_tt_live.node.delay import RetimingDelayNode
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.bindings._ebuttdt import LimitedClockTimingType
from ebu_tt_live.carriage.interface import IProducerCarriage
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from mock import MagicMock
from pytest_bdd import scenarios, given, when, then, parsers
import pytest

scenarios('features/timing/retimingDelayNode.feature')

@pytest.fixture
def body_begin():
    return None

@given(parsers.parse('it has body begin time {body_begin}'), target_fixture='given_body_begin')
@given(parsers.parse('it has body begin time'), target_fixture='given_body_begin')
def given_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@pytest.fixture
def body_end():
    return None

@given(parsers.parse('it has body end time {body_end}'), target_fixture='given_body_end')
@given(parsers.parse('it has body end time'), target_fixture='given_body_end')
def given_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@pytest.fixture
def body_dur():
    return None

@given(parsers.parse('it has body duration {body_dur}'), target_fixture='given_body_dur')
@given(parsers.parse('it has body duration'), target_fixture='given_body_dur')
def given_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur


@pytest.fixture
def div_begin():
    return None

@given(parsers.parse('it has div begin time {div_begin}'), target_fixture='given_div_begin')
@given(parsers.parse('it has div begin time'), target_fixture='given_div_begin')
def given_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin


@pytest.fixture
def div_end():
    return None

@given(parsers.parse('it has div end time {div_end}'), target_fixture='given_div_end')
@given(parsers.parse('it has div end time'), target_fixture='given_div_end')
def given_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end


@pytest.fixture
def p_begin():
    return None

@given(parsers.parse('it has p begin time {p_begin}'), target_fixture='given_p_begin')
@given(parsers.parse('it has p begin time'), target_fixture='given_p_begin')
def given_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin


@pytest.fixture
def p_end():
    return None

@given(parsers.parse('it has p end time {p_end}'), target_fixture='given_p_end')
@given(parsers.parse('it has p end time'), target_fixture='given_p_end')
def given_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end


@pytest.fixture
def span_begin():
    return None

@given(parsers.parse('it has span begin time {span_begin}'), target_fixture='given_span_begin')
@given(parsers.parse('it has span begin time'), target_fixture='given_span_begin')
def given_span_begin(span_begin, template_dict):
    template_dict['span_begin'] = span_begin


@pytest.fixture
def span_end():
    return None

@given(parsers.parse('it has span end time {span_end}'), target_fixture='given_span_end')
@given(parsers.parse('it has span end time'), target_fixture='given_span_end')
def given_span_end(span_end, template_dict):
    template_dict['span_end'] = span_end


@pytest.fixture
def span2_begin():
    return None

@given(parsers.parse('it has span2 begin time {span2_begin}'), target_fixture='given_span2_begin')
@given(parsers.parse('it has span2 begin time'), target_fixture='given_span2_begin')
def given_span2_begin(span2_begin, template_dict):
    template_dict['span2_begin'] = span2_begin


@pytest.fixture
def span2_end():
    return None

@given(parsers.parse('it has span2 end time {span2_end}'), target_fixture='given_span2_end')
@given(parsers.parse('it has span2 end time'), target_fixture='given_span2_end')
def given_span2_end(span2_end, template_dict):
    template_dict['span2_end'] = span2_end


@given(parsers.parse('it has sequence id {sequence_id_1}'), target_fixture='given_original_sequence_id')
def given_original_sequence_id(template_dict, sequence_id_1):
    template_dict['sequence_identifier'] = sequence_id_1


@pytest.fixture
def authoring_delay():
    return None

@given(parsers.parse('it has authoring delay {authoring_delay}'), target_fixture='given_authoring_delay')
@given(parsers.parse('it has authoring delay'), target_fixture='given_authoring_delay')
def given_authoring_delay(template_dict, authoring_delay):
    template_dict['authoring_delay'] = authoring_delay


@when(parsers.parse('the retiming delay node delays it by {delay}'))
def when_retiming_delay(delay, test_context, gen_document):

    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    carriage = MagicMock(spec=IProducerCarriage)
    carriage.expects.return_value = EBUTT3Document

    delay_float = LimitedClockTimingType(delay).timedelta.total_seconds()

    delay_node = RetimingDelayNode(
        node_id='simple-delay-node',
        producer_carriage=carriage,
        fixed_delay=delay_float,
        document_sequence='delayed_sequence',
    )
    delay_node.process_document(gen_document)
    # As long as you operate on a document produced by the given statement you do not have to do this step unless
    # you wanted to be compatible with some pre-existing implemented when statements expecting the
    # document in the test_context fixture.
    test_context['doc'] = gen_document


@then(parsers.parse('the retiming delay node with {produced_sequence} will reject it'))
def then_retiming_delay_node_rejects(gen_document, produced_sequence):
    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = 'local'
    carriage = MagicMock(spec=IProducerCarriage)
    carriage.expects.return_value = EBUTT3Document

    delay_float = 5.0

    delay_node = RetimingDelayNode(
        node_id='simple-delay-node',
        producer_carriage=carriage,
        fixed_delay=delay_float,
        document_sequence=produced_sequence
    )
    with pytest.raises(UnexpectedSequenceIdentifierError):
        delay_node.process_document(gen_document)


@then(parsers.parse('the delay node outputs the document at {delayed_avail_time}'))
def then_availability_time(delayed_avail_time, test_context):
    delayed_avail_time_float = LimitedClockTimingType(delayed_avail_time).timedelta
    assert test_context['doc'].availability_time == delayed_avail_time_float


# functions for computed times

@pytest.fixture
def updated_body_begin():
    return ''

@then(parsers.parse('the updated body computed begin time is {updated_body_begin}'))
@then(parsers.parse('the updated body computed begin time is'))
def then_updated_body_computed_begin_time(test_context, updated_body_begin):
    if updated_body_begin != '':
        assert test_context['doc'].binding.body.computed_begin_time == LimitedClockTimingType(updated_body_begin).timedelta
    else:
        assert test_context['doc'].binding.body.computed_begin_time is None


@pytest.fixture
def updated_body_end():
    return ''

@then(parsers.parse('the updated body computed end time is {updated_body_end}'))
@then(parsers.parse('the updated body computed end time is'))
def then_updated_body_computed_end_time(test_context, updated_body_end):
    if updated_body_end != '':
        assert test_context['doc'].binding.body.computed_end_time == LimitedClockTimingType(updated_body_end).timedelta
    else:
        assert test_context['doc'].binding.body.computed_end_time is None


@pytest.fixture
def updated_div_begin():
    return ''

@then(parsers.parse('the updated div computed begin time is {updated_div_begin}'))
@then(parsers.parse('the updated div computed begin time is'))
def then_updated_div_computed_begin_time(test_context, updated_div_begin):
    if updated_div_begin != '':
        assert test_context['doc'].binding.body.div[0].computed_begin_time == LimitedClockTimingType(updated_div_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].computed_begin_time is None


@pytest.fixture
def updated_div_end():
    return ''

@then(parsers.parse('the updated div computed end time is {updated_div_end}'))
@then(parsers.parse('the updated div computed end time is'))
def then_updated_div_computed_end_time(test_context, updated_div_end):
    if updated_div_end != '':
        assert test_context['doc'].binding.body.div[0].computed_end_time == LimitedClockTimingType(updated_div_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].computed_end_time is None


@pytest.fixture
def updated_p_begin():
    return ''

@then(parsers.parse('the updated p computed begin time is {updated_p_begin}'))
@then(parsers.parse('the updated p computed begin time is'))
def then_updated_p_computed_begin_time(test_context, updated_p_begin):
    if updated_p_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].computed_begin_time == LimitedClockTimingType(updated_p_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].computed_begin_time is None


@pytest.fixture
def updated_p_end():
    return ''

@then(parsers.parse('the updated p computed end time is {updated_p_end}'))
@then(parsers.parse('the updated p computed end time is'))
def then_updated_p_computed_end_time(test_context, updated_p_end):
    if updated_p_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].computed_end_time == LimitedClockTimingType(updated_p_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].computed_end_time is None


@pytest.fixture
def updated_span_begin():
    return ''

@then(parsers.parse('the updated span computed begin time is {updated_span_begin}'))
@then(parsers.parse('the updated span computed begin time is'))
def then_updated_span_computed_begin_time(test_context, updated_span_begin):
    if updated_span_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[0].computed_begin_time == LimitedClockTimingType(updated_span_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[0].computed_begin_time is None


@pytest.fixture
def updated_span_end():
    return ''

@then(parsers.parse('the updated span computed end time is {updated_span_end}'))
@then(parsers.parse('the updated span computed end time is'))
def then_updated_span_computed_end_time(test_context, updated_span_end):
    if updated_span_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[0].computed_end_time == LimitedClockTimingType(updated_span_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[0].computed_end_time is None


@pytest.fixture
def updated_span2_begin():
    return ''

@then(parsers.parse('the updated span2 computed begin time is {updated_span2_begin}'))
@then(parsers.parse('the updated span2 computed begin time is'))
def then_updated_span2_computed_begin_time(test_context, updated_span2_begin):
    if updated_span2_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[1].computed_begin_time == LimitedClockTimingType(updated_span2_begin).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[1].computed_begin_time is None


@pytest.fixture
def updated_span2_end():
    return ''

@then(parsers.parse('the updated span2 computed end time is {updated_span2_end}'))
@then(parsers.parse('the updated span2 computed end time is'))
def then_updated_span2_computed_end_time(test_context, updated_span2_end):
    if updated_span2_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[1].computed_end_time == LimitedClockTimingType(updated_span2_end).timedelta
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[1].computed_end_time is None


# functions for specified times

@pytest.fixture
def updated_body_specified_begin():
    return ''

@then(parsers.parse('the updated body specified begin time is {updated_body_specified_begin}'))
@then(parsers.parse('the updated body specified begin time is'))
def then_updated_body_specified_begin_time(test_context, updated_body_specified_begin):
    if updated_body_specified_begin != '':
        assert test_context['doc'].binding.body.begin == updated_body_specified_begin
    else:
        assert test_context['doc'].binding.body.begin is None


@pytest.fixture
def updated_body_specified_end():
    return ''

@then(parsers.parse('the updated body specified end time is {updated_body_specified_end}'))
@then(parsers.parse('the updated body specified end time is'))
def then_updated_body_specified_end_time(test_context, updated_body_specified_end):
    if updated_body_specified_end != '':
        assert test_context['doc'].binding.body.end == updated_body_specified_end
    else:
        assert test_context['doc'].binding.body.end is None


@pytest.fixture
def updated_div_specified_begin():
    return ''

@then(parsers.parse('the updated div specified begin time is {updated_div_specified_begin}'))
@then(parsers.parse('the updated div specified begin time is'))
def then_updated_div_specified_begin_time(test_context, updated_div_specified_begin):
    if updated_div_specified_begin != '':
        assert test_context['doc'].binding.body.div[0].begin == updated_div_specified_begin
    else:
        assert test_context['doc'].binding.body.div[0].begin is None


@pytest.fixture
def updated_div_specified_end():
    return ''

@then(parsers.parse('the updated div specified end time is {updated_div_specified_end}'))
@then(parsers.parse('the updated div specified end time is'))
def then_updated_div_specified_end_time(test_context, updated_div_specified_end):
    if updated_div_specified_end != '':
        assert test_context['doc'].binding.body.div[0].end == updated_div_specified_end
    else:
        assert test_context['doc'].binding.body.div[0].end is None


@pytest.fixture
def updated_p_begin():
    return ''

@then(parsers.parse('the updated p specified begin time is {updated_p_begin}'))
@then(parsers.parse('the updated p specified begin time is'))
def then_updated_p_specified_begin_time(test_context, updated_p_begin):
    if updated_p_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].begin == updated_p_begin
    else:
        assert test_context['doc'].binding.body.div[0].p[0].begin is None


@pytest.fixture
def updated_p_specified_end():
    return ''

@then(parsers.parse('the updated p specified end time is {updated_p_specified_end}'))
@then(parsers.parse('the updated p specified end time is'))
def then_updated_p_specified_end_time(test_context, updated_p_specified_end):
    if updated_p_specified_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].end == updated_p_specified_end
    else:
        assert test_context['doc'].binding.body.div[0].p[0].end is None


@pytest.fixture
def updated_span_specified_begin():
    return ''

@then(parsers.parse('the updated span specified begin time is {updated_span_specified_begin}'))
@then(parsers.parse('the updated span specified begin time is'))
def then_updated_span_specified_begin_time(test_context, updated_span_specified_begin):
    if updated_span_specified_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[0].begin == updated_span_specified_begin
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[0].begin is None


@pytest.fixture
def updated_span_specified_end():
    return ''

@then(parsers.parse('the updated span specified end time is {updated_span_specified_end}'))
@then(parsers.parse('the updated span specified end time is'))
def then_updated_span_specified_end_time(test_context, updated_span_specified_end):
    if updated_span_specified_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[0].end == updated_span_specified_end
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[0].end is None


@pytest.fixture
def updated_span2_specified_begin():
    return ''

@then(parsers.parse('the updated span2 specified begin time is {updated_span2_specified_begin}'))
@then(parsers.parse('the updated span2 specified begin time is'))
def then_updated_span2_specified_begin_time(test_context, updated_span2_specified_begin):
    if updated_span2_specified_begin != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[1].begin == updated_span2_specified_begin
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[1].begin is None


@pytest.fixture
def updated_span2_specified_end():
    return ''

@then(parsers.parse('the updated span2 specified end time is {updated_span2_specified_end}'))
@then(parsers.parse('the updated span2 specified end time is'))
def then_updated_span2_specified_end_time(test_context, updated_span2_specified_end):
    if updated_span2_specified_end != '':
        assert test_context['doc'].binding.body.div[0].p[0].span[1].end == updated_span2_specified_end
    else:
        assert test_context['doc'].binding.body.div[0].p[0].span[1].end is None


@pytest.fixture
def sequence_id_2():
    return None

@then(parsers.parse('the updated document has sequence id {sequence_id_2}'))
@then(parsers.parse('the updated document has sequence id'))
def then_updated_seq_id(test_context, sequence_id_2):
    assert test_context['doc'].sequence_identifier == sequence_id_2


# null authoring_delay fixture defined for previous step earlier in this file
@then(parsers.parse('the updated document has authoring delay {authoring_delay}'))
@then(parsers.parse('the updated document has authoring delay'))
def then_updated_auth_delay(test_context, authoring_delay):
    if authoring_delay:
        assert test_context['doc'].binding.authoringDelay == authoring_delay
    else:
        assert test_context['doc'].binding.authoringDelay is None
