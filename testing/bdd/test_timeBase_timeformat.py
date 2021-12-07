from pytest_bdd import scenarios, when, parsers
from pytest import fixture


scenarios('features/validation/timeBase_timeformat_constraints.feature')


@when(parsers.parse('it has timeBase {time_base}'))
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@fixture
def body_begin():
    return ''

@when(parsers.parse('it has body begin time {body_begin}'))
@when(parsers.parse('it has body begin time'))
def when_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@fixture
def body_end():
    return ''

@when(parsers.parse('it has body end time {body_end}'))
@when(parsers.parse('it has body end time'))
def when_body_end(body_end, template_dict):
    template_dict['body_end'] = body_end


@fixture
def body_dur():
    return ''

@when(parsers.parse('it has body duration {body_dur}'))
@when(parsers.parse('it has body duration'))
def when_body_dur(body_dur, template_dict):
    template_dict['body_dur'] = body_dur


@fixture
def div_begin():
    return ''

@when(parsers.parse('it has div begin time {div_begin}'))
@when(parsers.parse('it has div begin time'))
def when_div_begin(div_begin, template_dict):
    template_dict['div_begin'] = div_begin


@fixture
def div_end():
    return ''

@when(parsers.parse('it has div end time {div_end}'))
@when(parsers.parse('it has div end time'))
def when_div_end(div_end, template_dict):
    template_dict['div_end'] = div_end


@fixture
def p_begin():
    return ''

@when(parsers.parse('it has p begin time {p_begin}'))
@when(parsers.parse('it has p begin time'))
def when_p_begin(p_begin, template_dict):
    template_dict['p_begin'] = p_begin


@fixture
def p_end():
    return ''

@when(parsers.parse('it has p end time {p_end}'))
@when(parsers.parse('it has p end time'))
def when_p_end(p_end, template_dict):
    template_dict['p_end'] = p_end


@fixture
def span_begin():
    return ''

@when(parsers.parse('it has span begin time {span_begin}'))
@when(parsers.parse('it has span begin time'))
def when_span_begin(span_begin, template_dict):
    template_dict['span_begin'] = span_begin


@fixture
def span_end():
    return ''

@when(parsers.parse('it has span end time {span_end}'))
@when(parsers.parse('it has span end time'))
def when_span_end(span_end, template_dict):
    template_dict['span_end'] = span_end
