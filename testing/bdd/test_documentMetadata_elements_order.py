from pytest_bdd import when, scenarios, parsers
from pytest import fixture

scenarios('features/validation/documentMetadata_elements_order.feature')


def handle_document_metadata_element(element):
    if element == 'originalSourceServiceIdentifier':
        return '<ebuttm:originalSourceServiceIdentifier>Source identifier</ebuttm:originalSourceServiceIdentifier>\n'
    elif element == 'intendedDestinationServiceIdentifier':
        return '<ebuttm:intendedDestinationServiceIdentifier>Destination identifier</ebuttm:intendedDestinationServiceIdentifier>\n'
    elif element == 'documentFacet':
        return '<ebuttm:documentFacet summary="mixed">test</ebuttm:documentFacet>\n'
    elif element == 'appliedProcessing':
        return '<ebuttm:appliedProcessing process="creation" generatedBy="producer" />\n'
    elif element == 'documentIdentifier':
        return '<ebuttm:documentIdentifier>Doc ID</ebuttm:documentIdentifier>'
    else:
        return ''


@fixture
def document_metadata_1():
    return None

@when(parsers.parse('it has documentMetadata 1 {document_metadata_1}'))
@when(parsers.parse('it has documentMetadata 1'))
def when_document_metadata_1(document_metadata_1, template_dict):
    template_dict['document_metadata'] = ""
    template_dict['document_metadata'] += handle_document_metadata_element(document_metadata_1)


@fixture
def document_metadata_2():
    return None

@when(parsers.parse('it has documentMetadata 2 {document_metadata_2}'))
@when(parsers.parse('it has documentMetadata 2'))
def when_document_metadata_2(document_metadata_2, template_dict):
    template_dict['document_metadata'] += handle_document_metadata_element(document_metadata_2)


@fixture
def document_metadata_3():
    return None

@when(parsers.parse('it has documentMetadata 3 {document_metadata_3}'))
@when(parsers.parse('it has documentMetadata 3'))
def when_document_metadata_3(document_metadata_3, template_dict):
    template_dict['document_metadata'] += handle_document_metadata_element(document_metadata_3)


@fixture
def document_metadata_4():
    return None

@when(parsers.parse('it has documentMetadata 4 {document_metadata_4}'))
@when(parsers.parse('it has documentMetadata 4'))
def when_document_metadata_4(document_metadata_4, template_dict):
    template_dict['document_metadata'] += handle_document_metadata_element(document_metadata_4)
