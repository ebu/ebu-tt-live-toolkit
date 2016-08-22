from pytest_bdd import when, scenarios


scenarios('features/validation/facet.feature')


@when('it has facet1 applied to element <parent1>')
def when_child_element(parent1, template_dict):
    template_dict['body_content'] = handle_element(child_element)
