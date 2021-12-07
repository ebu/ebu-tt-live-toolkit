from pytest_bdd import when, scenarios, parsers
from pytest import fixture


scenarios('features/validation/padding_data_type.feature')


@when(parsers.parse('{tag} has a padding attribute'))
def when_tag_has_padding(tag, template_dict):
    if tag == "tt:style":
        template_dict["style_padding"] = 'tts:padding="1px"'
    elif tag == "tt:region":
        template_dict["region_padding"] = 'tts:padding="1px"'
    elif tag == "tt:p":
        template_dict["p_padding"] = 'tts:padding="1px"'
    elif tag == "tt:span":
        template_dict["span_padding"] = 'tts:padding="1px"'


@when(parsers.parse('it has a padding attribute'))
def when_padding_attribute(template_dict):
    template_dict["test_padding_syntax"] = True


@fixture
def value1():
    return ''

@when(parsers.parse('padding attribute component 1 is {value1}'))
@when(parsers.parse('padding attribute component 1 is'))
def when_padding_value1(value1, template_dict):
    template_dict["value1"] = value1


@fixture
def value2():
    return ''

@when(parsers.parse('padding attribute component 2 is {value2}'))
@when(parsers.parse('padding attribute component 2 is'))
def when_padding_value2(value2, template_dict):
    template_dict["value2"] = value2


@fixture
def value3():
    return ''

@when(parsers.parse('padding attribute component 3 is {value3}'))
@when(parsers.parse('padding attribute component 3 is'))
def when_padding_value3(value3, template_dict):
    template_dict["value3"] = value3


@fixture
def value4():
    return ''

@when(parsers.parse('padding attribute component 4 is {value4}'))
@when(parsers.parse('padding attribute component 4 is'))
def when_padding_value4(value4, template_dict):
    template_dict["value4"] = value4
