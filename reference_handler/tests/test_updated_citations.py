"""A reference cited again with a different text -- a program's citation after an
update, whose text holds its version -- is the same citation, and a failed citation
never leaves the database locked (SEAMM job 5366, 2026-10-23: a resumed job's
'UNIQUE constraint failed: citation.doi' kept the lock, and the parallel loop's
iterations then failed with 'database is locked')."""

import sqlite3

import pytest

import reference_handler


def raw(version):
    return (
        "@misc{seamm_exec,\n"
        "  author = {Saxe, Paul},\n"
        "  title = {seamm_exec},\n"
        f"  version = {{{version}}},\n"
        "  doi = {10.5281/zenodo.0000000},\n"
        "}\n"
    )


def cite(rh, version):
    return rh.cite(
        raw=raw(version),
        alias="seamm_exec",
        module="seamm_exec",
        level=1,
        note="The executor",
    )


def test_a_new_version_is_the_same_citation(tmp_path):
    db = str(tmp_path / "references.db")
    rh = reference_handler.Reference_Handler(db)
    first = cite(rh, "2026.10.20")
    again = cite(rh, "2026.10.23")
    assert again == first
    rh.cur.execute("SELECT raw FROM citation WHERE id=?;", (first,))
    assert "2026.10.23" in rh.cur.fetchone()[0]
    rh.cur.execute("SELECT count FROM context WHERE reference_id=?;", (first,))
    assert rh.cur.fetchone()[0] == 2


def test_a_failed_citation_does_not_keep_the_lock(tmp_path, monkeypatch):
    db = str(tmp_path / "references.db")
    rh = reference_handler.Reference_Handler(db)
    cite(rh, "2026.10.20")

    def broken(**kwargs):
        rh.cur.execute(
            "INSERT INTO citation (raw, alias, doi) VALUES (?, ?, ?);",
            ("@misc{x, title={x}}", "seamm_exec", None),
        )

    monkeypatch.setattr(rh, "_find_citation", lambda **kwargs: None)
    monkeypatch.setattr(rh, "_create_citation", broken)
    with pytest.raises(sqlite3.IntegrityError):
        cite(rh, "2026.10.23")
    assert not rh.conn.in_transaction

    # Another connection -- another process of the job -- can still write
    other = sqlite3.connect(db, timeout=0.5)
    other.execute("UPDATE context SET count = count + 1;")
    other.commit()
    other.close()
