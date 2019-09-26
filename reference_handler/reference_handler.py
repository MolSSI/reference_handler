"""
Reference_handler
A Python package that facilitates the citation of scientific material.

Handles the primary class
"""

import sqlite3
import pprint
import bibtexparser
from .utils import entry_to_bibtex

supported_fmts = ['bibtex', 'text']


class Reference_Handler(object):

    def __init__(self, database):
        """
        Constructs a reference handler class by connecting to a
        SQLite database and bulding the two tables within it.
        """

        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self._initialize_tables()

    def dump(self, outfile=None, fmt='bibtex', level=3):
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
            raise NameError('Format %s not currently supported.' % (fmt))

        if fmt not in supported_fmts:
            raise NameError('Format %s not currently supported.' % (fmt))

        if level not in range(1, 4) and level is not None:
            raise ValueError(
                'Invalid value for level. Please input a value in the range '
                '[1,3]'
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
        """, (level,)
        )

        query = self.cur.fetchall()

        if fmt == 'bibtex':

            ret = query

            if outfile is not None:
                if type(outfile) is not str:
                    raise TypeError(
                        'The name of the output file must be a string but it '
                        'is %s' % type(outfile)
                    )

                with open(outfile, 'w') as f:
                    for item in query:
                        f.write('TOTAL_MENTIONS: %s \n' % str(item[2]))
                        f.write('LEVEL: %s \n' % str(item[3]))
                        f.write(item[1])

        elif fmt == 'text':

            ret = []

            for item in query:
                parse = bibtexparser.loads(item[1]).entries[0]

                fstring = (
                    '{author}; {title}; {journal}; {year}; {volume}; {doi}.\n'
                )
                try:
                    if parse['ENTRYTYPE'] == 'misc':
                        plain_text = self.format_misc(parse)
                    else:
                        plain_text = fstring.format(**parse)

                    ret.append((item[0], plain_text, item[2], item[3]))
                except KeyError:
                    pprint.pprint(parse)

        return ret

    @staticmethod
    def load_bibliography(bibfile=None, fmt='bibtex'):
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
            raise FileNotFoundError('A bibliography file must be specified.')

        if fmt not in supported_fmts:
            raise NameError('Format %s not currently supported.' % (fmt))

        with open(bibfile, 'r') as f:
            parser = bibtexparser.bparser.BibTexParser(common_strings=True)
            bibliography = bibtexparser.load(f, parser=parser).entries

        ret = {k['ID']: {} for k in bibliography}

        for entry in bibliography:
            ret[entry['ID']] = entry_to_bibtex(entry)

        return ret

    def cite(
        self,
        raw=None,
        alias=None,
        module=None,
        level=1,
        note=None,
        fmt='bibtex',
        doi=None
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
                'Need to provide the "alias", "raw", "module" and "note" '
                'arguments'
            )

        doi = self._extract_doi(raw, fmt)

        reference_id = self._get_reference_id(raw=raw, alias=alias, doi=doi)

        if reference_id is None:
            self._create_citation(raw=raw, alias=alias, doi=doi)
            reference_id = self.cur.lastrowid
            self._create_context(
                reference_id=reference_id,
                module=module,
                note=note,
                level=level
            )
        else:
            context_id = self._get_context_id(
                reference_id=reference_id,
                module=module,
                note=note,
                level=level
            )

            if context_id is None:
                self._create_context(
                    reference_id=reference_id,
                    module=module,
                    note=note,
                    level=level
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

    def _extract_doi(self, raw=None, fmt='bibtex'):
        """
        Parses DOI from bibliographic format
        """

        if fmt not in supported_fmts:
            raise NameError('Format %s not currently supported.' % (fmt))

        if fmt == 'bibtex':
            ret = bibtexparser.loads(raw)
            ret = ret.entries[0]
            if 'doi' in ret.keys():
                return ret['doi']

    def _initialize_tables(self):
        """
        Initializes the citation and context tables
        """

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS "citation" (
            "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
            "alias" TEXT NOT NULL UNIQUE,
            "raw"	TEXT NOT NULL UNIQUE,
            "doi"	TEXT UNIQUE
            );
            """
        )

        self.cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_raw on citation (raw);"
        )
        self.cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_alias on citation (alias);"
        )
        self.cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_doi on citation (doi);"
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS "context" (
            "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
            "reference_id" INTEGER NOT NULL,
            "module" TEXT NOT NULL,
            "note" TEXT NOT NULL,
            "count"	INTEGER NOT NULL,
            "level" INTEGER NOT NULL,
            FOREIGN KEY(reference_id) REFERENCES Citation(id)
            );
            """
        )

        self.cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_refid on context (reference_id);"
        )
        self.cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_module on context (module);"
        )
        self.cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_count on context (count);"
        )
        self.cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_level on context (level);"
        )

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
                    self.cur.execute(
                        "SELECT id FROM citation WHERE doi=?;" (doi,)
                    )
            else:
                self.cur.execute(
                    "SELECT id FROM citation WHERE alias=?;" (alias,)
                )
        else:
            self.cur.execute("SELECT id FROM citation WHERE raw=?;", (raw,))

        ret = self.cur.fetchall()

        if len(ret) == 0:
            return None

        return ret[0][0]

    def _get_context_id(
        self, reference_id=None, module=None, note=None, level=None
    ):
        """
        Gets the ID of the context if exists. A context is specified by
        (reference_id, module, note, level) combination
        """

        if (
            reference_id is None or module is None or note is None or
            level is None
        ):
            raise NameError(
                'The variables "reference_id" and "module" and "note" and '
                '"level" must be specified'
            )

        self.cur.execute(
            "SELECT id FROM context WHERE reference_id=? AND module=? AND "
            "note=? AND level=?;", (reference_id, module, note, level)
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
            raise NameError('The value for raw and alias must be provided')
        else:
            self.cur.execute(
                "INSERT INTO citation (raw, alias, doi) VALUES (?, ?, ?);",
                (raw, alias, doi)
            )

        self.conn.commit()

    def _create_context(
        self, reference_id=None, module=None, note=None, level=None
    ):
        """
        Adds a new record to the context table using the combination of the
        provided arguments.
        """

        if reference_id is None:
            raise NameError("Variables 'reference_id' or must be specified.")

        self.cur.execute(
            "INSERT INTO context (reference_id, module, note, count, level) "
            "VALUES (?, ?, ?, ?, ?)", (reference_id, module, note, 1, level)
        )

        self.conn.commit()

    def __del__(self):
        try:
            self.conn.commit()
            self.conn.close()
            # print('Closed database connection.')
        except:  # noqa: E722
            pass
            # print('Database was already closed.')

    def total_mentions(self, reference_id=None, alias=None):
        """
        Returns the number of times a given citation has been used.
        """
        if reference_id is None:
            if alias is None:
                raise NameError(
                    "The 'reference_id' or 'alias' must be provided."
                )
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
                """, (alias,)
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
            """, (reference_id,)
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
                """, (alias,)
                )

        else:
            self.cur.execute(
                "SELECT COUNT(*) FROM context WHERE reference_id = ?;",
                (reference_id,)
            )

        return self.cur.fetchall()[0][0]

    def __str__(self):
        pass

    def format_misc(self, parse):
        """Format a misc BibTex record"""

        result = ''

        if 'title' in parse:
            result += parse['title']

        if 'version' in parse:
            result += ' version ' + parse['version']
        else:
            result += ', '

        for key in ['author', 'organization', 'address', 'url']:
            if key in parse:
                result += ', ' + parse[key]

        return result
