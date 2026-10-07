from pytest_bdd import given, scenarios

from testing.bdd.conftest import legacy_name

scenarios('features/timing/computed_times.feature')
scenarios('features/timing/computed_times_empty_doc.feature')


@given(**legacy_name(name='example_line is <l>'))
def given_example_line(l, template_dict):
    template_dict['l'] = l


@given(**legacy_name(name='it has timeBase <time_base>'))
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@given(**legacy_name(name='it has sequenceIdentifier <sequence_identifier>'))
def given_seq_id(sequence_identifier, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier


@given(**legacy_name(name='it has sequenceNumber <sequence_number>'))
def given_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number


# @given(**legacy_name(name='it has body <no_body>'))
# def given_no_body(no_body, template_dict):
#     template_dict['no_body'] = no_body


@given(**legacy_name(name='it has body begin time <body_begin>'))
def given_body_begin(body_begin, template_dict):
    # print(f'assigning body begin time of <{body_begin}>')
    template_dict['body_begin'] = body_begin


@given(**legacy_name(name='it has body end time <body_end>'))
def given_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@given(**legacy_name(name='it has body duration <body_dur>'))
def given_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur


@given(**legacy_name(name='it has div begin time <div_begin>'))
def given_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin


@given(**legacy_name(name='it has div end time <div_end>'))
def given_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end


@given(**legacy_name(name='it has p begin time <p_begin>'))
def given_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin


@given(**legacy_name(name='it has p end time <p_end>'))
def given_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end


@given(**legacy_name(name='it has span begin time <span_begin>'))
def given_span_begin(span_begin, template_dict):
    template_dict['span_begin'] = span_begin


@given(**legacy_name(name='it has span end time <span_end>'))
def given_span_end(span_end, template_dict):
    template_dict['span_end'] = span_end


@given(**legacy_name(name='it has span2 begin time <span2_begin>'))
def given_span2_begin(span2_begin, template_dict):
    template_dict['span2_begin'] = span2_begin


@given(**legacy_name(name='it has span2 end time <span2_end>'))
def given_span2_end(span2_end, template_dict):
    template_dict['span2_end'] = span2_end


@given(**legacy_name(name='it has span3 begin time <span3_begin>'))
def given_span3_begin(span3_begin, template_dict):
    template_dict['span3_begin'] = span3_begin


@given(**legacy_name(name='it has span3 end time <span3_end>'))
def given_span3_end(span3_end, template_dict):
    template_dict['span3_end'] = span3_end
