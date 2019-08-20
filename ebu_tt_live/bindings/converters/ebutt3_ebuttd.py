from ebu_tt_live.bindings import tt, ttd, tt_type, d_tt_type, body_type, d_body_type, div_type, d_div_type, \
    p_type, d_p_type, span_type, d_span_type, br_type, d_br_type, d_metadata_type, d_head_type, d_style_type, \
    d_styling_type, head_type, style_type, styling, layout, d_layout_type, region_type, d_region_type, ebuttdt, StyledElementMixin
from ebu_tt_live.bindings._ebuttm import headMetadata_type, documentMetadata
import copy
import logging
from pyxb.binding.basis import NonElementContent, ElementContent
from pyxb import BIND


log = logging.getLogger(__name__)

# NOTE: Some of the code below includes handling of SMPTE time base, which was removed from version 1.0 of the specification.

class EBUTT3EBUTTDConverter(object):

    _media_clock = None
    _font_size_style_template = 'autogenFontStyle_{}_{}'
    _dataset_key_for_font_styles = 'adjusted_sizing_styles'
    _semantic_dataset = None

    def __init__(self, media_clock):
        self._media_clock = media_clock

    def _children_contain(self, container_elem, binding_type):
        element_types = [type(item.value) for item in container_elem.orderedContent() if isinstance(item, ElementContent)]
        return binding_type in element_types

    def _process_timing_type(self, timing_type, dataset):
        if timing_type is None:
            return None
        time_base = dataset['timeBase']
        if time_base == 'clock':
            # Means we need to convert to media
            return ebuttdt.FullClockTimingType(self._media_clock.get_media_time(timing_type.timedelta))
        if time_base == 'media':
            return timing_type
        if time_base == 'smpte':
            raise NotImplementedError()

    def _adjusted_font_style_map(self):
        return self._semantic_dataset.setdefault(self._dataset_key_for_font_styles, {})

    def _get_font_size_style(self, vertical, dataset, horizontal=None):
        """
        This function either points us to an already generated version of this style or creates it on demand.
        :param vertical:
        :param horizontal:
        :return:
        """
        font_style_id = self._font_size_style_template.format(horizontal, vertical)
        adjusted_font_style_map = self._adjusted_font_style_map()
        if font_style_id in adjusted_font_style_map:
            instance = adjusted_font_style_map[font_style_id]
            return instance
        elif horizontal is None:
            instance = d_style_type(
                id=font_style_id,
                fontSize=ebuttdt.PercentageFontSizeType(vertical)
            )
        else:
            instance = d_style_type(
                id=font_style_id,
                fontSize=ebuttdt.PercentageFontSizeType(horizontal, vertical)
            )

        adjusted_font_style_map[font_style_id] = instance

        return instance

    def _fix_fontsize(self, elem, celem, parent, dataset):
        """
        This function generates styles for the purpose of conversion from c,px values to percentage values.
        The fontSize attributes were removed in the initial styling copy function so here we generate new ones to serve
        our purpose best and easiest
        :param elem: the original instance
        :param celem: the converted instance
        :param parent: the parent of the original
        :param dataset: semantic dataset
        :return:
        """

        if isinstance(elem, (p_type, span_type)):
            computed_font_size = elem.computed_style.fontSize
            computed_line_height = elem.computed_style.lineHeight

            if isinstance(elem, p_type):
                # Since we eliminated all our fontSize attributes from the original styles here it is
                # as simple as computing based on the default value. p does not recurse
                default_font_size = ebuttdt.CellFontSizeType('1c')
                if default_font_size == computed_font_size:
                    return
                else:
                    relative_font_size = computed_font_size / default_font_size
                    adjusted_style = self._get_font_size_style(
                        vertical=relative_font_size.vertical,
                        dataset=dataset
                    )

            elif isinstance(elem, span_type):
                parent_computed_font_size = parent.computed_style.fontSize
                if parent_computed_font_size == computed_font_size:
                    return
                else:
                    relative_font_size = computed_font_size / parent_computed_font_size
                    adjusted_style = self._get_font_size_style(
                        vertical=relative_font_size.vertical,
                        dataset=dataset
                    )

            if isinstance(computed_line_height, ebuttdt.CellLineHeightType):
                adjusted_style.lineHeight = ebuttdt.PercentageLineHeightType(
                    computed_line_height.vertical / computed_font_size.vertical * 100
                )
            if celem.style is None:
                celem.style = [
                    adjusted_style.id
                ]
            else:
                celem.style.insert(0, adjusted_style.id)

    def _link_adjusted_fonts_styling(self, adjusted_fonts, root_element):
        if not adjusted_fonts:
            return
        if root_element.head is None:
            root_element.head = d_head_type()
        if root_element.head.styling is None:
            root_element.head.styling = d_styling_type()
        root_element.head.styling.style.extend(list(adjusted_fonts.values()))

    def convert_tt(self, tt_in, dataset):
        dataset['timeBase'] = tt_in.timeBase
        dataset['cellResolution'] = tt_in.cellResolution
        new_elem = ttd(
            head=self.convert_element(tt_in.head, dataset),
            body=self.convert_element(tt_in.body, dataset),
            timeBase='media',
            lang=tt_in.lang,
            space=tt_in.space,
            cellResolution=tt_in.cellResolution,
            _strict_keywords=False
        )
        self._link_adjusted_fonts_styling(self._adjusted_font_style_map(), new_elem)

        return new_elem

    def convert_head(self, head_in, dataset):
        new_elem = d_head_type(
        )
        head_children = self.convert_children(head_in, dataset)
        for item in head_children:
            if isinstance(item, d_styling_type):
                new_elem.styling = item
            elif isinstance(item, d_layout_type):
                new_elem.layout = item
            else:
                new_elem.append(item)

        metadata = headMetadata_type()
        metadata.documentMetadata = documentMetadata(conformsToStandard = [
            'http://www.w3.org/ns/ttml/profile/imsc1/text', 
            'urn:ebu:tt:distribution:2018-04'
        ])
        new_elem.metadata = metadata

        # We need default values here in case styling or layout is omitted from the source document.
        if not self._children_contain(new_elem, d_styling_type):
            new_elem.styling = d_styling_type.create_default_value()
        if not self._children_contain(new_elem, d_layout_type):
            log.info('converter added a default layout')
            log.info([item.value for item in new_elem.orderedContent()])
            new_elem.layout = d_layout_type.create_default_value()

        return new_elem

    def convert_layout(self, layout_in, dataset):
        new_elem = d_layout_type(
            *self.convert_children(layout_in, dataset)
        )
        # Fill in the gaps with default values
        if not self._children_contain(new_elem, d_region_type):
            log.info('converter added a default region')
            new_elem.append(d_region_type.create_default_value())
        return new_elem

    def convert_region(self, region_in, dataset):
        origin = region_in.origin
        if origin is not None:
            if isinstance(origin, ebuttdt.cellOriginType):
                origin = ebuttdt.convert_cell_region_to_percentage(origin, dataset['cellResolution'])
        extent = region_in.extent
        if extent is not None:
            if isinstance(extent, ebuttdt.cellExtentType):
                extent = ebuttdt.convert_cell_region_to_percentage(extent, dataset['cellResolution'])
        new_elem = d_region_type(
            *self.convert_children(region_in, dataset),
            id=region_in.id,
            origin=origin,
            extent=extent,
            style=region_in.style,
            displayAlign=region_in.displayAlign,
            padding=region_in.padding,
            writingMode=region_in.writingMode,
            showBackground=region_in.showBackground,
            overflow=region_in.overflow
        )
        return new_elem

    def convert_styling(self, styling_in, dataset):
        new_elem = d_styling_type(
            *self.convert_children(styling_in, dataset)
        )
        # Fill in the gaps here
        if not self._children_contain(new_elem, d_style_type):
            new_elem.append(d_style_type.create_default_value())
        return new_elem

    def convert_style(self, style_in, dataset):
        color = style_in.color
        if color is not None:
            if isinstance(color, ebuttdt.namedColorType):
                color = ebuttdt.named_color_to_rgba(color)
        backgroundColor = style_in.backgroundColor
        if backgroundColor is not None:
            if isinstance(backgroundColor, ebuttdt.namedColorType):
                backgroundColor = ebuttdt.named_color_to_rgba(backgroundColor)
        new_elem = d_style_type(
            *self.convert_children(style_in, dataset),
            id=style_in.id,
            style=style_in.style,  # there is no ordering requirement in styling so too soon to deconflict here
            direction=style_in.direction,
            fontFamily=style_in.fontFamily,
            fontSize=None,  # This will be regenerated in separate style. This is necessary due to % fontSize conversions
            lineHeight=None,  # lineHeight also receives the fontSize treatment
            textAlign=style_in.textAlign,
            color=color,
            backgroundColor=backgroundColor,
            fontStyle=style_in.fontStyle,
            fontWeight=style_in.fontWeight,
            textDecoration=style_in.textDecoration,
            unicodeBidi=style_in.unicodeBidi,
            wrapOption=style_in.wrapOption,
            padding=style_in.padding,
            linePadding=style_in.linePadding,
            _strict_keywords=False
        )
        return new_elem

    def convert_body(self, body_in, dataset):
        if len(body_in.div) == 0:
            return None
        new_elem = d_body_type(
            *self.convert_children(body_in, dataset),
            agent=body_in.agent,
            role=body_in.role
        )
        return new_elem

    def convert_div(self, div_in, dataset):
        if len(div_in.orderedContent()) == 0:
            return None
        new_elem = d_div_type(
            *self.convert_children(div_in, dataset),
            id=div_in.id,
            region=div_in.region,
            style=div_in.style,
            agent=div_in.agent
        )
        return new_elem

    def convert_p(self, p_in, dataset):
        new_elem = d_p_type(
            *self.convert_children(p_in, dataset),
            space=p_in.space,
            begin=self._process_timing_type(p_in.begin, dataset=dataset),
            end=self._process_timing_type(p_in.end, dataset=dataset),
            lang=p_in.lang,
            id=p_in.id,
            region=p_in.region,
            style=p_in.style,
            agent=p_in.agent,
            role=p_in.role
        )
        return new_elem

    def convert_span(self, span_in, dataset):
        new_elem = d_span_type(
            *self.convert_children(span_in, dataset),
            space=span_in.space,
            begin=self._process_timing_type(span_in.begin, dataset=dataset),
            end=self._process_timing_type(span_in.end, dataset=dataset),
            lang=span_in.lang,
            id=span_in.id,
            style=span_in.style,
            agent=span_in.agent,
            role=span_in.role
        )
        return new_elem

    def convert_br(self, br_in, dataset):
        return d_br_type()

    def map_type(self, in_element):
        if isinstance(in_element, tt_type):
            return self.convert_tt
        elif isinstance(in_element, body_type):
            return self.convert_body
        elif isinstance(in_element, div_type):
            return self.convert_div
        elif isinstance(in_element, p_type):
            return self.convert_p
        elif isinstance(in_element, span_type):
            return self.convert_span
        elif isinstance(in_element, br_type):
            return self.convert_br
        elif isinstance(in_element, head_type):
            return self.convert_head
        elif isinstance(in_element, layout):
            return self.convert_layout
        elif isinstance(in_element, region_type):
            return self.convert_region
        elif isinstance(in_element, styling):
            return self.convert_styling
        elif isinstance(in_element, style_type):
            return self.convert_style
        else:
            return self.convert_unknown

    def convert_unknown(self, element, dataset):
        return None

    def convert_children(self, element, dataset):
        """
        Recursive step
        :param element:
        :param dataset:
        :return:
        """
        output = []

        children = element.orderedContent()

        for item in children:
            if isinstance(item, NonElementContent):
                output.append(copy.deepcopy(item.value))
            elif isinstance(item, ElementContent):
                conv_elem = self.convert_element(item.value, dataset)

                if conv_elem is not None:
                    if isinstance(item.value, StyledElementMixin) and not isinstance(item.value, style_type):
                        self._fix_fontsize(
                            elem=item.value,
                            celem=conv_elem,
                            parent=element,
                            dataset=dataset
                        )
                    output.append(conv_elem)
            else:
                raise Exception('Can this even happen!??!?!?!')
        return output

    def convert_element(self, element, dataset):
        converter = self.map_type(element)
        return converter(element, dataset)

    def convert_document(self, root_element, dataset=None):
        if dataset is None:
            self._semantic_dataset = {}
        else:
            self._semantic_dataset = dataset
        converted_bindings = self.convert_element(root_element, self._semantic_dataset)

        return converted_bindings
