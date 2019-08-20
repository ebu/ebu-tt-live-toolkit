import xml.etree.ElementTree as ET
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('features/nesting/ebuttd_nested_elements.feature')


@when(parsers.parse('it contains a div with id "{div_id}"'))
def given_div(test_context, template_dict, div_id):
    if 'divs' not in template_dict:
        template_dict['divs'] = list()
    div = {"id": div_id}    
    template_dict['divs'].append(div)
    test_context[div_id] = div
      
@when(parsers.parse('it has p_element "{p_id}"'))
def when_it_contains_p_element(test_context, template_dict, p_id):
    if 'p_elements' not in template_dict:
        template_dict['p_elements'] = list()
    p_element = {"id": p_id}    
    template_dict['p_elements'].append(p_element)
    test_context[p_id] = p_element

@when(parsers.parse('div "{div_id}" has element "{p_id}"'))
def given_div_has_p_element(test_context, template_dict, div_id, p_id):
    for i,div in enumerate(template_dict['divs']):
        if div['id'] == div_id:
            index = i
    if 'p_elements' not in template_dict['divs'][index]:
         template_dict['divs'][index]['p_elements'] = list()
    p_element = test_context[p_id]
    template_dict['divs'][index]['p_elements'].append(p_element)

