"""
reference_handler.py
A Python package that facilitates the citation of scientific material.

Handles the primary functions
"""

import sqlite3
import os.path
import random
import string

class Reference_Handler(object):

    def __init__(self, database):

        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self._initialize_tables()

    
    def cite(self, raw=None, module=None, level=None, note=None, doi=None):
        """
        Placeholder function to show example docstring (NumPy format)

        Replace this function and doc string for your own project

        Parameters
        ----------
        with_attribution : bool, Optional, default: True
            Set whether or not to display who the quote is from

        Returns
        -------
        quote : str
            Compiled string including quote and optional attribution
        """

        if raw is None or module is None or level is None or note is None:
            raise NameError('Need to provide the "raw", "module", "level" and "note" arguments')

        if doi is None:
            doi = self._extract_doi(raw) 

        reference_id = self._get_reference_id(raw=raw, doi=doi)

        if reference_id is None:
            self._create_citation(raw=raw, doi=doi)
            self._create_context(reference_id=self.cur.lastrowid, module=module, note=note, level=level)
        else:
            context_id = self._get_context_id(reference_id=reference_id, module=module, note=note, level=level)

            if context_id is None:
                self._create_context(reference_id=reference_id, module=module, note=note, level=level)

    def _extract_doi(self, raw=None):
        """ Insert routine to parse DOI from bibliographic format"""
        string_length = 10
        letters = string.ascii_lowercase
        return  ''.join(random.choice(letters) for i in range(string_length))
        
    def _initialize_tables(self):
        
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS "citation" (
            "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
            "raw"	TEXT NOT NULL UNIQUE,
            "doi"	TEXT NOT NULL UNIQUE
            ); 
            """
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
        self.conn.commit()


    def _get_reference_id(self, raw=None, doi=None):

        if raw is None and doi is None:
            raise NameError('Variables "raw" or "DOI" not found.')

        if raw is not None:
            self.cur.execute(
             """
             SELECT id FROM citation WHERE raw=?;
             """,
             (raw,)
            )

        if doi is not None and raw is None:
            self.cur.execute(
             """
             SELECT id FROM citation WHERE doi=?;
             """,
             (doi,)
            )

        ret = self.cur.fetchall()

        if len(ret) == 0:
            return None

        return ret[0][0]

    def _get_context_id(self, reference_id=None, module=None, note=None, level=None):

        if reference_id is None or module is None or note is None or level is None:
            raise NameError('The variables "reference_id" and "module" and "note" and "level" must be specified')

        self.cur.execute(
            """
            SELECT id FROM context WHERE reference_id=? AND module=? AND note=? AND level=?;
            """, 
            (reference_id, module, note, level)
        )

        ret = self.cur.fetchall()

        if len(ret) == 0:
            return None

        return ret[0][0]

    def _create_citation(self, raw=None, doi=None):

        if raw is None or doi is None:
            raise NameError('The values for raw and DOI must be provided')

        self.cur.execute(
            """
            INSERT INTO citation (raw, doi) VALUES (?, ?) 
            """,
            (raw, doi)
        )

        self.conn.commit()

    def _create_context(self, reference_id=None, module=None, note=None, level=None):

        if reference_id is None:
            raise NameError("Variables 'reference_id' or must be specified.")

        self.cur.execute(
            """
            INSERT INTO context (reference_id, module, note, count, level) VALUES (?, ?, ?, ?, ?)
            """, 
            (reference_id, module, note, 0, level)
        )

        self.conn.commit()

#    def _print_citations(self):
#        self.cur.execute(
#            """SELECT * FROM citation"""
#        )
#        print (self.cur.fetchall())

    def __del__(self):

        self.cur.close()

    def total_citations(self):

        self.cur.execute(
            """SELECT COUNT(*) FROM citation
            """)

        return self.cur.fetchall()[0][0]

    def total_contexts(self, reference_id=None):

        if reference_id is None:
                raise NameError("Variables 'reference_id' must be specified.")

        self.cur.execute(
            """
            SELECT COUNT(*) FROM context WHERE reference_id = ?;
            """, 
            (reference_id,) )

        return self.cur.fetchall()[0][0]

    def __str__(self):
        pass