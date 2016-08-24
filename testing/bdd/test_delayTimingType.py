from pytest_bdd import when, scenarios


scenarios('features/validation/delayTimingType.feature')


@when('ebuttm:authoringDelay attribute has value <authoring_delay>')
def when_authoring_delay(authoring_delay, template_dict):
    template_dict['authoring_delay'] = authoring_delay
