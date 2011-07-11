import re, string

__all__ = [ "Halfmark" ]

re_type = type(re.compile(""))

def curry_method(method):
    def curried(func):
        return lambda *args, **kwargs: func.__call__(method.__class__, *args, **kwargs)
    setattr(method.__class__, method.__name__, curried(method))
    return method

class Halfmark(object):
    entities = (
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        # double curly quotes
        (re.compile(r'(?<!\S)"(.*?)"(?![a-zA-Z0-9])'), r'&#8220;\1&#8221;'),
        # single curly quotes
        (re.compile(r"(?<!\S)'(.*?)'(?![a-zA-Z0-9])"), r'&#8216;\1&#8217;'),
        # leftover quotes
        (re.compile(r'\b"'), r'&#8221;'), # double curly
        (re.compile(r'"\b'), r'&#8220;'),
        (re.compile(r'"'),   r'&#8221;'),
        (re.compile(r"\b'"), r'&#8217;'), # single curly
        (re.compile(r"'\b"), r'&#8216;'),
        (re.compile(r"'"),   r'&#8217;'),
        
        # emdash
        (re.compile(r"(?<!-)--(?!-)"), r'&mdash;'),
        # TODO: transform word- word to word -- word?
        
        # endash
        (' - ', ' &ndash; '),
        #
    )
    
    def __init__(self, whitelist=None, *args, **kwargs):
        self.whitelist = whitelist or []
        self.entities  = Halfmark.entities # TODO extend with args
    
    def render(self, text):
        text = text.strip()
        if not text:
            return text
        # TODO don't markup anything between ``?
        text = self.html_encode(text)
        text = self.strong(text)
        text = self.em(text)
        text = self.code(text)
        text = self.blockify(text)
        return text
    
    def html_encode(self, text):
        for k, v in self.entities:
            if isinstance(k, str):
                text = text.replace(k, v)
            elif isinstance(k, re_type):
                text = k.sub(v, text)
        return text
    
    def strong(self, text):
        text = self.swap_symbol_with_tag(text, '*', 'strong')
        return text
    
    def em(self, text):
        text = self.swap_symbol_with_tag(text, '_', 'em')
        return text
    
    def code(self, text):
        text = self.swap_symbol_with_tag(text, '`', 'code')
        return text
    
    def swap_symbol_with_tag(self, text, symbol, tag):
        symbol = re.escape(symbol)
        tag    = r'<%s>\1</%s>' % (tag, tag)
        text   = re.sub(r'(?<![a-zA-Z0-9])%s([a-zA-Z0-9]+)%s(?![^a-zA-Z0-9])'
               % (symbol, symbol), tag, text)
        text   = re.sub(r'(?<!\S)%s(?!\s)(.+?)(?<!\s)%s(?!\S)'
               % (symbol, symbol), tag, text)
        text   = re.sub(r'(?<![^a-zA-Z0-9])%s([a-zA-Z0-9]+)%s(?![a-zA-Z0-9])'
               % (symbol, symbol), tag, text)
        return text
    
    def blockify(self, text):
        new_text = ""
        chunks = re.split(r'\n\n+', text)
        for chunk in chunks:
            if chunk.startswith('* '):
                chunk = self.listify(chunk)
            elif chunk.startswith('# '):
                chunk = self.listify(chunk, ordered=True)
            else:
                matched = re.match(r'^(\={1,6})\s*', chunk)
                if matched:
                    length = len(matched.group(0))
                    level  = len(matched.group(1))
                    chunk  = self.headerify(chunk[length:], level)
                else:
                    chunk = self.paragraphify(chunk)
            new_text += chunk
        return new_text
    
    def headerify(self, text, level=1):
        tag  = '<h%i>%s</h%i>'
        text = tag % (level, text, level)
        return text

    def listify(self, text, level=1, ordered=False):
        symbol = '#' if ordered else '*'
        starts = '%s ' % (symbol * level)
        tag    = '<ol>%s</ol>' if ordered else '<ul>%s</ul>'
        chunks = re.split(r'(?<![^\n])%s' % re.escape(starts), text)
        chunks = filter(None, chunks)
        li_tag = '<li>%s</li>'
        
        next_starts = symbol + starts
        new_text    = ""
        for chunk in chunks:
            subchunks = chunk.split('\n')
            subchunks = filter(None, subchunks)
            sub_text  = subchunks.pop(0)
            for subchunk in subchunks:
                if subchunk.startswith(next_starts):
                    sub_text += self.listify(subchunk,
                        level=level + 1,
                        ordered=ordered)
                else:
                    sub_text += '<br/>' + subchunk
            new_text += li_tag % sub_text
        return tag % new_text

    def paragraphify(self, text):
        tag = '<p>%s</p>' % text
        tag = tag.replace('\n', '<br/>')
        return tag
