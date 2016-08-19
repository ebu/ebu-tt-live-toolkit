from pytest_bdd import when, scenarios


scenarios('features/validation/padding_data_type.feature')


@when('<tag> has a padding attribute')
def when_tag_has_padding(tag, template_dict):
    if tag == "tt:style":
        template_dict["style_padding"] = 'tts:padding="1px"'
    elif tag == "tt:region":
        template_dict["region_padding"] = 'tts:padding="1px"'
    elif tag == "tt:p":
        template_dict["p_padding"] = 'tts:padding="1px"'
    elif tag == "tt:span":
        template_dict["span_padding"] = 'tts:padding="1px"'


@when('it has a padding attribute')
def when_padding_attribute(template_dict):
    template_dict["test_padding_syntax"] = True


@when('the padding attribute has <value1>')
def when_padding_value1(value1, template_dict):
    template_dict["value1"] = value1


@when('the padding attribute has <value2>')
def when_padding_value2(value2, template_dict):
    template_dict["value2"] = value2


@when('the padding attribute has <value3>')
def when_padding_value3(value3, template_dict):
    template_dict["value3"] = value3


@when('the padding attribute has <value4>')
def when_padding_value4(value4, template_dict):
    template_dict["value4"] = value4
