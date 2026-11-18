"""
parser.py - the LL(1) table-driven (predictive) syntax analyzer.

Input is the lexer's token list.  Newline, space, tab and comment tokens are
dropped and EOF becomes the end marker $.  The parser keeps a stack that
starts as [$, <program>]:

  * top is a terminal  -> it must equal the current token; pop and advance.
  * top is a non-terminal -> look up TABLE[top][token]; pop it and push the
    production's right side in reverse.  No entry is a syntax error.

Parsing stops at the first syntax error, which reports the token found and
every token that could have been accepted there.
"""

from .grammar import PRODUCTIONS, START, END, is_nonterminal
from .ll1 import TABLE

SKIPPED = {"newline", "space", "tab", "single_comm", "multi_comm"}


class SyntaxError_(Exception):
    """A syntax error (named with _ so it does not hide Python's SyntaxError)."""

    def __init__(self, message, line, col, found, lexeme, expected):
        super().__init__("%d:%d %s" % (line, col, message))
        self.message = message
        self.line = line
        self.col = col
        self.found = found          # token name, e.g. id, ;, $
        self.lexeme = lexeme
        self.expected = expected    # sorted list of token names
        self.kind = "Syntax error"


def _show(tok):
    return "end of file" if tok == END else "'%s'" % tok


def _sort_expected(tokens):
    return sorted(tokens, key=lambda t: (t == END, t))


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.type not in SKIPPED]
        self.errors = []
        self.steps = []     # production numbers applied, in order (leftmost derivation)

    def _token_name(self, tok):
        return END if tok.type == "EOF" else tok.type

    def parse(self):
        toks = self.tokens
        if not toks or toks[-1].type != "EOF":
            raise ValueError("token list must end with EOF")
        stack = [END, START]
        i = 0
        while stack:
            top = stack.pop()
            tok = toks[i]
            name = self._token_name(tok)

            if top == END:
                if name == END:
                    return True
                self._error(tok, name, [END])
                return False

            if not is_nonterminal(top):
                if top == name:
                    i += 1
                    continue
                self._error(tok, name, [top])
                return False

            k = TABLE[top].get(name)
            if k is None:
                self._error(tok, name, _sort_expected(TABLE[top]), top)
                return False
            self.steps.append(k)
            stack.extend(reversed(PRODUCTIONS[k - 1][1]))
        return False

    def _error(self, tok, name, expected, nonterminal=None):
        exp_text = ", ".join(_show(e) for e in expected)
        if name == END or name == tok.lexeme:
            found = _show(name)                       # e.g. ';' or end of file
        else:
            found = "%s '%s'" % (name, tok.lexeme)    # e.g. id 'score'
        msg = "Unexpected %s" % found
        if nonterminal:
            msg += " while parsing %s" % nonterminal
        msg += "."
        err = SyntaxError_(msg, tok.line, tok.col, name, tok.lexeme, expected)
        err.expected_text = exp_text
        err.nonterminal = nonterminal
        self.errors.append(err)


def parse(tokens):
    """Parse a token list.  Returns the Parser (check .errors)."""
    p = Parser(tokens)
    p.parse()
    return p
