"""
Reference_handler
A Python package that facilitates the citation of scientific material.

Handles the primary class
"""

import sqlite3
import pprint
import re

import bibtexparser
from .latex_utf8 import decode_latex
from .utils import entry_to_bibtex

supported_fmts = ["bibtex", "text"]

# '-' must be first for the regex to work.
subscript = {
    "-": "\N{SUBSCRIPT MINUS}",
    "0": "\N{SUBSCRIPT ZERO}",
    "1": "\N{SUBSCRIPT ONE}",
    "2": "\N{SUBSCRIPT TWO}",
    "3": "\N{SUBSCRIPT THREE}",
    "4": "\N{SUBSCRIPT FOUR}",
    "5": "\N{SUBSCRIPT FIVE}",
    "6": "\N{SUBSCRIPT SIX}",
    "7": "\N{SUBSCRIPT SEVEN}",
    "8": "\N{SUBSCRIPT EIGHT}",
    "9": "\N{SUBSCRIPT NINE}",
    "+": "\N{SUBSCRIPT PLUS SIGN}",
    "=": "\N{SUBSCRIPT EQUALS SIGN}",
    "(": "\N{SUBSCRIPT LEFT PARENTHESIS}",
    ")": "\N{SUBSCRIPT RIGHT PARENTHESIS}",
    "a": "\N{LATIN SUBSCRIPT SMALL LETTER A}",
    "e": "\N{LATIN SUBSCRIPT SMALL LETTER E}",
    "o": "\N{LATIN SUBSCRIPT SMALL LETTER O}",
    "x": "\N{LATIN SUBSCRIPT SMALL LETTER X}",
    "h": "\N{LATIN SUBSCRIPT SMALL LETTER H}",
    "k": "\N{LATIN SUBSCRIPT SMALL LETTER K}",
    "l": "\N{LATIN SUBSCRIPT SMALL LETTER L}",
    "m": "\N{LATIN SUBSCRIPT SMALL LETTER M}",
    "n": "\N{LATIN SUBSCRIPT SMALL LETTER N}",
    "p": "\N{LATIN SUBSCRIPT SMALL LETTER P}",
    "s": "\N{LATIN SUBSCRIPT SMALL LETTER S}",
    "t": "\N{LATIN SUBSCRIPT SMALL LETTER T}",
    "i": "\N{LATIN SUBSCRIPT SMALL LETTER I}",
    "r": "\N{LATIN SUBSCRIPT SMALL LETTER R}",
    "u": "\N{LATIN SUBSCRIPT SMALL LETTER U}",
    "v": "\N{LATIN SUBSCRIPT SMALL LETTER V}",
    r".": ".",
}
subscript_re = re.compile(r"\$_([" + "".join(subscript.keys()) + r"]+)\$")

# '-' must be first for the regex to work.
superscript = {
    "-": "\N{SUPERSCRIPT MINUS}",
    "0": "\N{SUPERSCRIPT ZERO}",
    "1": "\N{SUPERSCRIPT ONE}",
    "2": "\N{SUPERSCRIPT TWO}",
    "3": "\N{SUPERSCRIPT THREE}",
    "4": "\N{SUPERSCRIPT FOUR}",
    "5": "\N{SUPERSCRIPT FIVE}",
    "6": "\N{SUPERSCRIPT SIX}",
    "7": "\N{SUPERSCRIPT SEVEN}",
    "8": "\N{SUPERSCRIPT EIGHT}",
    "9": "\N{SUPERSCRIPT NINE}",
    "+": "\N{SUPERSCRIPT PLUS SIGN}",
    "=": "\N{SUPERSCRIPT EQUALS SIGN}",
    "(": "\N{SUPERSCRIPT LEFT PARENTHESIS}",
    ")": "\N{SUPERSCRIPT RIGHT PARENTHESIS}",
    "a": "\N{FEMININE ORDINAL INDICATOR}",
    "b": "ᵇ",
    "c": "ᶜ",
    "d": "ᵈ",
    "e": "ᵉ",
    "f": "ᶠ",
    "g": "ᵍ",
    "h": "ʰ",
    "i": "ⁱ",
    "j": "ʲ",
    "k": "ᵏ",
    "l": "ˡ",
    "m": "ᵐ",
    "n": "ⁿ",
    "o": "\N{MASCULINE ORDINAL INDICATOR}",
    "p": "ᵖ",
    "r": "ʳ",
    "s": "ˢ",
    "t": "ᵗ",
    "u": "ᵘ",
    "v": "ᵛ",
    "w": "ʷ",
    "x": "ˣ",
    "y": "ʸ",
    "z": "ᶻ",
}
superscript_re = re.compile(r"\$\^([" + "".join(superscript.keys()) + r"]+)\$")

greek_symbol = {
    "alpha": "\N{GREEK SMALL LETTER ALPHA}",
    "beta": "\N{GREEK SMALL LETTER BETA}",
    "gamma": "\N{GREEK SMALL LETTER GAMMA}",
    "delta": "\N{GREEK SMALL LETTER DELTA}",
    "epsilon": "\N{GREEK SMALL LETTER EPSILON}",
    "zeta": "\N{GREEK SMALL LETTER ZETA}",
    "eta": "\N{GREEK SMALL LETTER ETA}",
    "theta": "\N{GREEK SMALL LETTER THETA}",
    "iota": "\N{GREEK SMALL LETTER IOTA}",
    "kappa": "\N{GREEK SMALL LETTER KAPPA}",
    "lamda": "\N{GREEK SMALL LETTER LAMDA}",
    "lambda": "\N{GREEK SMALL LETTER LAMDA}",
    "mu": "\N{GREEK SMALL LETTER MU}",
    "nu": "\N{GREEK SMALL LETTER NU}",
    "xi": "\N{GREEK SMALL LETTER XI}",
    "omicron": "\N{GREEK SMALL LETTER OMICRON}",
    "pi": "\N{GREEK SMALL LETTER PI}",
    "rho": "\N{GREEK SMALL LETTER RHO}",
    "sigma": "\N{GREEK SMALL LETTER SIGMA}",
    "tau": "\N{GREEK SMALL LETTER TAU}",
    "upsilon": "\N{GREEK SMALL LETTER UPSILON}",
    "phi": "\N{GREEK SMALL LETTER PHI}",
    "chi": "\N{GREEK SMALL LETTER CHI}",
    "psi": "\N{GREEK SMALL LETTER PSI}",
    "omega": "\N{GREEK SMALL LETTER OMEGA}",
    "Alpha": "\N{GREEK CAPITAL LETTER ALPHA}",
    "Beta": "\N{GREEK CAPITAL LETTER BETA}",
    "Gamma": "\N{GREEK CAPITAL LETTER GAMMA}",
    "Delta": "\N{GREEK CAPITAL LETTER DELTA}",
    "Epsilon": "\N{GREEK CAPITAL LETTER EPSILON}",
    "Zeta": "\N{GREEK CAPITAL LETTER ZETA}",
    "Eta": "\N{GREEK CAPITAL LETTER ETA}",
    "Theta": "\N{GREEK CAPITAL LETTER THETA}",
    "Iota": "\N{GREEK CAPITAL LETTER IOTA}",
    "Kappa": "\N{GREEK CAPITAL LETTER KAPPA}",
    "Lamda": "\N{GREEK CAPITAL LETTER LAMDA}",
    "Lambda": "\N{GREEK CAPITAL LETTER LAMDA}",
    "Mu": "\N{GREEK CAPITAL LETTER MU}",
    "Nu": "\N{GREEK CAPITAL LETTER NU}",
    "Xi": "\N{GREEK CAPITAL LETTER XI}",
    "Omicron": "\N{GREEK CAPITAL LETTER OMICRON}",
    "Pi": "\N{GREEK CAPITAL LETTER PI}",
    "Rho": "\N{GREEK CAPITAL LETTER RHO}",
    "Sigma": "\N{GREEK CAPITAL LETTER SIGMA}",
    "Tau": "\N{GREEK CAPITAL LETTER TAU}",
    "Upsilon": "\N{GREEK CAPITAL LETTER UPSILON}",
    "Phi": "\N{GREEK CAPITAL LETTER PHI}",
    "Chi": "\N{GREEK CAPITAL LETTER CHI}",
    "Psi": "\N{GREEK CAPITAL LETTER PSI}",
    "Omega": "\N{GREEK CAPITAL LETTER OMEGA}",
}
greek_symbol_re = re.compile(r"\$\\(" + "|".join(greek_symbol.keys()) + r")\$")


class Reference_Handler(object):

    def __init__(self, database):
        """
        Constructs a reference handler class by connecting to a
        SQLite database and bulding the two tables within it.
        """

        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self._initialize_tables()

    def __del__(self):
        try:
            self.conn.commit()
            self.conn.close()
            # print('Closed database connection.')
        except:  # noqa: E722
            pass
            # print('Database was already closed.')

    def dump(self, outfile=None, fmt="bibtex", level=3):
        """
        Retrieves the individual citations that were collected during the
        execution of a program and tallies the number of times each citation
        was referenced.

        Parameters
        ----------
        outfile: str, Optional, default: None
            The file name where for the dump, if desired.

        fmt: str, Optional, default: 'bibtex'
            The format of the dump file, if desired.

        level: int, Optional, default: None
            Only those citations whose level at least the specified by level
            will be output.

        Returns
        -------
        ret: list
            A list whose elements are tuples containing pairs of raw citations
            and their counts.
        """

        if fmt not in supported_fmts:
            raise NameError("Format %s not currently supported." % (fmt))

        if fmt not in supported_fmts:
            raise NameError("Format %s not currently supported." % (fmt))

        if level not in range(1, 4) and level is not None:
            raise ValueError(
                "Invalid value for level. Please input a value in the range [1,3]"
            )

        self.cur.execute(
            """
            SELECT t1.id, t1.raw, t2.counts, t2.level
            FROM citation t1
            LEFT JOIN(
                SELECT id, reference_id, level, SUM(count) AS counts FROM
                context WHERE level <= ?
                GROUP BY reference_id
            ) t2
            ON t1.id = t2.reference_id WHERE counts > 0 ORDER BY counts DESC
        """,
            (level,),
        )

        query = self.cur.fetchall()

        if fmt == "bibtex":

            ret = query

            if outfile is not None:
                if type(outfile) is not str:
                    raise TypeError(
                        "The name of the output file must be a string but it "
                        "is %s" % type(outfile)
                    )

                with open(outfile, "w") as f:
                    for item in query:
                        f.write("TOTAL_MENTIONS: %s \n" % str(item[2]))
                        f.write("LEVEL: %s \n" % str(item[3]))
                        f.write(item[1])

        elif fmt == "text":

            ret = []

            for item in query:
                parse = bibtexparser.loads(item[1]).entries[0]
                entry_type = parse["ENTRYTYPE"]
                if entry_type == "misc":
                    plain_text = self.format_misc(parse)
                elif entry_type == "software":
                    plain_text = self.format_software(parse)
                elif entry_type == "article":
                    plain_text = self.format_article(parse)
                elif entry_type == "inbook":
                    plain_text = self.format_inbook(parse)
                elif entry_type == "phdthesis":
                    plain_text = self.format_phdthesis(parse)
                else:
                    plain_text = f"Do not have a handler for '{entry_type}':"
                    plain_text += "\n"
                    plain_text += pprint.pformat(parse)

                plain_text = decode_latex(plain_text)
                plain_text = self.decode_math_symbols(plain_text)
                ret.append((item[0], plain_text, item[2], item[3]))

        return ret

    @staticmethod
    def load_bibliography(bibfile=None, fmt="bibtex"):
        """
        Utility function to read a bibliographic file in common formats.
        The current supported formats are BibTeX.

        Parameters
        ----------
        bibfile: str, default: None
            The file name for the bibliographic file.

        fmt: str, Optional, default: 'bibtex'
            The format of the bibliographic file, if desired.

        Returns
        -------
        ret: dict
            A dictionary whose keys are the identifiers used in the
            bibliographic file (e.g. the first line in a BibTeX entry) and
            values are the raw entries found in such file. Note that the values
            of the dictionary might not be the exactly as found in the original
            bibliographic file.
        """

        if bibfile is None:
            raise FileNotFoundError("A bibliography file must be specified.")

        if fmt not in supported_fmts:
            raise NameError("Format %s not currently supported." % (fmt))

        with open(bibfile, "r") as f:
            parser = bibtexparser.bparser.BibTexParser(common_strings=True)
            bibliography = bibtexparser.load(f, parser=parser).entries

        ret = {k["ID"]: {} for k in bibliography}

        for entry in bibliography:
            ret[entry["ID"]] = entry_to_bibtex(entry)

        return ret

    def cite(
        self,
        raw=None,
        alias=None,
        module=None,
        level=1,
        note=None,
        fmt="bibtex",
        doi=None,
    ):
        """
        Adds a given reference to the internal database.

        Parameters
        ----------

        alias: str, default: None
            A string ID for the citation.

        raw: str, default: None
            The raw text for a given citation.

        module: str, default: None
            The module or function where this citation was called from

        level: int, default: 1
            The level of importance for this citation. References with the
            highest priority must have level 1 and references with lowest
            priority must have level 3.

        note: str, default: None
            A note that describes this citation.

        doi: str, Optional, default: None
            The digital object identifier if not provided in the raw
            argument. If provided in raw, DOI in the doi argument will be used.

        Returns
        -------
        None
        """

        if alias is None or raw is None or module is None or note is None:
            raise NameError(
                'Need to provide the "alias", "raw", "module" and "note" arguments'
            )

        doi = self._extract_doi(raw, fmt)

        reference_id = self._get_reference_id(raw=raw, alias=alias, doi=doi)

        if reference_id is None:
            self._create_citation(raw=raw, alias=alias, doi=doi)
            reference_id = self.cur.lastrowid
            self._create_context(
                reference_id=reference_id, module=module, note=note, level=level
            )
        else:
            context_id = self._get_context_id(
                reference_id=reference_id, module=module, note=note, level=level
            )

            if context_id is None:
                self._create_context(
                    reference_id=reference_id, module=module, note=note, level=level
                )
            else:
                self._update_counter(context_id=context_id)

        # Save the changes!
        self.conn.commit()

        return reference_id

    def _update_counter(self, context_id=None):
        """
        Updates the counter for given context
        """
        if context_id is None:
            raise NameError("The context ID must be provided")

        self.cur.execute(
            "UPDATE context SET count = count + 1 WHERE id=?;", (context_id,)
        )

    def _extract_doi(self, raw=None, fmt="bibtex"):
        """
        Parses DOI from bibliographic format
        """

        if fmt not in supported_fmts:
            raise NameError("Format %s not currently supported." % (fmt))

        if fmt == "bibtex":
            ret = bibtexparser.loads(raw)
            ret = ret.entries[0]
            if "doi" in ret.keys():
                return ret["doi"]

    def _initialize_tables(self):
        """
        Initializes the citation and context tables
        """

        self.cur.execute("""CREATE TABLE IF NOT EXISTS "citation" (
            "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
            "alias" TEXT NOT NULL UNIQUE,
            "raw"	TEXT NOT NULL UNIQUE,
            "doi"	TEXT UNIQUE
            );
            """)

        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_raw on citation (raw);")
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_alias on citation (alias);")
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_doi on citation (doi);")

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS "context" (
            "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
            "reference_id" INTEGER NOT NULL,
            "module" TEXT NOT NULL,
            "note" TEXT NOT NULL,
            "count"	INTEGER NOT NULL,
            "level" INTEGER NOT NULL,
            FOREIGN KEY(reference_id) REFERENCES Citation(id)
            );
            """)

        self.cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_refid on context (reference_id);"
        )
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_module on context (module);")
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_count on context (count);")
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_level on context (level);")

        self.conn.commit()

    def _get_reference_id(self, raw=None, alias=None, doi=None):
        """
        Gets the ID of the given raw or doi if exists
        """

        if raw is None:
            if alias is None:
                if doi is None:
                    raise NameError(
                        'Variables "raw" or "alias" or "DOI" must be input.'
                    )
                else:
                    self.cur.execute("SELECT id FROM citation WHERE doi=?;", (doi,))
            else:
                self.cur.execute("SELECT id FROM citation WHERE alias=?;", (alias,))
        else:
            self.cur.execute("SELECT id FROM citation WHERE raw=?;", (raw,))

        ret = self.cur.fetchall()

        if len(ret) == 0:
            return None

        return ret[0][0]

    def _get_context_id(self, reference_id=None, module=None, note=None, level=None):
        """
        Gets the ID of the context if exists. A context is specified by
        (reference_id, module, note, level) combination
        """

        if reference_id is None or module is None or note is None or level is None:
            raise NameError(
                'The variables "reference_id" and "module" and "note" and '
                '"level" must be specified'
            )

        self.cur.execute(
            "SELECT id FROM context WHERE reference_id=? AND module=? AND "
            "note=? AND level=?;",
            (reference_id, module, note, level),
        )

        ret = self.cur.fetchall()

        if len(ret) == 0:
            return None

        return ret[0][0]

    def _create_citation(self, raw=None, alias=None, doi=None):
        """
        Adds a new record to the citation table using a raw reference text.
        """

        if raw is None or alias is None:
            raise NameError("The value for raw and alias must be provided")
        else:
            self.cur.execute(
                "INSERT INTO citation (raw, alias, doi) VALUES (?, ?, ?);",
                (raw, alias, doi),
            )

        self.conn.commit()

    def _create_context(self, reference_id=None, module=None, note=None, level=None):
        """
        Adds a new record to the context table using the combination of the
        provided arguments.
        """

        if reference_id is None:
            raise NameError("Variables 'reference_id' or must be specified.")

        self.cur.execute(
            "INSERT INTO context (reference_id, module, note, count, level) "
            "VALUES (?, ?, ?, ?, ?)",
            (reference_id, module, note, 1, level),
        )

        self.conn.commit()

    def total_mentions(self, reference_id=None, alias=None):
        """
        Returns the number of times a given citation has been used.
        """
        if reference_id is None:
            if alias is None:
                raise NameError("The 'reference_id' or 'alias' must be provided.")
            else:
                self.cur.execute(
                    """
                    SELECT t1.alias, t2.counts
                    FROM citation t1
                    INNER JOIN (
                        SELECT reference_id, SUM(count) AS counts FROM context
                        GROUP BY reference_id
                    ) t2
                    ON t1.id = t2.reference_id
                    WHERE alias = ?
                """,
                    (alias,),
                )

        else:
            self.cur.execute(
                """
                SELECT t1.id, t2.counts
                FROM citation t1
                INNER JOIN (
                    SELECT reference_id, SUM(count) AS counts FROM context
                    GROUP BY reference_id
                ) t2
                ON t1.id = t2.reference_id
                WHERE id = ?
            """,
                (reference_id,),
            )

        ret = self.cur.fetchall()

        if len(ret) == 0:
            return 0

        return ret[0][1]

    def total_citations(self, reference_id=None, alias=None):
        """
        Returns the total number of citations in the citation table. If
        reference is provided, returns the total number of citations for a
        given reference ID.
        """

        if reference_id is None:
            if alias is None:

                self.cur.execute("SELECT COUNT(*) FROM citation")
                ret = self.cur.fetchall()[0][0]
                return ret

            else:
                self.cur.execute(
                    "SELECT COUNT(*) FROM citation WHERE alias = ?", (alias,)
                )

        else:

            self.cur.execute(
                "SELECT COUNT(*) FROM citation WHERE id=?;", (reference_id,)
            )

        ret = self.cur.fetchall()

        if len(ret) == 0:
            return 0

        return ret[0][0]

    def total_contexts(self, reference_id=None, alias=None):
        """
        Returns the total number of contexts for a given reference ID.
        """

        if reference_id is None:
            if alias is None:
                raise NameError(
                    "Variables 'reference_id' or 'alias' must be specified."
                )
            else:
                self.cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM citation
                    INNER JOIN (
                        SELECT id, reference_id FROM context
                    ) t2
                    ON citation.id = t2.reference_id WHERE alias=?
                """,
                    (alias,),
                )

        else:
            self.cur.execute(
                "SELECT COUNT(*) FROM context WHERE reference_id = ?;", (reference_id,)
            )

        return self.cur.fetchall()[0][0]

    def __str__(self):
        pass

    def format_article(self, data):
        """Format an article BibTex record

        ACS style:
            Foster, J. C.; Varlas, S.; Couturaud, B.; Coe, J.; O’Reilly,
            R. K. Getting into Shape: Reflections on a New Generation of
            Cylindrical Nanostructures’ Self-Assembly Using Polymer Building
            Block. J. Am. Chem. Soc. 2019, 141 (7), 2742−2753.
            DOI: 10.1021/jacs.8b08648
        """

        result = ""
        if "author" in data:
            result += "; ".join(data["author"].split(" and "))
            if result[-1] != ".":
                result += "."
        if "title" in data:
            result += " " + data["title"].rstrip(".") + "."
        if "journal" in data:
            result += " " + data["journal"]
        if "year" in data:
            result += f" {data['year']},"
        if "volume" in data:
            result += f" {data['volume']},"
        if "pages" in data:
            result += f" {data['pages']}."
        if "doi" in data:
            result += f" DOI: {data['doi']}"

        return result

    def format_phdthesis(self, data):
        """Format a PhD Thesis BibTex record

        ACS style:
            Cable, M. L. Life in Extreme Environments: Lanthanide-Based
            Detection of Bacterial Spores and Other Sensor Design Pursuits.
            Ph.D. Dissertation, California Institute of Technology, Pasadena,
            CA, 2010.
            http://resolver.caltech.edu/CaltechTHESIS:05102010-145436548
            (accessed 2019-09-10).
        """

        result = ""
        if "author" in data:
            result += "; ".join(data["author"].split(" and "))
            if result[-1] != ".":
                result += "."
        if "title" in data:
            result += " " + data["title"].rstrip(".") + "."
        result += " Ph.D. Dissertation"
        if "school" in data:
            result += f", {data['school']}"
        if "address" in data:
            result += f", {data['address']}"
        if "year" in data:
            result += f", {data['year']}."
        if "url" in data:
            result += f", {data['url']}"
        if "doi" in data:
            result += f", DOI: {data['doi']}"

        return result

    def format_misc(self, data):
        """Format a misc BibTex record, used for software

        Author 1; Author 2; etc. Program Title, version or edition; Publisher:
        Place of Publication, Year.

        Example:
            Binkley, J. S. GAUSSIAN82; Department of Chemistry, Carnegie Mellon
            University: Pittsburgh, PA, 1982.
        """

        result = ""

        if "author" in data:
            result += "; ".join(data["author"].split(" and "))
            if result[-1] != ".":
                result += "."
            result += " "
        if "title" in data:
            result += data["title"]
        if "version" in data:
            result += f", version {data['version']};"
        else:
            result += ";"

        if "organization" in data:
            result += " " + data["organization"]
        if "address" in data:
            result += f": {data['address']}"
        if "url" in data:
            result += f", {data['url']}"
        if "doi" in data:
            result += f", DOI: {data['doi']}"

        return result

    def format_software(self, data):
        return self.format_misc(self, data)

    def format_inbook(self, data):
        """Format a chapter or part of a book or series BibTex record

        ACS style:
            Bard, A. J.; Faulkner, L. R. Double-Layer Structure and Absorption.
            In Electrochemical Methods: Fundamentals and Applications, 2nd ed.;
            John Wiley & Sons, 2001; pp 534−579.

        for series:
            Gaede, H. C. Professional Development for REU Students. In Best
            Practices for Chemistry REU Programs; Griep, M. A, Watkins, L.,
            Eds.; ACS Symposium Series, Vol. 1295; American Chemical Society,
            2018; pp 33−44. DOI: 10.1021/bk-2018-1295.ch003
        """

        result = ""
        if "author" in data:
            result += "; ".join(data["author"].split(" and "))
            if result[-1] != ".":
                result += "."
        if "title" in data:
            result += " " + data["title"].rstrip(".") + ". In"
        if "booktitle" in data:
            result += f" {data['booktitle']}"
        if "series" in data:
            result += f"; {data['series']}"
        if "publisher" in data:
            result += f"; {data['publisher']}"
        if "place" in data:
            result += f", {data['place']}"
        if "year" in data:
            result += f", {data['year']}."
        if "url" in data:
            result += f", {data['url']}"
        if "doi" in data:
            result += f", DOI: {data['doi']}"

        return result

    def decode_math_symbols(self, text):
        """Clean up math symbols such as subscripts."""
        text = greek_symbol_re.sub(self._decode_greek_symbol, text)
        text = superscript_re.sub(self._decode_superscript, text)
        return subscript_re.sub(self._decode_subscript, text)

    def _decode_subscript(self, match):
        result = ""
        for digit in list(match[1]):
            result += subscript[digit]
        return result

    def _decode_superscript(self, match):
        result = ""
        for digit in list(match[1]):
            result += superscript[digit]
        return result

    def _decode_greek_symbol(self, match):
        return greek_symbol[match[1]]
