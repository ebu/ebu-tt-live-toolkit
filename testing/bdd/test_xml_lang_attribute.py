from pytest_bdd import scenarios, when

from testing.bdd.conftest import legacy_name

scenarios('features/validation/xml_lang_attribute.feature')


@when(**legacy_name('it has xml:lang attribute <lang>'))
def when_lang(lang, template_dict):
    template_dict['lang'] = lang
