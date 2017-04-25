from pytest_bdd import when, scenarios


scenarios('features/validation/applied-processing.feature')


@when('applied processing element has process attribute <action>')
def when_applied_processing_process_attribute(process, template_dict):
    template_dict["process"] = process


@when('applied processing element has generatedBy attribute <generated_by>')
def when_applied_processing_generatedBy_attribute(generated_by, template_dict):
    template_dict["generated_by"] = generated_by


@when('applied processing element has sourceId attribute <source_id>')
def when_applied_processing_sourceId_attribute(source_id, template_dict):
    template_dict["source_id"] = source_id
