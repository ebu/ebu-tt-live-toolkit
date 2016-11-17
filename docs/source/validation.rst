Document and sequence validation
================================

The validation of the documents require a semantic and a syntactic validation approach. Using the validation framework
the syntactic and semantic requirements can be fulfilled.

The conformance specification is in the SPEC-CONFORMANCE.md file, which contains the document semantics and their
explanations.

The validation framework uses a collection of mixins to add functionality to the XSD-derived datatypes and thereby
making it possible for us to add a granular functionality set that is the closest possible match to the datatype's
expected semantic behaviour. The validation is currently split into several source files in the validation package
based on the the general aspect they are applicable for.

  -  The :py:mod:`ebu_tt_live.bindings.validation.validator` contains the general validator class that is controlling the
     validation flow and managing the traversal of the document tree. The validation mixing are implementing the callback
     interface expected by this class to interact with the semantic validation flow. This basically means that as the
     document tree is walked at each element the :py:class:`ebu_tt_live.bindings.validator.SemanticValidator` class checks
     if that element is implementing the SemanticValidationMixin interface and if so it calls callbacks on the way down the
     tree and all the way up.

.. toctree::
    validation_framework


