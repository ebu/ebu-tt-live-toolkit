from pytest_bdd import scenarios, given

scenarios('features/validation/timeBase_timeformat_constraints.feature')


@given('it has timeBase <time_base>')
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@given('it has body begin time <body_begin>')
def given_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@given('it has body end time <body_end>')
def given_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@given('it has body duration <body_dur>')
def given_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur


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
