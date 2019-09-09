from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import div_type, p_type, span_type
from ebu_tt_live.bindings._ebuttm import divMetadata_type
import copy
import re


class Denester():
            
    @staticmethod
    def denest(document):
        divs = document.binding.body.div
        unnested_divs = []
        for div in divs:
            unnested_divs.extend(Denester.recurse(div))
        unnested_divs = Denester.combine_divs(unnested_divs)
        unnested_divs = Denester.check_p_regions(unnested_divs)
        document.binding.body.div = unnested_divs
        return document

    @staticmethod
    def check_p_regions(divs):
        for div in divs:
            if div.region is not None:
                div.p = [p for p in div.p if p.region == div.region or p.region == None]
                for p in div.p:
                    p.region = None

        divs = [div for div in divs if div.p != []]

        return divs

    @staticmethod
    def combine_divs(divs):
        new_divs = []
        if len(divs) != 0:
            new_divs.append(divs[0])
            i = 1
            j = 0
            while i < len(divs):
                if Denester.div_attr(divs[i]) == Denester.div_attr(divs[i-1]):
                    new_divs[j].p.extend(divs[i].p)
                else:
                    j += 1
                    new_divs.append(divs[i])
                i += 1
        return new_divs



    @staticmethod
    def div_attr(div):
        div_attributes =  {}
        div_attributes["styles"]=div.style
        div_attributes["lang"] = div.lang
        div_attributes["region"] = div.region
        div_attributes["begin"] = div.begin
        div_attributes["end"] = div.end
        div_attributes["metadata"] = div.metadata
        return div_attributes
    
    @staticmethod
    def merge_attr(parent_attr, div_attributes):
        merged_attributes ={ "styles": [], "begin": None, "end": None, "lang": None, "region": None, "metadata":divMetadata_type(facet = [])}
        if div_attributes["styles"] is not None:
             merged_attributes["styles"] = div_attributes["styles"] + parent_attr["styles"]
        else:
            merged_attributes["styles"] = parent_attr["styles"]
        if div_attributes["lang"] is not None:
            merged_attributes["lang"] = div_attributes["lang"]
        else:
            merged_attributes["lang"] = parent_attr["lang"]
        if parent_attr["region"] is not None:
            merged_attributes["region"] = parent_attr["region"]
        elif div_attributes["region"] is not None:
            merged_attributes["region"] = div_attributes["region"]
        if parent_attr["metadata"].facet is not None:
            merged_attributes["metadata"].facet.extend(parent_attr["metadata"].facet)
        if div_attributes["metadata"] is not None:
            merged_attributes["metadata"].facet.extend(div_attributes["metadata"].facet)
        return merged_attributes
         

    @staticmethod
    def recurse( div, merged_attr={"styles": [], "begin": None, "end": None, "lang": None, "region": None, "metadata": divMetadata_type(facet = [])}):
        merged_attr = Denester.merge_attr(merged_attr, Denester.div_attr(div))
        new_divs = []
        for c in div.orderedContent():
            if isinstance(c.value,div_type):
                if(div.region != c.value.region and c.value.region !=None and div.region !=None):
                    continue
                new_divs.extend(Denester.recurse(c.value, merged_attr))
            elif isinstance(c.value,divMetadata_type):
                continue
            else:
                new_spans = []
                for ic in c.value.orderedContent():
                    if isinstance(ic.value,span_type):
                        new_spans.extend(Denester.recurse_span(ic.value))
                        c.value.span = new_spans
                new_div = div_type(
                    id = div.id,
                    style = None if len(merged_attr["styles"]) == 0  else merged_attr["styles"],
                    begin = div.begin,
                    end = div.end,
                    lang = merged_attr["lang"],
                    region = merged_attr["region"],
                    metadata= merged_attr["metadata"]
                )   
                new_div.p.append(c.value)
                new_divs.append(new_div)
        
        return new_divs

    @staticmethod
    def recurse_span(span, span_styles = []):
        if span.style is not None:
            span_styles = span.style + span_styles
        new_spans = []
        for sc in span.orderedContent():
            if isinstance(sc.value,span_type):
                new_spans.extend(Denester.recurse_span(sc.value, span_styles))
            else:
                new_span = span_type(
                    sc.value
                )
                new_span.style = span_styles
                new_spans.append(new_span)
        return new_spans
                

if __name__ == '__main__':
    xml_file = "testing/bdd/templates/nested_spans_hardcoded.xml"
    with open(xml_file, 'r') as in_file:
        input_xml = in_file.read()
    input_xml = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", input_xml)
    ebutt3 = EBUTT3Document.create_from_xml(input_xml)
    Denester.denest(ebutt3)