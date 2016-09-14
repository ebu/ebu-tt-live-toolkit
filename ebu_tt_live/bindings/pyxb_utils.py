"""
This file contains those bits and pieces that are necessary to give PyXB extra functionality.
"""

import threading
import logging
import copy
from pyxb.binding.basis import NonElementContent, ElementContent, complexTypeDefinition

log = logging.getLogger(__name__)

__xml_parsing_context = threading.local()
__xml_parsing_context.parsing = False


def get_xml_parsing_context():
    """
    The parsing context is a simple python dictionary that helps tie together semantic rules at parsing time.

    For example: making sure that limitedClockTimingtype and fullClockTimingType are instantiated appropriately taking
    into account the timeBase attribute on the tt element. In that case when the timeBase element is encountered by the
    parser is is added to the parsing context object to help PyXB make the right type in the timingType union.

    :return: dict that is te parsing context for the currently running parser
    :return: None if not in parsing mode
    """
    log.debug('Accessing xml_parsing_context: {}'.format(__xml_parsing_context))
    if __xml_parsing_context.parsing is False:
        # We are not in parsing mode
        return None
    return __xml_parsing_context.context


def reset_xml_parsing_context(parsing=False):
    log.debug('Resetting xml_parsing_context: {}'.format(__xml_parsing_context))
    __xml_parsing_context.context = {}
    __xml_parsing_context.parsing = parsing


class xml_parsing_context(object):
    """
    This context manager is helpful to inject a thread local parsing context into the XML parser to be able to control
    its type choices based on semantic rules. The context manager makes sure the context is renewed every time a new
    document is parsed. This prevents unwanted correlation between documents.
    """

    def __enter__(self):
        reset_xml_parsing_context(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        reset_xml_parsing_context()


class RecursiveOperation(object):
    """
    A recursive operation can be a validation of the content model, a full- or partial copy of the document tree, the
    splicing of two documents together or conversion of one document format to another. This class contains the
    generic content iteration logic with hook functions that are meant to be customized by descendant classes.
    """

    __filter_criteria = None
    __root_element = None
    __post_order = None

    def __init__(self, root_element, filter=None, post_order=False):
        """
        This class requires a root element to operate on and an optional filter function to help limit the elements
        selected for the operations defined in the hook functions thereby reducing their complexity and improving
        general processing speeds.
        :param root_element: Practically the document root but could be any PyXB type instance that has children
        :param filter: A function that filters the elements selected for processing.
        :param post_order(boolean): Post order processing during the traversal. Defaults to False(pre-order).
        """
        if filter is None:
            self.__filter_criteria = lambda x: True
        else:
            self.__filter_criteria = filter

        self.__root_element = root_element
        self.__post_order = post_order

    def _process_children(self, element_value, **kwargs):
        """
        Recursive step
        :param element:
        :param dataset:
        :return:
        """
        output = []

        if isinstance(element_value, complexTypeDefinition):
            children = element_value.orderedContent()

            for item in children:
                proc_elem = self._recursive_step(element=item, **kwargs)
                if proc_elem is not None:
                    output.append(proc_elem)
        return output

    def _recursive_step(self, element, **kwargs):
        children = []
        proc_value = None
        element_value = element.value
        if isinstance(element, ElementContent) and self.__filter_criteria(element) is True:
            self._before_element(value=element_value, element=element, **kwargs)

            if self.__post_order:
                children = self._process_children(value=element_value, element=element, **kwargs)
                proc_value = self._process_element(value=element_value, element=element, proc_value=proc_value, children=children, **kwargs)
            if not self.__post_order:
                proc_value = self._process_element(value=element_value, element=element, **kwargs)
                children = self._process_children(value=element_value, element=element, proc_value=proc_value, **kwargs)

            self._after_element(value=element_value, element=element, proc_value=proc_value, children=children, **kwargs)
        else:
            proc_value = self._process_non_element(value=element_value, non_element=element, **kwargs)
        return proc_value

    def proceed(self, **kwargs):
        self._recursive_step(self.__root_element, **kwargs)

    def _before_element(self, value, element=None, **kwargs):
        return None

    def _process_element(self, value, element=None, **kwargs):
        raise NotImplementedError()

    def _process_non_element(self, value, non_element, **kwargs):
        raise NotImplementedError()

    def _after_element(self, value, element=None, **kwargs):
        return None
