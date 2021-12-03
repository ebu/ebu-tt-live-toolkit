from pytest_bdd import when, scenarios, parsers
from pytest import fixture


scenarios('features/validation/applied-processing.feature')

@fixture
def process():
    return None

@fixture
def generated_by():
    return None

@fixture
def source_id():
    return None

@when(parsers.parse('appliedProcessing element has process attribute {process}'))
@when(parsers.parse('appliedProcessing element has process attribute'))
def when_applied_processing_process_attribute(template_dict, process=None):
    template_dict["process"] = process


@when(parsers.parse('appliedProcessing element has generatedBy attribute {generated_by}'))
@when(parsers.parse('appliedProcessing element has generatedBy attribute'))
def when_applied_processing_generatedBy_attribute(template_dict, generated_by=None):
    template_dict["generated_by"] = generated_by


@when(parsers.parse('appliedProcessing element has sourceId attribute {source_id}'))
@when(parsers.parse('appliedProcessing element has sourceId attribute'))
def when_applied_processing_sourceId_attribute(template_dict, source_id=None):
    template_dict["source_id"] = source_id
