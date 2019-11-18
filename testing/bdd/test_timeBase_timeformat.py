from pytest_bdd import scenarios, when

scenarios('features/validation/timeBase_timeformat_constraints.feature')


@when('it has timeBase <time_base>')
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when('it has body begin time <body_begin>')
def when_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@when('it has body end time <body_end>')
def when_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@when('it has body duration <body_dur>')
def when_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur


@when('it has div begin time <div_begin>')
def when_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin


@when('it has div end time <div_end>')
def when_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end


@when('it has p begin time <p_begin>')
def when_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin


@when('it has p end time <p_end>')
def when_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end


@when('it has span begin time <span_begin>')
def when_span_begin(span_begin, template_dict):
    template_dict['span_begin'] = span_begin


@when('it has span end time <span_end>')
def when_span_end(span_end, template_dict):
    template_dict['span_end'] = span_end

@when('it has documentStartOfProgramme <start_time>')
def when_documentStartOfProgramme(start_time, template_dict):
    template_dict['start_of_programme'] = start_time
