
Coding style
============

In the main parts of the code follow the PEP8 code style guides.
https://www.python.org/dev/peps/pep-0008/

The style guide is not meant to be followed by code that directly interfaces with Twisted's
interfaces. Twisted predates the PEP8 style guidelines and PEP8 clearly states that backwards
compatibility in style is more important than compliance with this standard.

Twisted interfaces and mixins should belong to the ebu_tt_live.twisted subpackage and
should preferably be providing that functionality through mixins.


Test Suite
==========

For testing we use the py.test test runner.

## Initialization of the test suite

After initializing the virtual environment and installing the package run either one of the following commands:

    python setup.py test

or:

    py.test
    
**TODO: make test should work as well once implemented**

## Structure

Based on the test type the test code can be in different locations.

### For unittesting

Inside the ebu_tt_live python package inside a test directory within the subpackage it is testing. 

    i.e.: To test the clocks create a test directory inside the ebu_tt_live/clocks package. __init__.py is not needed. Place python sourcefiles with testing modules
    
### Functional/integration testing

In the repository root outside the ebu_tt_live package in a directory called testing.
Structure of the testing directory

    testing
    ├─bdd - Behaviour Driven Development
    │ ├─features - feature files for BDD
    │ │ ├─validation - features that tie in with the XML validation functionality
    │ │ │ └─*.feature - BDD feature files
    │ │ ├─timing - features that tie in with computed/resolved/activation times computation.
    │ │ └─...
    │ ├─templates - Jinja2 template files for mostly XML documents
    │ │ ├─*.xml - XML file templates
    │ │ └...
    │ └*.py - Python files with the BDD handlers
    └─*.py - Other python based tests unrelated to BDD

For BDD tests we use [pytest-bdd](https://pypi.python.org/pypi/pytest-bdd). Beware that some BDD steps are defined in the `testing/bdd/conftest.py` file because they are used by multiple feature files.


## Configuration files

Testing configuration files are mostly in the project root:

    pytest.ini - Pytest settings and command line switches
    .coveragerc - Coverage settings and exclusion patterns
    setup.cfg - setup.py integration settings
    
## Testing output

Test suite generates multiple outputs:

    htmlcov/ - Coverage of the ebu_tt_live python package in HTML for review
    .coverage - Python raw coverage output
    coverage.xml - Coverage data that XML based CI integration tools such as Jenkins Cobertura Plugin can understand and use

