# -*- coding: utf-8 -*-
from .raw import *
from . import raw

# Let's import customizations
from . import _ebuttdt as ebuttdt
from . import _ebuttm as ebuttm
from . import _ebuttlm as ebuttlm
from . import _ebuttp as ebuttp
from . import _ebutts as ebutts
from . import _ttm as ttm
from . import _ttp as ttp
from . import _tts as tts
from .pyxb_utils import xml_parsing_context, get_xml_parsing_context
from .validation.base import SemanticDocumentMixin, SemanticValidationMixin, IDMixin
from ebu_tt_live.bindings.validation.presentation import SizingValidationMixin, StyledElementMixin, RegionedElementMixin
from ebu_tt_live.bindings.validation.timing import TimingValidationMixin, BodyTimingValidationMixin
from ebu_tt_live.bindings.validation.content import SubtitleContentContainer, ContentContainerMixin
from .validation.validator import SemanticValidator
from ebu_tt_live.errors import SemanticValidationError, OutsideSegmentError, RegionExtendingOutsideDocumentError, InvalidRegionOriginType, InvalidRegionExtentType
from ebu_tt_live.strings import ERR_SEMANTIC_VALIDATION_MISSING_ATTRIBUTES, \
    ERR_SEMANTIC_VALIDATION_INVALID_ATTRIBUTES, ERR_SEMANTIC_STYLE_CIRCLE, ERR_SEMANTIC_STYLE_MISSING, \
    ERR_SEMANTIC_ELEMENT_BY_ID_MISSING, ERR_SEMANTIC_VALIDATION_EXPECTED
from pyxb.exceptions_ import SimpleTypeValueError
from pyxb.utils.domutils import BindingDOMSupport
from pyxb.binding.basis import ElementContent, NonElementContent
from datetime import timedelta
import threading
import copy
import logging


log = logging.getLogger(__name__)

# This mapping controls the namespace aliases used in the generated XML content.
# Not having these results in default mapping to ns1 ns2 ns3..., which should not be a problem
# but many downstream tools may have terrible custom XML parsing typically by using regular expressions
# to find `tt:head` for instance. So controlling these to match the spec namespaces helps interoperability.
namespace_prefix_map = {
    'tt': raw.Namespace,
    'ebuttdt': ebuttdt.Namespace,
    'ttp': ttp.Namespace,
    'tts': tts.Namespace,
    'ttm': ttm.Namespace,
    'ebuttm': ebuttm.Namespace,
    'ebutts': ebutts.Namespace,
    'ebuttp': ebuttp.Namespace,
    'ebuttlm': ebuttlm.Namespace
}


def CreateFromDocument(*args, **kwargs):
    """
    Resetting the parsing context on start
    :return:
    """
    with xml_parsing_context():
        result = raw.CreateFromDocument(*args, **kwargs)
    return result


def CreateFromDOM(*args, **kwargs):
    """
    Resetting the parsing context on start
    :return:
    """
    with xml_parsing_context():
        result = raw.CreateFromDOM(*args, **kwargs)
    return result


# Customizing validation mixins before application
# ================================================


class style_type(StyledElementMixin, IDMixin, SizingValidationMixin, SemanticValidationMixin, raw.style):

    # This helps us detecting infinite loops.
    _styling_lock = None
    # ordered styles cached
    _ordered_styles = None
    # This mapping is meant to simplify things. In case anything needs special calculation that value should be
    # lifted out to its own function.
    _simple_attr_defaults = {
        'backgroundColor': 'transparent',
        'padding': '0px',
        'unicodeBidi': 'normal'
    }
    _inherited_attr_defaults = {
        'color': None,  # See: https://www.w3.org/TR/ttaf1-dfxp/#style-attribute-color
        'direction': 'ltr',
        'fontFamily': 'default',
        'fontStyle': 'normal',
        'fontWeight': 'normal',
        'linePadding': '0c',
        'multiRowAlign': 'auto',
        'textAlign': 'start',
        'textDecoration': 'none',
        'wrapOption': 'wrap'
    }
    _default_attrs = None

    def check_equal(self, other):
        return (self.backgroundColor == other.backgroundColor and
            self.padding == other.padding and
            self.unicodeBidi == other.unicodeBidi and
            self.color == other.color and
            self.direction == other.direction and
            self.fontFamily == other.fontFamily and
            self.fontStyle == other.fontStyle and
            self.fontWeight == other.fontWeight and
            self.linePadding == other.linePadding and
            self.multiRowAlign == other.multiRowAlign and
            self.textAlign == other.textAlign and
            self.textDecoration == other.textDecoration and
            self.fontSize == other.fontSize and
            self.lineHeight == other.lineHeight and
            self.wrapOption == other.wrapOption)
            

    def __repr__(self):
        return '<style ID: {id} at {addr}>'.format(
            id=self.id,
            addr=hex(id(self))
        )

    def _semantic_copy(self, dataset):
        copied_style = style_type(
            id=self.id,
            # there is no ordering requirement in styling so too soon to deconflict here
            style=self.style,
            direction=self.direction,
            fontFamily=self.fontFamily,
            fontSize=self.fontSize,
            lineHeight=self.lineHeight,
            textAlign=self.textAlign,
            color=self.color,
            backgroundColor=self.backgroundColor,
            fontStyle=self.fontStyle,
            fontWeight=self.fontWeight,
            textDecoration=self.textDecoration,
            unicodeBidi=self.unicodeBidi,
            wrapOption=self.wrapOption,
            padding=self.padding,
            linePadding=self.linePadding,
            _strict_keywords=False
        )
        return copied_style

    @property
    def validated_styles(self):
        # The style element itself is not meant to implement this.
        raise NotImplementedError()

    def ordered_styles(self, dataset):
        """
        This function figures out the chain of styles.
        WARNING: Do not call this before the semantic validation of tt/head/styling is finished. Otherwise your style
        may not have been found yet!
        :param dataset: Semantic dataset
        :return: a list of styles applicable in order
        """

        if self._styling_lock.locked():
            raise SemanticValidationError(ERR_SEMANTIC_STYLE_CIRCLE.format(
                style=self.id
            ))

        with self._styling_lock:
            if self._ordered_styles is not None:
                return self._ordered_styles
            ordered_styles = [self]
            if self.style is not None:
                for style_id in self.style[::-1]: # Reverse style references: last reference should take precedence
                    try:
                        style_elem = dataset['tt_element'].get_element_by_id(
                            elem_id=style_id, elem_type=style_type)
                        cascading_styles = style_elem.ordered_styles(
                            dataset=dataset)
                        for style_elem in cascading_styles:
                            if style_elem in ordered_styles:
                                continue
                            ordered_styles.append(style_elem)
                    except LookupError:
                        raise SemanticValidationError(ERR_SEMANTIC_STYLE_MISSING.format(
                            style=style_id
                        ))

            self._ordered_styles = ordered_styles
            return ordered_styles

    def add(self, other):
        if self.direction is None and other.direction is not None:
            self.direction = other.direction
        if self.fontFamily is None and other.fontFamily is not None:
            self.fontFamily = other.fontFamily
        if self.fontSize is None and other.fontSize is not None:
            self.fontSize = other.fontSize
        if self.lineHeight is None and other.lineHeight is not None:
            self.lineHeight = other.lineHeight
        if self.textAlign is None and other.textAlign is not None:
            self.textAlign = other.textAlign
        if self.color is None and other.color is not None:
            self.color = other.color
        if self.backgroundColor is None and other.backgroundColor is not None:
            self.backgroundColor = other.backgroundColor
        if self.fontStyle is None and other.fontStyle is not None:
            self.fontStyle = other.fontStyle
        if self.fontWeight is None and other.fontWeight is not None:
            self.fontWeight = other.fontWeight
        if self.textDecoration is None and other.textDecoration is not None:
            self.textDecoration = other.textDecoration
        if self.unicodeBidi is None and other.unicodeBidi is not None:
            self.unicodeBidi = other.unicodeBidi
        if self.wrapOption is None and other.wrapOption is not None:
            self.wrapOption = other.wrapOption
        if self.padding is None and other.padding is not None:
            self.padding = other.padding
        if self.linePadding is None and other.linePadding is not None:
            self.linePadding = other.linePadding
        if self.multiRowAlign is None and other.multiRowAlign is not None:
            self.multiRowAlign = other.multiRowAlign
        return self

    @classmethod
    def resolve_styles(cls, referenced_styles):
        """
        Resolve the style attributes in inheritance chain
        :param referenced_styles:
        :return:
        """
        instance = cls()
        for item in referenced_styles:
            instance.add(item)
        return instance

    @classmethod
    def compute_font_size(cls, specified_style, parent_computed_style, region_computed_style, dataset, defer=False):
        spec_font_size = specified_style.fontSize
        default_font_size = ebuttdt.CellFontSizeType('1c')
        result_font_size = None
        if spec_font_size is not None:
            # Check relativeness
            if isinstance(spec_font_size, ebuttdt.PercentageFontSizeType):
                if parent_computed_style is not None and parent_computed_style.fontSize is not None:
                    result_font_size = parent_computed_style.fontSize * spec_font_size
                elif region_computed_style is not None and region_computed_style.fontSize is not None:
                    result_font_size = region_computed_style.fontSize * spec_font_size
                else:
                    if region_computed_style is None and defer is True:
                        # This is an edge-case. body or div can have styles attached with fontSize but may still have no
                        # region assigned so if they are percentage based the calculation needs to be deferred.
                        # In this case and in this case only we save percentage in the computed fontSize value
                        result_font_size = spec_font_size
                    else:
                        # This means the default font size needs to be modulated by the percentage
                        result_font_size = default_font_size * spec_font_size

                if isinstance(result_font_size, ebuttdt.PercentageFontSizeType) and defer is False:
                    # We cannot defer any longer so now it is time to resolve it.
                    result_font_size *= default_font_size
            else:
                # TODO: control the type here
                result_font_size = spec_font_size
        else:
            if region_computed_style is not None and region_computed_style.fontSize is not None:
                result_font_size = region_computed_style.fontSize
            if parent_computed_style is not None and parent_computed_style.fontSize is not None:
                if isinstance(parent_computed_style.fontSize, ebuttdt.PercentageFontSizeType):
                    if result_font_size is not None:
                        # There is a region we can proceed
                        result_font_size *= parent_computed_style.fontSize
                    else:
                        result_font_size = parent_computed_style.fontSize
                else:
                    result_font_size = parent_computed_style.fontSize
                if defer is False:
                    if isinstance(result_font_size, ebuttdt.PercentageFontSizeType):
                        result_font_size *= default_font_size

        if result_font_size is not None:
            if isinstance(result_font_size, ebuttdt.pixelFontSizeType):
                result_font_size = ebuttdt.CellFontSizeType(
                    *ebuttdt.pixels_to_cells(
                        result_font_size,
                        dataset['tt_element'].extent,
                        dataset['tt_element'].cellResolution
                    )
                )
        elif defer is not True:
            result_font_size = default_font_size

        return result_font_size

    @property
    def default_attrs(self):
        """
        This property function gives back a set in which we find the unspecified style attributes.

            :return: set for attribute names that were inheriting the default in the computed style. Important at
                     inheritance override

        """

        if self._default_attrs is None:
            self._default_attrs = set()
        return self._default_attrs

    def set_default_value(self, attr_name, default_value=None):
        # We must cater for the case when default computed values would override specified region style values
        # With fontSize the defaults are vital for computing relative values. At override the next element down the
        # line would not be able to tell if the parent computed an actually intended value or just the
        # inheritance of the default value.
        if default_value is None:
            if attr_name in self._simple_attr_defaults:
                default_value = self._simple_attr_defaults[attr_name]
            elif attr_name in self._inherited_attr_defaults:
                default_value = self._inherited_attr_defaults[attr_name]
            else:
                raise LookupError()
        # This is the extra step: register default value usage
        self.default_attrs.add(attr_name)
        setattr(
            self,
            attr_name,
            default_value
        )

    @classmethod
    def compute_inherited_attribute(cls, attr_name, specified_style, parent_computed_style, region_computed_style):
        fallback_order = [specified_style,
            parent_computed_style, region_computed_style]
        for item in fallback_order:
            if item is not None and attr_name not in item.default_attrs:
                attr_value = getattr(item, attr_name)
                if attr_value is not None:
                    return attr_value
        return None

    @classmethod
    def compute_simple_attribute(cls, attr_name, specified_style):
        if specified_style is not None:
            attr_value = getattr(specified_style, attr_name)
            if attr_value is not None:
                return attr_value
        return None

    @classmethod
    def compute_line_height(cls, specified_style, parent_computed_style, region_computed_style, dataset, font_size):
        fallback_order = [specified_style,
            parent_computed_style, region_computed_style]
        for item in fallback_order:
            if item is not None and item.lineHeight is not None and 'lineHeight' not in item.default_attrs:
                selected_value = item.lineHeight
                # NOTE: the return value should be cell based except when 'normal' is used
                if isinstance(selected_value, ebuttdt.PixelLineHeightType):
                    selected_value = ebuttdt.CellLineHeightType(
                        *ebuttdt.pixels_to_cells(
                            selected_value,
                            dataset['tt_element'].extent,
                            dataset['tt_element'].cellResolution
                        )
                    )
                elif isinstance(selected_value, ebuttdt.PercentageLineHeightType) and isinstance(font_size, ebuttdt.cellFontSizeType):
                    # We only need to deal with this case if fontSize was not deferred
                    selected_value *= font_size

                return selected_value
        return None

    @classmethod
    def compute_style(cls, specified_style, parent_computed_style, region_computed_style, dataset, defer_font_size):
        """
        This function holds the styling semantics of containers considering direct reference, inheritance and
        containment variables
        :param specified_style: Directly referenced resolved styles
        :param parent_computed_style: Inherited styling information from parent container
        :param region_computed_style: Default region styling information
        :param dataset: Semantic dataset needed for conversion context
        :return:
        """
        computed = cls()
        # Here we need to check for multiple things for each style attribute:
        # 1: If specified
        # 2: If specified value is relative
        # 3: If not specified and there is parent style attr
        # 4: If no parent style attr but there is region style attr
        # 5: If none of the above assume the default

        computed.fontSize = cls.compute_font_size(
            specified_style=specified_style,
            parent_computed_style=parent_computed_style,
            region_computed_style=region_computed_style,
            dataset=dataset,
            defer=defer_font_size
        )
        computed_line_height = cls.compute_line_height(
            specified_style=specified_style,
            parent_computed_style=parent_computed_style,
            region_computed_style=region_computed_style,
            dataset=dataset,
            font_size=computed.fontSize
        )

        if computed_line_height is None:
            computed.set_default_value('lineHeight', default_value='normal')
        else:
            computed.lineHeight = computed_line_height

        for attr_name in list(cls._simple_attr_defaults.keys()):
            comp_attr_value = cls.compute_simple_attribute(
                attr_name=attr_name,
                specified_style=specified_style
            )
            if comp_attr_value is None:
                computed.set_default_value(attr_name)
            else:
                setattr(
                    computed,
                    attr_name,
                    comp_attr_value
                )

        for attr_name in list(cls._inherited_attr_defaults.keys()):
            comp_attr_value = cls.compute_inherited_attribute(
                attr_name=attr_name,
                specified_style=specified_style,
                parent_computed_style=parent_computed_style,
                region_computed_style=region_computed_style
            )
            if comp_attr_value is None:
                computed.set_default_value(attr_name)
            else:
                setattr(
                    computed,
                    attr_name,
                    comp_attr_value
                )

        return computed

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_check_sizing_type(self.fontSize, dataset=dataset)
        self._semantic_check_sizing_type(self.lineHeight, dataset=dataset)
        self._semantic_check_sizing_type(self.padding, dataset=dataset)
        # Init recursion loop detection lock
        self._styling_lock = threading.Lock()
        self._ordered_styles = None

    def _semantic_before_copy(self, dataset, element_content=None):
        if self not in dataset['affected_elements']:
            raise OutsideSegmentError()


# For the requirements of the StyledElementMixin
style_type._compatible_style_type = style_type
raw.style._SetSupersedingClass(style_type)


class LiveStyledElementMixin(StyledElementMixin):

    _compatible_style_type = style_type


# EBU TT Live element types
# =========================
# NOTE: Some of the code below includes handling of SMPTE time base, which was removed from version 1.0 of the specification.


class tt_type(SemanticDocumentMixin, raw.tt_type):

    def __post_time_base_set_attribute(self, attr_use):
        context = get_xml_parsing_context()
        if context is not None:
            # This means we are in XML parsing mode
            context['timeBase'] = self.timeBase

    _attr_en_post = {
        (pyxb.namespace.ExpandedName(ttp.Namespace, 'timeBase')).uriTuple(): __post_time_base_set_attribute
    }
    _elements_by_id = None
    _validator_class = SemanticValidator

    def __copy__(self):
        copied_tt = tt_type(
            lang=self.lang,
            extent=self.extent,
            timeBase=self.timeBase,
            frameRate=self.frameRate,
            frameRateMultiplier=self.frameRateMultiplier,
            markerMode=self.markerMode,
            dropMode=self.dropMode,
            clockMode=self.clockMode,
            cellResolution=self.cellResolution,
            sequenceIdentifier=self.sequenceIdentifier,
            sequenceNumber=self.sequenceNumber,
            authoringDelay=self.authoringDelay,
            authorsGroupIdentifier=self.authorsGroupIdentifier,
            authorsGroupControlToken=self.authorsGroupControlToken,
            authorsGroupSelectedSequenceIdentifier=self.authorsGroupSelectedSequenceIdentifier,
            referenceClockIdentifier=self.referenceClockIdentifier,
            _strict_keywords=False
        )
        return copied_tt

    def merge(self, other, dataset):
        # TODO: compatibility check, rules of merging TBD
        # merged_tt = tt_type(
        #     lang=self.lang,
        #     extent=self.extent,
        #     timeBase=self.timeBase,
        #     frameRate=self.frameRate,
        #     frameRateMultiplier=self.frameRateMultiplier,
        #     markerMode=self.markerMode,
        #     dropMode=self.dropMode,
        #     clockMode=self.clockMode,
        #     cellResolution=self.cellResolution,
        #     sequenceIdentifier=self.sequenceIdentifier,
        #     sequenceNumber=self.sequenceNumber,
        #     authoringDelay=self.authoringDelay,
        #     authorsGroupIdentifier=self.authorsGroupIdentifier,
        #     authorsGroupControlToken=self.authorsGroupControlToken,
        #     authorsGroupControlRequest=self.authorsGroupControlRequest,
        #     referenceClockIdentifier=self.referenceClockIdentifier,
        #     _strict_keywords=False
        # )
        return self

    @classmethod
    def __check_bds(cls, bds):
        if bds:
            return bds
        else:
            return BindingDOMSupport(
                namespace_prefix_map=namespace_prefix_map
            )

    def toDOM(self, bds=None, parent=None, element_name=None):
        return super(tt_type, self).toDOM(
            bds=self.__check_bds(bds),
            parent=parent,
            element_name=element_name
        )

    def toxml(self, encoding=None, bds=None, root_only=False, element_name=None):
        dom = self.toDOM(self.__check_bds(bds), element_name=element_name)
        if root_only:
            dom = dom.documentElement
        return dom.toprettyxml(
            encoding=encoding,
            indent='  '
        )

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        # This one does not have another parent to link with but it can make itself an element
        copied_instance._setElement(raw.tt)

    def __semantic_test_smpte_attrs_present(self):
        smpte_attrs = [
            'frameRate',
            # 'frameRateMultiplier',
            'dropMode',
            'markerMode'
        ]
        missing_attrs = self._semantic_attributes_missing(smpte_attrs)
        if missing_attrs:
            raise SemanticValidationError(
                ERR_SEMANTIC_VALIDATION_MISSING_ATTRIBUTES.format(
                    elem_name='tt:tt',
                    attr_names=missing_attrs
                )
            )

    def __semantic_test_smpte_attrs_absent(self):
        smpte_attrs = [
            'dropMode',
            'markerMode'
        ]
        extra_attrs = self._semantic_attributes_present(smpte_attrs)
        if extra_attrs:
            raise SemanticValidationError(
                ERR_SEMANTIC_VALIDATION_INVALID_ATTRIBUTES.format(
                    elem_name='tt:tt',
                    attr_names=extra_attrs
                )
            )

    def __semantic_test_time_base_clock_attrs_present(self):
        clock_attrs = [
            'clockMode'
        ]
        missing_attrs = self._semantic_attributes_missing(clock_attrs)
        if missing_attrs:
            raise SemanticValidationError(
                ERR_SEMANTIC_VALIDATION_MISSING_ATTRIBUTES.format(
                    elem_name='tt:tt',
                    attr_names=missing_attrs
                )
            )

    def __semantic_test_time_base_clock_attrs_absent(self):
        clock_attrs = [
            'clockMode'
        ]
        extra_attrs = self._semantic_attributes_present(clock_attrs)
        if extra_attrs:
            raise SemanticValidationError(
                ERR_SEMANTIC_VALIDATION_MISSING_ATTRIBUTES.format(
                    elem_name='tt:tt',
                    attr_names=extra_attrs
                )
            )

    def __semantic_test_smpte_attr_combinations(self):
        # TODO: SMPTE validation(low priority) #52
        pass

    def _semantic_before_validation(self):
        """
        Here before anything semantic happens I check some SYNTACTIC errors.
        :raises ComplexTypeValidationError, SimpleTypeValueError
        """
        # The following edge case is ruined by the XSD associating the same extent type to this extent element.
        if self.extent is not None and not isinstance(self.extent, ebuttdt.pixelExtentType):
            raise SimpleTypeValueError(type(self.extent), self.extent)
        # This little gem is correcting a bug in PyXB and defult attribute values being instantiated to the old type
        # and not the customized one
        # e.g: instead of ebuttdt.CellResolutionType it creates raw._ebuttdt.cellResolutionType, which is a bug
        # NOTE: As a side effect however this monkey patch will cause cellResolution to be defined on all generated
        # documents' tt element.
        if isinstance(self.cellResolution, ebuttdt.cellResolutionType):
            self.cellResolution = ebuttdt.CellResolutionType(
                self.cellResolution)

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        # The tt element adds itself to the semantic dataset to help classes lower down the line to locate constraining
        # attributes.
        dataset['timing_begin_stack'] = []
        dataset['timing_end_stack'] = []
        dataset['div_stack'] = []
        dataset['timing_syncbase'] = timedelta()
        dataset['tt_element'] = self
        dataset['styles_stack'] = []
        self._elements_by_id = {}
        dataset['elements_by_id'] = self._elements_by_id
        if self.timeBase == 'smpte':
            self.__semantic_test_smpte_attrs_present()
        else:
            self.__semantic_test_smpte_attrs_absent()
        if self.timeBase == 'clock':
            self.__semantic_test_time_base_clock_attrs_present()
        else:
            self.__semantic_test_time_base_clock_attrs_absent()

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        # Save this for id lookup.
        self._elements_by_id = dataset['elements_by_id']

    def get_element_by_id(self, elem_id, elem_type=None):
        """
        Lookup an element and return it. Optionally type is checked as well.
        :param elem_id:
        :param elem_type:
        :return:
        """
        if self._elements_by_id is None:
            raise SemanticValidationError(ERR_SEMANTIC_VALIDATION_EXPECTED)
        element = self._elements_by_id.get(elem_id, None)
        if element is None or elem_type is not None and not isinstance(element, elem_type):
            raise LookupError(
                ERR_SEMANTIC_ELEMENT_BY_ID_MISSING.format(id=elem_id))
        return element

    def get_timing_type(self, timedelta_in):
        if self.timeBase == 'clock':
            return ebuttdt.LimitedClockTimingType(timedelta_in)
        if self.timeBase == 'media':
            return ebuttdt.FullClockTimingType(timedelta_in)
        if self.timeBase == 'smpte':
            return ebuttdt.SMPTETimingType(timedelta_in)


raw.tt_type._SetSupersedingClass(tt_type)


# Head classes
# ============


class head_type(SemanticValidationMixin, raw.head_type):

    def __copy__(self):
        copied_head = head_type()
        return copied_head

    def merge(self, other_elem, dataset):
        return self


raw.head_type._SetSupersedingClass(head_type)


# Body classes
# ============


class p_type(RegionedElementMixin, LiveStyledElementMixin, SubtitleContentContainer, raw.p_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_copy(self, dataset):
        copied_p = p_type(
            id=self.id,
            space=self.space,
            lang=self.lang,
            region=self._semantic_deconflicted_ids(
                attr_name='region', dataset=dataset),
            style=self._semantic_deconflicted_ids(
                attr_name='style', dataset=dataset),
            begin=self.begin,
            end=self.end,
            agent=self.agent,
            role=self.role,
            _strict_keywords=False
        )
        return copied_p

    def __copy__(self):
        copied_p = p_type(
            id=self.id,
            space=self.space,
            lang=self.lang,
            region=self.region,
            style=self.style,
            begin=self.begin,
            end=self.end,
            agent=self.agent,
            role=self.role,
            _strict_keywords=False
        )
        return copied_p

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_timebase_validation(
            dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(
            dataset=dataset, element_content=element_content)
        self._semantic_set_region(dataset=dataset, region_type=region_type)
        self._semantic_collect_applicable_styles(
            dataset=dataset, style_type=style_type, parent_binding=parent_binding)
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_postprocess_timing(
            dataset=dataset, element_content=element_content)
        self._semantic_manage_timeline(
            dataset=dataset, element_content=element_content)
        self._semantic_unset_region(dataset=dataset)
        self._semantic_pop_styles(dataset=dataset)

    def _semantic_before_copy(self, dataset, element_content=None):
        self._assert_in_segment(
            dataset=dataset, element_content=element_content)

    def is_timed_leaf(self):
        if len(self.span):
            return False
        else:
            return True

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        copied_instance._assert_empty_container()
        self._semantic_copy_apply_leaf_timing(
            copied_instance=copied_instance, dataset=dataset, element_content=element_content)
        self._semantic_copy_verify_referenced_styles(dataset=dataset)
        self._semantic_copy_verify_referenced_region(dataset=dataset)


raw.p_type._SetSupersedingClass(p_type)


class span_type(LiveStyledElementMixin, SubtitleContentContainer, raw.span_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_copy(self, dataset):
        copied_span = span_type(
            id=self.id,
            style=self._semantic_deconflicted_ids(
                attr_name='style', dataset=dataset),
            begin=self.begin,
            end=self.end,
            space=self.space,
            lang=self.lang,
            agent=self.agent,
            role=self.role,
            _strict_keywords=False
        )
        return copied_span

    def __copy__(self):
        copied_span = span_type(
            id=self.id,
            style=self.style,
            begin=self.begin,
            end=self.end,
            space=self.space,
            lang=self.lang,
            agent=self.agent,
            role=self.role,
            _strict_keywords=False
        )
        return copied_span

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_timebase_validation(
            dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(
            dataset=dataset, element_content=element_content)
        self._semantic_collect_applicable_styles(
            dataset=dataset, style_type=style_type, parent_binding=parent_binding)
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_postprocess_timing(
            dataset=dataset, element_content=element_content)
        self._semantic_manage_timeline(
            dataset=dataset, element_content=element_content)
        self._semantic_pop_styles(dataset=dataset)

    def _semantic_before_copy(self, dataset, element_content=None):
        self._assert_in_segment(
            dataset=dataset, element_content=element_content)

    def is_timed_leaf(self):
        if len(self.span):
            return False
        else:
            return True

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        copied_instance._assert_empty_container()
        self._semantic_copy_apply_leaf_timing(
            copied_instance=copied_instance, dataset=dataset, element_content=element_content)
        self._semantic_copy_verify_referenced_styles(dataset=dataset)


raw.span_type._SetSupersedingClass(span_type)


class br_type(SemanticValidationMixin, raw.br_type):

    def __copy__(self):
        return br_type()

    def content_to_string(self, begin=None, end=None):
        return '<br />'


raw.br_type._SetSupersedingClass(br_type)


class div_type(ContentContainerMixin, IDMixin, RegionedElementMixin, LiveStyledElementMixin, TimingValidationMixin,
               SemanticValidationMixin, raw.div_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_copy(self, dataset):
        copied_div = div_type(
            id=self.id,
            region=self._semantic_deconflicted_ids(
                attr_name='region', dataset=dataset),
            style=self._semantic_deconflicted_ids(
                attr_name='style', dataset=dataset),
            agent=self.agent,
            role=self.role,
            begin=self.begin,
            end=self.end,
            _strict_keywords=False
        )
        return copied_div

    def __copy__(self):
        copied_div = div_type(
            id=self.id,
            region=self.region,
            style=self.style,
            agent=self.agent,
            role=self.role,
            begin=self.begin,
            end=self.end,
            _strict_keywords=False
        )
        return copied_div

    def merge(self, elem):
        return self

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_timebase_validation(
            dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(
            dataset=dataset, element_content=element_content)
        self._semantic_set_region(dataset=dataset, region_type=region_type)
        self._semantic_collect_applicable_styles(
            dataset=dataset, style_type=style_type, parent_binding=parent_binding, defer_font_size=True
        )
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_postprocess_timing(
            dataset=dataset, element_content=element_content)
        self._semantic_unset_region(dataset=dataset)

    def _semantic_before_copy(self, dataset, element_content=None):
        self._assert_in_segment(
            dataset=dataset, element_content=element_content)

    def is_empty(self):
        if len(self.div):
            return False

        if len(self.p):
            return False

        return True

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        copied_instance._assert_empty_container()
        self._semantic_copy_apply_leaf_timing(
            copied_instance=copied_instance, dataset=dataset, element_content=element_content)
        self._semantic_copy_verify_referenced_styles(dataset=dataset)
        self._semantic_copy_verify_referenced_region(dataset=dataset)
    



raw.div_type._SetSupersedingClass(div_type)


class body_type(LiveStyledElementMixin, BodyTimingValidationMixin, SemanticValidationMixin, raw.body_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'dur')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_copy(self, dataset):
        copied_body = body_type(
            agent=self.agent,
            role=self.role,
            begin=self.begin,
            dur=self.dur,
            end=self.end,
            style=self._semantic_deconflicted_ids(
                attr_name='style', dataset=dataset),
            _strict_keywords=False
        )
        return copied_body

    def __copy__(self):
        copied_body = body_type(
            agent=self.agent,
            role=self.role,
            begin=self.begin,
            dur=self.dur,
            end=self.end,
            style=self.style,
            _strict_keywords=False
        )
        return copied_body

    @classmethod
    def _merge_deconflict_ids(cls, element, dest, ids):
        """
        Deconflict ids of body elements
        :param element:
        :return:
        """

        children = element.orderedContent()

        output = []

        for item in children:
            log.debug('processing child: {} of {}'.format(item.value, element))
            if isinstance(item, NonElementContent):
                copied_stuff = copy.copy(item.value)
                output.append(copied_stuff)
            elif isinstance(item, ElementContent):
                copied_elem = copy.copy(item.value)
                copied_elem._resetContent()
                cls._merge_deconflict_ids(item.value, copied_elem, ids)
                if isinstance(copied_elem, IDMixin):
                    if copied_elem.id is not None and copied_elem.id in ids:
                        next_try = copied_elem.id
                        while next_try in ids:
                            next_try = '{}.1'.format(next_try)
                        copied_elem.id = next_try
                    ids.add(copied_elem.id)
                output.append(copied_elem)

        for item in output:
            dest.append(item)

        return dest

    def merge(self, other_elem, dataset=None):
        # TODO: Sort out timing and styling merging rules
        merged_body = copy.copy(self)
        merged_body.begin = None
        merged_body.dur = None
        merged_body.end = None
        # The same recursive ID collision issue... DAMN!
        ids = dataset['ids']

        self._merge_deconflict_ids(element=self, dest=merged_body, ids=ids)
        self._merge_deconflict_ids(
            element=other_elem, dest=merged_body, ids=ids)

        return merged_body

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_timebase_validation(
            dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(
            dataset=dataset, element_content=element_content)
        self._semantic_collect_applicable_styles(
            dataset=dataset, style_type=style_type, parent_binding=parent_binding, defer_font_size=True
        )
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_postprocess_timing(
            dataset=dataset, element_content=element_content)
        self._semantic_pop_styles(dataset=dataset)

    def _semantic_before_copy(self, dataset, element_content=None):
        self._assert_in_segment(
            dataset=dataset, element_content=element_content)

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        self._semantic_copy_apply_leaf_timing(
            copied_instance=copied_instance, dataset=dataset, element_content=element_content)
        self._semantic_copy_verify_referenced_styles(dataset=dataset)


raw.body_type._SetSupersedingClass(body_type)


class styling(SemanticValidationMixin, raw.styling):

    def __copy__(self):
        copied_styling = styling()
        return copied_styling

    def merge(self, other_elem, dataset):
        style_ids = dataset['ids']
        for item in self.orderedContent():
            style_ids.add(item.value.id)
        if other_elem:
            for item in other_elem.orderedContent():
                copied_style = copy.copy(item.value)
                if item.value.id in style_ids:
                    copied_style.id = '{}.1'.format(copied_style.id)
                self.append(copied_style)

        return self

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        # The styles are not ordered by inheritance so they need an extra step here
        # to get their style ID resolutions sorted
        for style_elem in \
                [
                    item.value
                    for item in self.orderedContent()
                    if isinstance(item, ElementContent) and isinstance(item.value, style_type)
                ]:
            copied_style_elem = dataset['instance_mapping'].get(style_elem)
            # The style may not have been copied at all because it isn't used in the requested segment
            if copied_style_elem is not None:
                style_elem_styles = style_elem._semantic_deconflicted_ids(
                    attr_name='style', dataset=dataset)
                if style_elem_styles:
                    copied_style_elem.style = style_elem_styles


raw.styling._SetSupersedingClass(styling)


class region_type(IDMixin, LiveStyledElementMixin, SizingValidationMixin, SemanticValidationMixin, raw.region):

    def _semantic_copy(self, dataset):
        copied_region = region_type(
            id=self.id,
            origin=self.origin,
            extent=self.extent,
            style=self._semantic_deconflicted_ids(
                attr_name='style', dataset=dataset),
            displayAlign=self.displayAlign,
            padding=self.padding,
            writingMode=self.writingMode,
            showBackground=self.showBackground,
            overflow=self.overflow,
            _strict_keywords=False
        )

        return copied_region

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_check_sizing_type(self.origin, dataset=dataset)
        self._semantic_check_sizing_type(self.extent, dataset=dataset)
        self._semantic_check_sizing_type(self.padding, dataset=dataset)
        self._semantic_collect_applicable_styles(
            dataset=dataset,
            style_type=self._compatible_style_type,
            parent_binding=parent_binding,
            extra_referenced_styles=[
                self._compatible_style_type(
                    padding=self.padding,
                    _strict_keywords=False
                )
            ]
        )

    def _semantic_before_copy(self, dataset, element_content=None):
        if self not in dataset['affected_elements']:
            raise OutsideSegmentError()


raw.region._SetSupersedingClass(region_type)


class layout(SemanticValidationMixin, raw.layout):

    def __copy__(self):
        copied_layout = layout()
        return copied_layout

    def merge(self, other_elem, dataset):
        region_ids = dataset['ids']
        for item in self.orderedContent():
            region_ids.add(item.value.id)
        if other_elem:
            for item in other_elem.orderedContent():
                copied_region = copy.copy(item.value)
                if copied_region.id in region_ids:
                    copied_region.id = '{}.1'.format(copied_region.id)
                    region_ids.add(copied_region.id)
                self.append(copied_region)
        return self


raw.layout._SetSupersedingClass(layout)

# EBU TT D classes
# ================


class d_tt_type(SemanticDocumentMixin, raw.d_tt_type):

    _validator_class = SemanticValidator

    def __post_time_base_set_attribute(self, attr_use):
        context = get_xml_parsing_context()
        if context is not None:
            # This means we are in XML parsing mode
            context['timeBase'] = self.timeBase

    _attr_en_post = {
        (pyxb.namespace.ExpandedName(ttp.Namespace, 'timeBase')).uriTuple(): __post_time_base_set_attribute
    }
    _elements_by_id = None

    @classmethod
    def __check_bds(cls, bds):
        if bds:
            return bds
        else:
            return BindingDOMSupport(
                namespace_prefix_map=namespace_prefix_map
            )

    def toDOM(self, bds=None, parent=None, element_name=None):
        bds = self.__check_bds(bds)
        xml_dom = super(d_tt_type, self).toDOM(
            bds=bds,
            parent=parent,
            element_name=element_name
        )
        # Nasty workaround for the namespace collision EBU-TT-D and EBU-TT Live are causing by both defining the same
        # tt element in the ttml namespace
        if bds.defaultNamespace() != Namespace:
            xml_dom.documentElement.tagName = 'tt:tt'
        else:
            xml_dom.documentElement.tagName = 'tt'
        return xml_dom

    def toxml(self, encoding=None, bds=None, root_only=False, element_name=None):
        dom = self.toDOM(self.__check_bds(bds), element_name=element_name)
        if root_only:
            dom = dom.documentElement
        return dom.toprettyxml(
            encoding=encoding,
            indent='  '
        )

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
            # The tt element adds itself to the semantic dataset to help classes lower down the line to locate constraining
            # attributes.
        dataset['timing_begin_stack'] = []
        dataset['timing_end_stack'] = []
        dataset['timing_syncbase'] = timedelta()
        dataset['ttd_element'] = self #WIP with the namespace
        dataset['styles_stack'] = []
        self._elements_by_id = {}
        dataset['elements_by_id'] = self._elements_by_id

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        # Save this for id lookup.
        self._elements_by_id = dataset['elements_by_id']

    def get_element_by_id(self, elem_id, elem_type=None):
        """
        Lookup an element and return it. Optionally type is checked as well.
        :param elem_id:
        :param elem_type:
        :return:
        """
        if self._elements_by_id is None:
            raise SemanticValidationError(ERR_SEMANTIC_VALIDATION_EXPECTED)
        element = self._elements_by_id.get(elem_id, None)
        if element is None or elem_type is not None and not isinstance(element, elem_type):
            raise LookupError(
                ERR_SEMANTIC_ELEMENT_BY_ID_MISSING.format(id=elem_id))
        return element

    def _validateBinding_vx(self):
        if self.timeBase != 'media':
            raise SimpleTypeValueError(type(self.timeBase), self.timeBase)

        super(d_tt_type, self)._validateBinding_vx()


raw.d_tt_type._SetSupersedingClass(d_tt_type)


class d_layout_type(SemanticValidationMixin, raw.d_layout_type):

    @classmethod
    def create_default_value(cls):
        instance = cls(
            d_region_type.create_default_value()
        )
        return instance

raw.d_layout_type._SetSupersedingClass(d_layout_type)

class d_head_type(SemanticValidationMixin, raw.d_head_type):
    pass


raw.d_layout_type._SetSupersedingClass(d_layout_type)

class d_region_type(SemanticValidationMixin,IDMixin, raw.d_region_type):

    @classmethod
    def create_default_value(cls):
        instance = cls(
            id='region.default',
            origin='0% 0%',
            extent='100% 100%'
        )
        return instance

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)

    def _semantic_before_copy(self, dataset, element_content=None):
        pass

    def _validateBinding_vx(self):
        origins = self.origin.split(" ")
        extents = self.extent.split(" ")
        if not isinstance(self.origin, ebuttdt.percentageOriginType) and self.origin is not None:
            raise InvalidRegionOriginType(self)
        if not isinstance(self.extent, ebuttdt.percentageExtentType) and self.extent is not None:
            raise InvalidRegionExtentType(self)
        l1 = [float(origin.strip('%')) for origin in origins]  # l1
        r1 = [float(extent.strip('%')) for extent in extents]  # r1
        if l1[0] < 0.0 or (l1[0]+r1[0]) > 100.0 or l1[1] < 0.0 or (l1[1] + r1[1]) > 100.0:
            raise RegionExtendingOutsideDocumentError(self)

raw.d_region_type._SetSupersedingClass(d_region_type)


class d_styling_type(SemanticValidationMixin, raw.d_styling_type):

    @classmethod
    def create_default_value(cls):
        instance = cls(
            d_style_type.create_default_value()
        )
        return instance

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        pass


raw.d_styling_type._SetSupersedingClass(d_styling_type)


class d_style_type(SemanticValidationMixin, IDMixin, raw.d_style_type):
    
    @classmethod
    def create_default_value(cls):
        instance = cls(
            id='style.default'
        )
        return instance

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)


raw.d_style_type._SetSupersedingClass(d_style_type)


class d_body_type(SemanticValidationMixin, raw.d_body_type):


    def _semantic_before_copy(self, dataset, element_content=None):
        self._assert_in_segment(
        dataset=dataset, element_content=element_content)

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        self._semantic_copy_apply_leaf_timing(
        copied_instance=copied_instance, dataset=dataset, element_content=element_content)
        self._semantic_copy_verify_referenced_styles(dataset=dataset)

raw.d_body_type._SetSupersedingClass(d_body_type)


class d_div_type(ContentContainerMixin, IDMixin, TimingValidationMixin, SemanticValidationMixin, RegionedElementMixin ,raw.d_div_type):

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_set_d_region(dataset=dataset, region_type=d_region_type)

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_unset_region(dataset=dataset)

    def _semantic_before_copy(self, dataset, element_content=None):
        self._assert_in_segment(
            dataset=dataset, element_content=element_content)

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        copied_instance._assert_empty_container()
        self._semantic_copy_verify_referenced_styles(dataset=dataset)
        self._semantic_copy_verify_referenced_region(dataset=dataset)

raw.d_div_type._SetSupersedingClass(d_div_type)


class d_p_type(IDMixin, TimingValidationMixin, SemanticValidationMixin, RegionedElementMixin ,raw.d_p_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_timebase_validation(
        dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(
        dataset=dataset, element_content=element_content)
        self._semantic_set_d_region(dataset=dataset, region_type=d_region_type)


    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_postprocess_timing(
        dataset=dataset, element_content=element_content)
        self._semantic_manage_timeline(
        dataset=dataset, element_content=element_content)
        self._semantic_validate_active_areas(dataset=dataset)


raw.d_p_type._SetSupersedingClass(d_p_type)


class d_span_type(IDMixin, TimingValidationMixin,StyledElementMixin ,SemanticValidationMixin, RegionedElementMixin, raw.d_span_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self,dataset,element_content=None, parent_binding=None):
         self._semantic_preprocess_timing(
             dataset=dataset, element_content=element_content)

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_postprocess_timing(
                dataset=dataset, element_content=element_content)