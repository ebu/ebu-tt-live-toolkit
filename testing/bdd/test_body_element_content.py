from pytest_bdd import when, scenarios


scenarios('features/validation/body_element_content.feature')


def handle_element(element):
    if element == 'span':
        return '<tt:span></tt:span>'
    elif element == 'p':
        return '<tt:p xml:id="ID0010"></tt:p>'
    elif element == 'br':
        return '<tt:br/>'


@when('its body has a <child_element>')
def when_child_element(child_element, template_dict):
    template_dict['body_content'] = handle_element(child_element)
