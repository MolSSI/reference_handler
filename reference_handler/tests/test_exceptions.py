"""
Unit and regression test for the reference_handler package.
"""

# Import package, test suite, and other packages as needed
import os
import reference_handler
import pytest
from . import build_filenames
from inspect import signature

database = build_filenames.build_data_filename('database.db')

lammps_citation = """
        @article{PLIMPTON19951,
        title = "Fast Parallel Algorithms for Short-Range Molecular Dynamics",
        journal = "Journal of Computational Physics",
        volume = "117",
        number = "1",
        pages = "1 - 19",
        year = "1995",
        issn = "0021-9991",
        doi = "https://doi.org/10.1006/jcph.1995.1039",
        url = "http://www.sciencedirect.com/science/article/pii/S002199918571039X",
        author = "Steve Plimpton",
        abstract = "Three parallel algorithms for classical molecular dynamics are presented. The first assigns each processor a fixed subset of atoms; the second assigns each a fixed subset of inter-atomic forces to compute; the third assigns each a fixed spatial region. The algorithms are suitable for molecular dynamics models which can be difficult to parallelize efficiently—those with short-range forces where the neighbors of each atom change rapidly. They can be implemented on any distributed-memory parallel machine which allows for message-passing of data between independently executing processors. The algorithms are tested on a standard Lennard-Jones benchmark problem for system sizes ranging from 500 to 100,000,000 atoms on several parallel supercomputers--the nCUBE 2, Intel iPSC/860 and Paragon, and Cray T3D. Comparing the results to the fastest reported vectorized Cray Y-MP and C90 algorithm shows that the current generation of parallel machines is competitive with conventional vector supercomputers even for small problems. For large problems, the spatial algorithm achieves parallel efficiencies of 90% and a 1840-node Intel Paragon performs up to 165 faster than a single Cray C9O processor. Trade-offs between the three algorithms and guidelines for adapting them to more complex molecular dynamics simulations are also discussed."
    }  # noqa: E501
    """  # noqa: E501

namd_citation = """
        @article{PHILLIPS2005,
        author = {Phillips, James C. and Braun, Rosemary and Wang, Wei and Gumbart, James and Tajkhorshid, Emad and Villa, Elizabeth and Chipot, Christophe and Skeel, Robert D. and Kalé, Laxmikant and Schulten, Klaus},
        title = {Scalable molecular dynamics with NAMD},
        journal = {Journal of Computational Chemistry},
        volume = {26},
        number = {16},
        pages = {1781-1802},
        keywords = {biomolecular simulation, molecular dynamics, parallel computing},
        doi = {10.1002/jcc.20289},
        url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/jcc.20289},
        eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/jcc.20289},
        abstract = {Abstract NAMD is a parallel molecular dynamics code designed for high-performance simulation of large biomolecular systems. NAMD scales to hundreds of processors on high-end parallel platforms, as well as tens of processors on low-cost commodity clusters, and also runs on individual desktop and laptop computers. NAMD works with AMBER and CHARMM potential functions, parameters, and file formats. This article, directed to novices as well as experts, first introduces concepts and methods used in the NAMD program, describing the classical molecular dynamics force field, equations of motion, and integration methods along with the efficient electrostatics evaluation algorithms employed and temperature and pressure controls used. Features for steering the simulation across barriers and for calculating both alchemical and conformational free energy differences are presented. The motivations for and a roadmap to the internal design of NAMD, implemented in C++ and based on Charm++ parallel objects, are outlined. The factors affecting the serial and parallel performance of a simulation are discussed. Finally, typical NAMD use is illustrated with representative applications to a small, a medium, and a large biomolecular system, highlighting particular features of NAMD, for example, the Tcl scripting language. The article also provides a list of the key features of NAMD and discusses the benefits of combining NAMD with the molecular graphics/sequence analysis software VMD and the grid computing/collaboratory software BioCoRE. NAMD is distributed free of charge with source code at www.ks.uiuc.edu. © 2005 Wiley Periodicals, Inc. J Comput Chem 26: 1781–1802, 2005},
        year = {2005}
        }
"""  # noqa: E501


def _create_db():
    """Boiler plate"""
    database_name = 'tmp.db'
    database = build_filenames.build_scratch_filename(
        database_name
    )  # noqa: F821

    if os.path.exists(database):
        os.remove(database)
    return reference_handler.Reference_Handler(database)


@pytest.fixture(
    scope='function',
    params=[
        x for x in range(
            len(
                signature(reference_handler.Reference_Handler.cite).parameters
            ) - 1
        )
    ]
)
def create_test_arg(request):
    test_arg = [None] * (
        len(signature(reference_handler.Reference_Handler.cite).parameters) - 1
    )
    test_arg[request.param] = 'string'
    yield tuple(test_arg)


def test_initialization_exceptions(create_test_arg):

    with pytest.raises(NameError):

        test_input = create_test_arg
        rf = _create_db()
        rf.cite(*test_input)


def test_get_reference_exception():
    """This test will load in a bibtex citation that does not have a
    doi and the user does not provide the doi.
    """
    pass


def test_get_context_exception():
    with pytest.raises(NameError):

        rf = _create_db()
        rf._get_context_id()


def test_get_total_context_exception():

    with pytest.raises(NameError):

        rf = _create_db()

        rf.total_contexts()


def test_get_create_citation_exception():

    with pytest.raises(NameError):

        rf = _create_db()

        rf._create_citation()


def test_get_create_context_exception():

    with pytest.raises(NameError):

        rf = _create_db()

        rf._create_context()
