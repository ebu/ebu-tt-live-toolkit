from ebu_tt_live.documents import EBUTT3Document
from pyxb import ValidationError
from pytest_bdd import given, then, scenarios
import pytest


scenarios('features/validation/body_elements_order.feature')


def handle_element(element):
    if element == 'span':
        return '<tt:span></tt:span>'
    elif element == 'p':
        return '<tt:p xml:id="ID0010"></tt:p>'
    elif element == 'br':
        return '<tt:br/>'


@given('its body has a <body_element>')
def xml_body_element(body_element):
    return handle_element(body_element)


@then('document is invalid')
def invalid_doc(template_file, xml_body_element):
    xml = template_file.render(body_content=xml_body_element)
    with pytest.raises(ValidationError):
        EBUTT3Document.create_from_xml(xml)
