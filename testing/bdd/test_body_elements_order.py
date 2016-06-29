from pytest_bdd import given, scenarios


scenarios('features/validation/body_elements_order.feature')


def handle_element(element):
    if element == 'span':
        return '<tt:span></tt:span>'
    elif element == 'p':
        return '<tt:p xml:id="ID0010"></tt:p>'
    elif element == 'br':
        return '<tt:br/>'


@given('its body has a <body_element>')
def given_body_element(body_element, template_dict):
    template_dict['body_content'] = handle_element(body_element)
