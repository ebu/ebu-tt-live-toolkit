from datetime import timedelta

from pytest_bdd import scenarios, then, when

from ebu_tt_live.documents import EBUTT3Document
from testing.bdd.conftest import legacy_name

scenarios('features/validation/time_regex_parsing.feature')


@when(**legacy_name('it has timeBase <time_base>'))
def when_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when(**legacy_name('it has body begin time <body_begin>'))
def when_body_begin(body_begin, template_dict):
    template_dict['body_begin'] = body_begin


@then(**legacy_name('timedelta value given when reading body.begin should be <h> <m> <s> <ms>'))
def check_correct_parsing(template_file, template_dict, h, m, s, ms):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    assert document._ebutt3_content.body.begin.timedelta == timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))
