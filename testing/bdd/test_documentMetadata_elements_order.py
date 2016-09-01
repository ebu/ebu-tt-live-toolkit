from pytest_bdd import when, scenarios


scenarios('features/validation/documentMetadata_elements_order.feature')


def handle_document_metadata_element(element):
    if element == 'originalSourceServiceIdentifier':
        return '<ebuttm:originalSourceServiceIdentifier>Source identifier</ebuttm:originalSourceServiceIdentifier>\n'
    elif element == 'intendedDestinationServiceIdentifier':
        return '<ebuttm:intendedDestinationServiceIdentifier>Destination identifier</ebuttm:intendedDestinationServiceIdentifier>\n'
    elif element == 'documentFacet':
        return '<ebuttm:documentFacet summary="mixed">test</ebuttm:documentFacet>\n'
    elif element == 'trace':
        return '<ebuttm:trace action="creation" generatedBy="producer" />\n'
    elif element == 'documentIdentifier':
        return '<ebuttm:documentIdentifier>Doc ID</ebuttm:documentIdentifier>'
    else:
        return ''


@when('it has documentMetadata 1 <document_metadata_1>')
def when_document_metadata_1(document_metadata_1, template_dict):
    template_dict['document_metadata'] = ""
    template_dict['document_metadata'] += handle_document_metadata_element(document_metadata_1)


@when('it has documentMetadata 2 <document_metadata_2>')
def when_document_metadata_2(document_metadata_2, template_dict):
    template_dict['document_metadata'] += handle_document_metadata_element(document_metadata_2)


@when('it has documentMetadata 3 <document_metadata_3>')
def when_document_metadata_3(document_metadata_3, template_dict):
    template_dict['document_metadata'] += handle_document_metadata_element(document_metadata_3)


@when('it has documentMetadata 4 <document_metadata_4>')
def when_document_metadata_4(document_metadata_4, template_dict):
    template_dict['document_metadata'] += handle_document_metadata_element(document_metadata_4)
