#!/usr/bin/env python3

import re
import sys
from collections import namedtuple
import json

################################# Lexer #################################

SKIP_RE = re.compile(r'(\s+|\#.*)+')
INT_RE = re.compile(r'\d(\_?\d+)*')
ATOM_RE = re.compile(r'\:[_a-zA-Z]\w*')
KEY_RE = re.compile(r'[_a-zA-Z]\w*\:')
BOOL_RE = re.compile(r'\b(true|false)\b')
ARROW_RE = re.compile(r'\=\>')
FANCY_LBRACE_RE = re.compile(r'\%\{')

Token = namedtuple('Token', 'kind lexeme pos')

def tokenize(text, pos=0):
    toks = []
    while pos < len(text):
        m = SKIP_RE.match(text, pos)
        if m:
            pos += len(m.group())
        if pos >= len(text): break
        if m := INT_RE.match(text, pos):
            tok = Token('INT', m.group(), pos)
        elif m := ATOM_RE.match(text, pos):
            tok = Token('ATOM', m.group(), pos)
        elif m := KEY_RE.match(text, pos):
            tok = Token('KEY', m.group(), pos)
        elif m := BOOL_RE.match(text, pos):
            tok = Token('BOOL', m.group(), pos)
        elif m := ARROW_RE.match(text, pos):
            tok = Token('=>', m.group(), pos)
        elif m := FANCY_LBRACE_RE.match(text, pos):
            tok = Token('%{', m.group(), pos)
        else:
            tok = Token(text[pos], text[pos], pos)
        pos += len(tok.lexeme)
        toks.append(tok)
    toks.append(Token('EOF', '<EOF>', pos))
    return toks

################################# Parser #################################

def parse(text):
    toks = tokenize(text)
    toksIndex = 0
    tok = toks[toksIndex]
    toksIndex += 1

    def peek(kind):
        nonlocal tok
        return tok.kind == kind

    def consume(kind):
        nonlocal tok, toks, toksIndex
        if (peek(kind)):
            tok = toks[toksIndex]
            toksIndex += 1
        else:
            error(kind, text)

    def error(kind, text):
        nonlocal tok
        pos = tok.pos
        if pos >= len(text) or text[pos] == '\n': pos -= 1
        lineBegin = text.rfind('\n', 0, pos)
        if lineBegin < 0: lineBegin = 0
        lineEnd = text.find('\n', pos)
        if lineEnd < 0: lineEnd = len(text)
        line = text[lineBegin:lineEnd]
        print(f"error: expecting '{kind}' but got '{tok.kind}'", file=sys.stderr)
        print(line, file=sys.stderr)
        nSpace = pos - lineBegin if pos >= lineBegin else 0
        print('^'.rjust(nSpace+1), file=sys.stderr)
        sys.exit(1)

    def data_items():
        items = [];
        while is_item_start():
            items.append(data_item());
        return items

    def data_item():
        if peek('['):
            return list();
        elif peek('{'):
            return tuple();
        elif peek('%{'):
            return map();
        else:
            return primitive();

    def list():
        items = []
        consume('[')
        if is_item_start():
            items.append(data_item());
            while peek(','):
                consume(',')
                items.append(data_item())
        consume(']');
        return { '%k': 'list', '%v': items };

    def tuple():
        items = []
        consume('{')
        if is_item_start():
            items.append(data_item());
            while peek(','):
                consume(',')
                items.append(data_item())
        consume('}');
        return { '%k': 'tuple', '%v': items };

    def map():
        pairs = []
        consume('%{')
        if is_item_start() or peek('KEY'):
            pairs.append(keyValue());
            while peek(','):
                consume(',')
                pairs.append(keyValue())
        consume('}');
        return { '%k': 'map', '%v': pairs };

    def primitive():
        if peek('INT'):
            v = int(tok.lexeme.replace('_', ''));
            consume('INT');
            return { '%k': 'int', '%v': v };
        elif peek('ATOM'):
            v = tok.lexeme;
            consume('ATOM');
            return { '%k': 'atom', '%v': v };
        else:
            v = tok.lexeme == 'true';
            consume('BOOL');
            return { '%k': 'bool', '%v': v };

    def keyValue():
        key = '';
        if peek('KEY'):
            atom = ':' + tok.lexeme[0:-1];
            consume('KEY');
            key = { '%k': 'atom', '%v': atom };
        else:
            key = data_item();
            consume('=>');
        value = data_item();
        return [ key, value ];

    def is_item_start():
        return peek('ATOM') or peek('INT') or peek('BOOL') or \
               peek('[') or peek('{') or peek('%{');

    items = data_items()
    if tok.kind != 'EOF': error('EOF', text)
    return items

################################# Integration with Web Application ################################

def parse_text(text):
    try:
        result = parse(text)
        return json.dumps(result, separators=(',', ':'))
    except Exception as e:
        return json.dumps({"error": str(e)})

