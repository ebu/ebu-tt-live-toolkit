from ebu_tt_live.documents import EBUTT3Document
from datetime import timedelta
from pytest_bdd import scenarios, given, then

scenarios('features/validation/time_regex_parsing.feature', example_converters=dict(trusted_timedeltas_index=int))

trusted_timedeltas = [
    timedelta(hours=15),
    timedelta(minutes=30),
    timedelta(seconds=42),
    timedelta(milliseconds=67),
    timedelta(hours=42, minutes=5, seconds=60),
    timedelta(hours=999, minutes=9, seconds=60)
]


@given('it has timeBase <time_base>')
def given_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@given('it has body begin time <body_begin>')
def given_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@then('timedelta value given when reading body.begin should be <trusted_timedeltas_index>')
def check_correct_parsing(template_file, template_dict, trusted_timedeltas_index):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    assert document._ebutt3_content.body.begin.timedelta() == trusted_timedeltas[trusted_timedeltas_index]
