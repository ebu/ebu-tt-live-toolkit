Validation framework
====================

The validation framework consists of 2 kinds of validation: syntactic and semantic. The PyXB library does
a pretty good job validating the syntax but it does not provide any tooling to process any semantics that could not
be described in XSD 1.0 (PyXB does not understand XSD 1.1 and xpath assertions).

Example:
    If ttp:timebase="clock" then all begin and end attributes of timed elements shall be of type ebuttdt:clockTimingType.

Elements/types are independent and according to the principles of OOP they do not know much about one another.
In order to provide semantic validation there is need for a semantic validation context.
A common object that shared information can be collected to and each type/element receives it as a parameter in its
semantic validation hooks if the element needs to take part in the semantic validation process.

For an element to be part of the semantic validation flow it needs to inherit the
:py:class:`ebu_tt_live.bindings.validation.SemanticValidationMixin` mixin, which contains the boilerplate
that enables semantic validation and the hook functions, that the developer can override and write custom
functionality that effectively does the semantic validation of the type.


EBU-TT Part 1, EBU-TT Part 3 and EBU-TT-D constraints
=====================================================

EBU-TT Part 3 (EBU Tech3370) is derived from EBU-TT Part 1 (Tech3350).
Some of the changes are required syntactic additions, such as the sequence
identifier and sequence number. Others are relaxations, such as the permission
to omit elements such as ``styling`` and ``layout``.

Conversely EBU-TT-D is a complete syntactic and semantic subset of EBU-TT Part 1. There are two ways that we can code for these differences. 

The first is by creating **similar XML Schemas**, one for each flavour that we
want to support. This allows PyXB to validate the syntactic restrictions, and
might allow us to use vanilla off-the-shelf XML Schemas for these types.
However, they are all flavours of TTML, and so they use the same namespaces.
This is hard to manage in PyXB, without having completely separate
implementations for each type, with a lot of duplication.

The second is by creating a **single XML Schema**, which enforces only the more
relaxed constraints, and then coding additional validation rules in our own
classes. This is a little awkward to manage in PyXB, because PyXB needs to
instantiate an object of a known type for every XML element that it finds, and
it doesn't allow for some kind of selective choice. The calling code can
call ``_SetSupersedingClass()`` on the raw binding class, which registers the
type to create.

Given these two non-ideal options, we decided to use both!

EBU-TT Part 1 and EBU-TT Part 3
-------------------------------

We have one XML Schema for both of these, and put validation rules into the
classes. For example we need to ensure that ``ebuttp:sequenceIdentifier`` is
absent from the root ``tt`` element in a Part 1 document. Conversely we need
to check that it is present in a Part 3 document.

We do this by creating a 
:py:class:`ebu_tt_live.bindings.tt_type` class that is the basis of Part 3 documents and has a
:py:func:`ebu_tt_live.bindings.tt_type._validateBinding_vx` method
that raises an exception if the attribute is absent.

Then for Part 1 documents we make a sub-class of the `tt_type` called
:py:class:`ebu_tt_live.bindings.tt1_tt_type` whose 
:py:func:`ebu_tt_live.bindings.tt1_tt_type._validateBinding_vx` method
explicitly checks for the presence of the attribute and raises an
exception if it is there. This method does *not* call the base class's
method of the same name, otherwise we would always get an exception for
every document!

How can we have two classes for an XML element with the same qualified name?
We have to tell PyXB which class to use when making a Python object for the
element, and this is done using ``_SetSupersedingClass()``. For most elements
we only have to do this once, but for these two variants of the ``tt``
element we have to understand the context of the document and adjust the
setting before processing, otherwise PyXB gets very confused and starts
to throw exceptions.

There is a utility function provided to make this easier,
:py:func:`ebu_tt_live.bindings.load_types_for_document`, which takes one of
two values, either ``ebutt1`` for Part 1 documents or ``ebutt3`` for Part 3
documents, and makes sure PyXB is set up correctly.

This feels a bit ugly but does work. When code doesn't behave in an
expected way, the solution is sometimes to make sure that the right types
are loaded!

EBU-TT Part 3 and EBU-TT-D
--------------------------

The differences between EBU-TT Part 3 and EBU-TT-D are more significant, with
EBU-TT-D having many more restrictions on content structure and value.
Here, we use a separate XML Schema Document (XSD) so PyXB does the heavy
lifting, and create specific subclasses prefixed `d_`, such as
:py:class:`ebu_tt_live.bindings.d_tt_type` so that we can perform the
required checks, conversions etc.

This is straightforward in all but one respect: the namespace of the
root element is the same for both document formats, so how can we tell PyXB
which is which? The answer is a hack!
:py:func:ebu_tt_live.documents.EBUTTDDocument.create_from_xml changes the
root element tag from ``tt`` to ``ttd``, and the XSD has a whole separate
set of definitions for this made-up ``ttd`` root element.
Then when we serialise the EBU-TT-D document object back into XML, in
:py:func:`ebu_tt_live.bindings.d_tt_type.toDOM`, we explicitly fix the
element name back to ``tt``.

Using this method, we don't have to worry about setting superseding
classes dynamically, because each ``d_*`` type has its own explicit class,
and we set the superseding class just once for each. PyXB doesn't get
confused by this, because it knows the processing context.


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
:py:class:`ebu_tt_live.bindings.PyXB_utils.xml_parsing_context` context manager there is a threadLocal object that
keeps a similar dictionary to the one used at the semantic validation. The difference is that the
:py:func:`ebu_tt_live.bindings.CreateFromDocument` function resets the context by using the context manager
class and instead of the context being passed around as a parameter among functions the binding classes call the
:py:func:`ebu_tt_live.bindings.pyxb_utils.get_xml_parsing_context` function to gain access to the parsing context object.
