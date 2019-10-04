reference_handler
==============================
[//]: # (Badges)
[![Travis Build Status](https://travis-ci.org/molssi/reference_handler.png)](https://travis-ci.org/molssi/reference_handler)
[![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/REPLACE_WITH_APPVEYOR_LINK/branch/master?svg=true)](https://ci.appveyor.com/project/molssi/reference_handler/branch/master)
[![codecov](https://codecov.io/gh/molssi/reference_handler/branch/master/graph/badge.svg)](https://codecov.io/gh/molssi/reference_handler/branch/master)
[![Documentation Status](https://readthedocs.org/projects/reference-handler/badge/?version=latest)](https://reference-handler.readthedocs.io/en/latest/?badge=latest)

A Python package that creates a consolidated list of references (BibTex, RIS) of scientific material 
used in a Python package.

### Motivation

Authors of modeling tools (scientific software, method or model
developers) currently find it difficult to get fair attribution to their
software and scientific work. Scientific software developers create
tools that do not always get cited, as a typical citable
scientific article might not exist. Although new mechanisms for more
directly citing software have been recently created (i.e. Zenodo), they have
not gained widespread use in the community of computational
molecular science. 

Method and model developers face a similar problem. Consider for instance 
a molecular dynamics practitioner who needs to develop a new force field using
a specialized quantum mechanical calculation. The practitioner might not be
fully familiar with the correct references to use for the quantum mechanical software
and methods. To correctly
include the references, the model developer might spend a considerable amount of time
finding out which papers to cite. This problem is exponentially exacerbated in work that
involves complex workflows running hundreds of different software
components that might involve different areas of computational science.

## Goal

The goal of the *reference handler* is to provide an easy mechanism for
developers to record the appropriate references so that users of tools can
provide a complete set of citations for a particular run of the software in a
form convenient for the user. 

The output of *reference handler* is a consolidated list of
references (BibTeX, RIS) to go into the paper with as little effort as possible on the users
part.

## Audience

**1. Method and scientific software developers.** 

**2. Computational molecular science practitioners**

## Package overview

The reference handler is comprised of the following: 

**1. Central SQLite3 database.** It contains two tables. 
The first is named *citation* and holds the essential data associated to each unique
citation, such as the raw citation text and its ID number. 
The second is the *context* table. It
contains information about the context in which a given citation was used. For instance, 
the function where the citation was used or the number of times the citation was "mentioned" 
by any function of your Python package.

Each citation can have many contexts, yielding a one-to-many relationship between the two
tables. 

**2. Functions to ease the interaction with central database. ** Examples are a function
to cite a desired reference or a function to dump the contents of the database into a 
.bib file for subsequent compliation using BibTeX.

## Minimal example

```python
import reference_handler

lj_citation = """
@article{lj1924,
author = {J. E. Jones  and Sydney Chapman },
title = {On the determination of molecular fields. \&\#x2014;II. From the equation of state of a gas},
journal = {Proceedings of the Royal Society of London. Series A, Containing Papers of a Mathematical and Physical Character},
volume = {106},
number = {738},
pages = {463-477},
year = {1924},
doi = {10.1098/rspa.1924.0082},
}
"""

def lennard_jones(sigma, epsilon, rij):
    rf.cite(raw=lj_citation, alias='lj_citation', module='lennard_jones',
        level=1, note='The first version of the Lennard-Jones potential')
    sig_by_r6 = (sigma / rij ** 6)
    sig_by_r12 = (sig_by_r6 ** 2)
    return 4.0 * epsilon * (sig_by_r12 - sig_by_r6)

rf = reference_handler.Reference_Handler('database.db')

sigma = 3.54
epsilon = 98.0
rij = 20.0

lj_energy = lennard_jones(sigma, epsilon, rij)

rf.dump(outfile='bibliography.bib')
```

## Installation

## Documentation

## Contribute

## Citation

### Copyright

Copyright (c) 2019, MolSSI

#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.0.
