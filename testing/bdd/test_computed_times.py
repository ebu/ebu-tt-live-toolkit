from pytest_bdd import scenarios, given

scenarios('features/timing/computed_times.feature')


@given('it has timeBase <time_base>')
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@given('it has sequenceIdentifier <sequence_identifier>')
def given_seq_id(sequence_identifier, template_dict):
    template_dict['sequence_identifier'] = sequence_identifier


@given('it has sequenceNumber <sequence_number>')
def given_sequence_number(sequence_number, template_dict):
    template_dict['sequence_number'] = sequence_number


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


@given('it has span3 begin time <span3_begin>')
def given_span3_begin(span3_begin, template_dict):
    template_dict['span3_begin'] = span3_begin


@given('it has span3 end time <span3_end>')
def given_span3_end(span3_end, template_dict):
    template_dict['span3_end'] = span3_end
