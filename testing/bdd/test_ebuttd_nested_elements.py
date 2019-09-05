import xml.etree.ElementTree as ET
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('features/nesting/ebuttd_nested_elements.feature')

@then('the p does not have a region attribute')
def then_p_has_no_region(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')

    assert elements[0].get("region") == "R1"
    assert elements[0][0].get("region") == None

    assert len(elements) == 3

@then('the p has been removed from the div')
def then_p_has_been_removed(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')

    assert elements[1].get("region") == "R2"
    assert elements[1][0].get("region") == None

    assert len(elements[1]) == 1

@then('the div and p regions remain the same')
def then_div_and_p_remain_same(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')

    assert elements[2].get("region") == "R4"
    assert elements[2][0].get("region") == None

    assert len(elements[1]) == 1

@then('divs with no p elements are removed')
def then_it_contains_no_divs(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')
    for element in elements:
        assert len(list(element)) != 0

@then('no div contains any other divs')
def then_div_contains_no_divs(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')
    for element in elements:
        for child in list(element): 
            assert child.tag != "{http://www.w3.org/ns/ttml}div"

@then('no span contains any other spans')
def then_span_contains_no_spans(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')
    elements_2 = []
    elements_3 = []
    for element in elements:
            elements_2 += tree.findall('{http://www.w3.org/ns/ttml}p')
    for element in elements_2:
            elements_3 += tree.findall('{http://www.w3.org/ns/ttml}span')


    for element in elements_3:
        for child in list(element): 
            assert child.tag != "{http://www.w3.org/ns/ttml}span"
    pass

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
