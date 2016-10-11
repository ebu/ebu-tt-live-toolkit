from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings import style_type, region_type
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType
from pytest_bdd import scenarios, when, then

scenarios('features/segmentation/splitting_documents.feature')


def assert_raises(exc_class, callable, *args, **kwargs):
    try:
        callable(*args, **kwargs)
    except Exception as exc:
        assert isinstance(exc, exc_class)


@when('it has sequenceIdentifier <sequence_identifier>')
def when_sequence_identifier(template_dict, sequence_identifier):
    template_dict['sequence_identifier'] = sequence_identifier


@when('it has sequenceNumber <sequence_number>')
def when_sequence_number(template_dict, sequence_number):
    template_dict['sequence_number'] = sequence_number


@when('it has body from <body_begin> to <body_end>')
def when_body_times(template_dict, body_begin, body_end):
    template_dict['body_begin'] = body_begin
    template_dict['body_end'] = body_end


@when('it has span1 from <span1_begin> to <span1_end>')
def when_span1_times(template_dict, span1_begin, span1_end):
    template_dict['span1_begin'] = span1_begin
    template_dict['span1_end'] = span1_end


@when('it has span2 from <span2_begin> to <span2_end>')
def when_span2_times(template_dict, span2_begin, span2_end):
    template_dict['span2_begin'] = span2_begin
    template_dict['span2_end'] = span2_end


@when('it has span3 from <span3_begin> to <span3_end>')
def when_span3_times(template_dict, span3_begin, span3_end):
    template_dict['span3_begin'] = span3_begin
    template_dict['span3_end'] = span3_end


@when('the range from <range_from> to <range_to> is requested')
def when_range_requested(template_file, test_context, template_dict, range_from, range_to):
    xml_file = template_file.render(template_dict)
    document = EBUTT3Document.create_from_xml(xml_file)
    fragment = document.extract_segment(
        FullClockTimingType(range_from).timedelta,
        FullClockTimingType(range_to).timedelta
    )
    test_context['fragment'] = fragment


@then('the fragment contains body from <frag_body_begin> to <frag_body_end>')
def then_fragment_body_times(test_context, frag_body_begin, frag_body_end):

    assert test_context['fragment'].binding.body.computed_begin_time == FullClockTimingType(frag_body_begin).timedelta
    if frag_body_end == 'undefined':
        assert test_context['fragment'].binding.body.computed_end_time is None
    else:
        assert test_context['fragment'].binding.body.computed_end_time == FullClockTimingType(frag_body_end).timedelta


@then('the fragment contains span1 from <frag_span1_begin> to <frag_span1_end>')
def then_fragment_span1_times(test_context, frag_span1_begin, frag_span1_end):
    if frag_span1_begin == 'deleted':
        assert_raises(LookupError, test_context['fragment'].get_element_by_id, 'span1')
    else:
        assert test_context['fragment'].get_element_by_id('span1').computed_begin_time == FullClockTimingType(
            frag_span1_begin).timedelta
        if frag_span1_end == 'undefined':
            assert test_context['fragment'].get_element_by_id('span1').computed_end_time is None
        else:
            assert test_context['fragment'].get_element_by_id('span1').computed_end_time == FullClockTimingType(
                frag_span1_end).timedelta


@then('the fragment contains span2 from <frag_span2_begin> to <frag_span2_end>')
def then_fragment_span2_times(test_context, frag_span2_begin, frag_span2_end):
    if frag_span2_begin == 'deleted':
        assert_raises(LookupError, test_context['fragment'].get_element_by_id, 'span2')
    else:
        assert test_context['fragment'].get_element_by_id('span2').computed_begin_time == FullClockTimingType(
            frag_span2_begin).timedelta
        if frag_span2_end == 'undefined':
            assert test_context['fragment'].get_element_by_id('span2').computed_end_time is None
        else:
            assert test_context['fragment'].get_element_by_id('span2').computed_end_time == FullClockTimingType(
                frag_span2_end).timedelta


@then('the fragment contains span3 from <frag_span3_begin> to <frag_span3_end>')
def then_fragment_span3_times(test_context, frag_span3_begin, frag_span3_end):
    if frag_span3_begin == 'deleted':
        assert_raises(LookupError, test_context['fragment'].get_element_by_id, 'span3')
    else:
        assert test_context['fragment'].get_element_by_id('span3').computed_begin_time == FullClockTimingType(
            frag_span3_begin).timedelta
        if frag_span3_end == 'undefined':
            assert test_context['fragment'].get_element_by_id('span3').computed_end_time is None
        else:
            assert test_context['fragment'].get_element_by_id('span3').computed_end_time == FullClockTimingType(
                frag_span3_end).timedelta


@then('the fragment only contains styles <frag_styles>')
def then_fragment_styles_present(test_context, frag_styles):
    fragment = test_context['fragment']
    styling = fragment.binding.head.styling
    styles_present = []
    if frag_styles:
        styles_required = map(lambda item: item.strip(), frag_styles.split(','))
    else:
        styles_required = []

    if styling is not None:
        for item in styling.style:
            styles_present.append(item.id)

    assert set(styles_present) == set(styles_required)


@then('the fragment only contains regions <frag_regions>')
def then_fragment_regions_present(test_context, frag_regions):
    fragment = test_context['fragment']
    layout = fragment.binding.head.layout
    regions_present = []
    if frag_regions:
        regions_required = map(lambda item: item.strip(), frag_regions.split(','))
    else:
        regions_required = []

    if layout is not None:
        for item in layout.region:
            regions_present.append(item.id)

    assert set(regions_present) == set(regions_required)
