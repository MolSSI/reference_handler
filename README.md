reference_handler
==============================
[//]: # (Badges)
[![Travis Build Status](https://travis-ci.org/molssi/reference_handler.png)](https://travis-ci.org/molssi/reference_handler)
[![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/REPLACE_WITH_APPVEYOR_LINK/branch/master?svg=true)](https://ci.appveyor.com/project/molssi/reference_handler/branch/master)
[![codecov](https://codecov.io/gh/molssi/reference_handler/branch/master/graph/badge.svg)](https://codecov.io/gh/molssi/reference_handler/branch/master)
[![Documentation Status](https://readthedocs.org/projects/reference-handler/badge/?version=latest)](https://reference-handler.readthedocs.io/en/latest/?badge=latest)

A python package for scientific software citation.

## Motivation & goal

An appropriate recognition of the value of the scientific software on an equal footing with 
scholarly manuscripts and datasets is dependent upon the realization and promotion of
community guidelines and best practices for software citation. Such practices can improve 
reproducibility and validation of the scientific discoveries, encourage software reuse and 
boost collaborative efforts.

## Package overview

The *reference handler* is comprised of two core parts:

**1. Central SQLite3 database** which contains two tables:
(i) the *citation* table which hosts all essential data pertinent to each unique citation,
such as the raw citation text and its ID number, and (ii) the *context* table which contains
information about the context in which a given citation was used. For instance, the function
where the citation was used or the number of times the citation was "mentioned"
by any function of your Python package. Since each citation can have many contexts, a
one-to-many relationship exist between the *citation* and the *context* tables, respectively.

**2. Functions to ease the interaction with central database.** Examples are a function
to cite a desired reference or a function to dump the contents of the database into a
`.bib` file for subsequent compilation using BibTeX.

## Audience

* 1. Method and scientific software developers.
* 2. Computational molecular science practitioners

## Main features

* Automatic and seamless runtime citation to all adopted software modules in the executed program
* Managing citations within complex workflows and interoperable environments conveniently with simple syntax and APIs
* Providing context and number of counts for all modules used in the executed application
* Prioritization of all cited modules at different levels
* Recommended citation style according to the community guidelines and best practices
* Exporting references as databases and formatted documents in BibTeX and RIS

## Installation

* **Step 1**: Clone this repository on a host machine:

```bash
$ git clone git@github.com:MolSSI/reference_handler.git
```

* **Step 2**: Change the current directory to *reference_handler's* root directory:

```bash
$ cd <path-to-reference-handler-root-directory>/reference_handler
```

* **Step 3**: Create a Conda environment with *python 3.9* and *pip*:

```bash
$ conda create -n <env-name> python=3.9 pip
```

replace the `<env-name>` with the desired name of your environment.

* **Step 4**: Activate your conda environment:

```bash
$ conda activate <env-name>
```

* **Step 5**: Run the following command to install *bibtexparser 1.2.0* using pip
within your conda environment

```bash
$ pip install bibtexparser==1.2.0 
```

* **Step 6**: Finally, run the following command to install *reference_handler* in
your conda environment

```bash
$ make install 
```

* **Step 7 (optional)**: Make sure all tests run without errors

```bash
$ pytest -v
```

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

## Documentation

The documentation is under development. Please check back later.

## References

* [Katz, D. S., Chue Hong, N. P., Clark T., Muench, A., Stall, S., Bouquin, D., Cannon, M., Edmunds, S., Faez, T., Farmer, R., \
Feeney, P., Fenner, M., Friedman, M., Grenier, G., Harrison, M., Heber, J., Leary, A., MacCallum, C., Murray, H., ... Yeston, J. \
(2020) Recognizing the value of software: a software citation guide. F1000 Research. https://doi.org/10.12688/f1000research.26932.2](https://doi.org/10.12688/f1000research.26932.2)

* [Smith A. M., Katz D. S., Niemeyer K. E., FORCE11 Software Citation Working Group.2016. \
Software citation principles. PeerJ Computer Science 2:e86 https://doi.org/10.7717/peerj-cs.86](https://doi.org/10.7717/peerj-cs.86)

## Copyright

Copyright (c) 2019-2022, MolSSI

## Acknowledgements
 
Project based on the
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.0.
