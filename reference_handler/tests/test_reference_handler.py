"""
Unit and regression test for the reference_handler package.
"""

# Import package, test suite, and other packages as needed
import os
import reference_handler
import pytest
import sys
from . import build_filenames

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
    }
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


def _create_db(database_name):
    """Boiler plate"""
    database = build_filenames.build_scratch_filename(database_name)

    if os.path.exists(database):
        os.remove(database)
    return reference_handler.Reference_Handler(database)


def test_reference_handler_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "reference_handler" in sys.modules


def test_initialization():

    rf = _create_db('database.db')

    assert rf.total_citations() == 0

    assert rf.total_citations(alias='my_alias') == 0
    assert rf.total_citations(reference_id=1) == 0

    assert rf.total_mentions(alias='my_alias') == 0
    assert rf.total_mentions(reference_id=1) == 0

    assert rf.total_contexts(alias='my_alias') == 0
    assert rf.total_contexts(reference_id=1) == 0


def test_add_new_cite_to_empty_db():

    rf = _create_db('database.db')

    rf.cite(
        raw=lammps_citation,
        alias='new_citation',
        module='test_add_new_cite',
        level=1,
        note='This is a test'
    )

    assert rf.total_citations() == 1

    assert rf.total_citations(reference_id=1) == 1
    assert rf.total_citations(alias='new_citation') == 1

    assert rf.total_mentions(reference_id=1) == 1
    assert rf.total_mentions(alias='new_citation') == 1

    assert rf.total_contexts(reference_id=1) == 1
    assert rf.total_contexts(alias='new_citation') == 1


def test_add_existing_citation():

    rf = _create_db('database.db')

    rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=1,
        note='The main LAMMPS paper'
    )
    rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=1,
        note='The main LAMMPS paper'
    )

    assert rf.total_citations() == 1

    assert rf.total_citations(reference_id=1) == 1
    assert rf.total_citations(alias='lammps_paper') == 1

    assert rf.total_mentions(reference_id=1) == 2
    assert rf.total_mentions(alias='lammps_paper') == 2

    assert rf.total_contexts(reference_id=1) == 1
    assert rf.total_contexts(alias='lammps_paper') == 1


def test_add_new_context():

    rf = _create_db('database.db')

    rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=1,
        note='Context 1'
    )
    rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=1,
        note='Context 2'
    )

    assert rf.total_citations() == 1

    assert rf.total_citations(reference_id=1) == 1
    assert rf.total_citations(alias='lammps_paper') == 1

    assert rf.total_mentions(reference_id=1) == 2
    assert rf.total_mentions(alias='lammps_paper') == 2

    assert rf.total_contexts(reference_id=1) == 2
    assert rf.total_contexts(alias='lammps_paper') == 2

    rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=2,
        note='Context 1'
    )

    assert rf.total_citations() == 1

    assert rf.total_citations(reference_id=1) == 1
    assert rf.total_citations(alias='lammps_paper') == 1

    assert rf.total_mentions(reference_id=1) == 3
    assert rf.total_mentions(alias='lammps_paper') == 3

    assert rf.total_contexts(reference_id=1) == 3
    assert rf.total_contexts(alias='lammps_paper') == 3

    rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS_2',
        level=2,
        note='Context 1'
    )

    assert rf.total_citations() == 1

    assert rf.total_citations(reference_id=1) == 1
    assert rf.total_citations(alias='lammps_paper') == 1

    assert rf.total_mentions(reference_id=1) == 4
    assert rf.total_mentions(alias='lammps_paper') == 4

    assert rf.total_contexts(reference_id=1) == 4
    assert rf.total_contexts(alias='lammps_paper') == 4


def test_add_new_cite_to_existing_db():

    rf = _create_db('database.db')

    rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=1,
        note='Context 1'
    )
    rf.cite(
        raw=namd_citation,
        alias='namd_paper',
        module='NAMD',
        level=1,
        note='Context 1'
    )

    assert rf.total_citations() == 2
    assert rf.total_citations(reference_id=1) == 1
    assert rf.total_citations(reference_id=2) == 1

    assert rf.total_mentions(reference_id=1) == 1
    assert rf.total_mentions(reference_id=2) == 1

    assert rf.total_citations(alias='lammps_paper') == 1
    assert rf.total_citations(alias='namd_paper') == 1

    assert rf.total_mentions(alias="lammps_paper") == 1
    assert rf.total_mentions(alias='namd_paper') == 1

    assert rf.total_contexts(reference_id=1) == 1
    assert rf.total_contexts(reference_id=2) == 1
    assert rf.total_contexts(alias='lammps_paper') == 1
    assert rf.total_contexts(alias='namd_paper') == 1


def test_load_bibliography():

    rf = _create_db('database.db')

    bibfile = build_filenames.build_data_filename('library.bib')

    bib = rf.load_bibliography(bibfile=bibfile)

    assert len(list(bib)) == 4


def test_add_many_cites_and_many_contexts():

    pass


def _get_dump(outfile=None, level=None):

    rf = _create_db('database.db')

    bibfile = build_filenames.build_data_filename('library.bib')

    bib = reference_handler.Reference_Handler.load_bibliography(
        bibfile=bibfile, fmt='bibtex'
    )

    rf.cite(
        raw=bib['Jakobtorweihen.JCP.2006.125.224709'],
        alias='Jakobtorweihen',
        module='Code1',
        level=1,
        note='Context1'
    )
    rf.cite(
        raw=bib['Afzal.JCED.2014.59.954'],
        alias='Afzal',
        module='Code2',
        level=1,
        note='Context1'
    )
    rf.cite(
        raw=bib['Kilaru.IECR.2008.47.910'],
        alias='Kilaru',
        module='Code3',
        level=1,
        note='Context1'
    )
    rf.cite(
        raw=bib['Argauer.USPatent.1972.3702886'],
        alias='Argauer',
        module='Code1',
        level=3,
        note='Context2'
    )
    rf.cite(
        raw=bib['Afzal.JCED.2014.59.954'],
        alias='Afzal',
        module='Code4',
        level=1,
        note='Context1'
    )
    rf.cite(
        raw=bib['Jakobtorweihen.JCP.2006.125.224709'],
        alias='Jakobtorweihen',
        module='Code2',
        level=3,
        note='Context1'
    )
    rf.cite(
        raw=bib['Afzal.JCED.2014.59.954'],
        alias='Afzal',
        module='Code2',
        level=1,
        note='Context1'
    )

    dump = rf.dump(outfile=outfile, level=level)
    return dump


@pytest.mark.parametrize(
    'name, count',
    [('Afzal', 3), ('Jakobtorweihen', 2), ('Kilaru', 1), ('Argauer', 1)]
)
def test_dump(name, count):

    dump = _get_dump()
    for item in dump:
        if name in item[1]:
            assert item[2] == count


@pytest.mark.parametrize(
    'name, count',
    [('Afzal', 3), ('Jakobtorweihen', 1), ('Kilaru', 1), ('Argauer', 0)]
)
def test_dump_with_level(name, count):

    outfile = build_filenames.build_scratch_filename('outfile.bib')
    dump = _get_dump(outfile=outfile, level=2)
    for item in dump:
        if name in item[1]:
            assert item[2] == count


def test_dump_output():

    outfile = build_filenames.build_scratch_filename('outfile.bib')
    dump = _get_dump(outfile=outfile)  # noqa: F841

    assert os.path.exists(outfile) is True


def test_cite_return():

    rf = _create_db('database.db')

    lammps_id1 = rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=1,
        note='Context 1'
    )
    lammps_id2 = rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=1,
        note='Context 1'
    )
    lammps_id3 = rf.cite(
        raw=lammps_citation,
        alias='lammps_paper',
        module='LAMMPS',
        level=1,
        note='Context 2'
    )
    namd_id = rf.cite(
        raw=namd_citation,
        alias='namd_paper',
        module='NAMD',
        level=1,
        note='Context 1'
    )

    assert lammps_id1 == lammps_id2
    assert lammps_id1 == lammps_id3
    assert namd_id == 2
