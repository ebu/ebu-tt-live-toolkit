
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

For testing we use the py.test test runner. Based on the test type the test code can be in different locations.\

## For unittesting:

Inside the ebu_tt_live python package inside a test directory within the subpackage it is testing. 

    I.e.: To test the clocks create a test directory inside the ebu_tt_live/clocks package. __init__.py is not needed. Place python sourcefiles with testing modules
    
## Functional/integration testing

In the repository root outside the ebu_tt_live package in a directory called testing.
