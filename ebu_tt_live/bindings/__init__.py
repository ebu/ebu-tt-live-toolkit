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
from .validation import SemanticDocumentMixin, SemanticValidationMixin, TimingValidationMixin, BodyTimingValidationMixin
from ebu_tt_live.errors import SemanticValidationError
from ebu_tt_live.strings import ERR_SEMANTIC_VALIDATION_MISSING_ATTRIBUTES, ERR_SEMANTIC_VALIDATION_INVALID_ATTRIBUTES

from pyxb.utils.domutils import BindingDOMSupport
from datetime import timedelta

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


class tt_type(SemanticDocumentMixin, raw.tt_type):

    def __post_time_base_set_attribute(self, attr_use):
        context = get_xml_parsing_context()
        if context is not None:
            # This means we are in XML parsing mode
            context['timeBase'] = self.timeBase

    _attr_en_post = {
        (pyxb.namespace.ExpandedName(ttp.Namespace, 'timeBase')).uriTuple(): __post_time_base_set_attribute
    }

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
        extra_attrs = self._semantic_attributes_present(extra_attrs)
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

    def _semantic_before_traversal(self, dataset, element_content=None):
        # The tt element adds itself to the semantic dataset to help classes lower down the line to locate constraining
        # attributes.
        dataset['timing_begin_stack'] = []
        dataset['timing_end_stack'] = []
        dataset['timing_syncbase'] = timedelta()
        dataset['timing_end_limit'] = None
        dataset['timing_begin_limit'] = None
        dataset['tt_element'] = self
        if self.timeBase == 'smpte':
            self.__semantic_test_smpte_attrs_present()
        else:
            self.__semantic_test_smpte_attrs_absent()
        if self.timeBase == 'clock':
            self.__semantic_test_time_base_clock_attrs_present()
        else:
            self.__semantic_test_time_base_clock_attrs_absent()


raw.tt_type._SetSupersedingClass(tt_type)


class p_type(TimingValidationMixin, SemanticValidationMixin, raw.p_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(Namespace, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)

    def _semantic_after_traversal(self, dataset, element_content=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)

raw.p_type._SetSupersedingClass(p_type)


class span_type(TimingValidationMixin, SemanticValidationMixin, raw.span_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(Namespace, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)

    def _semantic_after_traversal(self, dataset, element_content=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)

raw.span_type._SetSupersedingClass(span_type)


class div_type(TimingValidationMixin, SemanticValidationMixin, raw.div_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(Namespace, 'begin')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'end')).uriTuple(): TimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)

    def _semantic_after_traversal(self, dataset, element_content=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)

raw.div_type._SetSupersedingClass(div_type)


class body_type(BodyTimingValidationMixin, SemanticValidationMixin, raw.body_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(Namespace, 'begin')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'dur')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'end')).uriTuple(): BodyTimingValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)

    def _semantic_after_traversal(self, dataset, element_content=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)

raw.body_type._SetSupersedingClass(body_type)


# Namespace.setPrefix('tt')
# _Namespace_ttm.setPrefix('ttm')
# _Namespace_ttp.setPrefix('ttp')
# _Namespace_tts.setPrefix('tts')
# _Namespace_ebuttm.setPrefix('ebuttm')
# _Namespace_ebuttp.setPrefix('ebuttp')
# _Namespace_ebutts.setPrefix('ebutts')
