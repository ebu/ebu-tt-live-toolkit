from pytest_bdd import when, scenarios


scenarios('features/validation/facet.feature')


@when('it has facet1 applied to element <parent1>')
def when_facet1_to_parent1(parent1, template_dict, test_context):
    test_context['parent1'] = parent1
    key = parent1 + "_facets"
    if key in template_dict:
        template_dict[key] += "<ebuttm:facet"
    else:
        template_dict[key] = "<ebuttm:facet"


@when('facet1 has attribute <link1>')
def when_facet1_link1(link1, template_dict, test_context):
    key = test_context['parent1'] + "_facets"
    if link1:
        template_dict[key] += ' link="{}"'.format(link1)


@when('facet1 contains string <term1>')
def when_facet1_term1(term1, template_dict, test_context):
    key = test_context['parent1'] + "_facets"
    template_dict[key] += '>{}</ebuttm:facet>'.format(term1)


@when('it has facet2 applied to element <parent2>')
def when_facet2_to_parent2(parent2, template_dict, test_context):
    test_context['parent2'] = parent2
    key = parent2 + "_facets"
    if key in template_dict:
        template_dict[key] += "<ebuttm:facet"
    else:
        template_dict[key] = "<ebuttm:facet"


@when('facet2 has attribute <link2>')
def when_facet2_link2(link2, template_dict, test_context):
    key = test_context['parent2'] + "_facets"
    if link2:
        template_dict[key] += ' link="{}"'.format(link2)


@when('facet2 contains string <term2>')
def when_facet2_term2(term2, template_dict, test_context):
    key = test_context['parent2'] + "_facets"
    template_dict[key] += '>{}</ebuttm:facet>'.format(term2)


@when('it has element facet1 with attribute <expresses1>')
def when_facet1_expresses1(expresses1, template_dict):
    value = '<ebuttm:facet'
    if expresses1:
        value += ' expresses="{}">test_facet</ebuttm:facet>'.format(expresses1)
    else:
        value += '>test_facet</ebuttm:facet>'
    template_dict['body_facets'] = value


@when('it has element facet2 with attribute <expresses2>')
def when_facet2_expresses2(expresses2, template_dict):
    value = '<ebuttm:facet'
    if expresses2:
        value += ' expresses="{}">test_facet</ebuttm:facet>'.format(expresses2)
    else:
        value += '>test_facet</ebuttm:facet>'
    template_dict['div_facets'] = value


@when('it has element facet3 with attribute <expresses3>')
def when_facet3_expresses3(expresses3, template_dict):
    value = '<ebuttm:facet'
    if expresses3:
        value += ' expresses="{}">test_facet</ebuttm:facet>'.format(expresses3)
    else:
        value += '>test_facet</ebuttm:facet>'
    template_dict['p_facets'] = value


@when('documentFacet has atribute <summary>')
def when_documentFacet_summary(summary, template_dict):
    template_dict['document_facets'] = '<ebuttm:documentFacet summary="{}">test_facet</ebuttm:documentFacet>'.format(summary)
