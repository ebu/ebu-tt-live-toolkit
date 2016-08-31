from pytest_bdd import when, scenarios


scenarios('features/validation/timeBase_clock_clockMode_mandatory.feature')


@when('it has ttp:timeBase attribute <time_base>')
def when_has_time_base(time_base, template_dict):
    template_dict['time_base'] = time_base


@when('it has ttp:clockMode attribute <clock_mode>')
def when_has_clock_mode(clock_mode, template_dict):
    template_dict['clock_mode'] = clock_mode
