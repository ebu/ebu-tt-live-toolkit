# -*- coding: utf-8 -*-
from .raw._ebuttlm import *
from .raw import _ebuttlm as raw
from .raw import _ebuttp as ebuttp
from pyxb.utils.domutils import BindingDOMSupport


namespace_prefix_map = {
    'ebuttlm': Namespace,
    'ebuttp': ebuttp.Namespace
}


class message_type(raw.message_type):

    @classmethod
    def __check_bds(cls, bds):
        if bds:
            return bds
        else:
            return BindingDOMSupport(
                namespace_prefix_map=namespace_prefix_map
            )

    def toDOM(self, bds=None, parent=None, element_name=None):
        return super(message_type, self).toDOM(
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


raw.message_type._SetSupersedingClass(message_type)
