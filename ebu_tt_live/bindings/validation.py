"""
This file contains all the pyxb helpers needed for enabling a concise semantic validation approach.
"""

from pyxb import ValidationConfig, GlobalValidationConfig
import logging

log = logging.getLogger(__name__)


class SemanticValidationConfig(ValidationConfig):

    def __init__(self):
        log.warning('SemanticValidationConfig init {}'.format(hex(id(self))))

    def __del__(self):
        log.warning('SemanticValidationConfig deleted {}'.format(hex(id(self))))


class SemanticValidationMixin(object):

    _validationConfig_ = SemanticValidationConfig

    def _semantic_before_traversal(self):
        pass

    def _semantic_after_traversal(self):
        pass


class SemanticDocumentMixin(SemanticValidationMixin):

    def _semantic_before_validation(self):
        pass

    def _semantic_after_validation(self):
        pass

    def _validateBinding_vx(self):
        # Step1: Before
        self._semantic_before_validation()

        # Step2: DFS
        # This line is hacky as f*** and non-standard way of getting the desired behaviour but python and MRO are not
        # always man's best friend...
        self.__class__.__bases__[1]._validateBinding_vx(self)

        # Step3: Process current object
        self._semantic_after_validation()
