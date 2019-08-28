from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import div_type
import copy


class Denester():
    @staticmethod
    def denest(document):

        return document

    @staticmethod
    def convert_div(div_in, passed_properties=None):
        if len(div_in.orderedContent()) == 0:
            return None
        #if ordered content has a div in it
        if len(div_in.div) != 0:
            divs = div_in.div
            if passed_properties == None:
                passed_properties = {}
                passed_properties["styles"] = div_in.style
                passed_properties["region"] = div_in.region
                passed_properties["metadata"] = "temp"
                passed_properties["language"] = "temp"
            else:
                passed_properties = Denester.setup_properties(passed_properties, div_in.style, div_in.region, "temp", "temp")

            passed_properties
            #passed_properties += my_properties (4 properties, style, regions, metadata, language)
                # If they have different styles: they can safely be merged
                # If they have different regions: this is an error: proceed as if the child div does not exist
                # If they have different metadata: merge it
                # If they have different language content - the child div's xml:lang overrides the parent's
                # If they have different begin and end times on them - these will be discarded anyway after computing the leaf span timings

            #for div in divs
                #convert_div(div, passed_properties)

        #use properties, own and inherited
        #delete any divs that are inside ordered content, they have already been converted and put in body at this stage
        #div might be empty now, re-check that it has any content
        new_elem = div_type(
            # *self.convert_children(div_in),   how to pass in children without trying to convert them?
            div_in.orderedContent(),
            id=div_in.id,
            region=div_in.region,
            style=div_in.style,
            agent=div_in.agent
        )
        #put new elem in body

    @staticmethod
    def setup_properties(passed, style, region, metadata, language):
        
        passed["styles"] = style.append(passed["styles"])
        if passed["region"] != region:
            raise Exception
        passed["metadata"] 

        return passed

    # def convert_children(self, element):
    #     """
    #     Recursive step
    #     :param element:
    #     :param dataset:
    #     :return:
    #     """
    #     output = []

    #     children = element.orderedContent()

    #     for item in children:
    #         if isinstance(item, NonElementContent):
    #             output.append(copy.deepcopy(item.value))
    #         elif isinstance(item, ElementContent):
    #             conv_elem = self.convert_div(item.value)

    #             if conv_elem is not None:
    #                 output.append(conv_elem)
    #         else:
    #             raise Exception('Can this even happen!??!?!?!')
    #     return output
