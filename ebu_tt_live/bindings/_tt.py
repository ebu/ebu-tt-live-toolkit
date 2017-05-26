# -*- coding: utf-8 -*-
from raw import style as rawstyle
from pyxb.utils.domutils import BindingDOMSupport

class style(rawstyle):
    
    def __eq__(self,other):
        print('style.__eq__ called')
        if isinstance(other, style):
            return (
                self.multiRowAlign == other.multiRowAlign and
                self.linePadding == other.linePadding and
                self.backgroundColor == other.backgroundColor and
                self.color == other.color and 
                self.direction == other.direction and
                self.displayAlign == other.displayAlign and
                self.extent == other.extent and
                self.fontFamily == other.fontFamily and
                self.fontSize == other.fontSize and
                self.fontWeight == other.fontWeight and
                self.lineHeight == other.lineHeight and
                self.origin == other.origin and
                self.overflow == other.overflow and
                self.padding == other.padding and
                self.showBackground == other.showBackground and
                self.textAlign == other.textAlign and
                self.textDecoration == other.textDecoration and
                self.unicodeBidi == other.unicodeBidi and
                self.wrapOption == other.wrapOption and
                self.writingMode == other.writingMode
                )
        else:
            return NotImplemented
            
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
rawstyle._SetSupersedingClass(style)
