from pytest_bdd import when, scenarios, parsers
from pytest import fixture


scenarios('features/validation/xml_lang_attribute.feature')


@fixture
def lang():
    return None

@when(parsers.parse('it has xml:lang attribute {lang}'))
@when(parsers.parse('it has xml:lang attribute'))
def when_lang(lang, template_dict):
    template_dict['lang'] = lang
