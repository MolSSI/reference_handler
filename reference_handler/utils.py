import bibtexparser


def _str_or_expr_to_bibtex(e):
    if isinstance(e, bibtexparser.bibdatabase.BibDataStringExpression):
        return ' # '.join([_str_or_expr_to_bibtex(s) for s in e.expr])
    elif isinstance(e, bibtexparser.bibdatabase.BibDataString):
        return e.name
    else:
        return '{' + e + '}'


def entry_to_bibtex(entry):

    bibtex = ''

    bibtex += '@' + entry['ENTRYTYPE'] + '{' + entry['ID']

    display_order = [i for i in sorted(entry)]
    field_fmt = u",\n{indent}{field:<{field_max_w}} = {value}"

    for field in [i for i in display_order if i not in ['ENTRYTYPE', 'ID']]:
        try:
            bibtex += field_fmt.format(
                indent=' ',
                field=field,
                field_max_w=0,
                value=_str_or_expr_to_bibtex(entry[field])
            )
        except TypeError:
            raise TypeError(
                u"The field %s in entry %s must be a string" %
                (field, entry['ID'])
            )

    bibtex += "\n}\n\n"
    return bibtex
