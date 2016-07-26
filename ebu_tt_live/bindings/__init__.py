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
from .validation import SemanticDocumentMixin, SemanticValidationMixin, TimeBaseValidationMixin

from pyxb.utils.domutils import BindingDOMSupport

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

    def _semantic_before_traversal(self, dataset, element_content=None):
        # The tt element adds itself to the semantic dataset to help classes lower down the line to locate contraining
        # attributes.
        dataset['tt_element'] = self

raw.tt_type._SetSupersedingClass(tt_type)


class p_type(TimeBaseValidationMixin, SemanticValidationMixin, raw.p_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(Namespace, 'begin')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'end')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)

raw.p_type._SetSupersedingClass(p_type)


class span_type(TimeBaseValidationMixin, SemanticValidationMixin, raw.span_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(Namespace, 'begin')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'end')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)

raw.span_type._SetSupersedingClass(span_type)


class div_type(TimeBaseValidationMixin, SemanticValidationMixin, raw.div_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(Namespace, 'begin')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'end')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)

raw.div_type._SetSupersedingClass(div_type)


class body_type(TimeBaseValidationMixin, SemanticValidationMixin, raw.body_type):

    _attr_en_pre = {
        (pyxb.namespace.ExpandedName(Namespace, 'begin')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'dur')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute,
        (pyxb.namespace.ExpandedName(Namespace, 'end')).uriTuple(): TimeBaseValidationMixin._pre_timing_set_attribute
    }

    def _semantic_before_traversal(self, dataset, element_content=None):
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)

raw.body_type._SetSupersedingClass(body_type)


# Namespace.setPrefix('tt')
# _Namespace_ttm.setPrefix('ttm')
# _Namespace_ttp.setPrefix('ttp')
# _Namespace_tts.setPrefix('tts')
# _Namespace_ebuttm.setPrefix('ebuttm')
# _Namespace_ebuttp.setPrefix('ebuttp')
# _Namespace_ebutts.setPrefix('ebutts')
