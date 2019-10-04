"""
Unit and regression test for the reference_handler package.
"""

# Import package, test suite, and other packages as needed
import reference_handler  # noqa: F401
from reference_handler import decode_latex
from reference_handler import encode_latex
import sys

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def test_latex_utf8_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert 'reference_handler' in sys.modules


def test_latex_umlauts():
    """LaTex command for an umlaut on a character, e.g. \"{a}"""
    answer = 'ÄB̈C̈D̈ËF̈G̈ḦÏJ̈K̈L̈M̈N̈ÖP̈Q̈R̈S̈T̈ÜV̈ẄẌŸZ̈äb̈c̈d̈ëf̈g̈ḧïj̈k̈l̈m̈n̈öp̈q̈r̈s̈ẗüv̈ẅẍÿz̈ı̈ȷ̈'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\"{' + char + '}'
    text += r'\"{\i}'  # dotless i
    text += r'\"{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_acute_accents():
    """LaTex command for an acute accent character, e.g. \'{a}"""
    answer = 'ÁB́ĆD́ÉF́ǴH́ÍJ́ḰĹḾŃÓṔQ́ŔŚT́ÚV́ẂX́ÝŹáb́ćd́éf́ǵh́íj́ḱĺḿńóṕq́ŕśt́úv́ẃx́ýźı́ȷ́'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r"\'{" + char + '}'
    text += r"\'{\i}"  # dotless i
    text += r"\'{\j}"  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_dot_above():
    r"""LaTex command for a dot above the character, e.g. \.{a}"""
    answer = 'ȦḂĊḊĖḞĠḢİJ̇K̇L̇ṀṄȮṖQ̇ṘṠṪU̇V̇ẆẊẎŻȧḃċḋėḟġḣi̇j̇k̇l̇ṁṅȯṗq̇ṙṡṫu̇v̇ẇẋẏżı̇ȷ̇'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\.{' + char + '}'
    text += r'\.{\i}'  # dotless i
    text += r'\.{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_macron_above():
    r"""LaTex command for a macron above the character, e.g. \={a}"""
    answer = 'ĀB̄C̄D̄ĒF̄ḠH̄ĪJ̄K̄L̄M̄N̄ŌP̄Q̄R̄S̄T̄ŪV̄W̄X̄ȲZ̄āb̄c̄d̄ēf̄ḡh̄īj̄k̄l̄m̄n̄ōp̄q̄r̄s̄t̄ūv̄w̄x̄ȳz̄ı̄ȷ̄'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\={' + char + '}'
    text += r'\={\i}'  # dotless i
    text += r'\={\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_circumflex_above():
    r"""LaTex command for a circumflex above the character, e.g. \^{a}"""
    answer = 'ÂB̂ĈD̂ÊF̂ĜĤÎĴK̂L̂M̂N̂ÔP̂Q̂R̂ŜT̂ÛV̂ŴX̂ŶẐâb̂ĉd̂êf̂ĝĥîĵk̂l̂m̂n̂ôp̂q̂r̂ŝt̂ûv̂ŵx̂ŷẑı̂ȷ̂'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\^{' + char + '}'
    text += r'\^{\i}'  # dotless i
    text += r'\^{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_grave_accent():
    r"""LaTex command for a grave accent on the character, e.g. \`{a}"""
    answer = 'ÀB̀C̀D̀ÈF̀G̀H̀ÌJ̀K̀L̀M̀ǸÒP̀Q̀R̀S̀T̀ÙV̀ẀX̀ỲZ̀àb̀c̀d̀èf̀g̀h̀ìj̀k̀l̀m̀ǹòp̀q̀r̀s̀t̀ùv̀ẁx̀ỳz̀ı̀ȷ̀'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\`{' + char + '}'
    text += r'\`{\i}'  # dotless i
    text += r'\`{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_vertical_line_above():
    r"""LaTex command for a vertical line above the character, e.g. \|{a}"""
    answer = 'A̍B̍C̍D̍E̍F̍G̍H̍I̍J̍K̍L̍M̍N̍O̍P̍Q̍R̍S̍T̍U̍V̍W̍X̍Y̍Z̍a̍b̍c̍d̍e̍f̍g̍h̍i̍j̍k̍l̍m̍n̍o̍p̍q̍r̍s̍t̍u̍v̍w̍x̍y̍z̍ı̍ȷ̍'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\|{' + char + '}'
    text += r'\|{\i}'  # dotless i
    text += r'\|{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_tilde_above():
    r"""LaTex command for a tilde above the character, e.g. \~{a}"""
    answer = 'ÃB̃C̃D̃ẼF̃G̃H̃ĨJ̃K̃L̃M̃ÑÕP̃Q̃R̃S̃T̃ŨṼW̃X̃ỸZ̃ãb̃c̃d̃ẽf̃g̃h̃ĩj̃k̃l̃m̃ñõp̃q̃r̃s̃t̃ũṽw̃x̃ỹz̃ı̃ȷ̃'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\~{' + char + '}'
    text += r'\~{\i}'  # dotless i
    text += r'\~{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_macron_below():
    r"""LaTex command for a macron below the character, e.g. \b{a}"""
    answer = 'A̱ḆC̱ḎE̱F̱G̱H̱I̱J̱ḴḺM̱ṈO̱P̱Q̱ṞS̱ṮU̱V̱W̱X̱Y̱Ẕa̱ḇc̱ḏe̱f̱g̱ẖi̱j̱ḵḻm̱ṉo̱p̱q̱ṟs̱ṯu̱v̱w̱x̱y̱ẕı̱ȷ̱'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\b{' + char + '}'
    text += r'\b{\i}'  # dotless i
    text += r'\b{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_cedilla():
    r"""LaTex command for a cedilla on the character, e.g. \c{a}"""
    answer = 'A̧B̧ÇḐȨF̧ĢḨI̧J̧ĶĻM̧ŅO̧P̧Q̧ŖŞŢU̧V̧W̧X̧Y̧Z̧a̧b̧çḑȩf̧ģḩi̧j̧ķļm̧ņo̧p̧q̧ŗşţu̧v̧w̧x̧y̧z̧ı̧ȷ̧'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\c{' + char + '}'
    text += r'\c{\i}'  # dotless i
    text += r'\c{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_double_grave_accent():
    r"""LaTex command for a double grave accent on the character, e.g. \C{a}"""
    answer = 'ȀB̏C̏D̏ȄF̏G̏H̏ȈJ̏K̏L̏M̏N̏ȌP̏Q̏ȐS̏T̏ȔV̏W̏X̏Y̏Z̏ȁb̏c̏d̏ȅf̏g̏h̏ȉj̏k̏l̏m̏n̏ȍp̏q̏ȑs̏t̏ȕv̏w̏x̏y̏z̏ı̏ȷ̏'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\C{' + char + '}'
    text += r'\C{\i}'  # dotless i
    text += r'\C{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_dot_below():
    r"""LaTex command for a dot below the character, e.g. \d{a}"""
    answer = 'ẠḄC̣ḌẸF̣G̣ḤỊJ̣ḲḶṂṆỌP̣Q̣ṚṢṬỤṾẈX̣ỴẒạḅc̣ḍẹf̣g̣ḥịj̣ḳḷṃṇọp̣q̣ṛṣṭụṿẉx̣ỵẓı̣ȷ̣'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\d{' + char + '}'
    text += r'\d{\i}'  # dotless i
    text += r'\d{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_inverted_breve():
    r"""LaTex command for an inverted breve above the character, e.g. \f{a}"""
    answer = 'ȂB̑C̑D̑ȆF̑G̑H̑ȊJ̑K̑L̑M̑N̑ȎP̑Q̑ȒS̑T̑ȖV̑W̑X̑Y̑Z̑ȃb̑c̑d̑ȇf̑g̑h̑ȋj̑k̑l̑m̑n̑ȏp̑q̑ȓs̑t̑ȗv̑w̑x̑y̑z̑ı̑ȷ̑'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\f{' + char + '}'
    text += r'\f{\i}'  # dotless i
    text += r'\f{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_hook_above():
    r"""LaTex command for a hook above the character, e.g. \h{a}"""
    answer = 'ẢB̉C̉D̉ẺF̉G̉H̉ỈJ̉K̉L̉M̉N̉ỎP̉Q̉R̉S̉T̉ỦV̉W̉X̉ỶZ̉ảb̉c̉d̉ẻf̉g̉h̉ỉj̉k̉l̉m̉n̉ỏp̉q̉r̉s̉t̉ủv̉w̉x̉ỷz̉ı̉ȷ̉'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\h{' + char + '}'
    text += r'\h{\i}'  # dotless i
    text += r'\h{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_double_acute_accent():
    r"""LaTex command for a double acute accent on the character, e.g. \H{a}"""
    answer = 'A̋B̋C̋D̋E̋F̋G̋H̋I̋J̋K̋L̋M̋N̋ŐP̋Q̋R̋S̋T̋ŰV̋W̋X̋Y̋Z̋a̋b̋c̋d̋e̋f̋g̋h̋i̋j̋k̋l̋m̋n̋őp̋q̋r̋s̋t̋űv̋w̋x̋y̋z̋ı̋ȷ̋'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\H{' + char + '}'
    text += r'\H{\i}'  # dotless i
    text += r'\H{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_ogonek():
    r"""LaTex command for a ogonek on the character, e.g. \k{a}"""
    answer = 'ĄB̨C̨D̨ĘF̨G̨H̨ĮJ̨K̨L̨M̨N̨ǪP̨Q̨R̨S̨T̨ŲV̨W̨X̨Y̨Z̨ąb̨c̨d̨ęf̨g̨h̨įj̨k̨l̨m̨n̨ǫp̨q̨r̨s̨t̨ųv̨w̨x̨y̨z̨ı̨ȷ̨'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\k{' + char + '}'
    text += r'\k{\i}'  # dotless i
    text += r'\k{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_ring_above():
    r"""LaTex command for a ring above the character, e.g. \r{a}"""
    answer = 'ÅB̊C̊D̊E̊F̊G̊H̊I̊J̊K̊L̊M̊N̊O̊P̊Q̊R̊S̊T̊ŮV̊W̊X̊Y̊Z̊åb̊c̊d̊e̊f̊g̊h̊i̊j̊k̊l̊m̊n̊o̊p̊q̊r̊s̊t̊ův̊ẘx̊ẙz̊ı̊ȷ̊'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\r{' + char + '}'
    text += r'\r{\i}'  # dotless i
    text += r'\r{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_double_inverted_breve():
    r"""LaTex command for a double inverted breve on the character, e.g.
    \t{a}"""
    answer = 'A͡AB͡BC͡CD͡DE͡EF͡FG͡GH͡HI͡IJ͡JK͡KL͡LM͡MN͡NO͡OP͡PQ͡QR͡RS͡ST͡TU͡UV͡VW͡WX͡XY͡YZ͡Za͡ab͡bc͡cd͡de͡ef͡fg͡gh͡hi͡ij͡jk͡kl͡lm͡mn͡no͡op͡pq͡qr͡rs͡st͡tu͡uv͡vw͡wx͡xy͡yz͡zı͡ıȷ͡ȷ'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\t{' + char + '}' + char
    text += r'\t{\i}\i'  # dotless i
    text += r'\t{\j}\j'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_breve():
    r"""LaTex command for a breve on the character, e.g. \u{a}"""
    answer = 'ĂB̆C̆D̆ĔF̆ĞH̆ĬJ̆K̆L̆M̆N̆ŎP̆Q̆R̆S̆T̆ŬV̆W̆X̆Y̆Z̆ăb̆c̆d̆ĕf̆ğh̆ĭj̆k̆l̆m̆n̆ŏp̆q̆r̆s̆t̆ŭv̆w̆x̆y̆z̆ı̆ȷ̆'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\u{' + char + '}'
    text += r'\u{\i}'  # dotless i
    text += r'\u{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_double_vertical_line_above():
    r"""LaTex command for a double vertical line above the character,
    e.g. \b{a}"""
    answer = 'A̎B̎C̎D̎E̎F̎G̎H̎I̎J̎K̎L̎M̎N̎O̎P̎Q̎R̎S̎T̎U̎V̎W̎X̎Y̎Z̎a̎b̎c̎d̎e̎f̎g̎h̎i̎j̎k̎l̎m̎n̎o̎p̎q̎r̎s̎t̎u̎v̎w̎x̎y̎z̎ı̎ȷ̎'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\U{' + char + '}'
    text += r'\U{\i}'  # dotless i
    text += r'\U{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_caron():
    r"""LaTex command for a caron on the character, e.g. \v{a}"""
    answer = 'ǍB̌ČĎĚF̌ǦȞǏJ̌ǨĽM̌ŇǑP̌Q̌ŘŠŤǓV̌W̌X̌Y̌Žǎb̌čďěf̌ǧȟǐǰǩľm̌ňǒp̌q̌řšťǔv̌w̌x̌y̌žı̌ȷ̌'  # noqa: E501

    text = ''
    for char in list(alphabet):
        text += r'\v{' + char + '}'
    text += r'\v{\i}'  # dotless i
    text += r'\v{\j}'  # dotless j

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_symbols():
    r"""LaTex command for symbols, e.g. \i"""
    answer = 'ıȷłŁøØ'  # noqa: E501

    text = ''
    for char in list('ijlLoO'):
        text += '\\' + char

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)


def test_latex_dashes():
    r"""LaTex command for dashes, e.g. \i"""
    answer = '- – —'  # noqa: E501

    text = '- -- ---'

    result = decode_latex(text)
    check = encode_latex(result)

    assert (result == answer and check == text)
