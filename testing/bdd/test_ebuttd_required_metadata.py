import xml.etree.ElementTree as ET
from pytest_bdd import scenarios, then

scenarios('features/metadata/ebuttd_required_metadata.feature')


@then('the EBUTTD document contains a documentMetadata element <element_name> with value <element_value>')
def then_ebuttd_metadata_contains(test_context, element_name, element_value):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}head/{http://www.w3.org/ns/ttml}metadata//{urn:ebu:tt:metadata}%s' % element_name)
    assert element_value in [e.text for e in elements]
