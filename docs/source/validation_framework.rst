Validation framework
====================

The validation framework consists of 2 kinds of validation: syntactic and semantic. The PyXB library does
a pretty good job validating the syntax but it does not provide any tooling to process any semantics that could not
be described in XSD 1.0 (PyXB does not understand XSD 1.1 and xpath assertions).

Example:

    if tt:tt has timeBase=clock smpteTimingType must not be present anywhere in the document.

Elements/types are independent and according to the principles of OOP they do not know much about one another.
In order to provide semantic validation there is need for a semantic validation context.
A common object that shared information can be collected to and each type/element receives it as a parameter in its
semantic validation hooks if the element needs to take part in the semantic validation process.

For an element to be part of the semantic validation flow it needs to inherit the
:py:class:`ebu_tt_live.bindings.validation.SemanticValidationMixin` mixin, which contains the boilerplate
that enables semantic validation and the hook functions, that the developer can override and write custom
functionality that effectively does the semantic validation of the type.
