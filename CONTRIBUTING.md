
Coding style
============

In the main parts of the code follow the PEP8 code style guides.
https://www.python.org/dev/peps/pep-0008/

The style guide is not meant to be followed by code that directly interfaces with Twisted's
interfaces. Twisted predates the PEP8 style guidelines and PEP8 clearly states that backwards
compatibility in style is more important than compliance with this standard.

Twisted interfaces and mixins should belong to the ebu_tt_live.twisted subpackage and
should preferably be providing that functionality through mixins.
