"""
This file contains all the pyxb helpers needed for enabling a concise semantic validation approach.
"""
import copy
import logging
import re

from pyxb.namespace import ExpandedName

from ebu_tt_live.errors import SemanticValidationError
from ebu_tt_live.strings import DOC_SYNTACTIC_VALIDATION_SUCCESSFUL, ERR_SEMANTIC_ID_UNIQUENESS
from pyxb.binding.basis import NonElementContent, ElementContent

log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class SemanticValidationMixin(object):
    """
    This mixin contains the necessary boilerplate to enable semantic validation as well as enabling _setAttribute hooks
    to help populate the context object with useful data.
    """

    # This dictionary exists to override attribute setters. Used in contextual parsing
    _attr_en_pre = {}
    _attr_en_post = {}

    def _setAttribute(self, attr_en, value_lex):
        uri_tuple = attr_en.uriTuple()
        if uri_tuple in self._attr_en_pre:
            self._attr_en_pre[uri_tuple](self, attr_en, value_lex)
        au = super(SemanticValidationMixin, self)._setAttribute(attr_en, value_lex)
        if uri_tuple in self._attr_en_post:
            self._attr_en_post[uri_tuple](self, au)
        return au

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        """
        Semantic validation preprocess hook.
        :param dataset: semantic context object
        :param element_content: the element itself
        """
        pass

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        """
        Semantic validation postprocess hook.
        :param dataset: semantic context object
        :param element_content: the element itself
        """
        pass

    def _do_link_copy_with_copied_parent(self, dataset, element_content, parent_binding):
        celem = dataset['instance_mapping'][self]
        # Link with parent
        cparent = dataset['instance_mapping'][parent_binding]

        if element_content.elementDeclaration.isPlural():
            cparent.append(celem)
        else:
            setattr(cparent, element_content.elementDeclaration.name().localName(), celem)

    def _semantic_before_copy(self, dataset, element_content=None):
        """
        Meant for checks before attempting to copy an element
        :param dataset:
        :param element_content:
        :return:
        """
        pass

    def _semantic_before_subtree_copy(self, copied_instance, dataset, element_content=None):
        """
        This is helpful hook function at the copying operation
        :param dataset:
        :param element_content:
        :return:
        """
        pass

    def _semantic_after_subtree_copy(self, copied_instance, dataset, element_content=None):
        """
        This is helpful hook function at the copying operation
        :param dataset:
        :param element_content:
        :return:
        """
        pass

    def _semantic_attributes_missing(self, attr_names):
        """
        Making sure that attributes specified in attr_names have no value defined on the binding.
        :param attr_names: The attributes that were defined on the element.
        :return:
        """
        result = [attr for attr in attr_names if getattr(self, attr) is None]
        return result

    def _semantic_attributes_present(self, attr_names):
        """
        Making sure that attributes specified in attr_names have a value defined on the binding
        :param attr_names: The missing attributes that were not defined.
        :return:
        """
        result = [attr for attr in attr_names if getattr(self, attr) is not None]
        return result

    def _semantic_copy(self, dataset):
        """
        This copy function is more powerful as it accepts an extra copying context where a smarter copy can be made.
        It can be customised by classes. The default is the shallow copy.
        :param dataset:
        :return: cloned element
        """
        return copy.copy(self)

    def merge(self, other_elem, dataset):
        """
        Try and merge the contents of 2 elements of the same type.
        :param other_elem:
        :return:
        """
        raise NotImplementedError()

    def _find_deconflicted_elem_by_id(self, elem_id, dataset):
        old_elem = dataset['tt_element'].get_element_by_id(elem_id)
        new_elem = dataset['instance_mapping'][old_elem]
        return new_elem

    def _semantic_deconflicted_ids(self, attr_name, dataset):
        """
        Looks up its referenced styles/region in the conversion mapping and returns the new idref string
        :param datset:
        :return:
        """
        old_elem_ids = getattr(self, attr_name)
        if old_elem_ids is None:
            return None

        if isinstance(old_elem_ids, basestring):
            new_elem = self._find_deconflicted_elem_by_id(elem_id=old_elem_ids, dataset=dataset)
            return new_elem.id
        else:
            new_elem_ids = []
            for elem_id in old_elem_ids:
                new_elem = self._find_deconflicted_elem_by_id(elem_id=elem_id, dataset=dataset)
                new_elem_ids.append(new_elem.id)
            return new_elem_ids

    def get_attribute_value(self, att_name):
        """
        This function is a handy extension that allows us to easily look up attribute values regardless whether they
        are local or namespaced attribute names. I did not find its equivalent in PyXB.
        :param att_name:
        :return:
        """
        attr_en = ExpandedName(*att_name.split(':'))
        # NOTE: At this point we should go to attribute map locate the attribute but for that the namespace has to be
        # located too because its fully qualified name is required... etc. cutting corners here as we don't mix local
        # and namespaced attributes of the same name so fairly safe to just take the localname bit. But this
        # is not a fully XML compliant way to support all possibilities in all cases.
        return getattr(self, attr_en.localName())


class SemanticDocumentMixin(SemanticValidationMixin):

    _validator_class = None

    def _semantic_before_validation(self):
        """
        Before PyXB starts its syntactic validation this hook runs where the user may execute custom code.
        """
        pass

    def validateBinding (self, **extra_kwargs):
        """Check whether the binding content matches its content model.

        @return: C{True} if validation was not performed due to settings.
        @return: Complex result dictionary with success and semantic_dataset keys.
        @raise pyxb.BatchContentValidationError: complex content does not match model # Wondering about this...
        @raise pyxb.SimpleTypeValueError: attribute or simple content fails to satisfy constraints
        """
        if self._performValidation():
            # Step1: Before
            self._semantic_before_validation()
            # Step2: DFS of syntactic validation
            self._validateBinding_vx()
            # Step3: DFS of semantic validation
            validator = self._validator_class(root_element=self)
            result = validator.proceed(**extra_kwargs)
            return {
                "success": True,
                "semantic_dataset": result
            }
        return True


class IDMixin(object):
    """
    Making sure the IDs are collected and maintained appropriately
    """

    _re_ebu_id_deconflict = re.compile('SEQ([0-9]+)\.(.*)')
    _tp_ebu_id_deconflict = 'SEQ{sequence_number}.{original_id}'

    def deconflict_id(self, seq_num):
        if self.id is not None:
            self.id = self._tp_ebu_id_deconflict.format(
                sequence_number=seq_num,
                original_id=self.id
            )

    def _semantic_register_id(self, dataset):
        ebid = dataset['elements_by_id']
        if self.id is not None:
            if self.id in ebid:
                raise SemanticValidationError(
                    ERR_SEMANTIC_ID_UNIQUENESS.format(
                        id=self.id
                    )
                )
            ebid[self.id] = self
