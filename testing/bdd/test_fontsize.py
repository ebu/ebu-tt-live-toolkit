from pytest_bdd import when, scenarios, then

scenarios('features/styles/fontSize.feature')


@when('it has a cell resolution of <cell_resolution>')
def when_cell_resolution(template_dict, cell_resolution):
    template_dict['cell_resolution'] = cell_resolution


@when('it has extent of <extent>')
def when_extent(template_dict, extent):
    template_dict['extent'] = extent


@when('it contains style S1 with <style_attribute> value <S1_value>')
def when_s1_attr_value(template_dict, style_attribute, S1_value):
    template_dict['S1_value'] = S1_value
    template_dict['style_attribute'] = style_attribute


@when('it contains style S2 with <style_attribute> value <S2_value>')
def when_s2_attr_value(template_dict, style_attribute, S2_value):
    template_dict['S2_value'] = S2_value
    template_dict['style_attribute'] = style_attribute


@when('it contains style S3 with <style_attribute> value <S3_value>')
def when_s3_attr_value(template_dict, style_attribute, S3_value):
    template_dict['S3_value'] = S3_value
    template_dict['style_attribute'] = style_attribute


@when('it contains style S4 with <style_attribute> value <S4_value>')
def when_s4_attr_value(template_dict, style_attribute, S4_value):
    template_dict['S4_value'] = S4_value
    template_dict['style_attribute'] = style_attribute
