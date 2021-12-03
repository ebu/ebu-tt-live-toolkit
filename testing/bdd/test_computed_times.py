from pytest_bdd import scenarios, given, parsers
from pytest import fixture

scenarios('features/timing/computed_times.feature')
scenarios('features/timing/computed_times_empty_doc.feature')

@fixture
def l():
    return None

@given(parsers.parse('example_line is {l}'))
@given(parsers.parse('example_line is'))
def given_example_line(l, template_dict):
    template_dict['l'] = l

@fixture
def time_base():
    return None

@given(parsers.parse('it has timeBase {time_base}'))
@given(parsers.parse('it has timeBase'))
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@fixture
def sequence_identifier():
    return None

@given(parsers.parse('it has sequenceIdentifier {sequence_identifier}'))
@given(parsers.parse('it has sequenceIdentifier'))
def given_seq_id(sequence_identifier, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier


@fixture
def sequence_number():
    return None

@given(parsers.parse('it has sequenceNumber {sequence_number}'))
@given(parsers.parse('it has sequenceNumber'))
def given_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number


@fixture
def no_body():
    return None

@given(parsers.parse('it has body {no_body}'))
@given(parsers.parse('it has body'))
def given_no_body(no_body, template_dict):
    template_dict['no_body'] = no_body


@fixture
def body_begin():
    return None

@given(parsers.parse('it has body begin time {body_begin}'))
@given(parsers.parse('it has body begin time'))
def given_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@fixture
def body_end():
    return None

@given(parsers.parse('it has body end time {body_end}'))
@given(parsers.parse('it has body end time'))
def given_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@fixture
def body_dur():
    return None

@given(parsers.parse('it has body duration {body_dur}'))
@given(parsers.parse('it has body duration'))
def given_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur

@fixture
def div_begin():
    return None

@given(parsers.parse('it has div begin time {div_begin}'))
@given(parsers.parse('it has div begin time'))
def given_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin


@fixture
def div_end():
    return None

@given(parsers.parse('it has div end time {div_end}'))
@given(parsers.parse('it has div end time'))
def given_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end


@fixture
def p_begin():
    return None

@given(parsers.parse('it has p begin time {p_begin}'))
@given(parsers.parse('it has p begin time'))
def given_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin

@fixture
def p_end():
    return None

@given(parsers.parse('it has p end time {p_end}'))
@given(parsers.parse('it has p end time'))
def given_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end

@fixture
def span_begin():
    return None

@given(parsers.parse('it has span begin time {span_begin}'))
@given(parsers.parse('it has span begin time'))
def given_span_begin(span_begin, template_dict):
    template_dict['span_begin'] = span_begin

@fixture
def span_end():
    return None

@given(parsers.parse('it has span end time {span_end}'))
@given(parsers.parse('it has span end time'))
def given_span_end(span_end, template_dict):
    template_dict['span_end'] = span_end

@fixture
def span2_begin():
    return None

@given(parsers.parse('it has span2 begin time {span2_begin}'))
@given(parsers.parse('it has span2 begin time'))
def given_span2_begin(span2_begin, template_dict):
    template_dict['span2_begin'] = span2_begin

@fixture
def span2_end():
    return None

@given(parsers.parse('it has span2 end time {span2_end}'))
@given(parsers.parse('it has span2 end time'))
def given_span2_end(span2_end, template_dict):
    template_dict['span2_end'] = span2_end


@fixture
def span3_begin():
    return None

@given(parsers.parse('it has span3 begin time {span3_begin}'))
@given(parsers.parse('it has span3 begin time'))
def given_span3_begin(span3_begin, template_dict):
    template_dict['span3_begin'] = span3_begin


@fixture
def span3_end():
    return None

@given(parsers.parse('it has span3 end time {span3_end}'))
@given(parsers.parse('it has span3 end time'))
def given_span3_end(span3_end, template_dict):
    template_dict['span3_end'] = span3_end
