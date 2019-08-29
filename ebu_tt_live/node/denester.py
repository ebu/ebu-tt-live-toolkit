from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import div_type, p_type
import copy
import re


class Denester():
    
    @staticmethod
    def denest(document):
        divs = document.binding.body.div
        for div in divs:
            div2 = Denester.recurse(div)
        document.binding.body.div = div2
        print(document.get_xml())
        return document

    @staticmethod
    def div_attr(div):
        div_attributes =  {}
        if div.style is not None:
            div_attributes["styles"]=div.style
        return div_attributes

    @staticmethod
    def recurse( div, merged_attr={}):
        merged_attr = {**merged_attr, **Denester.div_attr(div)}
        new_divs = []
        for c in div.orderedContent():
            if isinstance(c.value,div_type):
                new_divs.extend(Denester.recurse(c.value, merged_attr))
            else:
                new_div = div_type(
                    id = div.id,
                    style = merged_attr["styles"]
                )
                new_div.p.append(c.value)
                new_divs.append(new_div)
        return new_divs

if __name__ == '__main__':
    xml_file = "testing/bdd/templates/many_nested_elements_hardcoded.xml"
    with open(xml_file, 'r') as in_file:
        input_xml = in_file.read()
    input_xml = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", input_xml)
    ebutt3 = EBUTT3Document.create_from_xml(input_xml)
    Denester.denest(ebutt3)