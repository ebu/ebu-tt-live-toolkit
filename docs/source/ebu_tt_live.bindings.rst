bindings Package
================

This package contains 2 sets of bindings, which are directly generated from XML
(these are the [ebutt_live,ebutt_d]/raw/*.py also ignored in the gitignore) and every generated file has a pair
outside the raw folder where the extensions are meant to go.

Most of this toolkit is built around the EBU TT Live specification and therefore whenever bindings are referred to it
mostly means those in ebutt_live.

The EBU TT D bindings are present to make te EBU TT Live -> EBU TT D conversion easier and more reliable.

Subpackages
-----------

.. toctree::
    ebu_tt_live.bindings.ebutt_live
    ebu_tt_live.bindings.ebutt_d
