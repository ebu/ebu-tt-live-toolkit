"""
This file contains those bits and pieces that are necessary to give PyXB extra functionality.
"""

import threading
import logging
from ebu_tt_live.errors import StopBranchIteration
from pyxb.binding.basis import NonElementContent, ElementContent, complexTypeDefinition
from pyxb.exceptions_ import NotComplexContentError


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

    _filter_criteria = None
    _root_element = None
    _post_order = None
    _children_iterator = None

    def __init__(self, root_element, filter=None, post_order=False, children_iterator=None):
        """
        This class requires a root element to operate on and an optional filter function to help limit the elements
        selected for the operations defined in the hook functions thereby reducing their complexity and improving
        general processing speeds.
        :param root_element: Practically the document root but could be any PyXB type instance that has children
        :param filter: A function that filters the elements selected for processing.
        :param post_order(boolean): Post order processing during the traversal. Defaults to False(pre-order).
        :param children_iterator: PyXB has multiple ways it likes to traverse the structure. It can be based on the
        order described in the XSD or it can be the order described by the document that is using that schema. The
        value of this parameter will be resolved on matching complexTypeDefinition objects and called to give children
        in the specified order.
        """
        if filter is None:
            self._filter_criteria = lambda value, element: True
        else:
            self._filter_criteria = filter

        self._root_element = root_element
        self._post_order = post_order

        if children_iterator is None:
            self._children_iterator = 'orderedContent'
        else:
            self._children_iterator = children_iterator

    def _process_children(self, value, element=None, proc_value=None, **kwargs):
        """
        Recursive step
        :param element:
        :param dataset:
        :return:
        """
        output = []

        if isinstance(value, complexTypeDefinition):
            try:
                children = getattr(value, self._children_iterator)()
            except NotComplexContentError:
                return output

            for item in children:
                try:
                    proc_elem = self._recursive_step(value=item.value, element=item, parent_binding=value, **kwargs)
                    if proc_elem is not None:
                        output.append(proc_elem)
                except StopBranchIteration:
                    # Moving on...
                    continue

        return output

    def _recursive_step(self, value, element, parent_binding=None, **kwargs):
        children = []
        proc_value = None
        element_value = value
        if (element is not None and isinstance(element, ElementContent) or element is None) \
                and self._filter_criteria(value, element) is True:
            self._before_element(value=element_value, element=element, parent_binding=parent_binding, **kwargs)

            if self._post_order:
                children = self._process_children(value=element_value, element=element, **kwargs)
                proc_value = self._process_element(
                    value=element_value, element=element, parent_binding=parent_binding,proc_value=proc_value,
                    children=children, **kwargs)
            if not self._post_order:
                proc_value = self._process_element(
                    value=element_value, element=element, parent_binding=parent_binding, **kwargs)
                children = self._process_children(value=element_value, element=element, proc_value=proc_value, **kwargs)

            self._after_element(value=element_value, element=element, parent_binding=parent_binding, proc_value=proc_value, children=children, **kwargs)
        else:
            proc_value = self._process_non_element(
                value=element_value, non_element=element, parent_binding=parent_binding, **kwargs)
        return proc_value

    def proceed(self, **kwargs):
        return self._recursive_step(value=self._root_element, element=None, **kwargs)

    def _before_element(self, value, element=None, parent_binding=None, **kwargs):
        return None

    def _process_element(self, value, element=None, parent_binding=None, **kwargs):
        raise NotImplementedError()

    def _process_non_element(self, value, non_element, parent_binding=None, **kwargs):
        raise NotImplementedError()

    def _after_element(self, value, element=None, parent_binding=None, **kwargs):
        return None
