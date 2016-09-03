# -*- coding: utf-8 -*-
from .raw import *
from . import raw

# Let's import customizations
from . import _ebuttdt as ebuttdt
from . import _ebuttm as ebuttm
from . import _ebuttp as ebuttp
from . import _ebutts as ebutts
from . import _ttm as ttm
from . import _ttp as ttp
from . import _tts as tts
from .pyxb_utils import xml_parsing_context, get_xml_parsing_context
from .validation import SemanticDocumentMixin, SemanticValidationMixin, TimingValidationMixin, \
    BodyTimingValidationMixin, SizingValidationMixin, StyledElementMixin, RegionedElementMixin, IDMixin
from ebu_tt_live.errors import SemanticValidationError
from ebu_tt_live.strings import ERR_SEMANTIC_VALIDATION_MISSING_ATTRIBUTES, \
    ERR_SEMANTIC_VALIDATION_INVALID_ATTRIBUTES, ERR_SEMANTIC_STYLE_CIRCLE, ERR_SEMANTIC_STYLE_MISSING, \
    ERR_SEMANTIC_ELEMENT_BY_ID_MISSING, ERR_SEMANTIC_VALIDATION_EXPECTED
from pyxb.exceptions_ import SimpleTypeValueError, ComplexTypeValidationError
from pyxb.utils.domutils import BindingDOMSupport
from datetime import timedelta
import threading

namespace_prefix_map = {
    'tt': raw.Namespace,
    'ebuttdt': ebuttdt.Namespace,
    'ttp': ttp.Namespace,
    'tts': tts.Namespace,
    'ttm': ttm.Namespace,
    'ebuttm': ebuttm.Namespace,
    'ebutts': ebutts.Namespace,
    'ebuttp': ebuttp.Namespace
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

# EBU TT Live classes
# ===================


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

    def _semantic_before_traversal(self, dataset, element_content=None):
        # The tt element adds itself to the semantic dataset to help classes lower down the line to locate constraining
        # attributes.
        dataset['timing_begin_stack'] = []
        dataset['timing_end_stack'] = []
        dataset['timing_syncbase'] = timedelta()
        dataset['timing_end_limit'] = None
        dataset['timing_begin_limit'] = None
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

    def _semantic_after_traversal(self, dataset, element_content=None):
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
        if elem_type is not None and not isinstance(element, elem_type):
            raise LookupError(ERR_SEMANTIC_ELEMENT_BY_ID_MISSING.format(id=elem_id))
        return element


raw.tt_type._SetSupersedingClass(tt_type)


class p_type(IDMixin, RegionedElementMixin, StyledElementMixin, TimingValidationMixin,
             SemanticValidationMixin, raw.p_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_set_region(dataset=dataset, region_type=region_type)
        self._semantic_collect_applicable_styles(dataset=dataset, style_type=style_type)
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_manage_timeline(dataset=dataset, element_content=element_content)
        self._semantic_unset_region(dataset=dataset)
        self._semantic_pop_styles(dataset=dataset)

raw.p_type._SetSupersedingClass(p_type)


class span_type(IDMixin, StyledElementMixin, TimingValidationMixin, SemanticValidationMixin, raw.span_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_collect_applicable_styles(dataset=dataset, style_type=style_type)
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_manage_timeline(dataset=dataset, element_content=element_content)
        self._semantic_pop_styles(dataset=dataset)

raw.span_type._SetSupersedingClass(span_type)


class div_type(IDMixin, RegionedElementMixin, StyledElementMixin, TimingValidationMixin,
               SemanticValidationMixin, raw.div_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_set_region(dataset=dataset, region_type=region_type)
        self._semantic_collect_applicable_styles(dataset=dataset, style_type=style_type)
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_unset_region(dataset=dataset)

raw.div_type._SetSupersedingClass(div_type)


class body_type(StyledElementMixin, BodyTimingValidationMixin, SemanticValidationMixin, raw.body_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(None, 'begin')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'dur')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(None, 'end')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_collect_applicable_styles(dataset=dataset, style_type=style_type)
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_pop_styles(dataset=dataset)

raw.body_type._SetSupersedingClass(body_type)


class style_type(IDMixin, SizingValidationMixin, SemanticValidationMixin, raw.style):

    # This helps us detecting infinite loops.
    _styling_lock = None
    # ordered styles cached
    _ordered_styles = None

    def __repr__(self):
        return u'<style ID: {id} at {addr}>'.format(
            id=self.id,
            addr=hex(id(self))
        )

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
                for style_id in self.style:
                    try:
                        style_elem = dataset['tt_element'].get_element_by_id(elem_id=style_id, elem_type=style_type)
                        cascading_styles = style_elem.ordered_styles(dataset=dataset)
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

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_check_sizing_type(self.fontSize, dataset=dataset)
        self._semantic_check_sizing_type(self.lineHeight, dataset=dataset)
        # Init recursion loop detection lock
        self._styling_lock = threading.Lock()
        self._ordered_styles = None


raw.style._SetSupersedingClass(style_type)


class styling(SemanticValidationMixin, raw.styling):

    def _semantic_before_traversal(self, dataset, element_content=None):
        pass


raw.styling._SetSupersedingClass(styling)


class region_type(IDMixin, StyledElementMixin, SizingValidationMixin, SemanticValidationMixin, raw.region):

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_check_sizing_type(self.origin, dataset=dataset)
        self._semantic_check_sizing_type(self.extent, dataset=dataset)
        self._semantic_collect_applicable_styles(dataset=dataset, style_type=style_type)


raw.region._SetSupersedingClass(region_type)


# EBU TT D classes
# ================

class d_tt_type(raw.d_tt_type):

    @classmethod
    def __check_bds(cls, bds):
        if bds:
            return bds
        else:
            return BindingDOMSupport(
                namespace_prefix_map=namespace_prefix_map
            )

    def toDOM(self, bds=None, parent=None, element_name=None):
        xml_dom = super(d_tt_type, self).toDOM(
            bds=self.__check_bds(bds),
            parent=parent,
            element_name=element_name
        )
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

raw.d_tt_type._SetSupersedingClass(d_tt_type)


class d_layout_type(raw.d_layout_type):

    @classmethod
    def create_default_value(cls):
        instance = cls(
            d_region_type.create_default_value()
        )
        return instance

raw.d_layout_type._SetSupersedingClass(d_layout_type)


class d_region_type(raw.d_region_type):

    @classmethod
    def create_default_value(cls):
        instance = cls(
            id='region.default',
            origin='0% 0%',
            extent='100% 100%'
        )
        return instance

raw.d_region_type._SetSupersedingClass(d_region_type)


class d_styling_type(raw.d_styling_type):

    @classmethod
    def create_default_value(cls):
        instance = cls(
            d_style_type.create_default_value()
        )
        return instance

raw.d_styling_type._SetSupersedingClass(d_styling_type)


class d_style_type(raw.d_style_type):

    @classmethod
    def create_default_value(cls):
        instance = cls(
            id='style.default'
        )
        return instance

raw.d_style_type._SetSupersedingClass(d_style_type)
