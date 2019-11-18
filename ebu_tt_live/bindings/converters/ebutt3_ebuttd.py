from ebu_tt_live.bindings import ttd, tt_type, body_type, d_body_type, \
    div_type, d_div_type, p_type, d_p_type, span_type, d_span_type, \
    br_type, d_br_type, d_head_type, d_style_type, \
    d_styling_type, head_type, style_type, styling, layout, d_layout_type, \
    region_type, d_region_type, ebuttdt, StyledElementMixin
from ebu_tt_live.bindings._ebuttm import headMetadata_type, documentMetadata
from ebu_tt_live.bindings._ebuttdt import PercentageExtentType, \
    PercentageOriginType, PercentageLineHeightType, \
    CellFontSizeType, PercentageFontSizeType
from ebu_tt_live.project import description, name, version
from ebu_tt_live.errors import InvalidRegionExtentType, \
    InvalidRegionOriginType, \
    SemanticValidationError
from ebu_tt_live.strings import ERR_REGION_ORIGIN_TYPE, \
    ERR_REGION_EXTENT_TYPE, \
    ERR_SEMANTIC_VALIDATION_EXPECTED
import copy
import logging
from pyxb.binding.basis import NonElementContent, ElementContent

log = logging.getLogger(__name__)


DEFAULT_CELL_FONT_SIZE = CellFontSizeType('1c')


class EBUTT3EBUTTDConverter(object):

    _media_clock = None
    _font_size_style_template = 'autogenFontStyle_{}_{}_{}'
    _dataset_key_for_font_styles = 'adjusted_sizing_styles'
    _semantic_dataset = None

    def __init__(self, media_clock, calculate_active_area=False):
        self._media_clock = media_clock
        self._do_calculate_active_area = calculate_active_area

    def _children_contain(self, container_elem, binding_type):
        element_types = [
            type(item.value) for item in container_elem.orderedContent()
            if isinstance(item, ElementContent)]
        return binding_type in element_types

    def _process_timing_type(self, timing_type, dataset):
        if timing_type is None:
            return None
        time_base = dataset['timeBase']
        if time_base == 'clock':
            # Means we need to convert to media
            return ebuttdt.FullClockTimingType(
                self._media_clock.get_media_time(timing_type.timedelta))
        if time_base == 'media':
            return timing_type
        if time_base == 'smpte':
            raise NotImplementedError()

    def _process_timing_from_timedelta(self, timing_type):
        if timing_type is None:
            return None
        return ebuttdt.FullClockTimingType.from_timedelta(timing_type)

    def _adjusted_font_style_map(self):
        return self._semantic_dataset.setdefault(
            self._dataset_key_for_font_styles, {})

    def _get_font_size_style(
            self,
            vertical,
            dataset,
            horizontal=None,
            line_height=None):
        """
        Get a style with a font size, even if one doesn't already exist.

        This function either points us to an already generated version of this
        style or creates it on demand.
        :param vertical:
        :param horizontal:
        :param line_height:
        :return:
        """
        adjusted_line_height = 'n'

        if isinstance(line_height, PercentageLineHeightType):
            adjusted_line_height = line_height.vertical

        font_style_id = \
            self._font_size_style_template.format(
                horizontal, vertical, adjusted_line_height)
        adjusted_font_style_map = self._adjusted_font_style_map()
        if font_style_id in adjusted_font_style_map:
            instance = adjusted_font_style_map[font_style_id]
            return instance
        else:
            font_size = None
            if vertical is not None:
                if horizontal is None:
                    font_size = ebuttdt.PercentageFontSizeType(
                        vertical)
                else:
                    font_size = ebuttdt.PercentageFontSizeType(
                        horizontal, vertical)

            instance = d_style_type(
                id=font_style_id,
                fontSize=font_size,
                lineHeight=line_height
            )

            adjusted_font_style_map[font_style_id] = instance

            return instance

    def _fix_fontsize(self, elem, celem, parent, dataset):
        """
        Generate styles with percent unit font size values.

        This function generates styles for the purpose of conversion from c,px
        values to percentage values.
        The fontSize attributes were removed in the initial styling copy
        function so here we generate new ones to serve
        our purpose best and easiest
        :param elem: the original instance
        :param celem: the converted instance
        :param parent: the parent of the original
        :param dataset: semantic dataset
        :return:
        """
        if isinstance(elem, (body_type, div_type, p_type, span_type)):
            if elem.computed_style is None:
                raise SemanticValidationError(ERR_SEMANTIC_VALIDATION_EXPECTED)
            specified_font_size = elem.specified_style.fontSize
            specified_line_height = elem.specified_style.lineHeight

            if specified_font_size is None and specified_line_height is None:
                # Waste no more time here
                return

            computed_font_size = elem.computed_style.fontSize
            computed_line_height = elem.computed_style.lineHeight

            required_font_size = None
            required_line_height = None

            if specified_font_size is not None:
                # Fallback for body element fontSize is the default value
                # because EBU-TT Live does not allow fontSize on region
                # elements.
                if isinstance(elem, body_type) and computed_font_size is None:
                    computed_font_size = DEFAULT_CELL_FONT_SIZE

                if isinstance(elem, (body_type, div_type, p_type)):
                    # Since we eliminated all our fontSize attributes from the
                    # original styles here it is as simple as computing based
                    # on the default value.
                    if isinstance(computed_font_size,
                                  CellFontSizeType) \
                       and computed_font_size != DEFAULT_CELL_FONT_SIZE:
                        required_font_size = \
                            computed_font_size / DEFAULT_CELL_FONT_SIZE
                    elif isinstance(computed_font_size,
                                    PercentageFontSizeType):
                        required_font_size = computed_font_size

                elif isinstance(elem, span_type):
                    parent_computed_font_size = parent.computed_style.fontSize
                    if parent_computed_font_size != computed_font_size:
                        required_font_size = \
                            computed_font_size / parent_computed_font_size

            if specified_line_height is not None:
                if isinstance(
                        computed_line_height, ebuttdt.CellLineHeightType):
                    required_line_height = ebuttdt.PercentageLineHeightType(
                        '{0:g}%'.format(
                            round(computed_line_height.vertical /
                                  computed_font_size.vertical * 100, 2))
                    )
                elif isinstance(computed_line_height,
                                ebuttdt.PercentageLineHeightType):
                    required_line_height = computed_line_height
                elif isinstance(computed_line_height,
                                ebuttdt.PixelLineHeightType):
                    required_line_height = ebuttdt.PercentageLineHeightType(
                        '{0:g}%'.format(round((computed_line_height.vertical /
                                               dataset['extent'].vertical) /
                                              computed_font_size.vertical *
                                              100, 2))
                    )
                elif computed_line_height == 'normal':
                    required_line_height = computed_line_height

            if required_font_size is not None or \
               required_line_height is not None:
                # Get or make a style and use it
                adjusted_style = self._get_font_size_style(
                    vertical=required_font_size.vertical
                    if required_font_size is not None else None,
                    horizontal=None,  # H component prohibited in EBU-TT-D
                    line_height=required_line_height
                    if required_line_height is not None else None,
                    dataset=dataset
                )

                if celem.style is None:
                    celem.style = [
                        adjusted_style.id
                    ]
                else:
                    celem.style.insert(0, adjusted_style.id)
        else:
            log.warn(
                'EBUTT3EBUTTDConverter._fix_fontsize() called on unexpected element {}'.format(type(elem).__name__))  # noqa: E501

    def _link_adjusted_fonts_styling(self, adjusted_fonts, root_element):
        if not adjusted_fonts:
            return
        if root_element.head is None:
            root_element.head = d_head_type()
        if root_element.head.styling is None:
            root_element.head.styling = d_styling_type()
        root_element.head.styling.style.extend(list(adjusted_fonts.values()))

    def _calculate_active_area(self, document, dataset):
        if 'activated_region_ids' not in dataset:
            log.error('No activated_region_ids set in dataset')
            return

        activated_region_ids = dataset['activated_region_ids']
        if len('activated_region_ids') == 0:
            log.warn('No regions activated in document')

            # Check for default region condition, which is a special case
            # that only occurs when no regions are defined at all in the
            # document. This is actually illegal in EBU-TT-D and should
            # never occur
            if document.head.layout is None \
                    or len(document.head.layout.region) == 0:
                log.warn('Default region used - not legal in EBU-TT-D')
                document.activeArea = '0% 0% 100% 100%'
            else:
                log.warn('No regions referenced: not adding activeArea.')
        elif document.head.layout is not None:
            left = top = right = bottom = None
            region_found = False

            for region in document.head.layout.region:
                if region.id in activated_region_ids:
                    region_l, region_t, region_r, region_b = \
                        self._decode_origin_and_extent(
                            region.origin, region.extent)
                    if not region_found:
                        left = region_l
                        right = region_r
                        top = region_t
                        bottom = region_b

                        region_found = True
                    else:
                        if region_l < left:
                            left = region_l
                        if region_r > right:
                            right = region_r
                        if region_t < top:
                            top = region_t
                        if region_b > bottom:
                            bottom = region_b

            if region_found:
                document.activeArea = '{}% {}% {}% {}%'.format(
                    left, top, right - left, bottom - top
                )
            else:
                log.warn('None of the active regions found')
        else:
            log.error(
                'EBU-TT-D Document refers to regions but has no layout')

    def _decode_origin_and_extent(self, origin, extent):
        if not isinstance(origin, PercentageOriginType):
            raise InvalidRegionOriginType(ERR_REGION_ORIGIN_TYPE)
        if not isinstance(extent, PercentageExtentType):
            raise InvalidRegionExtentType(ERR_REGION_EXTENT_TYPE)

        origin_x = origin.horizontal
        origin_y = origin.vertical
        width = extent.horizontal
        height = extent.vertical

        return origin_x, origin_y, origin_x + width, origin_y + height

    def convert_tt(self, tt_in, dataset):
        dataset['timeBase'] = tt_in.timeBase
        dataset['cellResolution'] = tt_in.cellResolution
        dataset['extent'] = tt_in.extent
        dataset['activated_region_ids'] = set()
        new_elem = ttd(
            head=self.convert_element(tt_in.head, dataset),
            body=self.convert_element(tt_in.body, dataset),
            timeBase='media',
            lang=tt_in.lang,
            space=tt_in.space,
            cellResolution=tt_in.cellResolution,
            activeArea=tt_in.activeArea,
            _strict_keywords=False
        )
        self._fix_fontsize(tt_in.body, new_elem.body, tt_in, dataset)
        self._link_adjusted_fonts_styling(
            self._adjusted_font_style_map(),
            new_elem)
        if self._do_calculate_active_area:
            self._calculate_active_area(new_elem, dataset)

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
        metadata.documentMetadata = documentMetadata(conformsToStandard=[
            'http://www.w3.org/ns/ttml/profile/imsc1/text',
            'urn:ebu:tt:distribution:2018-04'
            ],
            documentOriginatingSystem=name + '.' + version +
            '.' + type(self).__name__
            )
        new_elem.metadata = metadata

        # We need default values here in case styling or layout is omitted
        # from the source document.
        if not self._children_contain(new_elem, d_styling_type):
            new_elem.styling = d_styling_type.create_default_value()
        if not self._children_contain(new_elem, d_layout_type):
            log.info('converter added a default layout')
            log.info([item.value for item in new_elem.orderedContent()])
            new_elem.layout = d_layout_type.create_default_value()

        return new_elem

    def convert_layout(self, layout_in, dataset):
        new_elem = d_layout_type(
            region=[self.convert_element(r, dataset) for r in layout_in.region]
        )

        # Fill in the gaps with default values
        if len(new_elem.region) == 0:
            log.info('converter added a default region')
            new_elem.append(d_region_type.create_default_value())

        return new_elem

    def convert_region(self, region_in, dataset):
        origin = region_in.origin
        if origin is not None:
            if isinstance(origin, ebuttdt.cellOriginType):
                origin = ebuttdt.convert_cell_region_to_percentage(
                    origin, dataset['cellResolution'])
            elif isinstance(origin, ebuttdt.pixelOriginType):
                origin = ebuttdt.convert_pixel_region_to_percentage(
                    origin, dataset['extent'])
        extent = region_in.extent
        if extent is not None:
            if isinstance(extent, ebuttdt.cellExtentType):
                extent = ebuttdt.convert_cell_region_to_percentage(
                    extent, dataset['cellResolution'])
            elif isinstance(extent, ebuttdt.pixelExtentType):
                extent = ebuttdt.convert_pixel_region_to_percentage(
                    extent, dataset['extent'])

        if region_in.padding is None:
            region_validated_styles = \
                [style for style in
                 region_in.validated_styles
                 if style.id in region_in.style]
            for region_style in region_validated_styles:
                parent_styles = region_style.ordered_styles(dataset)
                if parent_styles:
                    for parent_style in parent_styles:
                        if parent_style.padding:
                            region_in.padding = parent_style.padding
                else:
                    if region_style.padding:
                        region_in.padding = region_style.padding

        new_elem = d_region_type(
            *self.convert_children(region_in, dataset),
            id=region_in.id,
            origin=PercentageOriginType(origin),
            extent=PercentageExtentType(extent),
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
        ordered_styles = style_in.ordered_styles(dataset)
        computed_style = style_type(id=style_in.id)
        for s in ordered_styles:
            computed_style.add(s)
        color = computed_style.color
        if color is not None:
            if isinstance(color, ebuttdt.namedColorType):
                color = ebuttdt.named_color_to_rgba(color)
        backgroundColor = computed_style.backgroundColor
        if backgroundColor is not None:
            if isinstance(backgroundColor, ebuttdt.namedColorType):
                backgroundColor = ebuttdt.named_color_to_rgba(backgroundColor)
        new_elem = d_style_type(
            *self.convert_children(computed_style, dataset),
            id=computed_style.id,
            style=computed_style.style,  # there is no ordering requirement in
                                         # styling so too soon to deconflict
                                         # here
            direction=computed_style.direction,
            fontFamily=computed_style.fontFamily,
            fontSize=None,  # This will be regenerated in separate style.
                            # This is necessary due to % fontSize conversions
            lineHeight=None,  # lineHeight also receives the fontSize treatment
            textAlign=computed_style.textAlign,
            color=color,
            backgroundColor=backgroundColor,
            fontStyle=computed_style.fontStyle,
            fontWeight=computed_style.fontWeight,
            textDecoration=computed_style.textDecoration,
            unicodeBidi=computed_style.unicodeBidi,
            wrapOption=computed_style.wrapOption,
            padding=computed_style.padding,
            linePadding=computed_style.linePadding,
            fillLineGap=computed_style.fillLineGap,
            _strict_keywords=False
        )

        return new_elem

    def convert_body(self, body_in, dataset):
        new_div_list = []
        for div in body_in.div:
            new_div = self.convert_element(div, dataset)
            if new_div is not None:
                self._fix_fontsize(
                    elem=div,
                    celem=new_div,
                    parent=body_in,
                    dataset=dataset
                )
                new_div_list.append(new_div)

        new_metadata = self.convert_element(body_in.metadata, dataset)

        if len(new_div_list) == 0 and new_metadata is None:
            log.warn('Removing an empty body element')
            return None

        new_elem = d_body_type(
            div=new_div_list,
            metadata=new_metadata,
            agent=body_in.agent,
            role=body_in.role,
            style=body_in.style
        )

        return new_elem

    def convert_div(self, div_in, dataset):
        new_p_list = []
        for p in div_in.p:
            new_p = self.convert_element(p, dataset)
            if new_p is not None:
                self._fix_fontsize(
                    elem=p,
                    celem=new_p,
                    parent=div_in,
                    dataset=dataset
                )
                new_p_list.append(new_p)

        new_metadata = self.convert_element(div_in.metadata, dataset)

        if len(new_p_list) == 0 and new_metadata is None:
            log.warn('Removing an empty div element')
            return None

        new_elem = d_div_type(
            p=new_p_list,
            metadata=new_metadata,
            id=div_in.id,
            region=div_in.region,
            style=div_in.style,
            agent=div_in.agent
        )

        if new_elem.region is not None:
            dataset['activated_region_ids'].add(new_elem.region)

        return new_elem

    def convert_p(self, p_in, dataset):
        new_elem = d_p_type(
            *self.convert_children(p_in, dataset),
            space=p_in.space,
            begin=None if p_in.is_timed_leaf() is False else
            self._process_timing_from_timedelta(p_in.computed_begin_time),
            end=None if p_in.is_timed_leaf() is False else
            self._process_timing_from_timedelta(p_in.computed_end_time),
            lang=p_in.lang,
            id=p_in.id,
            region=p_in.region,
            style=p_in.style,
            agent=p_in.agent,
            role=p_in.role
        )
        if new_elem.region is not None:
            dataset['activated_region_ids'].add(new_elem.region)
        return new_elem

    def convert_span(self, span_in, dataset):
        new_elem = d_span_type(
            *self.convert_children(span_in, dataset),
            space=span_in.space,
            begin=self._process_timing_from_timedelta(
                span_in.computed_begin_time),
            end=self._process_timing_from_timedelta(span_in.computed_end_time),
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
                    if isinstance(item.value, StyledElementMixin) and \
                       not isinstance(item.value, style_type):
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
        converted_bindings = \
            self.convert_element(root_element, self._semantic_dataset)

        return converted_bindings
