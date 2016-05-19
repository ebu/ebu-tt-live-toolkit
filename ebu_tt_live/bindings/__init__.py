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

from pyxb.utils.domutils import BindingDOMSupport

namespace_prefix_map = {
    'tt': 'http://www.w3.org/ns/ttml',
    'ebuttdt': 'urn:ebu:tt:datatypes',
    'ttp': 'http://www.w3.org/ns/ttml#parameter',
    'tts': 'http://www.w3.org/ns/ttml#styling',
    'ttm': 'http://www.w3.org/ns/ttml#metadata',
    'ebuttm': 'urn:ebu:tt:metadata',
    'ebutts': 'urn:ebu:tt:style',
    'ebuttp': 'urn:ebu:tt:parameters'
}

default_bds = BindingDOMSupport(
    default_namespace=raw.Namespace,
    namespace_prefix_map=namespace_prefix_map
)


class tt_type(raw.tt_type):

    def toDOM(self, bds=default_bds, parent=None, element_name=None):
        return super(tt_type, self).toDOM(
            bds=bds,
            parent=parent,
            element_name=element_name
        )

    def toxml(self, encoding=None, bds=default_bds, root_only=False, element_name=None):
        dom = self.toDOM(bds, element_name=element_name)
        if root_only:
            dom = dom.documentElement
        return dom.toprettyxml(
            encoding=encoding,
            indent='  '
        )

raw.tt_type._SetSupersedingClass(tt_type)

# Namespace.setPrefix('tt')
# _Namespace_ttm.setPrefix('ttm')
# _Namespace_ttp.setPrefix('ttp')
# _Namespace_tts.setPrefix('tts')
# _Namespace_ebuttm.setPrefix('ebuttm')
# _Namespace_ebuttp.setPrefix('ebuttp')
# _Namespace_ebutts.setPrefix('ebutts')
