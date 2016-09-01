from pytest_bdd import when, scenarios


scenarios('features/validation/trace.feature')


@when('trace element has action attribute <action>')
def when_trace_action_attribute(action, template_dict):
    template_dict["action"] = action


@when('trace element has generatedBy attribute <generated_by>')
def when_trace_generatedBy_attribute(generated_by, template_dict):
    template_dict["generated_by"] = generated_by


@when('trace element has sourceId attribute <source_id>')
def when_trace_sourceId_attribute(source_id, template_dict):
    template_dict["source_id"] = source_id
