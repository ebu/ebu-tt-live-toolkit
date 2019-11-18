import pytest
from pytest_bdd import parsers, scenarios, when, then
from ebu_tt_live.documents import EBUTT1Document
from pyxb.exceptions_ import IncompleteElementContentError, UnrecognizedAttributeError

scenarios('features/ebutt1/ebutt1_validity.feature')


@when(parsers.parse('the document contains a "{element}" element'))
def when_document_contains_element(template_dict, element):
    template_dict[element] = True


@when(parsers.parse('the document body contains a "{attribute}" attribute'))
def when_document_body_contains_attribute(template_dict, attribute):
    template_dict[attribute] = True


@when('the document\'s timeBase is set to <timebase>')
def when_document_timebase(template_dict, timebase):
    # timeBase in ebutt1_template.xml is 'media' by default
    template_dict['timeBase'] = timebase


@when('the document contains an ebuttp attribute <attribute>')
def when_document_contains_ebuttp_attribute(template_dict, attribute):
    template_dict['ebuttp'] = True
    template_dict[attribute] = True


@when('the XML is parsed as an EBU-TT-1 document')
def when_document_parsed_ebutt1(test_context, template_file, template_dict):
    xml_text = template_file.render(template_dict)
    print(xml_text)
    ebutt1_document = EBUTT1Document.create_from_xml(xml_text)
    test_context['ebutt1_document'] = ebutt1_document


@then('the document fails to parse as an EBU-TT-1 document because of an IncompleteElementContentError')
def then_document_fails_ebutt1_element(template_file, template_dict):
    xml_text = template_file.render(template_dict)
    print(xml_text)
    with pytest.raises(IncompleteElementContentError):
        EBUTT1Document.create_from_xml(xml_text)


@then('the document fails to parse as an EBU-TT-1 document because of an UnrecognizedAttributeError')
def then_document_fails_ebutt1_attribute(template_file, template_dict):
    xml_text = template_file.render(template_dict)
    print(xml_text)
    with pytest.raises(UnrecognizedAttributeError):
        EBUTT1Document.create_from_xml(xml_text)


@then('the EBU-TT-1 document is valid')
def then_ebutt1_valid(test_context):
    document = test_context['ebutt1_document']
    document.validate()
