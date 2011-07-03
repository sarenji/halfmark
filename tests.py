from halfmark import Halfmark

_hm = Halfmark()

def pos(input, result):
    rendered = _hm.render(input)
    assert rendered == result, "Wanted:\n%s\nGot:\n%s" % (result, rendered)

def neg(input, result):
    assert _hm.render(input) != result

def testWhitespace():
    pos("hello world.", "<p>hello world.</p>")
    pos("hello world.\n\nhi", "<p>hello world.</p><p>hi</p>")
    pos("hello world.\n\n\nhi", "<p>hello world.</p><p>hi</p>")
    pos("hello world.\nhi", "<p>hello world.<br/>hi</p>")

def testQuotes():
    pos('hey "wat up" ?', '<p>hey &#8220;wat up&#8221; ?</p>')
    pos('hey "wat up"?', '<p>hey &#8220;wat up&#8221;?</p>')
    pos('"wat up" ?', '<p>&#8220;wat up&#8221; ?</p>')
    pos('"wat up"?', '<p>&#8220;wat up&#8221;?</p>')
    pos('1"wat up" ?', '<p>1&#8221;wat up&#8221; ?</p>')
    pos('this is--', '<p>this is&mdash;</p>')

def testDashes():
    pos('--not that amazing', '<p>&mdash;not that amazing</p>')
    pos('check--this out', '<p>check&mdash;this out</p>')
    pos('check this-- out', '<p>check this&mdash; out</p>')
    pos('check this --out', '<p>check this &mdash;out</p>')
    pos('Speed -- of an unladen swallow?', '<p>Speed &mdash; of an unladen swallow?</p>')
    pos('Go on - go on.', '<p>Go on &ndash; go on.</p>')

def testStrong():
    pos('*this* is amazing', '<p><strong>this</strong> is amazing</p>')
    pos('*this* is amazing*', '<p><strong>this</strong> is amazing*</p>')
    pos('*this i*s* amazing*', '<p><strong>this i*s</strong> amazing*</p>')
    pos('th*is i*s* amazing*', '<p>th*is i<strong>s</strong> amazing*</p>')
    pos('th*is *i*s amazing*', '<p>th*is <strong>i</strong>s amazing*</p>')

def testEm():
    pos('_Herp_ derp.', '<p><em>Herp</em> derp.</p>')
    pos('Herp _derp._', '<p>Herp <em>derp.</em></p>')
    pos('Herp_ derp._', '<p>Herp_ derp._</p>')
    pos('_Herp _derp.', '<p>_Herp _derp.</p>')
    pos('This _variable herp_derp has a cool name._', '<p>This <em>variable herp_derp has a cool name.</em></p>')

def testSmileys():
    pos('*_*', '<p><strong>_</strong></p>')
    pos('*-*', '<p><strong>-</strong></p>')
    pos('*-*', '<p><strong>-</strong></p>')
    pos('*@*', '<p><strong>@</strong></p>')
    pos('*A*', '<p><strong>A</strong></p>')

if __name__ == "__main__":
    testQuotes()
    testWhitespace()
    testDashes()
    testStrong()
    testEm()
    testSmileys()