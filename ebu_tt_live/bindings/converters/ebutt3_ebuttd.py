from ebu_tt_live.bindings import tt_type, d_tt_type, body_type, d_body_type, div_type, d_div_type, \
    p_type, d_p_type, span_type, d_span_type, br_type, d_br_type, d_metadata_type
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
        new_elem = d_div_type(
            cls.convert_children(div_in, dataset),
            metadata=copy.deepcopy(div_in.metadata),
            id=div_in.id,
            region=div_in.region,
            style=div_in.style,
            agent=div_in.agent,
            begin=div_in.begin,
            end=div_in.end
        )
        return new_elem

    @classmethod
    def convert_p(cls, p_in, dataset):
        new_elem = d_p_type(
            cls.convert_children(p_in, dataset),
            metadata=copy.deepcopy(p_in.metadata),
            space=p_in.space,
            begin=p_in.begin,
            end=p_in.end,
            lang=p_in.lang,
            id=p_in.id,
            region=p_in.region,
            style=p_in.style,
            agent=p_in.agent,
            role=p_in.role
        )
        return new_elem

    @classmethod
    def convert_span(cls, span_in, dataset):
        new_elem = d_span_type(
            cls.convert_children(span_in, dataset),
            space=span_in.space,
            begin=span_in.begin,
            end=span_in.end,
            lang=span_in.lang,
            id=span_in.id,
            style=span_in.style,
            agent=span_in.agent,
            role=span_in.role
        )
        return new_elem

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
