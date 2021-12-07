from pytest_bdd import when, scenarios, parsers


scenarios('features/validation/delayTimingType.feature')


@when(parsers.parse('ebuttm:authoringDelay attribute has value {authoring_delay}'))
def when_authoring_delay(authoring_delay, template_dict):
    template_dict['authoring_delay'] = authoring_delay
