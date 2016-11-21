Source code reference
=====================

The toolkit is implemented inside the ebu_tt_live python package. The following reference helps to get an insight of
what the different components and classes are responsible for.

Layout of the source files
--------------------------

The sources comprise subpackages and submodules to create a modular system that can be configured as required by the
user. The very quick overview before the generated source code reference hopefully helps find one's bearings faster.

  Code Structure : ::

     ebu_tt_live
     ├─bindings - PyXB based bindings and custom code that provides advanced validation functionality
     │ ├─raw - Low-level PyXB generated code based on the XSD schema definitions in ebu_tt_live/xsd
     │ ├─converters - Low-level converters to convert bindings from one schema to another
     │ ├─validation - Custom extension python mixins that are used for adding semantic validation functionality to binding types
     │ └*.py - Custom extension code importing bindings from the raw package and enhancing them with extra functions such as validation capability
     ├─carriage - Carriage Mechanism classes to be used by the Nodes
     ├─clocks - Various reference clock implementations
     ├─documents - Document wrapper classes wrapping bindings into an less cluttered interface
     ├─example_data - Built-in data files that are used to make the tools easier to run
     ├─node - Processing node code mostly on the document level independent on carriage mechanism implementation
     ├─scripts - Console scripts that make things easier to run
     ├─twisted - Carriage implementations using the twisted framework(currently websocket server and client classes)
     ├─ui - Files needed to run the User Input Producer webapp
     ├─xsd - Schema definitions
     ├errors.py - Custom Exception types for the Toolkit
     ├strings.py - Various error and response strings in t translatable format all in one place for easy translation
     └utils.py - Standalone utilities independent from the live toolkit but used by the toolkit for some tasks

Subpackages
-----------

.. toctree::

    ebu_tt_live.bindings
    ebu_tt_live.carriage
    ebu_tt_live.clocks
    ebu_tt_live.configspec
    ebu_tt_live.documents
    ebu_tt_live.example_data
    ebu_tt_live.node
    ebu_tt_live.scripts
    ebu_tt_live.twisted

:mod:`errors` Module
--------------------

.. automodule:: ebu_tt_live.errors
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`strings` Module
---------------------

.. automodule:: ebu_tt_live.strings
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`utils` Module
-------------------

.. automodule:: ebu_tt_live.utils
    :members:
    :undoc-members:
    :show-inheritance:



