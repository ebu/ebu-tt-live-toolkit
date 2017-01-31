
from pytest_bdd import scenarios, when

scenarios('features/validation/documentRevisionNumber.feature')


@when('document revision number is <document_revision_number>')
def when_document_revision_number(template_dict, document_revision_number):
    template_dict['document_revision_number'] = document_revision_number
