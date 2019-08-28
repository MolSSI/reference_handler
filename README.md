reference_handler
==============================
[//]: # (Badges)
[![Travis Build Status](https://travis-ci.org/REPLACE_WITH_OWNER_ACCOUNT/reference_handler.png)](https://travis-ci.org/REPLACE_WITH_OWNER_ACCOUNT/reference_handler)
[![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/REPLACE_WITH_APPVEYOR_LINK/branch/master?svg=true)](https://ci.appveyor.com/project/REPLACE_WITH_OWNER_ACCOUNT/reference_handler/branch/master)
[![codecov](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/reference_handler/branch/master/graph/badge.svg)](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/reference_handler/branch/master)

A Python package that creates a consolidated list of references (BibTex, RIS) of scientific material 
used in a Python package.

### Motivation

Authors of modeling tools (scientific software, method or model
developers) currently find it difficult to get fair attribution to their
software and scientific work. Scientific software developers create
tools that do not always get cited, as a typical citable
scientific article might not exist. Although new mechanisms for more
directly citing software have been recently created (i.e. Zenodo), they have
not gained widespread use in the community of users. Therefore many
software developers feel forced to publish one or more papers on the 
software, adding more work and introducing a considerable delay.

Method and model developers face a similar problem. For instance, consider
force field developers who refine their parameters over time, creating a
new version of the force field on each iteration. The correct references
can only be determined by looking at the molecule and the parameters.

From the user point of view, it might be very time consuming to go find
the correct references for all software, model or methods 
used in a research work. This problem is exponentially exacerbated in work that
involves complex workflows running hundreds of different software
components.

## Goal

The goal of the Reference Handler is to provide an easy mechanism for
developers to record the appropriate references so that users of tools can
provide a complete set of citations for a particular run of the software in a
form convenient for the user. 

The output of the Reference Handler is a consolidated list of
references (BibTeX, RIS) to go into the paper with as little effort as possible on the users
part.

## Features

## Examples

## Installation

## Documentation

## Contribute

## Citation


### Copyright

Copyright (c) 2019, MolSSI

#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.0.
