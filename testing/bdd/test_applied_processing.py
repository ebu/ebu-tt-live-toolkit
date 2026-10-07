from pytest_bdd import parsers, scenarios, when

scenarios('features/validation/applied-processing.feature')

@when(parsers.parse('appliedProcessing element has process attribute {process}'))
def when_applied_processing_process_attribute(process, template_dict):
    template_dict["process"] = process


@when(parsers.parse('appliedProcessing element has process attribute '))
def when_applied_processing_empty_process_attribute(template_dict):
    # template_dict["process"] = process
    return


@when(parsers.parse('appliedProcessing element has generatedBy attribute {generated_by}'))
def when_applied_processing_generatedBy_attribute(generated_by, template_dict):
    template_dict["generated_by"] = generated_by


@when(parsers.parse('appliedProcessing element has generatedBy attribute '))
def when_applied_processing_empty_generatedBy_attribute(template_dict):
    # template_dict["generated_by"] = generated_by
    return


@when(parsers.parse('appliedProcessing element has sourceId attribute {source_id}'))
def when_applied_processing_sourceId_attribute(source_id, template_dict):
    template_dict["source_id"] = source_id


@when(parsers.parse('appliedProcessing element has sourceId attribute '))
def when_applied_processing_empty_sourceId_attribute(template_dict):
    # template_dict["source_id"] = source_id
    return
