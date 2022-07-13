import re
from rdflib import Literal, URIRef, BNode
from rdflib.plugins.parsers.ntriples import unquote, ParseError

uriref = r'<([^:]+:[^\s"<>]+)>'
literal = r'"([^"\\]*(?:\\.[^"\\]*)*)"'
litinfo = r'(?:@([a-z]+(?:-[a-zA-Z0-9]+)*)|\^\^' + uriref + r')?'
r_literal = re.compile(literal + litinfo)


def str_to_uri(string):
    # string =  string.encode().decode('raw-unicode-escape')
    return URIRef(string)

def subject_to_rdflib(term):
    if "nodeID://" in term:
        return BNode(term.split("//")[1])
    elif ("://") in term:
        return str_to_uri(term)
    else:
        return BNode(term)

def tuple_to_triple(tuple):

    try:
        # Subject
        subject = subject_to_rdflib(tuple[0])

        # Predicate
        predicate = str_to_uri(tuple[1])

        # Object
        if tuple[2].startswith('"'):
            object = parse_literal(str(tuple[2]))
        else:
            object = str_to_uri(tuple[2])
        return (subject, predicate, object)
    except ParseError as e:
        raise e


def parse_literal(strng):
    m = r_literal.match(strng)
    if not m:
        m = r_literal.match(strng.replace("\\", ""))
    if not m:
        raise ParseError("Failed to eat %s at %s" % (r_literal.pattern, strng))
    lit, lang, dtype = m.groups()
    if lang:
        lang = lang
    else:
        lang = None
    if dtype:
        dtype = dtype
    else:
        dtype = None
    if lang and dtype:
        raise ParseError("Can't have both a language and a datatype")
    lit = unquote(lit)
    return Literal(lit, lang, dtype)


def _quoteLiteral(value, language=None, datatype=None):
    '''
    a simpler version of term.Literal.n3()
    '''

    encoded = _quote_encode(value)

    if language:
        if datatype:
            raise Exception("Literal has datatype AND language!")
        return '%s@%s' % (encoded, language)
    elif datatype:
        return '%s^^<%s>' % (encoded, datatype)
    else:
        return '%s' % encoded


def _quote_encode(l):
    return '"%s"' % l.replace('\\', '\\\\')\
        .replace('\n', '\\n')\
        .replace('"', '\\"')\
        .replace('\r', '\\r')

def _quote_encode_uri(u):
    return f"<{u.replace(' ', '')}>"
    return '<%s>' % u.replace('\\', '\\\\')\
        .replace('\n', '\\n')\
        .replace('"', '')\
        .replace('\r', '\\r')

def tuple_to_ntriple(tuple):
    try:
        # Subject
        if tuple[0].startswith("_"):
            subject = tuple[0]
        else:
            subject = _quote_encode_uri(tuple[0])

        # Predicate
        predicate = _quote_encode_uri(tuple[1])

        # Object
        if tuple[2].startswith('"'):
            litstr = tuple[2].replace("\\", "")
            m = r_literal.match(litstr)
            if not m:
                raise ParseError(f"Could not parse Literal: {tuple[2]}")
            lit, lang, dtype = m.groups()
            lit = unquote(lit)
            object = _quoteLiteral(lit, lang, dtype)
        elif tuple[2].startswith("_"):
            object = tuple[2]
        else:
            object = _quote_encode_uri(tuple[2])
        return f"{subject} {predicate} {object} .\n"
    except ParseError as e:
        raise ParseError(f"Could not parse triple: {tuple}")