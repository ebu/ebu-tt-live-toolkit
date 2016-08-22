[![Build Status](https://api.travis-ci.org/ebu/ebu-tt-live-toolkit.svg?branch=master)](https://travis-ci.org/ebu/ebu-tt-live-toolkit) 
[![Coverage Status](https://coveralls.io/repos/github/ebu/ebu-tt-live-toolkit/badge.svg?branch=ebu_master)](https://coveralls.io/github/ebu/ebu-tt-live-toolkit?branch=ebu_master)

# ebu-tt-live-toolkit

This is the repository for the interoperability kit of [EBU-TT Live](https://tech.ebu.ch/publications/tech3370). 

The kit is envisaged to contain a set of components for generating, testing and distributing subtitle documents in EBU-TT Part 3 format.

This is an open source project. Anyone is welcome to contribute to the development of the components. Please see the [wiki](https://github.com/ebu/ebu-tt-live-toolkit/wiki) for the list of required components, guidelines and release plan. 

We have a Slack team called [ebu-tt-lit](https://ebu-tt-lit.slack.com) for day to day communications, questions etc. Please join up!

If you would like to contribute or join the Slack team, please contact <subtitling@ebu.ch> or <nigel.megitt@bbc.co.uk>

Preparing the build environment
===============================

Make sure you have python 2.7+. Make sure you have python virtual environment capability.

If not you can install virtualenv systemwide from your operating system's package repository
or by pip:

    sudo pip install virtualenv

After that creating a virtual environment should be as simple as:

    virtualenv env

Let's activate it (source makes sure the current shell executes the script
and assumes the environment variables that the activation script sets):

    source ./env/bin/activate

To build the project you will also need node.js. Please read the instructions for your system [here](https://nodejs.org/en/download/package-manager/).

After having created the python virtual environment, having activated it and having installed node.js the package
can be built by typing make if you have GNU build tooling on your system.

    make


Alternatively:

    pip install -r requirements.txt
    python setup.py develop

    pyxbgen --binding-root=./ebu_tt_live/bindings/ebutt_live -m __init__ --schema-root=./ebu_tt_live/xsd/ebutt_live -r -u ebutt_live.xsd
    pyxbgen --binding-root=./ebu_tt_live/bindings/ebutt_d -m __init__ --schema-root=./ebu_tt_live/xsd/ebutt_d -r -u ebutt_d.xsd

    npm install nunjucks
    node_modules/nunjucks/bin/precompile ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.xml > ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.js

After this you are supposed to be able to launch the command line tools this python package
provides i.e.:

    ebu-dummy-encoder
    
Windows users
=============

Windows is not the best friend of Makefiles. So there is a make.bat file for those who would like to develop using 
Windows. Assuming python 2.7 and virtualenv is installed and are on the PATH. To build the project you will also need node.js. Please read the instructions for your system [here](https://nodejs.org/en/download/package-manager/). Then run :

    make

This will make sure a virtual environment is created and activated and installs all the tools into it.

After that the following command should work:

    ebu-dummy-encoder

The Schema definitions XSD
==========================

The schema definitions are to be found embedded in the Python library in the xsd subfolder.

##### The EBU TT Live XSD 

The XSD resides in xsd/ebutt_live folder. The root schemadocument is called [ebutt_live.xsd](xsd/ebutt_live/ebutt_live.xsd).

##### The EBU TT D XSD

The XSD resides in xsd/ebutt_d folder. The root schemadocument is called [ebutt_d.xsd](xsd/ebutt_d/ebutt_d.xsd)

The Python library
==================

The library uses XSD schemas from the xsd subdirectory.
The bindings will keep the validation sane and PyXB makes sure that updates are working as
expected. Should the schema be modified a regeneration can be run and the bindings will respect
the changes.

Scripts
=======

There are several scripts that emulate different components in the infrastructure. Assuming the Makefile worked,
the package is installed in a virtual environment and the virtual environment is active the following scripts should
be available directly from the command line.

The simple producer is the beginning of the data pipeline. It generates
EBU-TT-Live documents in a timed manner. In the repository root there is a *test.html* file that can be used for manual testing of the producer in any websocket capable browser.

    ebu-simple-producer

The simple consumer connects to the producer or later on in the pipeline, assuming there are more components inserted.

    ebu-simple-consumer

The user input consumer script is intended to receive data from the user input producer. The user input producer is a user interface that allows users to create documents
and to send them live (see the documentation for details). To run it, just run `ebu-user-input-consumer` and open the file `ebu_tt_live/ui/user_input_producer/user_input_producer.html` file.

    ebu-user-input-consumer


Documentation
=============

The documentation framework uses the popular Sphinx documentation generating engine and autodoc plugins to give
developers the flexibility of writing Extra documentation interleaved with the autogenerated documentation created by
autodoc.

## Prerequisite: Graphviz

To display the images in the documentation, you need to have [Graphviz](http://www.graphviz.org/) installed and make sure the *dot* executable is on the PATH. For example, for users of [homebrew](http://brew.sh/):

    brew install graphviz

## Generating documentation

Documentation can be generated based on the sources in the docs/source directory. After having installed the packages in 
requirements.txt (which is done automatically by the make command) documentation can be generated by one of the 
following three ways:

 1 Calling setuptools

```Shell
python setup.py build_sphinx
```

 2 Running make in the docs directory where separate makefiles and a make.bat file is giving a variety of options.

```Shell
cd docs
make html
```

 3 Calling the sphinx-build command line script that comes with sphinx. WARNING: Platform-dependent path-separators.

```Shell
sphinx-build -b html docs/source/ docs/build/html
```

## Previewing the documentation

After sphinx finished with a successful execution log the generated documentation should be accessible by opening the 
docs/build/html/index.html in any web browser.

Tests
=====

The test framework is described in [CONTRIBUTING.md](CONTRIBUTING.md) 

How to contribute
=================

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) 
