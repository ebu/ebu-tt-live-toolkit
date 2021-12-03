DeDuplication of EBU-TT-Live documents
======================================

When documents are ReSequenced, duplication of ``style`` and ``region`` elements
and attributes can occur. To address this, the DeDuplicator node processes the
document(s) with the
:py:func:`ebu_tt_live.node.deduplicator.DeDuplicatorNode.remove_duplication` function.

After copying ``styling`` and ``layout`` into a ``list()`` and setting them up for new
``style`` and ``region`` elements, respectively, the ``list()`` is passed through the
:py:func:`ebu_tt_live.node.deduplicator.DeDuplicatorNode.CollateUniqueVals` function.

Because ``style`` and ``region`` elements can have ``style`` attributes, these
are deduplicated first. At this stage, it's possible that where two identical elements
that differed only in their style references, these may end up looking the same.
Each element is then passed through the
:py:class:`ebu_tt_live.node.deduplicator.ComparableElement` class, which processes
each attribute, omitting the ``xml:id`` and using the
:py:func:`ebu_tt_live.node.deduplicator.ReplaceNone` function to replace empty
attributes with a non-legal character to avoid collisions, and assigns a hash
to each element. The hash is then stored in ``old_id_dict`` as a key-value pair,
where the ``xml:id`` is the ``key`` and the hash is the ``value``. The hash is also stored
in ``hash_dict`` where the hash is the ``key``, and the ``value`` is the contents of the element.

The ``list()`` is then passed through the :py:func:`ebu_tt_live.node.deduplicator.DeDuplicatorNode.AppendNewElements`
function, which takes in the list of elements, the path to the parent element
(``styling`` or ``layout``), ``old_id_dict``, ``new_id_dict`` and ``hash_dict``

The function iterates through the key-value pairs of ``hash_dict`` and the contents
of the list of elements; where the ``xml:id`` of both matches, the element is appended to
the parent element. The hash and ``xml:id`` is then stored in ``new_id_dict``,
where the hash is the ``key`` and the ``xml:id`` is the ``value``.

In the final step, before emitting the document, the document as it is at this stage is passed
through the :py:class:`ebu_tt_live.node.deduplicator.ReplaceStylesAndRegions` class.
This utilises RecursiveOperation i.e. this class is used to recursively fix
the style and region attribute values, by addressing where a ``style`` or ``region``
attribute has been declared, and replaces the reference to the old ``xml:id`` with
the new one stored in ``new_id_dict``, which is done by taking the reference to
the old ``xml:id``, matching it to the key in ``old_id_dict`` to find the hash
``value``, then matching the hash to the ``key`` in ``new_id_dict`` to get the
new ``xml:id`` reference. While doing this, it also deduplicates instances where
multiple ``style`` attributes have been referenced, removing duplicates while
maintaining the hierarchy in which they were declared.
