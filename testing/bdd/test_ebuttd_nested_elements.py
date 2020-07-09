import xml.etree.ElementTree as ET
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('features/nesting/ebuttd_nested_elements.feature')

@then('p elements do not have a region')
def then_p_has_no_region(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')
    for element in elements:
        for item in list(element):
            if item.tag == "{http://www.w3.org/ns/ttml}p":
                assert item.get("region") == None


@then('there is one div containing one p')
def then_p_has_been_removed(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')
    assert len(elements) == 1
    assert len(elements[0]) == 1
    assert elements[0][0].tag == "{http://www.w3.org/ns/ttml}p"

@then('all divs contain at least one p element')
def then_it_contains_no_divs(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body//{http://www.w3.org/ns/ttml}div')
    for element in elements:
        assert len(list(element)) != 0
        p_count = 0
        for p in list(element):
            if p.tag == "{http://www.w3.org/ns/ttml}p":
                p_count += 1
        assert p_count > 0

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
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    for element in elements:
        for tmp in list(element):
            assert tmp.tag != "{http://www.w3.org/ns/ttml}span"

@then('the second span\'s style is outerinnerYellow')
def combine_span_styles(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    assert elements[1].get("style") == "autogenFontStyle_n_200_n outerinnerYellow"

@then('the second span contains a br')
def second_span_contains_br(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    assert elements[1].find("{http://www.w3.org/ns/ttml}br") is not None

@then(parsers.parse('there is no style named "{style_name}"'))
def no_duplicate_styles(test_context, style_name):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}head/{http://www.w3.org/ns/ttml}styling/{http://www.w3.org/ns/ttml}style')
    for element in elements:
        assert element.get("{http://www.w3.org/XML/1998/namespace}id") != style_name


@then(parsers.parse('any span with the style "{style_name}" also has the style "{size_style}"'))
def percentage_size_for_nested_styles(test_context, style_name, size_style):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    for element in elements:
        styles = element.get("style").split(" ")
        if style_name in styles:
            assert size_style in styles

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
