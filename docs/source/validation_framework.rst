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


Semantic parser patch
=====================

PyXB uses the same bindings and same object model for 2 very different purposes. On one hand it allows the user
to programmatically create syntactically valid XML documents, on the other hand it can pick up an XML document and
parse it.  When the document is parsed PyXB does most of the heavy lifting and the user does not have much access
to the logic of the parser. The problem with this parser is the fact that it does not hold on to semantic context so
it follows the XSD and instantiates the elements/attributes using the values from the parsed xml. The problem occurs
when 2 types are just vaguely similar and they belong in the same union in the structure so the parser based on the
information it has in context cannot make a decision which one to instantiate. This causes however an issue with
the timingType union, which has fullClockTimingType and limitedClockTimingType. In the first 99 hours the 2 type
overlaps in values so PyXB will instantiate the first one it can and continues on to the next attribute. This conflicts
with the semantic validation, which expects particularly one timing type in that case and it may receive the wrong one.

Hence the SemanticValidationMixin also has an overloaded _setAttribute function, which applies 2 hooks for the types
in which custom code can enforce the right behaviour. The complexity and layered architecture of the parser limits the
capability to pass around a context object the same way the semantic validation can so in the
:py:class:`ebu_tt_live.bindings.pyxb_utils.xml_parsing_context` context manager there is a threadLocal object that
keeps a similar dictionary to the one used at the semantic validation. The difference is that the
:py:func:`ebu_tt_live.bindings.CreateFromDocument` function resets the context by using the context manager
class and instead of the context being passed around as a parameter among functions the binding classes call the
:py:func:`ebu_tt_live.bindings.pyxb_utils.get_xml_parsing_context` function to gain access to the parsing context object.
