from ebu_tt_live.documents import EBUTT3Document
from pytest_bdd import scenarios, given, when, then

scenarios('features/timing/delay.feature')


@when('the delay is <delay>')
def when_delay(delay, template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    document.availability_time += delay


@then('the delay node outputs the document at <delayed_avail_time>')
def then_availability_time(delayed_avail_time, template_file, template_dict):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    assert document.availability_time == delayed_avail_time

