from pytest_bdd import when, scenarios


scenarios('features/validation/xml_lang_attribute.feature')


@when('it has xml:lang attribute <lang>')
def when_lang(lang, template_dict):
    template_dict['lang'] = lang
