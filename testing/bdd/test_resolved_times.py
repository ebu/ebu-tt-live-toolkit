from pytest_bdd import scenarios, given
from datetime import timedelta
from conftest import timestr_to_timedelta

scenarios('features/timing/resolved_times.feature')


@given('it has timeBase <time_base>')
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


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



