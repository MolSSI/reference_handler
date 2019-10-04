# -*- coding: utf-8 -*-

r"""
A Python package to translate accents and special characters from LaTeX
to UTF-8, and vice versa.

Handles the following:

Accents
^^^^^^^
LaTeX uses commands of the form \\<char>{<letter>}, i.e. \\\\"{u} = ü, where
<char> specifies the type of accent, and <letter> is the letter that has the
accent:

========= ========= ===============
  <char>   Example     Accent
========= ========= ===============
    "         ö       Diaeresis
    '         ó       Acute Accent
    .         ȯ       Dot Above
    =         ō       Macron
   \^         ô       Circumflex Accent
   \`         ò       Grave Accent
   \|         o̍       Vertical Line Above
    ~         õ       Tilde
    b         o̱       Macron Below
    c         ç       Cedilla
    C         ȍ       Double Grave Accent
    d         ọ       Dot Below
    f         ȏ       Inverted Breve
    h         ả       Hook Above
    H         ő       Double Acute Accent
    k         ǫ       Ogonek
    r         o̊       Ring Above
    t         o͡o      Double Inverted Breve
    u         ŏ       Breve
    U         o̎       Double Vertical Line Above
    v         ǒ       Caron
========= ========= ===============

Special Symbols
^^^^^^^^^^^^^^^
LaTeX uses commands of the form \\<letter>, i.e. \\o = ø, where <letter> is
one of the following:

========= ========= ===================
<letter>   Result           Description
========= ========= ===================
   i         ı      Latin Small Letter Dotless I
   j         ȷ      Latin Small Letter Dotless J
   l         ł      Latin Small Letter L With Stroke
   L         Ł      Latin Capital Letter L With Stroke
   o         ø      Latin Small Letter O With Stroke
   O         Ø      Latin Capital Letter O With Stroke
========= ========= ===================

Dashes
^^^^^^
LaTeX uses multiple dashes to represent different dashes:

========= ========= ===================
<letters>   Result           Description
========= ========= ===================
  ``--``         –       en-dash
  ``---``         —       em-dash
========= ========= ===================
"""

import re
import typing
import unicodedata

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# LaTeX characters in accent macros of form \<char>{<letter>}, i.e. \"{u}
accent = {
    '"': '\N{Combining Diaeresis}',
    "'": '\N{Combining Acute Accent}',
    '.': '\N{Combining Dot Above}',
    '=': '\N{Combining Macron}',
    '^': '\N{Combining Circumflex Accent}',
    '`': '\N{Combining Grave Accent}',
    '|': '\N{Combining Vertical Line Above}',
    '~': '\N{Combining Tilde}',
    'b': '\N{Combining Macron Below}',
    'c': '\N{Combining Cedilla}',
    'C': '\N{Combining Double Grave Accent}',
    'd': '\N{Combining Dot Below}',
    'f': '\N{Combining Inverted Breve}',
    'h': '\N{Combining Hook Above}',
    'H': '\N{Combining Double Acute Accent}',
    'k': '\N{Combining Ogonek}',
    'r': '\N{Combining Ring Above}',
    't': '\N{Combining Double Inverted Breve}',
    'u': '\N{Combining Breve}',
    'U': '\N{Combining Double Vertical Line Above}',
    'v': '\N{Combining Caron}'
}

# The regexp to detect the LaTeX accent commands. The two added characters
# are the dotless i and j.
accent_re = re.compile(
    r'\\([' + ''.join(accent.keys()) + r']){([a-zA-Z\u0131\u0237])}'
)

# Invert the accent dictionary for each letter in the alphabet to make
# a dictionary of LaTeX encodings.
encoding = {}
for key, val in accent.items():
    for char in list(alphabet):
        encoding[char + val] = '\\' + key + '{' + char + '}'
        # handle any precombined versions of the character
        string = unicodedata.normalize('NFC', char + val)
        if len(string) == 1:
            encoding[string] = encoding[char + val]
    for char in [
        '\N{Latin Small Letter Dotless I}', '\N{Latin Small Letter Dotless J}'
    ]:
        encoding[char + val] = r'\%s{%s}' % (key, char)
        string = unicodedata.normalize('NFC', char + val)
        # These characters have no precombined versions, but check anyway
        if len(string) == 1:
            encoding[string] = encoding[char + val]


def _decode_latex_accent(match: typing.Match) -> str:
    """Helper function for re.sub for replacing LaTeX accents.

    Parameters:
        match: The match object from re.sub

    Returns:
        The unicode character for the accented letter
    """
    return match[2] + accent[match[1]]


# LaTeX single character symbols
symbol = {
    'i': '\N{Latin Small Letter Dotless I}',
    'j': '\N{Latin Small Letter Dotless J}',
    'l': '\N{Latin Small Letter L With Stroke}',
    'L': '\N{Latin Capital Letter L With Stroke}',
    'o': '\N{Latin Small Letter O With Stroke}',
    'O': '\N{Latin Capital Letter O With Stroke}'
}

# The regexp to detect the LaTeX commands for special characters
symbol_re = re.compile(r'\\([' + ''.join(symbol.keys()) + '])')

# Invert the symbol dictionary to make a dictionary of LaTeX encodings.
for key, val in symbol.items():
    encoding[val] = '\\' + key


def _decode_latex_symbol(match: typing.Match) -> str:
    """Helper function for re.sub for replacing LaTeX special characters.

    Parameters:
        match: The match object from re.sub

    Returns:
        The unicode character for the symbol.
    """
    return symbol[match[1]]


# LaTeX dashes
dash = {'--': '\N{EN Dash}', '---': '\N{EM Dash}'}

# The regexp to detect the LaTeX commands for dashes
dash_re = re.compile(r'([^-]?)(-{2,3})([^-]?)')

# Invert the dictionary tomake a dictionary of LaTeX encodings.
for key, val in dash.items():
    encoding[val] = key


def _decode_latex_dash(match: typing.Match) -> str:
    """Helper function for re.sub for replacing LaTeX dashes.

    Parameters:
        match: The match object from re.sub

    Returns:
        The unicode character for the dash.
    """
    return match[1] + dash[match[2]] + match[3]


# LaTeX braces to protect capitalization.
brace_re = re.compile(r"""{([^}]*)}""")


def decode_latex(text: str) -> str:
    """Replaces all LaTeX accents in the input string with their UTF8
    equivalents.

    Parameters:
        text: The text to translate.

    Returns:
        The translated string, using LaTeX commands for accents and special
        characters.
    """

    return brace_re.sub(
        r'\1',
        accent_re.sub(
            _decode_latex_accent,
            symbol_re.sub(
                _decode_latex_symbol, dash_re.sub(_decode_latex_dash, text)
            )
        )
    )


def encode_latex(text: str) -> str:
    """
    Encode the accented and special unicode characters into LaTeX commands.

    Parameters:
        text: The text to translate

    Returns:
        The translated text, using LaTeX commands for accents and special
        characters
    """

    # Map the double character representations
    text2 = ''
    char1 = text[0]
    i = 1
    len_text = len(text)
    while i < len_text:
        char2 = text[i]
        # print(char1 + ' ' + char2)
        if char1 + char2 in encoding:
            text2 += encoding[char1 + char2]
            i += 1
            if i >= len_text:
                char1 = None
                break
            char1 = text[i]
        else:
            text2 += char1
            char1 = char2
        i += 1
    if char1 is not None:
        text2 += char1

    # Map the single characters representations
    result = ''
    for char in list(text2):
        if char in encoding:
            result += encoding[char]
        else:
            result += char

    return result


if __name__ == '__main__':  # pragma: no cover
    text = r"""
(Vorlova_2015) Barbora Vorlov{\'{a}} and Dana Nachtigallov{\'{a}} and Jana
Jir{\'{a}}skov{\'{a}}-Van{\'{\i}}{\v{c}}kov{\'{a}} and Haresh Ajani and Petr
Jansa and Jan {\v{R}}ez{\'{a}}{\v{c}} and Jind{\v{r}}ich Fanfrl{\'{\i}}k and
Michal Otyepka and Pavel Hobza and Jan Konvalinka and Martin
Lep{\v{s}}{\'{\i}}k; Malonate-based inhibitors of mammalian serine racemase:
Kinetic characterization and structure-based computational study; European
Journal of Medicinal Chemistry; 2015; 89; 189--197;
10.1016/j.ejmech.2014.10.043.
"""

    print(text)

    text2 = decode_latex(text)
    print(text2)

    text3 = encode_latex(text2)
    print(text3)

    print(text3 == text)

    text4 = decode_latex(text3)
    print(text4)
    print(text2 == text4)

    ris = """
TY  - JOUR
DO  - 10.1016/j.ejmech.2014.10.043
UR  - http://dx.doi.org/10.1016/j.ejmech.2014.10.043
TI  - Malonate-based inhibitors of mammalian serine racemase: Kinetic characterization and structure-based computational study
T2  - European Journal of Medicinal Chemistry
AU  - Vorlová, Barbora
AU  - Nachtigallová, Dana
AU  - Jirásková-Vaníčková, Jana
AU  - Ajani, Haresh
AU  - Jansa, Petr
AU  - Řezáč, Jan
AU  - Fanfrlík, Jindřich
AU  - Otyepka, Michal
AU  - Hobza, Pavel
AU  - Konvalinka, Jan
AU  - Lepšík, Martin
PY  - 2015
DA  - 2015/01
PB  - Elsevier BV
SP  - 189-197
VL  - 89
SN  - 0223-5234
ER  - """  # noqa: E501

    # print(encode_latex('Řezáč'))
