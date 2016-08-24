from pytest_bdd import when, scenarios


scenarios('features/validation/3350-value-types.feature')


@when('it has tts:color attribute with value <color>')
def when_color(color, template_dict):
    template_dict['color'] = color


@when('it has extent attribute with value <extent>')
def when_extent(extent, template_dict):
    template_dict['extent'] = extent


@when('it has tts:fontSize attribute with value <font_size>')
def when_font_size(font_size, template_dict):
    template_dict['font_size'] = font_size


@when('it has linePadding attribute with value <line_padding>')
def when_line_padding(line_padding, template_dict):
    template_dict['line_padding'] = line_padding


@when('it has lineHeight attribute with value <line_height>')
def when_line_height(line_height, template_dict):
    template_dict['line_height'] = line_height


@when('it has origin attribute with value <origin>')
def when_origin(origin, template_dict):
    template_dict['origin'] = origin
