from ebu_tt_live.bindings import tt_type, d_tt_type, body_type, d_body_type, div_type, d_div_type, \
    p_type, d_p_type, span_type, d_span_type, br_type, d_br_type
import copy
from pyxb.binding.basis import NonElementContent, ElementContent


class EBUTT3EBUTTDConverter(object):

    @classmethod
    def convert_tt(cls, tt_in, dataset):
        return d_tt_type

    @classmethod
    def convert_body(cls, body_in, dataset):
        return d_body_type

    @classmethod
    def convert_div(cls, div_in, dataset):
        return d_div_type

    @classmethod
    def convert_p(cls, p_in, dataset):
        return d_p_type

    @classmethod
    def convert_span(cls, span_in, dataset):
        return d_span_type

    @classmethod
    def convert_br(cls, br_in, dataset):
        return d_br_type(
            br_in.value,
            metadata=copy.deepcopy(br_in.metadata)
        )

    @classmethod
    def map_type(cls, in_element):
        if isinstance(in_element, tt_type):
            return cls.convert_tt
        elif isinstance(in_element, body_type):
            return cls.convert_body
        elif isinstance(in_element, div_type):
            return cls.convert_div
        elif isinstance(in_element, p_type):
            return cls.convert_p
        elif isinstance(in_element, span_type):
            return cls.convert_span
        elif isinstance(in_element, br_type):
            return cls.convert_br

    @classmethod
    def convert_children(cls, element, dataset):
        """
        Recursive step
        :param element:
        :param dataset:
        :return:
        """
        output = []

        children = element.orderedContent()

        for item in children:
            if isinstance(item, NonElementContent):
                output.append(copy.deepcopy(item.value))
            elif isinstance(item, ElementContent):
                output.append(cls.convert_element(item.value, dataset))
            else:
                raise Exception('Can this even happen!??!?!?!')
        return output

    @classmethod
    def convert_element(cls, element, dataset):
        converter = cls.map_type(element)
        return converter(element, dataset)
