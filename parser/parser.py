"""
parser.py - the LL(1) syntax analyzer, written as one if / elif branch per
non-terminal and one per (non-terminal, token) pair, the same way the lexer
is written as one branch per transition-diagram state.

Input is the lexer's token list.  Newline, space, tab and comment tokens are
dropped and EOF becomes the end marker $.

The parser keeps a stack of the symbols it still expects.  It starts as
[$, <program>] and each round of the loop looks at the top of the stack and
the current token t (the lookahead):

  * top is $          -> t must also be $: the program is accepted.
  * top is a terminal -> t must be the same token: pop it and read the next
                         token ("Match").
  * top is <something> -> the branch for that non-terminal checks t against
                         the PREDICT SET of each of its productions
                         (pp. 144-167) and sets prod to the production
                         number, like the lexer sets state.  The
                         non-terminal is then replaced on the stack by the
                         right side of production `prod` (grammar.py).
                         If no PREDICT set holds t, prod stays None and it
                         is a syntax error.

Parsing stops at the first syntax error, which reports the token found and
every token that could have been accepted there.
"""

from .grammar import PRODUCTIONS, START, END, is_nonterminal

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
        self.expected = expected    # list of token names
        self.kind = "Syntax error"


def _show(tok):
    return "end of file" if tok == END else "'%s'" % tok


def production_text(k):
    """Production k as written in the paper, e.g. '<var_tail> → = <base_init>'."""
    lhs, rhs = PRODUCTIONS[k - 1]
    return "%s → %s" % (lhs, " ".join(rhs) if rhs else "λ")


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.type not in SKIPPED]
        self.pos = 0
        self.errors = []
        self.steps = []     # production numbers applied, in order (leftmost derivation)
        self.trace = []     # every step: stack, lookahead, action (see _trace)

    def parse(self):
        toks = self.tokens
        if not toks or toks[-1].type != "EOF":
            raise ValueError("token list must end with EOF")
        stack = [END, START]

        while True:
            stack_before = " ".join(reversed(stack))      # top of stack first
            top = stack.pop()
            tok = toks[self.pos]
            t = END if tok.type == "EOF" else tok.type    # current token
            prod = None
            expected = []

            # --- end marker: every production is done -------------------------------
            if top == END:
                if t == END:
                    self._trace(stack_before, tok, t, "accept", None,
                                "Accept: input fully parsed")
                    return True
                self._fail(stack_before, tok, t, [END])
                return False

            # --- terminal on top: it must be the current token ----------------------
            if not is_nonterminal(top):
                if t == top:
                    self._trace(stack_before, tok, t, "match", None,
                                "Match %s" % _show(t))
                    self.pos += 1
                    continue
                self._fail(stack_before, tok, t, [top])
                return False

            # --- non-terminal on top: pick the production from the PREDICT sets ------
            if top == "<program>":
                #   1  <program> → <global_decl> <functions> <statements>
                if t == "++":                    # PREDICT 1
                    prod = 1
                elif t == "--":                  # PREDICT 1
                    prod = 1
                elif t == "Append":              # PREDICT 1
                    prod = 1
                elif t == "Blend":               # PREDICT 1
                    prod = 1
                elif t == "Clear":               # PREDICT 1
                    prod = 1
                elif t == "Factor":              # PREDICT 1
                    prod = 1
                elif t == "Harvest":             # PREDICT 1
                    prod = 1
                elif t == "Insert":              # PREDICT 1
                    prod = 1
                elif t == "Mix":                 # PREDICT 1
                    prod = 1
                elif t == "Pour":                # PREDICT 1
                    prod = 1
                elif t == "Produce":             # PREDICT 1
                    prod = 1
                elif t == "Reap":                # PREDICT 1
                    prod = 1
                elif t == "Recipe":              # PREDICT 1
                    prod = 1
                elif t == "Remove":              # PREDICT 1
                    prod = 1
                elif t == "Same":                # PREDICT 1
                    prod = 1
                elif t == "Squeeze":             # PREDICT 1
                    prod = 1
                elif t == "Test":                # PREDICT 1
                    prod = 1
                elif t == "Uproot":              # PREDICT 1
                    prod = 1
                elif t == "Vary":                # PREDICT 1
                    prod = 1
                elif t == "id":                  # PREDICT 1
                    prod = 1
                elif t == "$":                   # PREDICT 1
                    prod = 1
                else:
                    expected = ["++", "--", "Append", "Blend", "Clear", "Factor",
                                "Harvest", "Insert", "Mix", "Pour", "Produce", "Reap",
                                "Recipe", "Remove", "Same", "Squeeze", "Test", "Uproot",
                                "Vary", "id", "$"]

            elif top == "<global_decl>":
                #   2  <global_decl> → <global_item> <global_decl>
                #   3  <global_decl> → λ
                if t == "Recipe":                # PREDICT 2
                    prod = 2
                elif t == "Same":                # PREDICT 2
                    prod = 2
                elif t == "Vary":                # PREDICT 2
                    prod = 2
                elif t == "++":                  # PREDICT 3
                    prod = 3
                elif t == "--":                  # PREDICT 3
                    prod = 3
                elif t == "Append":              # PREDICT 3
                    prod = 3
                elif t == "Blend":               # PREDICT 3
                    prod = 3
                elif t == "Clear":               # PREDICT 3
                    prod = 3
                elif t == "Factor":              # PREDICT 3
                    prod = 3
                elif t == "Harvest":             # PREDICT 3
                    prod = 3
                elif t == "Insert":              # PREDICT 3
                    prod = 3
                elif t == "Mix":                 # PREDICT 3
                    prod = 3
                elif t == "Pour":                # PREDICT 3
                    prod = 3
                elif t == "Produce":             # PREDICT 3
                    prod = 3
                elif t == "Reap":                # PREDICT 3
                    prod = 3
                elif t == "Remove":              # PREDICT 3
                    prod = 3
                elif t == "Squeeze":             # PREDICT 3
                    prod = 3
                elif t == "Test":                # PREDICT 3
                    prod = 3
                elif t == "Uproot":              # PREDICT 3
                    prod = 3
                elif t == "id":                  # PREDICT 3
                    prod = 3
                elif t == "$":                   # PREDICT 3
                    prod = 3
                else:
                    expected = ["++", "--", "Append", "Blend", "Clear", "Factor",
                                "Harvest", "Insert", "Mix", "Pour", "Produce", "Reap",
                                "Recipe", "Remove", "Same", "Squeeze", "Test", "Uproot",
                                "Vary", "id", "$"]

            elif top == "<global_item>":
                #   4  <global_item> → <var_decl> ;
                #   5  <global_item> → <const_decl> ;
                #   6  <global_item> → Recipe id <recipe_tail>
                if t == "Vary":                  # PREDICT 4
                    prod = 4
                elif t == "Same":                # PREDICT 5
                    prod = 5
                elif t == "Recipe":              # PREDICT 6
                    prod = 6
                else:
                    expected = ["Recipe", "Same", "Vary"]

            elif top == "<recipe_tail>":
                #   7  <recipe_tail> → { <member> <member_tail> }
                #   8  <recipe_tail> → : id ;
                if t == "{":                     # PREDICT 7
                    prod = 7
                elif t == ":":                   # PREDICT 8
                    prod = 8
                else:
                    expected = [":", "{"]

            elif top == "<member_tail>":
                #   9  <member_tail> → <member> <member_tail>
                #  10  <member_tail> → λ
                if t == "id":                    # PREDICT 9
                    prod = 9
                elif t == "}":                   # PREDICT 10
                    prod = 10
                else:
                    expected = ["id", "}"]

            elif top == "<member>":
                #  11  <member> → id : <type_spec> ;
                if t == "id":                    # PREDICT 11
                    prod = 11
                else:
                    expected = ["id"]

            elif top == "<var_decl>":
                #  12  <var_decl> → Vary id : <data_type> <var_tail>
                if t == "Vary":                  # PREDICT 12
                    prod = 12
                else:
                    expected = ["Vary"]

            elif top == "<var_tail>":
                #  13  <var_tail> → = <base_init>
                #  14  <var_tail> → [ ] <arr_tail>
                if t == "=":                     # PREDICT 13
                    prod = 13
                elif t == "[":                   # PREDICT 14
                    prod = 14
                else:
                    expected = ["=", "["]

            elif top == "<arr_tail>":
                #  15  <arr_tail> → = <array_1d_value>
                #  16  <arr_tail> → [ ] = <array_2d_value>
                if t == "=":                     # PREDICT 15
                    prod = 15
                elif t == "[":                   # PREDICT 16
                    prod = 16
                else:
                    expected = ["=", "["]

            elif top == "<base_init>":
                #  17  <base_init> → <expression>
                #  18  <base_init> → Absorb ( )
                if t == "(":                     # PREDICT 17
                    prod = 17
                elif t == "++":                  # PREDICT 17
                    prod = 17
                elif t == "--":                  # PREDICT 17
                    prod = 17
                elif t == "Length":              # PREDICT 17
                    prod = 17
                elif t == "Not":                 # PREDICT 17
                    prod = 17
                elif t == "ToNumber":            # PREDICT 17
                    prod = 17
                elif t == "ToRational":          # PREDICT 17
                    prod = 17
                elif t == "ToTruth":             # PREDICT 17
                    prod = 17
                elif t == "ToWord":              # PREDICT 17
                    prod = 17
                elif t == "boo_lit":             # PREDICT 17
                    prod = 17
                elif t == "flo_lit":             # PREDICT 17
                    prod = 17
                elif t == "id":                  # PREDICT 17
                    prod = 17
                elif t == "int_lit":             # PREDICT 17
                    prod = 17
                elif t == "str_lit":             # PREDICT 17
                    prod = 17
                elif t == "~":                   # PREDICT 17
                    prod = 17
                elif t == "Absorb":              # PREDICT 18
                    prod = 18
                else:
                    expected = ["(", "++", "--", "Absorb", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "id", "int_lit", "str_lit", "~"]

            elif top == "<array_1d_value>":
                #  19  <array_1d_value> → <basket_1d>
                #  20  <array_1d_value> → <array_source>
                if t == "Basket":                # PREDICT 19
                    prod = 19
                elif t == "id":                  # PREDICT 20
                    prod = 20
                else:
                    expected = ["Basket", "id"]

            elif top == "<array_2d_value>":
                #  21  <array_2d_value> → <basket_2d>
                #  22  <array_2d_value> → <array_source>
                if t == "Basket":                # PREDICT 21
                    prod = 21
                elif t == "id":                  # PREDICT 22
                    prod = 22
                else:
                    expected = ["Basket", "id"]

            elif top == "<array_source>":
                #  23  <array_source> → id <name_tail>
                if t == "id":                    # PREDICT 23
                    prod = 23
                else:
                    expected = ["id"]

            elif top == "<basket_1d>":
                #  24  <basket_1d> → Basket [ <elem_list> ]
                if t == "Basket":                # PREDICT 24
                    prod = 24
                else:
                    expected = ["Basket"]

            elif top == "<elem_list>":
                #  25  <elem_list> → <expression> <elem_tail>
                #  26  <elem_list> → λ
                if t == "(":                     # PREDICT 25
                    prod = 25
                elif t == "++":                  # PREDICT 25
                    prod = 25
                elif t == "--":                  # PREDICT 25
                    prod = 25
                elif t == "Length":              # PREDICT 25
                    prod = 25
                elif t == "Not":                 # PREDICT 25
                    prod = 25
                elif t == "ToNumber":            # PREDICT 25
                    prod = 25
                elif t == "ToRational":          # PREDICT 25
                    prod = 25
                elif t == "ToTruth":             # PREDICT 25
                    prod = 25
                elif t == "ToWord":              # PREDICT 25
                    prod = 25
                elif t == "boo_lit":             # PREDICT 25
                    prod = 25
                elif t == "flo_lit":             # PREDICT 25
                    prod = 25
                elif t == "id":                  # PREDICT 25
                    prod = 25
                elif t == "int_lit":             # PREDICT 25
                    prod = 25
                elif t == "str_lit":             # PREDICT 25
                    prod = 25
                elif t == "~":                   # PREDICT 25
                    prod = 25
                elif t == "]":                   # PREDICT 26
                    prod = 26
                else:
                    expected = ["(", "++", "--", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "]", "boo_lit",
                                "flo_lit", "id", "int_lit", "str_lit", "~"]

            elif top == "<elem_tail>":
                #  27  <elem_tail> → , <expression> <elem_tail>
                #  28  <elem_tail> → λ
                if t == ",":                     # PREDICT 27
                    prod = 27
                elif t == "]":                   # PREDICT 28
                    prod = 28
                else:
                    expected = [",", "]"]

            elif top == "<basket_2d>":
                #  29  <basket_2d> → Basket [ <row_items> ]
                if t == "Basket":                # PREDICT 29
                    prod = 29
                else:
                    expected = ["Basket"]

            elif top == "<row_items>":
                #  30  <row_items> → <row_item> <row_items_tail>
                #  31  <row_items> → λ
                if t == "[":                     # PREDICT 30
                    prod = 30
                elif t == "id":                  # PREDICT 30
                    prod = 30
                elif t == "]":                   # PREDICT 31
                    prod = 31
                else:
                    expected = ["[", "]", "id"]

            elif top == "<row_items_tail>":
                #  32  <row_items_tail> → , <row_item> <row_items_tail>
                #  33  <row_items_tail> → λ
                if t == ",":                     # PREDICT 32
                    prod = 32
                elif t == "]":                   # PREDICT 33
                    prod = 33
                else:
                    expected = [",", "]"]

            elif top == "<row_item>":
                #  34  <row_item> → [ <elem_list> ]
                #  35  <row_item> → id <accessor>
                if t == "[":                     # PREDICT 34
                    prod = 34
                elif t == "id":                  # PREDICT 35
                    prod = 35
                else:
                    expected = ["[", "id"]

            elif top == "<const_decl>":
                #  36  <const_decl> → Same id : <data_type> <const_tail>
                if t == "Same":                  # PREDICT 36
                    prod = 36
                else:
                    expected = ["Same"]

            elif top == "<const_tail>":
                #  37  <const_tail> → = <base_init>
                #  38  <const_tail> → [ ] <const_arr>
                if t == "=":                     # PREDICT 37
                    prod = 37
                elif t == "[":                   # PREDICT 38
                    prod = 38
                else:
                    expected = ["=", "["]

            elif top == "<const_arr>":
                #  39  <const_arr> → = <same_basket_1d>
                #  40  <const_arr> → [ ] = <same_basket_2d>
                if t == "=":                     # PREDICT 39
                    prod = 39
                elif t == "[":                   # PREDICT 40
                    prod = 40
                else:
                    expected = ["=", "["]

            elif top == "<same_basket_1d>":
                #  41  <same_basket_1d> → Basket [ <literal> <lit_tail> ]
                if t == "Basket":                # PREDICT 41
                    prod = 41
                else:
                    expected = ["Basket"]

            elif top == "<lit_tail>":
                #  42  <lit_tail> → , <literal> <lit_tail>
                #  43  <lit_tail> → λ
                if t == ",":                     # PREDICT 42
                    prod = 42
                elif t == "]":                   # PREDICT 43
                    prod = 43
                else:
                    expected = [",", "]"]

            elif top == "<same_basket_2d>":
                #  44  <same_basket_2d> → Basket [ <lit_row> <lit_row_tail> ]
                if t == "Basket":                # PREDICT 44
                    prod = 44
                else:
                    expected = ["Basket"]

            elif top == "<lit_row>":
                #  45  <lit_row> → [ <literal> <lit_tail> ]
                if t == "[":                     # PREDICT 45
                    prod = 45
                else:
                    expected = ["["]

            elif top == "<lit_row_tail>":
                #  46  <lit_row_tail> → , <lit_row> <lit_row_tail>
                #  47  <lit_row_tail> → λ
                if t == ",":                     # PREDICT 46
                    prod = 46
                elif t == "]":                   # PREDICT 47
                    prod = 47
                else:
                    expected = [",", "]"]

            elif top == "<literal>":
                #  48  <literal> → int_lit
                #  49  <literal> → flo_lit
                #  50  <literal> → str_lit
                #  51  <literal> → boo_lit
                if t == "int_lit":               # PREDICT 48
                    prod = 48
                elif t == "flo_lit":             # PREDICT 49
                    prod = 49
                elif t == "str_lit":             # PREDICT 50
                    prod = 50
                elif t == "boo_lit":             # PREDICT 51
                    prod = 51
                else:
                    expected = ["boo_lit", "flo_lit", "int_lit", "str_lit"]

            elif top == "<type_spec>":
                #  52  <type_spec> → <data_type> <dims>
                if t == "Number":                # PREDICT 52
                    prod = 52
                elif t == "Rational":            # PREDICT 52
                    prod = 52
                elif t == "Truth":               # PREDICT 52
                    prod = 52
                elif t == "Word":                # PREDICT 52
                    prod = 52
                else:
                    expected = ["Number", "Rational", "Truth", "Word"]

            elif top == "<data_type>":
                #  53  <data_type> → Number
                #  54  <data_type> → Rational
                #  55  <data_type> → Word
                #  56  <data_type> → Truth
                if t == "Number":                # PREDICT 53
                    prod = 53
                elif t == "Rational":            # PREDICT 54
                    prod = 54
                elif t == "Word":                # PREDICT 55
                    prod = 55
                elif t == "Truth":               # PREDICT 56
                    prod = 56
                else:
                    expected = ["Number", "Rational", "Truth", "Word"]

            elif top == "<dims>":
                #  57  <dims> → [ ] <second_dims>
                #  58  <dims> → λ
                if t == "[":                     # PREDICT 57
                    prod = 57
                elif t == ")":                   # PREDICT 58
                    prod = 58
                elif t == ",":                   # PREDICT 58
                    prod = 58
                elif t == ";":                   # PREDICT 58
                    prod = 58
                elif t == "{":                   # PREDICT 58
                    prod = 58
                else:
                    expected = [")", ",", ";", "[", "{"]

            elif top == "<second_dims>":
                #  59  <second_dims> → [ ]
                #  60  <second_dims> → λ
                if t == "[":                     # PREDICT 59
                    prod = 59
                elif t == ")":                   # PREDICT 60
                    prod = 60
                elif t == ",":                   # PREDICT 60
                    prod = 60
                elif t == ";":                   # PREDICT 60
                    prod = 60
                elif t == "{":                   # PREDICT 60
                    prod = 60
                else:
                    expected = [")", ",", ";", "[", "{"]

            elif top == "<init_value>":
                #  61  <init_value> → <expression>
                #  62  <init_value> → <basket_value>
                #  63  <init_value> → Absorb ( )
                if t == "(":                     # PREDICT 61
                    prod = 61
                elif t == "++":                  # PREDICT 61
                    prod = 61
                elif t == "--":                  # PREDICT 61
                    prod = 61
                elif t == "Length":              # PREDICT 61
                    prod = 61
                elif t == "Not":                 # PREDICT 61
                    prod = 61
                elif t == "ToNumber":            # PREDICT 61
                    prod = 61
                elif t == "ToRational":          # PREDICT 61
                    prod = 61
                elif t == "ToTruth":             # PREDICT 61
                    prod = 61
                elif t == "ToWord":              # PREDICT 61
                    prod = 61
                elif t == "boo_lit":             # PREDICT 61
                    prod = 61
                elif t == "flo_lit":             # PREDICT 61
                    prod = 61
                elif t == "id":                  # PREDICT 61
                    prod = 61
                elif t == "int_lit":             # PREDICT 61
                    prod = 61
                elif t == "str_lit":             # PREDICT 61
                    prod = 61
                elif t == "~":                   # PREDICT 61
                    prod = 61
                elif t == "Basket":              # PREDICT 62
                    prod = 62
                elif t == "Absorb":              # PREDICT 63
                    prod = 63
                else:
                    expected = ["(", "++", "--", "Absorb", "Basket", "Length", "Not",
                                "ToNumber", "ToRational", "ToTruth", "ToWord", "boo_lit",
                                "flo_lit", "id", "int_lit", "str_lit", "~"]

            elif top == "<basket_value>":
                #  64  <basket_value> → Basket [ <basket_body> ]
                if t == "Basket":                # PREDICT 64
                    prod = 64
                else:
                    expected = ["Basket"]

            elif top == "<basket_body>":
                #  65  <basket_body> → <basket_items>
                #  66  <basket_body> → λ
                if t == "(":                     # PREDICT 65
                    prod = 65
                elif t == "++":                  # PREDICT 65
                    prod = 65
                elif t == "--":                  # PREDICT 65
                    prod = 65
                elif t == "Length":              # PREDICT 65
                    prod = 65
                elif t == "Not":                 # PREDICT 65
                    prod = 65
                elif t == "ToNumber":            # PREDICT 65
                    prod = 65
                elif t == "ToRational":          # PREDICT 65
                    prod = 65
                elif t == "ToTruth":             # PREDICT 65
                    prod = 65
                elif t == "ToWord":              # PREDICT 65
                    prod = 65
                elif t == "[":                   # PREDICT 65
                    prod = 65
                elif t == "boo_lit":             # PREDICT 65
                    prod = 65
                elif t == "flo_lit":             # PREDICT 65
                    prod = 65
                elif t == "id":                  # PREDICT 65
                    prod = 65
                elif t == "int_lit":             # PREDICT 65
                    prod = 65
                elif t == "str_lit":             # PREDICT 65
                    prod = 65
                elif t == "~":                   # PREDICT 65
                    prod = 65
                elif t == "]":                   # PREDICT 66
                    prod = 66
                else:
                    expected = ["(", "++", "--", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "[", "]", "boo_lit",
                                "flo_lit", "id", "int_lit", "str_lit", "~"]

            elif top == "<basket_items>":
                #  67  <basket_items> → [ <elem_list> ] <row_items_tail>
                #  68  <basket_items> → <elem_not_name> <elem_tail>
                #  69  <basket_items> → id <basket_name_tail>
                if t == "[":                     # PREDICT 67
                    prod = 67
                elif t == "(":                   # PREDICT 68
                    prod = 68
                elif t == "++":                  # PREDICT 68
                    prod = 68
                elif t == "--":                  # PREDICT 68
                    prod = 68
                elif t == "Length":              # PREDICT 68
                    prod = 68
                elif t == "Not":                 # PREDICT 68
                    prod = 68
                elif t == "ToNumber":            # PREDICT 68
                    prod = 68
                elif t == "ToRational":          # PREDICT 68
                    prod = 68
                elif t == "ToTruth":             # PREDICT 68
                    prod = 68
                elif t == "ToWord":              # PREDICT 68
                    prod = 68
                elif t == "boo_lit":             # PREDICT 68
                    prod = 68
                elif t == "flo_lit":             # PREDICT 68
                    prod = 68
                elif t == "int_lit":             # PREDICT 68
                    prod = 68
                elif t == "str_lit":             # PREDICT 68
                    prod = 68
                elif t == "~":                   # PREDICT 68
                    prod = 68
                elif t == "id":                  # PREDICT 69
                    prod = 69
                else:
                    expected = ["(", "++", "--", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "[", "boo_lit",
                                "flo_lit", "id", "int_lit", "str_lit", "~"]

            elif top == "<basket_name_tail>":
                #  70  <basket_name_tail> → ( <arguments> ) <expr_result_tail> <elem_tail>
                #  71  <basket_name_tail> → <accessor> <basket_after_name>
                if t == "(":                     # PREDICT 70
                    prod = 70
                elif t == "!=":                  # PREDICT 71
                    prod = 71
                elif t == "%":                   # PREDICT 71
                    prod = 71
                elif t == "*":                   # PREDICT 71
                    prod = 71
                elif t == "+":                   # PREDICT 71
                    prod = 71
                elif t == "++":                  # PREDICT 71
                    prod = 71
                elif t == ",":                   # PREDICT 71
                    prod = 71
                elif t == "-":                   # PREDICT 71
                    prod = 71
                elif t == "--":                  # PREDICT 71
                    prod = 71
                elif t == ".":                   # PREDICT 71
                    prod = 71
                elif t == "/":                   # PREDICT 71
                    prod = 71
                elif t == "<":                   # PREDICT 71
                    prod = 71
                elif t == "<=":                  # PREDICT 71
                    prod = 71
                elif t == "==":                  # PREDICT 71
                    prod = 71
                elif t == ">":                   # PREDICT 71
                    prod = 71
                elif t == ">=":                  # PREDICT 71
                    prod = 71
                elif t == "And":                 # PREDICT 71
                    prod = 71
                elif t == "Or":                  # PREDICT 71
                    prod = 71
                elif t == "[":                   # PREDICT 71
                    prod = 71
                elif t == "]":                   # PREDICT 71
                    prod = 71
                elif t == "^":                   # PREDICT 71
                    prod = 71
                else:
                    expected = ["!=", "%", "(", "*", "+", "++", ",", "-", "--", ".", "/",
                                "<", "<=", "==", ">", ">=", "And", "Or", "[", "]", "^"]

            elif top == "<basket_after_name>":
                #  72  <basket_after_name> → , <basket_items>
                #  73  <basket_after_name> → <expr_var_ops> <elem_tail>
                #  74  <basket_after_name> → λ
                if t == ",":                     # PREDICT 72
                    prod = 72
                elif t == "!=":                  # PREDICT 73
                    prod = 73
                elif t == "%":                   # PREDICT 73
                    prod = 73
                elif t == "*":                   # PREDICT 73
                    prod = 73
                elif t == "+":                   # PREDICT 73
                    prod = 73
                elif t == "++":                  # PREDICT 73
                    prod = 73
                elif t == "-":                   # PREDICT 73
                    prod = 73
                elif t == "--":                  # PREDICT 73
                    prod = 73
                elif t == "/":                   # PREDICT 73
                    prod = 73
                elif t == "<":                   # PREDICT 73
                    prod = 73
                elif t == "<=":                  # PREDICT 73
                    prod = 73
                elif t == "==":                  # PREDICT 73
                    prod = 73
                elif t == ">":                   # PREDICT 73
                    prod = 73
                elif t == ">=":                  # PREDICT 73
                    prod = 73
                elif t == "And":                 # PREDICT 73
                    prod = 73
                elif t == "Or":                  # PREDICT 73
                    prod = 73
                elif t == "^":                   # PREDICT 73
                    prod = 73
                elif t == "]":                   # PREDICT 74
                    prod = 74
                else:
                    expected = ["!=", "%", "*", "+", "++", ",", "-", "--", "/", "<",
                                "<=", "==", ">", ">=", "And", "Or", "]", "^"]

            elif top == "<elem_not_name>":
                #  75  <elem_not_name> → <num_literal_exp> <num_compare_tail>
                #  76  <elem_not_name> → <word_literal_exp> <word_compare_tail>
                #  77  <elem_not_name> → <truth_literal_exp> <truth_compare_tail>
                #  78  <elem_not_name> → ( <expression> ) <expr_result_tail>
                if t == "++":                    # PREDICT 75
                    prod = 75
                elif t == "--":                  # PREDICT 75
                    prod = 75
                elif t == "Length":              # PREDICT 75
                    prod = 75
                elif t == "ToNumber":            # PREDICT 75
                    prod = 75
                elif t == "ToRational":          # PREDICT 75
                    prod = 75
                elif t == "flo_lit":             # PREDICT 75
                    prod = 75
                elif t == "int_lit":             # PREDICT 75
                    prod = 75
                elif t == "~":                   # PREDICT 75
                    prod = 75
                elif t == "ToWord":              # PREDICT 76
                    prod = 76
                elif t == "str_lit":             # PREDICT 76
                    prod = 76
                elif t == "Not":                 # PREDICT 77
                    prod = 77
                elif t == "ToTruth":             # PREDICT 77
                    prod = 77
                elif t == "boo_lit":             # PREDICT 77
                    prod = 77
                elif t == "(":                   # PREDICT 78
                    prod = 78
                else:
                    expected = ["(", "++", "--", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "int_lit", "str_lit", "~"]

            elif top == "<functions>":
                #  79  <functions> → <func_def> <functions>
                #  80  <functions> → λ
                if t == "Blend":                 # PREDICT 79
                    prod = 79
                elif t == "++":                  # PREDICT 80
                    prod = 80
                elif t == "--":                  # PREDICT 80
                    prod = 80
                elif t == "Append":              # PREDICT 80
                    prod = 80
                elif t == "Clear":               # PREDICT 80
                    prod = 80
                elif t == "Factor":              # PREDICT 80
                    prod = 80
                elif t == "Harvest":             # PREDICT 80
                    prod = 80
                elif t == "Insert":              # PREDICT 80
                    prod = 80
                elif t == "Mix":                 # PREDICT 80
                    prod = 80
                elif t == "Pour":                # PREDICT 80
                    prod = 80
                elif t == "Produce":             # PREDICT 80
                    prod = 80
                elif t == "Reap":                # PREDICT 80
                    prod = 80
                elif t == "Remove":              # PREDICT 80
                    prod = 80
                elif t == "Squeeze":             # PREDICT 80
                    prod = 80
                elif t == "Test":                # PREDICT 80
                    prod = 80
                elif t == "Uproot":              # PREDICT 80
                    prod = 80
                elif t == "id":                  # PREDICT 80
                    prod = 80
                elif t == "$":                   # PREDICT 80
                    prod = 80
                else:
                    expected = ["++", "--", "Append", "Blend", "Clear", "Factor",
                                "Harvest", "Insert", "Mix", "Pour", "Produce", "Reap",
                                "Remove", "Squeeze", "Test", "Uproot", "id", "$"]

            elif top == "<func_def>":
                #  81  <func_def> → Blend id ( <param_list> ) -> <return_type> <body>
                if t == "Blend":                 # PREDICT 81
                    prod = 81
                else:
                    expected = ["Blend"]

            elif top == "<param_list>":
                #  82  <param_list> → <param> <param_tail>
                #  83  <param_list> → λ
                if t == "id":                    # PREDICT 82
                    prod = 82
                elif t == ")":                   # PREDICT 83
                    prod = 83
                else:
                    expected = [")", "id"]

            elif top == "<param_tail>":
                #  84  <param_tail> → , <param> <param_tail>
                #  85  <param_tail> → λ
                if t == ",":                     # PREDICT 84
                    prod = 84
                elif t == ")":                   # PREDICT 85
                    prod = 85
                else:
                    expected = [")", ","]

            elif top == "<param>":
                #  86  <param> → id : <type_spec>
                if t == "id":                    # PREDICT 86
                    prod = 86
                else:
                    expected = ["id"]

            elif top == "<return_type>":
                #  87  <return_type> → Bland
                #  88  <return_type> → <type_spec>
                if t == "Bland":                 # PREDICT 87
                    prod = 87
                elif t == "Number":              # PREDICT 88
                    prod = 88
                elif t == "Rational":            # PREDICT 88
                    prod = 88
                elif t == "Truth":               # PREDICT 88
                    prod = 88
                elif t == "Word":                # PREDICT 88
                    prod = 88
                else:
                    expected = ["Bland", "Number", "Rational", "Truth", "Word"]

            elif top == "<body>":
                #  89  <body> → { <local_decls> <statements> }
                if t == "{":                     # PREDICT 89
                    prod = 89
                else:
                    expected = ["{"]

            elif top == "<local_decls>":
                #  90  <local_decls> → <local_decl> <local_decls>
                #  91  <local_decls> → λ
                if t == "Recipe":                # PREDICT 90
                    prod = 90
                elif t == "Same":                # PREDICT 90
                    prod = 90
                elif t == "Vary":                # PREDICT 90
                    prod = 90
                elif t == "++":                  # PREDICT 91
                    prod = 91
                elif t == "--":                  # PREDICT 91
                    prod = 91
                elif t == "Append":              # PREDICT 91
                    prod = 91
                elif t == "Clear":               # PREDICT 91
                    prod = 91
                elif t == "Factor":              # PREDICT 91
                    prod = 91
                elif t == "Harvest":             # PREDICT 91
                    prod = 91
                elif t == "Insert":              # PREDICT 91
                    prod = 91
                elif t == "Mix":                 # PREDICT 91
                    prod = 91
                elif t == "Pour":                # PREDICT 91
                    prod = 91
                elif t == "Produce":             # PREDICT 91
                    prod = 91
                elif t == "Reap":                # PREDICT 91
                    prod = 91
                elif t == "Remove":              # PREDICT 91
                    prod = 91
                elif t == "Squeeze":             # PREDICT 91
                    prod = 91
                elif t == "Test":                # PREDICT 91
                    prod = 91
                elif t == "Uproot":              # PREDICT 91
                    prod = 91
                elif t == "id":                  # PREDICT 91
                    prod = 91
                elif t == "}":                   # PREDICT 91
                    prod = 91
                else:
                    expected = ["++", "--", "Append", "Clear", "Factor", "Harvest",
                                "Insert", "Mix", "Pour", "Produce", "Reap", "Recipe",
                                "Remove", "Same", "Squeeze", "Test", "Uproot", "Vary",
                                "id", "}"]

            elif top == "<local_decl>":
                #  92  <local_decl> → <var_decl> ;
                #  93  <local_decl> → <const_decl> ;
                #  94  <local_decl> → Recipe id : id ;
                if t == "Vary":                  # PREDICT 92
                    prod = 92
                elif t == "Same":                # PREDICT 93
                    prod = 93
                elif t == "Recipe":              # PREDICT 94
                    prod = 94
                else:
                    expected = ["Recipe", "Same", "Vary"]

            elif top == "<statements>":
                #  95  <statements> → <statement> <statements>
                #  96  <statements> → λ
                if t == "++":                    # PREDICT 95
                    prod = 95
                elif t == "--":                  # PREDICT 95
                    prod = 95
                elif t == "Append":              # PREDICT 95
                    prod = 95
                elif t == "Clear":               # PREDICT 95
                    prod = 95
                elif t == "Factor":              # PREDICT 95
                    prod = 95
                elif t == "Harvest":             # PREDICT 95
                    prod = 95
                elif t == "Insert":              # PREDICT 95
                    prod = 95
                elif t == "Mix":                 # PREDICT 95
                    prod = 95
                elif t == "Pour":                # PREDICT 95
                    prod = 95
                elif t == "Produce":             # PREDICT 95
                    prod = 95
                elif t == "Reap":                # PREDICT 95
                    prod = 95
                elif t == "Remove":              # PREDICT 95
                    prod = 95
                elif t == "Squeeze":             # PREDICT 95
                    prod = 95
                elif t == "Test":                # PREDICT 95
                    prod = 95
                elif t == "Uproot":              # PREDICT 95
                    prod = 95
                elif t == "id":                  # PREDICT 95
                    prod = 95
                elif t == "}":                   # PREDICT 96
                    prod = 96
                elif t == "$":                   # PREDICT 96
                    prod = 96
                else:
                    expected = ["++", "--", "Append", "Clear", "Factor", "Harvest",
                                "Insert", "Mix", "Pour", "Produce", "Reap", "Remove",
                                "Squeeze", "Test", "Uproot", "id", "}", "$"]

            elif top == "<statement>":
                #  97  <statement> → id <id_stmt_tail> ;
                #  98  <statement> → <incdec_op> id <accessor> ;
                #  99  <statement> → Test <condition> <body> <stir_list> <taste_opt>
                # 100  <statement> → Harvest <harvest_value> { <try_clause> <try_list> Unripe <body> }
                # 101  <statement> → Mix <condition> <body>
                # 102  <statement> → Pour <body> Mix <condition> ;
                # 103  <statement> → Factor ( <factor_init> ; <factor_cond> ; <factor_step> ) <body>
                # 104  <statement> → Reap ;
                # 105  <statement> → Uproot ;
                # 106  <statement> → Produce <produce_value> ;
                # 107  <statement> → Squeeze ( <expression> ) ;
                # 108  <statement> → Append ( <array_target> , <arg> ) ;
                # 109  <statement> → Insert ( <array_target> , <index_exp> , <arg> ) ;
                # 110  <statement> → Remove ( <array_target> , <index_exp> ) ;
                # 111  <statement> → Clear ( <array_target> ) ;
                if t == "id":                    # PREDICT 97
                    prod = 97
                elif t == "++":                  # PREDICT 98
                    prod = 98
                elif t == "--":                  # PREDICT 98
                    prod = 98
                elif t == "Test":                # PREDICT 99
                    prod = 99
                elif t == "Harvest":             # PREDICT 100
                    prod = 100
                elif t == "Mix":                 # PREDICT 101
                    prod = 101
                elif t == "Pour":                # PREDICT 102
                    prod = 102
                elif t == "Factor":              # PREDICT 103
                    prod = 103
                elif t == "Reap":                # PREDICT 104
                    prod = 104
                elif t == "Uproot":              # PREDICT 105
                    prod = 105
                elif t == "Produce":             # PREDICT 106
                    prod = 106
                elif t == "Squeeze":             # PREDICT 107
                    prod = 107
                elif t == "Append":              # PREDICT 108
                    prod = 108
                elif t == "Insert":              # PREDICT 109
                    prod = 109
                elif t == "Remove":              # PREDICT 110
                    prod = 110
                elif t == "Clear":               # PREDICT 111
                    prod = 111
                else:
                    expected = ["++", "--", "Append", "Clear", "Factor", "Harvest",
                                "Insert", "Mix", "Pour", "Produce", "Reap", "Remove",
                                "Squeeze", "Test", "Uproot", "id"]

            elif top == "<id_stmt_tail>":
                # 112  <id_stmt_tail> → ( <arguments> )
                # 113  <id_stmt_tail> → <accessor> <assign_tail>
                if t == "(":                     # PREDICT 112
                    prod = 112
                elif t == "%=":                  # PREDICT 113
                    prod = 113
                elif t == "*=":                  # PREDICT 113
                    prod = 113
                elif t == "++":                  # PREDICT 113
                    prod = 113
                elif t == "+=":                  # PREDICT 113
                    prod = 113
                elif t == "--":                  # PREDICT 113
                    prod = 113
                elif t == "-=":                  # PREDICT 113
                    prod = 113
                elif t == ".":                   # PREDICT 113
                    prod = 113
                elif t == "/=":                  # PREDICT 113
                    prod = 113
                elif t == "=":                   # PREDICT 113
                    prod = 113
                elif t == "[":                   # PREDICT 113
                    prod = 113
                else:
                    expected = ["%=", "(", "*=", "++", "+=", "--", "-=", ".", "/=", "=",
                                "["]

            elif top == "<assign_tail>":
                # 114  <assign_tail> → = <init_value>
                # 115  <assign_tail> → += <non_truth_exp>
                # 116  <assign_tail> → <num_assign_op> <num_exp>
                # 117  <assign_tail> → <incdec_op>
                if t == "=":                     # PREDICT 114
                    prod = 114
                elif t == "+=":                  # PREDICT 115
                    prod = 115
                elif t == "%=":                  # PREDICT 116
                    prod = 116
                elif t == "*=":                  # PREDICT 116
                    prod = 116
                elif t == "-=":                  # PREDICT 116
                    prod = 116
                elif t == "/=":                  # PREDICT 116
                    prod = 116
                elif t == "++":                  # PREDICT 117
                    prod = 117
                elif t == "--":                  # PREDICT 117
                    prod = 117
                else:
                    expected = ["%=", "*=", "++", "+=", "--", "-=", "/=", "="]

            elif top == "<non_truth_exp>":
                # 118  <non_truth_exp> → <num_literal_exp>
                # 119  <non_truth_exp> → <word_literal_exp>
                # 120  <non_truth_exp> → <untyped_exp>
                if t == "++":                    # PREDICT 118
                    prod = 118
                elif t == "--":                  # PREDICT 118
                    prod = 118
                elif t == "Length":              # PREDICT 118
                    prod = 118
                elif t == "ToNumber":            # PREDICT 118
                    prod = 118
                elif t == "ToRational":          # PREDICT 118
                    prod = 118
                elif t == "flo_lit":             # PREDICT 118
                    prod = 118
                elif t == "int_lit":             # PREDICT 118
                    prod = 118
                elif t == "~":                   # PREDICT 118
                    prod = 118
                elif t == "ToWord":              # PREDICT 119
                    prod = 119
                elif t == "str_lit":             # PREDICT 119
                    prod = 119
                elif t == "(":                   # PREDICT 120
                    prod = 120
                elif t == "id":                  # PREDICT 120
                    prod = 120
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "ToRational",
                                "ToWord", "flo_lit", "id", "int_lit", "str_lit", "~"]

            elif top == "<num_assign_op>":
                # 121  <num_assign_op> → -=
                # 122  <num_assign_op> → *=
                # 123  <num_assign_op> → /=
                # 124  <num_assign_op> → %=
                if t == "-=":                    # PREDICT 121
                    prod = 121
                elif t == "*=":                  # PREDICT 122
                    prod = 122
                elif t == "/=":                  # PREDICT 123
                    prod = 123
                elif t == "%=":                  # PREDICT 124
                    prod = 124
                else:
                    expected = ["%=", "*=", "-=", "/="]

            elif top == "<incdec_op>":
                # 125  <incdec_op> → ++
                # 126  <incdec_op> → --
                if t == "++":                    # PREDICT 125
                    prod = 125
                elif t == "--":                  # PREDICT 126
                    prod = 126
                else:
                    expected = ["++", "--"]

            elif top == "<accessor>":
                # 127  <accessor> → [ <index_exp> ] <second_index>
                # 128  <accessor> → . id <member_index>
                # 129  <accessor> → λ
                if t == "[":                     # PREDICT 127
                    prod = 127
                elif t == ".":                   # PREDICT 128
                    prod = 128
                elif t == "!=":                  # PREDICT 129
                    prod = 129
                elif t == "%":                   # PREDICT 129
                    prod = 129
                elif t == "%=":                  # PREDICT 129
                    prod = 129
                elif t == ")":                   # PREDICT 129
                    prod = 129
                elif t == "*":                   # PREDICT 129
                    prod = 129
                elif t == "*=":                  # PREDICT 129
                    prod = 129
                elif t == "+":                   # PREDICT 129
                    prod = 129
                elif t == "++":                  # PREDICT 129
                    prod = 129
                elif t == "+=":                  # PREDICT 129
                    prod = 129
                elif t == ",":                   # PREDICT 129
                    prod = 129
                elif t == "-":                   # PREDICT 129
                    prod = 129
                elif t == "--":                  # PREDICT 129
                    prod = 129
                elif t == "-=":                  # PREDICT 129
                    prod = 129
                elif t == "/":                   # PREDICT 129
                    prod = 129
                elif t == "/=":                  # PREDICT 129
                    prod = 129
                elif t == ";":                   # PREDICT 129
                    prod = 129
                elif t == "<":                   # PREDICT 129
                    prod = 129
                elif t == "<=":                  # PREDICT 129
                    prod = 129
                elif t == "=":                   # PREDICT 129
                    prod = 129
                elif t == "==":                  # PREDICT 129
                    prod = 129
                elif t == ">":                   # PREDICT 129
                    prod = 129
                elif t == ">=":                  # PREDICT 129
                    prod = 129
                elif t == "And":                 # PREDICT 129
                    prod = 129
                elif t == "Or":                  # PREDICT 129
                    prod = 129
                elif t == "]":                   # PREDICT 129
                    prod = 129
                elif t == "^":                   # PREDICT 129
                    prod = 129
                elif t == "{":                   # PREDICT 129
                    prod = 129
                else:
                    expected = ["!=", "%", "%=", ")", "*", "*=", "+", "++", "+=", ",",
                                "-", "--", "-=", ".", "/", "/=", ";", "<", "<=", "=",
                                "==", ">", ">=", "And", "Or", "[", "]", "^", "{"]

            elif top == "<member_index>":
                # 130  <member_index> → [ <index_exp> ] <second_index>
                # 131  <member_index> → λ
                if t == "[":                     # PREDICT 130
                    prod = 130
                elif t == "!=":                  # PREDICT 131
                    prod = 131
                elif t == "%":                   # PREDICT 131
                    prod = 131
                elif t == "%=":                  # PREDICT 131
                    prod = 131
                elif t == ")":                   # PREDICT 131
                    prod = 131
                elif t == "*":                   # PREDICT 131
                    prod = 131
                elif t == "*=":                  # PREDICT 131
                    prod = 131
                elif t == "+":                   # PREDICT 131
                    prod = 131
                elif t == "++":                  # PREDICT 131
                    prod = 131
                elif t == "+=":                  # PREDICT 131
                    prod = 131
                elif t == ",":                   # PREDICT 131
                    prod = 131
                elif t == "-":                   # PREDICT 131
                    prod = 131
                elif t == "--":                  # PREDICT 131
                    prod = 131
                elif t == "-=":                  # PREDICT 131
                    prod = 131
                elif t == "/":                   # PREDICT 131
                    prod = 131
                elif t == "/=":                  # PREDICT 131
                    prod = 131
                elif t == ";":                   # PREDICT 131
                    prod = 131
                elif t == "<":                   # PREDICT 131
                    prod = 131
                elif t == "<=":                  # PREDICT 131
                    prod = 131
                elif t == "=":                   # PREDICT 131
                    prod = 131
                elif t == "==":                  # PREDICT 131
                    prod = 131
                elif t == ">":                   # PREDICT 131
                    prod = 131
                elif t == ">=":                  # PREDICT 131
                    prod = 131
                elif t == "And":                 # PREDICT 131
                    prod = 131
                elif t == "Or":                  # PREDICT 131
                    prod = 131
                elif t == "]":                   # PREDICT 131
                    prod = 131
                elif t == "^":                   # PREDICT 131
                    prod = 131
                elif t == "{":                   # PREDICT 131
                    prod = 131
                else:
                    expected = ["!=", "%", "%=", ")", "*", "*=", "+", "++", "+=", ",",
                                "-", "--", "-=", "/", "/=", ";", "<", "<=", "=", "==",
                                ">", ">=", "And", "Or", "[", "]", "^", "{"]

            elif top == "<second_index>":
                # 132  <second_index> → [ <index_exp> ]
                # 133  <second_index> → λ
                if t == "[":                     # PREDICT 132
                    prod = 132
                elif t == "!=":                  # PREDICT 133
                    prod = 133
                elif t == "%":                   # PREDICT 133
                    prod = 133
                elif t == "%=":                  # PREDICT 133
                    prod = 133
                elif t == ")":                   # PREDICT 133
                    prod = 133
                elif t == "*":                   # PREDICT 133
                    prod = 133
                elif t == "*=":                  # PREDICT 133
                    prod = 133
                elif t == "+":                   # PREDICT 133
                    prod = 133
                elif t == "++":                  # PREDICT 133
                    prod = 133
                elif t == "+=":                  # PREDICT 133
                    prod = 133
                elif t == ",":                   # PREDICT 133
                    prod = 133
                elif t == "-":                   # PREDICT 133
                    prod = 133
                elif t == "--":                  # PREDICT 133
                    prod = 133
                elif t == "-=":                  # PREDICT 133
                    prod = 133
                elif t == "/":                   # PREDICT 133
                    prod = 133
                elif t == "/=":                  # PREDICT 133
                    prod = 133
                elif t == ";":                   # PREDICT 133
                    prod = 133
                elif t == "<":                   # PREDICT 133
                    prod = 133
                elif t == "<=":                  # PREDICT 133
                    prod = 133
                elif t == "=":                   # PREDICT 133
                    prod = 133
                elif t == "==":                  # PREDICT 133
                    prod = 133
                elif t == ">":                   # PREDICT 133
                    prod = 133
                elif t == ">=":                  # PREDICT 133
                    prod = 133
                elif t == "And":                 # PREDICT 133
                    prod = 133
                elif t == "Or":                  # PREDICT 133
                    prod = 133
                elif t == "]":                   # PREDICT 133
                    prod = 133
                elif t == "^":                   # PREDICT 133
                    prod = 133
                elif t == "{":                   # PREDICT 133
                    prod = 133
                else:
                    expected = ["!=", "%", "%=", ")", "*", "*=", "+", "++", "+=", ",",
                                "-", "--", "-=", "/", "/=", ";", "<", "<=", "=", "==",
                                ">", ">=", "And", "Or", "[", "]", "^", "{"]

            elif top == "<index_exp>":
                # 134  <index_exp> → <int_exp>
                if t == "(":                     # PREDICT 134
                    prod = 134
                elif t == "++":                  # PREDICT 134
                    prod = 134
                elif t == "--":                  # PREDICT 134
                    prod = 134
                elif t == "Length":              # PREDICT 134
                    prod = 134
                elif t == "ToNumber":            # PREDICT 134
                    prod = 134
                elif t == "id":                  # PREDICT 134
                    prod = 134
                elif t == "int_lit":             # PREDICT 134
                    prod = 134
                elif t == "~":                   # PREDICT 134
                    prod = 134
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "id", "int_lit",
                                "~"]

            elif top == "<array_target>":
                # 135  <array_target> → id <accessor>
                if t == "id":                    # PREDICT 135
                    prod = 135
                else:
                    expected = ["id"]

            elif top == "<stir_list>":
                # 136  <stir_list> → Stir <condition> <body> <stir_list>
                # 137  <stir_list> → λ
                if t == "Stir":                  # PREDICT 136
                    prod = 136
                elif t == "++":                  # PREDICT 137
                    prod = 137
                elif t == "--":                  # PREDICT 137
                    prod = 137
                elif t == "Append":              # PREDICT 137
                    prod = 137
                elif t == "Clear":               # PREDICT 137
                    prod = 137
                elif t == "Factor":              # PREDICT 137
                    prod = 137
                elif t == "Harvest":             # PREDICT 137
                    prod = 137
                elif t == "Insert":              # PREDICT 137
                    prod = 137
                elif t == "Mix":                 # PREDICT 137
                    prod = 137
                elif t == "Pour":                # PREDICT 137
                    prod = 137
                elif t == "Produce":             # PREDICT 137
                    prod = 137
                elif t == "Reap":                # PREDICT 137
                    prod = 137
                elif t == "Remove":              # PREDICT 137
                    prod = 137
                elif t == "Squeeze":             # PREDICT 137
                    prod = 137
                elif t == "Taste":               # PREDICT 137
                    prod = 137
                elif t == "Test":                # PREDICT 137
                    prod = 137
                elif t == "Uproot":              # PREDICT 137
                    prod = 137
                elif t == "id":                  # PREDICT 137
                    prod = 137
                elif t == "}":                   # PREDICT 137
                    prod = 137
                elif t == "$":                   # PREDICT 137
                    prod = 137
                else:
                    expected = ["++", "--", "Append", "Clear", "Factor", "Harvest",
                                "Insert", "Mix", "Pour", "Produce", "Reap", "Remove",
                                "Squeeze", "Stir", "Taste", "Test", "Uproot", "id", "}",
                                "$"]

            elif top == "<taste_opt>":
                # 138  <taste_opt> → Taste <body>
                # 139  <taste_opt> → λ
                if t == "Taste":                 # PREDICT 138
                    prod = 138
                elif t == "++":                  # PREDICT 139
                    prod = 139
                elif t == "--":                  # PREDICT 139
                    prod = 139
                elif t == "Append":              # PREDICT 139
                    prod = 139
                elif t == "Clear":               # PREDICT 139
                    prod = 139
                elif t == "Factor":              # PREDICT 139
                    prod = 139
                elif t == "Harvest":             # PREDICT 139
                    prod = 139
                elif t == "Insert":              # PREDICT 139
                    prod = 139
                elif t == "Mix":                 # PREDICT 139
                    prod = 139
                elif t == "Pour":                # PREDICT 139
                    prod = 139
                elif t == "Produce":             # PREDICT 139
                    prod = 139
                elif t == "Reap":                # PREDICT 139
                    prod = 139
                elif t == "Remove":              # PREDICT 139
                    prod = 139
                elif t == "Squeeze":             # PREDICT 139
                    prod = 139
                elif t == "Test":                # PREDICT 139
                    prod = 139
                elif t == "Uproot":              # PREDICT 139
                    prod = 139
                elif t == "id":                  # PREDICT 139
                    prod = 139
                elif t == "}":                   # PREDICT 139
                    prod = 139
                elif t == "$":                   # PREDICT 139
                    prod = 139
                else:
                    expected = ["++", "--", "Append", "Clear", "Factor", "Harvest",
                                "Insert", "Mix", "Pour", "Produce", "Reap", "Remove",
                                "Squeeze", "Taste", "Test", "Uproot", "id", "}", "$"]

            elif top == "<try_clause>":
                # 140  <try_clause> → Try <try_value> <body>
                if t == "Try":                   # PREDICT 140
                    prod = 140
                else:
                    expected = ["Try"]

            elif top == "<try_list>":
                # 141  <try_list> → <try_clause> <try_list>
                # 142  <try_list> → λ
                if t == "Try":                   # PREDICT 141
                    prod = 141
                elif t == "Unripe":              # PREDICT 142
                    prod = 142
                else:
                    expected = ["Try", "Unripe"]

            elif top == "<try_value>":
                # 143  <try_value> → int_lit
                # 144  <try_value> → str_lit
                # 145  <try_value> → id
                if t == "int_lit":               # PREDICT 143
                    prod = 143
                elif t == "str_lit":             # PREDICT 144
                    prod = 144
                elif t == "id":                  # PREDICT 145
                    prod = 145
                else:
                    expected = ["id", "int_lit", "str_lit"]

            elif top == "<factor_init>":
                # 146  <factor_init> → Vary id : <data_type> = <expression>
                # 147  <factor_init> → id <accessor> <factor_assign>
                # 148  <factor_init> → λ
                if t == "Vary":                  # PREDICT 146
                    prod = 146
                elif t == "id":                  # PREDICT 147
                    prod = 147
                elif t == ";":                   # PREDICT 148
                    prod = 148
                else:
                    expected = [";", "Vary", "id"]

            elif top == "<factor_cond>":
                # 149  <factor_cond> → <condition>
                # 150  <factor_cond> → λ
                if t == "(":                     # PREDICT 149
                    prod = 149
                elif t == "++":                  # PREDICT 149
                    prod = 149
                elif t == "--":                  # PREDICT 149
                    prod = 149
                elif t == "Length":              # PREDICT 149
                    prod = 149
                elif t == "Not":                 # PREDICT 149
                    prod = 149
                elif t == "ToNumber":            # PREDICT 149
                    prod = 149
                elif t == "ToRational":          # PREDICT 149
                    prod = 149
                elif t == "ToTruth":             # PREDICT 149
                    prod = 149
                elif t == "ToWord":              # PREDICT 149
                    prod = 149
                elif t == "boo_lit":             # PREDICT 149
                    prod = 149
                elif t == "flo_lit":             # PREDICT 149
                    prod = 149
                elif t == "id":                  # PREDICT 149
                    prod = 149
                elif t == "int_lit":             # PREDICT 149
                    prod = 149
                elif t == "str_lit":             # PREDICT 149
                    prod = 149
                elif t == "~":                   # PREDICT 149
                    prod = 149
                elif t == ";":                   # PREDICT 150
                    prod = 150
                else:
                    expected = ["(", "++", "--", ";", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "id", "int_lit", "str_lit", "~"]

            elif top == "<factor_step>":
                # 151  <factor_step> → id <accessor> <step_tail>
                # 152  <factor_step> → <incdec_op> id <accessor>
                # 153  <factor_step> → λ
                if t == "id":                    # PREDICT 151
                    prod = 151
                elif t == "++":                  # PREDICT 152
                    prod = 152
                elif t == "--":                  # PREDICT 152
                    prod = 152
                elif t == ")":                   # PREDICT 153
                    prod = 153
                else:
                    expected = [")", "++", "--", "id"]

            elif top == "<step_tail>":
                # 154  <step_tail> → <factor_assign>
                # 155  <step_tail> → <incdec_op>
                if t == "%=":                    # PREDICT 154
                    prod = 154
                elif t == "*=":                  # PREDICT 154
                    prod = 154
                elif t == "+=":                  # PREDICT 154
                    prod = 154
                elif t == "-=":                  # PREDICT 154
                    prod = 154
                elif t == "/=":                  # PREDICT 154
                    prod = 154
                elif t == "=":                   # PREDICT 154
                    prod = 154
                elif t == "++":                  # PREDICT 155
                    prod = 155
                elif t == "--":                  # PREDICT 155
                    prod = 155
                else:
                    expected = ["%=", "*=", "++", "+=", "--", "-=", "/=", "="]

            elif top == "<factor_assign>":
                # 156  <factor_assign> → = <expression>
                # 157  <factor_assign> → += <non_truth_exp>
                # 158  <factor_assign> → <num_assign_op> <num_exp>
                if t == "=":                     # PREDICT 156
                    prod = 156
                elif t == "+=":                  # PREDICT 157
                    prod = 157
                elif t == "%=":                  # PREDICT 158
                    prod = 158
                elif t == "*=":                  # PREDICT 158
                    prod = 158
                elif t == "-=":                  # PREDICT 158
                    prod = 158
                elif t == "/=":                  # PREDICT 158
                    prod = 158
                else:
                    expected = ["%=", "*=", "+=", "-=", "/=", "="]

            elif top == "<produce_value>":
                # 159  <produce_value> → <expression>
                # 160  <produce_value> → λ
                if t == "(":                     # PREDICT 159
                    prod = 159
                elif t == "++":                  # PREDICT 159
                    prod = 159
                elif t == "--":                  # PREDICT 159
                    prod = 159
                elif t == "Length":              # PREDICT 159
                    prod = 159
                elif t == "Not":                 # PREDICT 159
                    prod = 159
                elif t == "ToNumber":            # PREDICT 159
                    prod = 159
                elif t == "ToRational":          # PREDICT 159
                    prod = 159
                elif t == "ToTruth":             # PREDICT 159
                    prod = 159
                elif t == "ToWord":              # PREDICT 159
                    prod = 159
                elif t == "boo_lit":             # PREDICT 159
                    prod = 159
                elif t == "flo_lit":             # PREDICT 159
                    prod = 159
                elif t == "id":                  # PREDICT 159
                    prod = 159
                elif t == "int_lit":             # PREDICT 159
                    prod = 159
                elif t == "str_lit":             # PREDICT 159
                    prod = 159
                elif t == "~":                   # PREDICT 159
                    prod = 159
                elif t == ";":                   # PREDICT 160
                    prod = 160
                else:
                    expected = ["(", "++", "--", ";", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "id", "int_lit", "str_lit", "~"]

            elif top == "<arguments>":
                # 161  <arguments> → <arg> <arg_tail>
                # 162  <arguments> → λ
                if t == "(":                     # PREDICT 161
                    prod = 161
                elif t == "++":                  # PREDICT 161
                    prod = 161
                elif t == "--":                  # PREDICT 161
                    prod = 161
                elif t == "Basket":              # PREDICT 161
                    prod = 161
                elif t == "Length":              # PREDICT 161
                    prod = 161
                elif t == "Not":                 # PREDICT 161
                    prod = 161
                elif t == "ToNumber":            # PREDICT 161
                    prod = 161
                elif t == "ToRational":          # PREDICT 161
                    prod = 161
                elif t == "ToTruth":             # PREDICT 161
                    prod = 161
                elif t == "ToWord":              # PREDICT 161
                    prod = 161
                elif t == "boo_lit":             # PREDICT 161
                    prod = 161
                elif t == "flo_lit":             # PREDICT 161
                    prod = 161
                elif t == "id":                  # PREDICT 161
                    prod = 161
                elif t == "int_lit":             # PREDICT 161
                    prod = 161
                elif t == "str_lit":             # PREDICT 161
                    prod = 161
                elif t == "~":                   # PREDICT 161
                    prod = 161
                elif t == ")":                   # PREDICT 162
                    prod = 162
                else:
                    expected = ["(", ")", "++", "--", "Basket", "Length", "Not",
                                "ToNumber", "ToRational", "ToTruth", "ToWord", "boo_lit",
                                "flo_lit", "id", "int_lit", "str_lit", "~"]

            elif top == "<arg_tail>":
                # 163  <arg_tail> → , <arg> <arg_tail>
                # 164  <arg_tail> → λ
                if t == ",":                     # PREDICT 163
                    prod = 163
                elif t == ")":                   # PREDICT 164
                    prod = 164
                else:
                    expected = [")", ","]

            elif top == "<arg>":
                # 165  <arg> → <expression>
                # 166  <arg> → <basket_value>
                if t == "(":                     # PREDICT 165
                    prod = 165
                elif t == "++":                  # PREDICT 165
                    prod = 165
                elif t == "--":                  # PREDICT 165
                    prod = 165
                elif t == "Length":              # PREDICT 165
                    prod = 165
                elif t == "Not":                 # PREDICT 165
                    prod = 165
                elif t == "ToNumber":            # PREDICT 165
                    prod = 165
                elif t == "ToRational":          # PREDICT 165
                    prod = 165
                elif t == "ToTruth":             # PREDICT 165
                    prod = 165
                elif t == "ToWord":              # PREDICT 165
                    prod = 165
                elif t == "boo_lit":             # PREDICT 165
                    prod = 165
                elif t == "flo_lit":             # PREDICT 165
                    prod = 165
                elif t == "id":                  # PREDICT 165
                    prod = 165
                elif t == "int_lit":             # PREDICT 165
                    prod = 165
                elif t == "str_lit":             # PREDICT 165
                    prod = 165
                elif t == "~":                   # PREDICT 165
                    prod = 165
                elif t == "Basket":              # PREDICT 166
                    prod = 166
                else:
                    expected = ["(", "++", "--", "Basket", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "id", "int_lit", "str_lit", "~"]

            elif top == "<expression>":
                # 167  <expression> → <num_literal_exp> <num_compare_tail>
                # 168  <expression> → <word_literal_exp> <word_compare_tail>
                # 169  <expression> → <truth_literal_exp> <truth_compare_tail>
                # 170  <expression> → id <expr_name_tail>
                # 171  <expression> → ( <expression> ) <expr_result_tail>
                if t == "++":                    # PREDICT 167
                    prod = 167
                elif t == "--":                  # PREDICT 167
                    prod = 167
                elif t == "Length":              # PREDICT 167
                    prod = 167
                elif t == "ToNumber":            # PREDICT 167
                    prod = 167
                elif t == "ToRational":          # PREDICT 167
                    prod = 167
                elif t == "flo_lit":             # PREDICT 167
                    prod = 167
                elif t == "int_lit":             # PREDICT 167
                    prod = 167
                elif t == "~":                   # PREDICT 167
                    prod = 167
                elif t == "ToWord":              # PREDICT 168
                    prod = 168
                elif t == "str_lit":             # PREDICT 168
                    prod = 168
                elif t == "Not":                 # PREDICT 169
                    prod = 169
                elif t == "ToTruth":             # PREDICT 169
                    prod = 169
                elif t == "boo_lit":             # PREDICT 169
                    prod = 169
                elif t == "id":                  # PREDICT 170
                    prod = 170
                elif t == "(":                   # PREDICT 171
                    prod = 171
                else:
                    expected = ["(", "++", "--", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "id", "int_lit", "str_lit", "~"]

            elif top == "<expr_name_tail>":
                # 172  <expr_name_tail> → ( <arguments> ) <expr_result_tail>
                # 173  <expr_name_tail> → <accessor> <expr_var_tail>
                if t == "(":                     # PREDICT 172
                    prod = 172
                elif t == "!=":                  # PREDICT 173
                    prod = 173
                elif t == "%":                   # PREDICT 173
                    prod = 173
                elif t == ")":                   # PREDICT 173
                    prod = 173
                elif t == "*":                   # PREDICT 173
                    prod = 173
                elif t == "+":                   # PREDICT 173
                    prod = 173
                elif t == "++":                  # PREDICT 173
                    prod = 173
                elif t == ",":                   # PREDICT 173
                    prod = 173
                elif t == "-":                   # PREDICT 173
                    prod = 173
                elif t == "--":                  # PREDICT 173
                    prod = 173
                elif t == ".":                   # PREDICT 173
                    prod = 173
                elif t == "/":                   # PREDICT 173
                    prod = 173
                elif t == ";":                   # PREDICT 173
                    prod = 173
                elif t == "<":                   # PREDICT 173
                    prod = 173
                elif t == "<=":                  # PREDICT 173
                    prod = 173
                elif t == "==":                  # PREDICT 173
                    prod = 173
                elif t == ">":                   # PREDICT 173
                    prod = 173
                elif t == ">=":                  # PREDICT 173
                    prod = 173
                elif t == "And":                 # PREDICT 173
                    prod = 173
                elif t == "Or":                  # PREDICT 173
                    prod = 173
                elif t == "[":                   # PREDICT 173
                    prod = 173
                elif t == "]":                   # PREDICT 173
                    prod = 173
                elif t == "^":                   # PREDICT 173
                    prod = 173
                else:
                    expected = ["!=", "%", "(", ")", "*", "+", "++", ",", "-", "--", ".",
                                "/", ";", "<", "<=", "==", ">", ">=", "And", "Or", "[",
                                "]", "^"]

            elif top == "<num_compare_tail>":
                # 174  <num_compare_tail> → <compare_op> <num_exp> <logic_tail>
                # 175  <num_compare_tail> → λ
                if t == "!=":                    # PREDICT 174
                    prod = 174
                elif t == "<":                   # PREDICT 174
                    prod = 174
                elif t == "<=":                  # PREDICT 174
                    prod = 174
                elif t == "==":                  # PREDICT 174
                    prod = 174
                elif t == ">":                   # PREDICT 174
                    prod = 174
                elif t == ">=":                  # PREDICT 174
                    prod = 174
                elif t == ")":                   # PREDICT 175
                    prod = 175
                elif t == ",":                   # PREDICT 175
                    prod = 175
                elif t == ";":                   # PREDICT 175
                    prod = 175
                elif t == "]":                   # PREDICT 175
                    prod = 175
                else:
                    expected = ["!=", ")", ",", ";", "<", "<=", "==", ">", ">=", "]"]

            elif top == "<word_compare_tail>":
                # 176  <word_compare_tail> → <equal_op> <word_exp> <logic_tail>
                # 177  <word_compare_tail> → λ
                if t == "!=":                    # PREDICT 176
                    prod = 176
                elif t == "==":                  # PREDICT 176
                    prod = 176
                elif t == ")":                   # PREDICT 177
                    prod = 177
                elif t == ",":                   # PREDICT 177
                    prod = 177
                elif t == ";":                   # PREDICT 177
                    prod = 177
                elif t == "]":                   # PREDICT 177
                    prod = 177
                else:
                    expected = ["!=", ")", ",", ";", "==", "]"]

            elif top == "<truth_compare_tail>":
                # 178  <truth_compare_tail> → <equal_op> <truth_unary> <logic_tail>
                # 179  <truth_compare_tail> → <logic_tail>
                if t == "!=":                    # PREDICT 178
                    prod = 178
                elif t == "==":                  # PREDICT 178
                    prod = 178
                elif t == ")":                   # PREDICT 179
                    prod = 179
                elif t == ",":                   # PREDICT 179
                    prod = 179
                elif t == ";":                   # PREDICT 179
                    prod = 179
                elif t == "And":                 # PREDICT 179
                    prod = 179
                elif t == "Or":                  # PREDICT 179
                    prod = 179
                elif t == "]":                   # PREDICT 179
                    prod = 179
                else:
                    expected = ["!=", ")", ",", ";", "==", "And", "Or", "]"]

            elif top == "<expr_var_tail>":
                # 180  <expr_var_tail> → <expr_var_ops>
                # 181  <expr_var_tail> → λ
                if t == "!=":                    # PREDICT 180
                    prod = 180
                elif t == "%":                   # PREDICT 180
                    prod = 180
                elif t == "*":                   # PREDICT 180
                    prod = 180
                elif t == "+":                   # PREDICT 180
                    prod = 180
                elif t == "++":                  # PREDICT 180
                    prod = 180
                elif t == "-":                   # PREDICT 180
                    prod = 180
                elif t == "--":                  # PREDICT 180
                    prod = 180
                elif t == "/":                   # PREDICT 180
                    prod = 180
                elif t == "<":                   # PREDICT 180
                    prod = 180
                elif t == "<=":                  # PREDICT 180
                    prod = 180
                elif t == "==":                  # PREDICT 180
                    prod = 180
                elif t == ">":                   # PREDICT 180
                    prod = 180
                elif t == ">=":                  # PREDICT 180
                    prod = 180
                elif t == "And":                 # PREDICT 180
                    prod = 180
                elif t == "Or":                  # PREDICT 180
                    prod = 180
                elif t == "^":                   # PREDICT 180
                    prod = 180
                elif t == ")":                   # PREDICT 181
                    prod = 181
                elif t == ",":                   # PREDICT 181
                    prod = 181
                elif t == ";":                   # PREDICT 181
                    prod = 181
                elif t == "]":                   # PREDICT 181
                    prod = 181
                else:
                    expected = ["!=", "%", ")", "*", "+", "++", ",", "-", "--", "/", ";",
                                "<", "<=", "==", ">", ">=", "And", "Or", "]", "^"]

            elif top == "<expr_var_ops>":
                # 182  <expr_var_ops> → <incdec_op> <pow_tail> <mul_tail> <add_tail> <num_compare_tail>
                # 183  <expr_var_ops> → <expr_result_ops>
                if t == "++":                    # PREDICT 182
                    prod = 182
                elif t == "--":                  # PREDICT 182
                    prod = 182
                elif t == "!=":                  # PREDICT 183
                    prod = 183
                elif t == "%":                   # PREDICT 183
                    prod = 183
                elif t == "*":                   # PREDICT 183
                    prod = 183
                elif t == "+":                   # PREDICT 183
                    prod = 183
                elif t == "-":                   # PREDICT 183
                    prod = 183
                elif t == "/":                   # PREDICT 183
                    prod = 183
                elif t == "<":                   # PREDICT 183
                    prod = 183
                elif t == "<=":                  # PREDICT 183
                    prod = 183
                elif t == "==":                  # PREDICT 183
                    prod = 183
                elif t == ">":                   # PREDICT 183
                    prod = 183
                elif t == ">=":                  # PREDICT 183
                    prod = 183
                elif t == "And":                 # PREDICT 183
                    prod = 183
                elif t == "Or":                  # PREDICT 183
                    prod = 183
                elif t == "^":                   # PREDICT 183
                    prod = 183
                else:
                    expected = ["!=", "%", "*", "+", "++", "-", "--", "/", "<", "<=",
                                "==", ">", ">=", "And", "Or", "^"]

            elif top == "<expr_result_tail>":
                # 184  <expr_result_tail> → <expr_result_ops>
                # 185  <expr_result_tail> → λ
                if t == "!=":                    # PREDICT 184
                    prod = 184
                elif t == "%":                   # PREDICT 184
                    prod = 184
                elif t == "*":                   # PREDICT 184
                    prod = 184
                elif t == "+":                   # PREDICT 184
                    prod = 184
                elif t == "-":                   # PREDICT 184
                    prod = 184
                elif t == "/":                   # PREDICT 184
                    prod = 184
                elif t == "<":                   # PREDICT 184
                    prod = 184
                elif t == "<=":                  # PREDICT 184
                    prod = 184
                elif t == "==":                  # PREDICT 184
                    prod = 184
                elif t == ">":                   # PREDICT 184
                    prod = 184
                elif t == ">=":                  # PREDICT 184
                    prod = 184
                elif t == "And":                 # PREDICT 184
                    prod = 184
                elif t == "Or":                  # PREDICT 184
                    prod = 184
                elif t == "^":                   # PREDICT 184
                    prod = 184
                elif t == ")":                   # PREDICT 185
                    prod = 185
                elif t == ",":                   # PREDICT 185
                    prod = 185
                elif t == ";":                   # PREDICT 185
                    prod = 185
                elif t == "]":                   # PREDICT 185
                    prod = 185
                else:
                    expected = ["!=", "%", ")", "*", "+", ",", "-", "/", ";", "<", "<=",
                                "==", ">", ">=", "And", "Or", "]", "^"]

            elif top == "<expr_result_ops>":
                # 186  <expr_result_ops> → ^ <num_unary> <mul_tail> <add_tail> <num_compare_tail>
                # 187  <expr_result_ops> → <mul_op> <num_unary> <mul_tail> <add_tail> <num_compare_tail>
                # 188  <expr_result_ops> → - <num_term> <add_tail> <num_compare_tail>
                # 189  <expr_result_ops> → + <expr_after_plus>
                # 190  <expr_result_ops> → <rel_op> <num_exp> <logic_tail>
                # 191  <expr_result_ops> → <equal_op> <any_exp> <logic_tail>
                # 192  <expr_result_ops> → And <logic_operand> <and_tail> <or_tail>
                # 193  <expr_result_ops> → Or <logic_operand> <and_tail> <or_tail>
                if t == "^":                     # PREDICT 186
                    prod = 186
                elif t == "%":                   # PREDICT 187
                    prod = 187
                elif t == "*":                   # PREDICT 187
                    prod = 187
                elif t == "/":                   # PREDICT 187
                    prod = 187
                elif t == "-":                   # PREDICT 188
                    prod = 188
                elif t == "+":                   # PREDICT 189
                    prod = 189
                elif t == "<":                   # PREDICT 190
                    prod = 190
                elif t == "<=":                  # PREDICT 190
                    prod = 190
                elif t == ">":                   # PREDICT 190
                    prod = 190
                elif t == ">=":                  # PREDICT 190
                    prod = 190
                elif t == "!=":                  # PREDICT 191
                    prod = 191
                elif t == "==":                  # PREDICT 191
                    prod = 191
                elif t == "And":                 # PREDICT 192
                    prod = 192
                elif t == "Or":                  # PREDICT 193
                    prod = 193
                else:
                    expected = ["!=", "%", "*", "+", "-", "/", "<", "<=", "==", ">",
                                ">=", "And", "Or", "^"]

            elif top == "<expr_after_plus>":
                # 194  <expr_after_plus> → <num_literal_start> <mul_tail> <add_tail> <num_compare_tail>
                # 195  <expr_after_plus> → <word_value> <word_tail> <word_compare_tail>
                # 196  <expr_after_plus> → id <expr_plus_name_tail>
                # 197  <expr_after_plus> → ( <expression> ) <expr_plus_result_tail>
                if t == "++":                    # PREDICT 194
                    prod = 194
                elif t == "--":                  # PREDICT 194
                    prod = 194
                elif t == "Length":              # PREDICT 194
                    prod = 194
                elif t == "ToNumber":            # PREDICT 194
                    prod = 194
                elif t == "ToRational":          # PREDICT 194
                    prod = 194
                elif t == "flo_lit":             # PREDICT 194
                    prod = 194
                elif t == "int_lit":             # PREDICT 194
                    prod = 194
                elif t == "~":                   # PREDICT 194
                    prod = 194
                elif t == "ToWord":              # PREDICT 195
                    prod = 195
                elif t == "str_lit":             # PREDICT 195
                    prod = 195
                elif t == "id":                  # PREDICT 196
                    prod = 196
                elif t == "(":                   # PREDICT 197
                    prod = 197
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "ToRational",
                                "ToWord", "flo_lit", "id", "int_lit", "str_lit", "~"]

            elif top == "<expr_plus_name_tail>":
                # 198  <expr_plus_name_tail> → ( <arguments> ) <expr_plus_result_tail>
                # 199  <expr_plus_name_tail> → <accessor> <expr_plus_var_tail>
                if t == "(":                     # PREDICT 198
                    prod = 198
                elif t == "!=":                  # PREDICT 199
                    prod = 199
                elif t == "%":                   # PREDICT 199
                    prod = 199
                elif t == ")":                   # PREDICT 199
                    prod = 199
                elif t == "*":                   # PREDICT 199
                    prod = 199
                elif t == "+":                   # PREDICT 199
                    prod = 199
                elif t == "++":                  # PREDICT 199
                    prod = 199
                elif t == ",":                   # PREDICT 199
                    prod = 199
                elif t == "-":                   # PREDICT 199
                    prod = 199
                elif t == "--":                  # PREDICT 199
                    prod = 199
                elif t == ".":                   # PREDICT 199
                    prod = 199
                elif t == "/":                   # PREDICT 199
                    prod = 199
                elif t == ";":                   # PREDICT 199
                    prod = 199
                elif t == "<":                   # PREDICT 199
                    prod = 199
                elif t == "<=":                  # PREDICT 199
                    prod = 199
                elif t == "==":                  # PREDICT 199
                    prod = 199
                elif t == ">":                   # PREDICT 199
                    prod = 199
                elif t == ">=":                  # PREDICT 199
                    prod = 199
                elif t == "[":                   # PREDICT 199
                    prod = 199
                elif t == "]":                   # PREDICT 199
                    prod = 199
                elif t == "^":                   # PREDICT 199
                    prod = 199
                else:
                    expected = ["!=", "%", "(", ")", "*", "+", "++", ",", "-", "--", ".",
                                "/", ";", "<", "<=", "==", ">", ">=", "[", "]", "^"]

            elif top == "<expr_plus_var_tail>":
                # 200  <expr_plus_var_tail> → <incdec_op> <pow_tail> <mul_tail> <add_tail> <num_compare_tail>
                # 201  <expr_plus_var_tail> → <expr_plus_result_tail>
                if t == "++":                    # PREDICT 200
                    prod = 200
                elif t == "--":                  # PREDICT 200
                    prod = 200
                elif t == "!=":                  # PREDICT 201
                    prod = 201
                elif t == "%":                   # PREDICT 201
                    prod = 201
                elif t == ")":                   # PREDICT 201
                    prod = 201
                elif t == "*":                   # PREDICT 201
                    prod = 201
                elif t == "+":                   # PREDICT 201
                    prod = 201
                elif t == ",":                   # PREDICT 201
                    prod = 201
                elif t == "-":                   # PREDICT 201
                    prod = 201
                elif t == "/":                   # PREDICT 201
                    prod = 201
                elif t == ";":                   # PREDICT 201
                    prod = 201
                elif t == "<":                   # PREDICT 201
                    prod = 201
                elif t == "<=":                  # PREDICT 201
                    prod = 201
                elif t == "==":                  # PREDICT 201
                    prod = 201
                elif t == ">":                   # PREDICT 201
                    prod = 201
                elif t == ">=":                  # PREDICT 201
                    prod = 201
                elif t == "]":                   # PREDICT 201
                    prod = 201
                elif t == "^":                   # PREDICT 201
                    prod = 201
                else:
                    expected = ["!=", "%", ")", "*", "+", "++", ",", "-", "--", "/", ";",
                                "<", "<=", "==", ">", ">=", "]", "^"]

            elif top == "<expr_plus_result_tail>":
                # 202  <expr_plus_result_tail> → ^ <num_unary> <mul_tail> <add_tail> <num_compare_tail>
                # 203  <expr_plus_result_tail> → <mul_op> <num_unary> <mul_tail> <add_tail> <num_compare_tail>
                # 204  <expr_plus_result_tail> → - <num_term> <add_tail> <num_compare_tail>
                # 205  <expr_plus_result_tail> → + <expr_after_plus>
                # 206  <expr_plus_result_tail> → <rel_op> <num_exp> <logic_tail>
                # 207  <expr_plus_result_tail> → <equal_op> <non_truth_exp> <logic_tail>
                # 208  <expr_plus_result_tail> → λ
                if t == "^":                     # PREDICT 202
                    prod = 202
                elif t == "%":                   # PREDICT 203
                    prod = 203
                elif t == "*":                   # PREDICT 203
                    prod = 203
                elif t == "/":                   # PREDICT 203
                    prod = 203
                elif t == "-":                   # PREDICT 204
                    prod = 204
                elif t == "+":                   # PREDICT 205
                    prod = 205
                elif t == "<":                   # PREDICT 206
                    prod = 206
                elif t == "<=":                  # PREDICT 206
                    prod = 206
                elif t == ">":                   # PREDICT 206
                    prod = 206
                elif t == ">=":                  # PREDICT 206
                    prod = 206
                elif t == "!=":                  # PREDICT 207
                    prod = 207
                elif t == "==":                  # PREDICT 207
                    prod = 207
                elif t == ")":                   # PREDICT 208
                    prod = 208
                elif t == ",":                   # PREDICT 208
                    prod = 208
                elif t == ";":                   # PREDICT 208
                    prod = 208
                elif t == "]":                   # PREDICT 208
                    prod = 208
                else:
                    expected = ["!=", "%", ")", "*", "+", ",", "-", "/", ";", "<", "<=",
                                "==", ">", ">=", "]", "^"]

            elif top == "<logic_tail>":
                # 209  <logic_tail> → <and_tail> <or_tail>
                if t == ")":                     # PREDICT 209
                    prod = 209
                elif t == ",":                   # PREDICT 209
                    prod = 209
                elif t == ";":                   # PREDICT 209
                    prod = 209
                elif t == "And":                 # PREDICT 209
                    prod = 209
                elif t == "Or":                  # PREDICT 209
                    prod = 209
                elif t == "]":                   # PREDICT 209
                    prod = 209
                elif t == "{":                   # PREDICT 209
                    prod = 209
                else:
                    expected = [")", ",", ";", "And", "Or", "]", "{"]

            elif top == "<condition>":
                # 210  <condition> → <logic_operand> <logic_tail>
                if t == "(":                     # PREDICT 210
                    prod = 210
                elif t == "++":                  # PREDICT 210
                    prod = 210
                elif t == "--":                  # PREDICT 210
                    prod = 210
                elif t == "Length":              # PREDICT 210
                    prod = 210
                elif t == "Not":                 # PREDICT 210
                    prod = 210
                elif t == "ToNumber":            # PREDICT 210
                    prod = 210
                elif t == "ToRational":          # PREDICT 210
                    prod = 210
                elif t == "ToTruth":             # PREDICT 210
                    prod = 210
                elif t == "ToWord":              # PREDICT 210
                    prod = 210
                elif t == "boo_lit":             # PREDICT 210
                    prod = 210
                elif t == "flo_lit":             # PREDICT 210
                    prod = 210
                elif t == "id":                  # PREDICT 210
                    prod = 210
                elif t == "int_lit":             # PREDICT 210
                    prod = 210
                elif t == "str_lit":             # PREDICT 210
                    prod = 210
                elif t == "~":                   # PREDICT 210
                    prod = 210
                else:
                    expected = ["(", "++", "--", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "id", "int_lit", "str_lit", "~"]

            elif top == "<and_tail>":
                # 211  <and_tail> → And <logic_operand> <and_tail>
                # 212  <and_tail> → λ
                if t == "And":                   # PREDICT 211
                    prod = 211
                elif t == ")":                   # PREDICT 212
                    prod = 212
                elif t == ",":                   # PREDICT 212
                    prod = 212
                elif t == ";":                   # PREDICT 212
                    prod = 212
                elif t == "Or":                  # PREDICT 212
                    prod = 212
                elif t == "]":                   # PREDICT 212
                    prod = 212
                elif t == "{":                   # PREDICT 212
                    prod = 212
                else:
                    expected = [")", ",", ";", "And", "Or", "]", "{"]

            elif top == "<or_tail>":
                # 213  <or_tail> → Or <logic_operand> <and_tail> <or_tail>
                # 214  <or_tail> → λ
                if t == "Or":                    # PREDICT 213
                    prod = 213
                elif t == ")":                   # PREDICT 214
                    prod = 214
                elif t == ",":                   # PREDICT 214
                    prod = 214
                elif t == ";":                   # PREDICT 214
                    prod = 214
                elif t == "]":                   # PREDICT 214
                    prod = 214
                elif t == "{":                   # PREDICT 214
                    prod = 214
                else:
                    expected = [")", ",", ";", "Or", "]", "{"]

            elif top == "<logic_operand>":
                # 215  <logic_operand> → <num_literal_exp> <compare_op> <num_exp>
                # 216  <logic_operand> → <word_literal_exp> <equal_op> <word_exp>
                # 217  <logic_operand> → <truth_literal_exp> <cond_truth_compare>
                # 218  <logic_operand> → id <cond_name_tail>
                # 219  <logic_operand> → ( <expression> ) <cond_result_tail>
                if t == "++":                    # PREDICT 215
                    prod = 215
                elif t == "--":                  # PREDICT 215
                    prod = 215
                elif t == "Length":              # PREDICT 215
                    prod = 215
                elif t == "ToNumber":            # PREDICT 215
                    prod = 215
                elif t == "ToRational":          # PREDICT 215
                    prod = 215
                elif t == "flo_lit":             # PREDICT 215
                    prod = 215
                elif t == "int_lit":             # PREDICT 215
                    prod = 215
                elif t == "~":                   # PREDICT 215
                    prod = 215
                elif t == "ToWord":              # PREDICT 216
                    prod = 216
                elif t == "str_lit":             # PREDICT 216
                    prod = 216
                elif t == "Not":                 # PREDICT 217
                    prod = 217
                elif t == "ToTruth":             # PREDICT 217
                    prod = 217
                elif t == "boo_lit":             # PREDICT 217
                    prod = 217
                elif t == "id":                  # PREDICT 218
                    prod = 218
                elif t == "(":                   # PREDICT 219
                    prod = 219
                else:
                    expected = ["(", "++", "--", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "id", "int_lit", "str_lit", "~"]

            elif top == "<cond_truth_compare>":
                # 220  <cond_truth_compare> → <equal_op> <truth_unary>
                # 221  <cond_truth_compare> → λ
                if t == "!=":                    # PREDICT 220
                    prod = 220
                elif t == "==":                  # PREDICT 220
                    prod = 220
                elif t == ")":                   # PREDICT 221
                    prod = 221
                elif t == ",":                   # PREDICT 221
                    prod = 221
                elif t == ";":                   # PREDICT 221
                    prod = 221
                elif t == "And":                 # PREDICT 221
                    prod = 221
                elif t == "Or":                  # PREDICT 221
                    prod = 221
                elif t == "]":                   # PREDICT 221
                    prod = 221
                elif t == "{":                   # PREDICT 221
                    prod = 221
                else:
                    expected = ["!=", ")", ",", ";", "==", "And", "Or", "]", "{"]

            elif top == "<cond_name_tail>":
                # 222  <cond_name_tail> → ( <arguments> ) <cond_result_tail>
                # 223  <cond_name_tail> → <accessor> <cond_var_tail>
                if t == "(":                     # PREDICT 222
                    prod = 222
                elif t == "!=":                  # PREDICT 223
                    prod = 223
                elif t == "%":                   # PREDICT 223
                    prod = 223
                elif t == ")":                   # PREDICT 223
                    prod = 223
                elif t == "*":                   # PREDICT 223
                    prod = 223
                elif t == "+":                   # PREDICT 223
                    prod = 223
                elif t == "++":                  # PREDICT 223
                    prod = 223
                elif t == ",":                   # PREDICT 223
                    prod = 223
                elif t == "-":                   # PREDICT 223
                    prod = 223
                elif t == "--":                  # PREDICT 223
                    prod = 223
                elif t == ".":                   # PREDICT 223
                    prod = 223
                elif t == "/":                   # PREDICT 223
                    prod = 223
                elif t == ";":                   # PREDICT 223
                    prod = 223
                elif t == "<":                   # PREDICT 223
                    prod = 223
                elif t == "<=":                  # PREDICT 223
                    prod = 223
                elif t == "==":                  # PREDICT 223
                    prod = 223
                elif t == ">":                   # PREDICT 223
                    prod = 223
                elif t == ">=":                  # PREDICT 223
                    prod = 223
                elif t == "And":                 # PREDICT 223
                    prod = 223
                elif t == "Or":                  # PREDICT 223
                    prod = 223
                elif t == "[":                   # PREDICT 223
                    prod = 223
                elif t == "]":                   # PREDICT 223
                    prod = 223
                elif t == "^":                   # PREDICT 223
                    prod = 223
                elif t == "{":                   # PREDICT 223
                    prod = 223
                else:
                    expected = ["!=", "%", "(", ")", "*", "+", "++", ",", "-", "--", ".",
                                "/", ";", "<", "<=", "==", ">", ">=", "And", "Or", "[",
                                "]", "^", "{"]

            elif top == "<cond_var_tail>":
                # 224  <cond_var_tail> → <incdec_op> <pow_tail> <mul_tail> <add_tail> <compare_op> <num_exp>
                # 225  <cond_var_tail> → <cond_result_tail>
                if t == "++":                    # PREDICT 224
                    prod = 224
                elif t == "--":                  # PREDICT 224
                    prod = 224
                elif t == "!=":                  # PREDICT 225
                    prod = 225
                elif t == "%":                   # PREDICT 225
                    prod = 225
                elif t == ")":                   # PREDICT 225
                    prod = 225
                elif t == "*":                   # PREDICT 225
                    prod = 225
                elif t == "+":                   # PREDICT 225
                    prod = 225
                elif t == ",":                   # PREDICT 225
                    prod = 225
                elif t == "-":                   # PREDICT 225
                    prod = 225
                elif t == "/":                   # PREDICT 225
                    prod = 225
                elif t == ";":                   # PREDICT 225
                    prod = 225
                elif t == "<":                   # PREDICT 225
                    prod = 225
                elif t == "<=":                  # PREDICT 225
                    prod = 225
                elif t == "==":                  # PREDICT 225
                    prod = 225
                elif t == ">":                   # PREDICT 225
                    prod = 225
                elif t == ">=":                  # PREDICT 225
                    prod = 225
                elif t == "And":                 # PREDICT 225
                    prod = 225
                elif t == "Or":                  # PREDICT 225
                    prod = 225
                elif t == "]":                   # PREDICT 225
                    prod = 225
                elif t == "^":                   # PREDICT 225
                    prod = 225
                elif t == "{":                   # PREDICT 225
                    prod = 225
                else:
                    expected = ["!=", "%", ")", "*", "+", "++", ",", "-", "--", "/", ";",
                                "<", "<=", "==", ">", ">=", "And", "Or", "]", "^", "{"]

            elif top == "<cond_result_tail>":
                # 226  <cond_result_tail> → ^ <num_unary> <mul_tail> <add_tail> <compare_op> <num_exp>
                # 227  <cond_result_tail> → <mul_op> <num_unary> <mul_tail> <add_tail> <compare_op> <num_exp>
                # 228  <cond_result_tail> → - <num_term> <add_tail> <compare_op> <num_exp>
                # 229  <cond_result_tail> → + <cond_after_plus>
                # 230  <cond_result_tail> → <rel_op> <num_exp>
                # 231  <cond_result_tail> → <equal_op> <any_exp>
                # 232  <cond_result_tail> → λ
                if t == "^":                     # PREDICT 226
                    prod = 226
                elif t == "%":                   # PREDICT 227
                    prod = 227
                elif t == "*":                   # PREDICT 227
                    prod = 227
                elif t == "/":                   # PREDICT 227
                    prod = 227
                elif t == "-":                   # PREDICT 228
                    prod = 228
                elif t == "+":                   # PREDICT 229
                    prod = 229
                elif t == "<":                   # PREDICT 230
                    prod = 230
                elif t == "<=":                  # PREDICT 230
                    prod = 230
                elif t == ">":                   # PREDICT 230
                    prod = 230
                elif t == ">=":                  # PREDICT 230
                    prod = 230
                elif t == "!=":                  # PREDICT 231
                    prod = 231
                elif t == "==":                  # PREDICT 231
                    prod = 231
                elif t == ")":                   # PREDICT 232
                    prod = 232
                elif t == ",":                   # PREDICT 232
                    prod = 232
                elif t == ";":                   # PREDICT 232
                    prod = 232
                elif t == "And":                 # PREDICT 232
                    prod = 232
                elif t == "Or":                  # PREDICT 232
                    prod = 232
                elif t == "]":                   # PREDICT 232
                    prod = 232
                elif t == "{":                   # PREDICT 232
                    prod = 232
                else:
                    expected = ["!=", "%", ")", "*", "+", ",", "-", "/", ";", "<", "<=",
                                "==", ">", ">=", "And", "Or", "]", "^", "{"]

            elif top == "<cond_after_plus>":
                # 233  <cond_after_plus> → <num_literal_start> <mul_tail> <add_tail> <compare_op> <num_exp>
                # 234  <cond_after_plus> → <word_value> <word_tail> <equal_op> <word_exp>
                # 235  <cond_after_plus> → id <cond_plus_name_tail>
                # 236  <cond_after_plus> → ( <expression> ) <cond_plus_result_tail>
                if t == "++":                    # PREDICT 233
                    prod = 233
                elif t == "--":                  # PREDICT 233
                    prod = 233
                elif t == "Length":              # PREDICT 233
                    prod = 233
                elif t == "ToNumber":            # PREDICT 233
                    prod = 233
                elif t == "ToRational":          # PREDICT 233
                    prod = 233
                elif t == "flo_lit":             # PREDICT 233
                    prod = 233
                elif t == "int_lit":             # PREDICT 233
                    prod = 233
                elif t == "~":                   # PREDICT 233
                    prod = 233
                elif t == "ToWord":              # PREDICT 234
                    prod = 234
                elif t == "str_lit":             # PREDICT 234
                    prod = 234
                elif t == "id":                  # PREDICT 235
                    prod = 235
                elif t == "(":                   # PREDICT 236
                    prod = 236
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "ToRational",
                                "ToWord", "flo_lit", "id", "int_lit", "str_lit", "~"]

            elif top == "<cond_plus_name_tail>":
                # 237  <cond_plus_name_tail> → ( <arguments> ) <cond_plus_result_tail>
                # 238  <cond_plus_name_tail> → <accessor> <cond_plus_var_tail>
                if t == "(":                     # PREDICT 237
                    prod = 237
                elif t == "!=":                  # PREDICT 238
                    prod = 238
                elif t == "%":                   # PREDICT 238
                    prod = 238
                elif t == "*":                   # PREDICT 238
                    prod = 238
                elif t == "+":                   # PREDICT 238
                    prod = 238
                elif t == "++":                  # PREDICT 238
                    prod = 238
                elif t == "-":                   # PREDICT 238
                    prod = 238
                elif t == "--":                  # PREDICT 238
                    prod = 238
                elif t == ".":                   # PREDICT 238
                    prod = 238
                elif t == "/":                   # PREDICT 238
                    prod = 238
                elif t == "<":                   # PREDICT 238
                    prod = 238
                elif t == "<=":                  # PREDICT 238
                    prod = 238
                elif t == "==":                  # PREDICT 238
                    prod = 238
                elif t == ">":                   # PREDICT 238
                    prod = 238
                elif t == ">=":                  # PREDICT 238
                    prod = 238
                elif t == "[":                   # PREDICT 238
                    prod = 238
                elif t == "^":                   # PREDICT 238
                    prod = 238
                else:
                    expected = ["!=", "%", "(", "*", "+", "++", "-", "--", ".", "/", "<",
                                "<=", "==", ">", ">=", "[", "^"]

            elif top == "<cond_plus_var_tail>":
                # 239  <cond_plus_var_tail> → <incdec_op> <pow_tail> <mul_tail> <add_tail> <compare_op> <num_exp>
                # 240  <cond_plus_var_tail> → <cond_plus_result_tail>
                if t == "++":                    # PREDICT 239
                    prod = 239
                elif t == "--":                  # PREDICT 239
                    prod = 239
                elif t == "!=":                  # PREDICT 240
                    prod = 240
                elif t == "%":                   # PREDICT 240
                    prod = 240
                elif t == "*":                   # PREDICT 240
                    prod = 240
                elif t == "+":                   # PREDICT 240
                    prod = 240
                elif t == "-":                   # PREDICT 240
                    prod = 240
                elif t == "/":                   # PREDICT 240
                    prod = 240
                elif t == "<":                   # PREDICT 240
                    prod = 240
                elif t == "<=":                  # PREDICT 240
                    prod = 240
                elif t == "==":                  # PREDICT 240
                    prod = 240
                elif t == ">":                   # PREDICT 240
                    prod = 240
                elif t == ">=":                  # PREDICT 240
                    prod = 240
                elif t == "^":                   # PREDICT 240
                    prod = 240
                else:
                    expected = ["!=", "%", "*", "+", "++", "-", "--", "/", "<", "<=",
                                "==", ">", ">=", "^"]

            elif top == "<cond_plus_result_tail>":
                # 241  <cond_plus_result_tail> → ^ <num_unary> <mul_tail> <add_tail> <compare_op> <num_exp>
                # 242  <cond_plus_result_tail> → <mul_op> <num_unary> <mul_tail> <add_tail> <compare_op> <num_exp>
                # 243  <cond_plus_result_tail> → - <num_term> <add_tail> <compare_op> <num_exp>
                # 244  <cond_plus_result_tail> → + <cond_after_plus>
                # 245  <cond_plus_result_tail> → <rel_op> <num_exp>
                # 246  <cond_plus_result_tail> → <equal_op> <non_truth_exp>
                if t == "^":                     # PREDICT 241
                    prod = 241
                elif t == "%":                   # PREDICT 242
                    prod = 242
                elif t == "*":                   # PREDICT 242
                    prod = 242
                elif t == "/":                   # PREDICT 242
                    prod = 242
                elif t == "-":                   # PREDICT 243
                    prod = 243
                elif t == "+":                   # PREDICT 244
                    prod = 244
                elif t == "<":                   # PREDICT 245
                    prod = 245
                elif t == "<=":                  # PREDICT 245
                    prod = 245
                elif t == ">":                   # PREDICT 245
                    prod = 245
                elif t == ">=":                  # PREDICT 245
                    prod = 245
                elif t == "!=":                  # PREDICT 246
                    prod = 246
                elif t == "==":                  # PREDICT 246
                    prod = 246
                else:
                    expected = ["!=", "%", "*", "+", "-", "/", "<", "<=", "==", ">",
                                ">=", "^"]

            elif top == "<any_exp>":
                # 247  <any_exp> → <num_literal_exp>
                # 248  <any_exp> → <word_literal_exp>
                # 249  <any_exp> → <truth_literal_exp>
                # 250  <any_exp> → <untyped_exp>
                if t == "++":                    # PREDICT 247
                    prod = 247
                elif t == "--":                  # PREDICT 247
                    prod = 247
                elif t == "Length":              # PREDICT 247
                    prod = 247
                elif t == "ToNumber":            # PREDICT 247
                    prod = 247
                elif t == "ToRational":          # PREDICT 247
                    prod = 247
                elif t == "flo_lit":             # PREDICT 247
                    prod = 247
                elif t == "int_lit":             # PREDICT 247
                    prod = 247
                elif t == "~":                   # PREDICT 247
                    prod = 247
                elif t == "ToWord":              # PREDICT 248
                    prod = 248
                elif t == "str_lit":             # PREDICT 248
                    prod = 248
                elif t == "Not":                 # PREDICT 249
                    prod = 249
                elif t == "ToTruth":             # PREDICT 249
                    prod = 249
                elif t == "boo_lit":             # PREDICT 249
                    prod = 249
                elif t == "(":                   # PREDICT 250
                    prod = 250
                elif t == "id":                  # PREDICT 250
                    prod = 250
                else:
                    expected = ["(", "++", "--", "Length", "Not", "ToNumber",
                                "ToRational", "ToTruth", "ToWord", "boo_lit", "flo_lit",
                                "id", "int_lit", "str_lit", "~"]

            elif top == "<num_literal_exp>":
                # 251  <num_literal_exp> → <num_literal_start> <mul_tail> <add_tail>
                if t == "++":                    # PREDICT 251
                    prod = 251
                elif t == "--":                  # PREDICT 251
                    prod = 251
                elif t == "Length":              # PREDICT 251
                    prod = 251
                elif t == "ToNumber":            # PREDICT 251
                    prod = 251
                elif t == "ToRational":          # PREDICT 251
                    prod = 251
                elif t == "flo_lit":             # PREDICT 251
                    prod = 251
                elif t == "int_lit":             # PREDICT 251
                    prod = 251
                elif t == "~":                   # PREDICT 251
                    prod = 251
                else:
                    expected = ["++", "--", "Length", "ToNumber", "ToRational",
                                "flo_lit", "int_lit", "~"]

            elif top == "<num_literal_start>":
                # 252  <num_literal_start> → ~ <num_unary>
                # 253  <num_literal_start> → <num_value> <pow_tail>
                # 254  <num_literal_start> → <incdec_value> <pow_tail>
                if t == "~":                     # PREDICT 252
                    prod = 252
                elif t == "Length":              # PREDICT 253
                    prod = 253
                elif t == "ToNumber":            # PREDICT 253
                    prod = 253
                elif t == "ToRational":          # PREDICT 253
                    prod = 253
                elif t == "flo_lit":             # PREDICT 253
                    prod = 253
                elif t == "int_lit":             # PREDICT 253
                    prod = 253
                elif t == "++":                  # PREDICT 254
                    prod = 254
                elif t == "--":                  # PREDICT 254
                    prod = 254
                else:
                    expected = ["++", "--", "Length", "ToNumber", "ToRational",
                                "flo_lit", "int_lit", "~"]

            elif top == "<num_exp>":
                # 255  <num_exp> → <num_term> <add_tail>
                if t == "(":                     # PREDICT 255
                    prod = 255
                elif t == "++":                  # PREDICT 255
                    prod = 255
                elif t == "--":                  # PREDICT 255
                    prod = 255
                elif t == "Length":              # PREDICT 255
                    prod = 255
                elif t == "ToNumber":            # PREDICT 255
                    prod = 255
                elif t == "ToRational":          # PREDICT 255
                    prod = 255
                elif t == "flo_lit":             # PREDICT 255
                    prod = 255
                elif t == "id":                  # PREDICT 255
                    prod = 255
                elif t == "int_lit":             # PREDICT 255
                    prod = 255
                elif t == "~":                   # PREDICT 255
                    prod = 255
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "ToRational",
                                "flo_lit", "id", "int_lit", "~"]

            elif top == "<add_tail>":
                # 256  <add_tail> → + <num_term> <add_tail>
                # 257  <add_tail> → - <num_term> <add_tail>
                # 258  <add_tail> → λ
                if t == "+":                     # PREDICT 256
                    prod = 256
                elif t == "-":                   # PREDICT 257
                    prod = 257
                elif t == "!=":                  # PREDICT 258
                    prod = 258
                elif t == ")":                   # PREDICT 258
                    prod = 258
                elif t == ",":                   # PREDICT 258
                    prod = 258
                elif t == ";":                   # PREDICT 258
                    prod = 258
                elif t == "<":                   # PREDICT 258
                    prod = 258
                elif t == "<=":                  # PREDICT 258
                    prod = 258
                elif t == "==":                  # PREDICT 258
                    prod = 258
                elif t == ">":                   # PREDICT 258
                    prod = 258
                elif t == ">=":                  # PREDICT 258
                    prod = 258
                elif t == "And":                 # PREDICT 258
                    prod = 258
                elif t == "Or":                  # PREDICT 258
                    prod = 258
                elif t == "]":                   # PREDICT 258
                    prod = 258
                elif t == "{":                   # PREDICT 258
                    prod = 258
                else:
                    expected = ["!=", ")", "+", ",", "-", ";", "<", "<=", "==", ">",
                                ">=", "And", "Or", "]", "{"]

            elif top == "<num_term>":
                # 259  <num_term> → <num_unary> <mul_tail>
                if t == "(":                     # PREDICT 259
                    prod = 259
                elif t == "++":                  # PREDICT 259
                    prod = 259
                elif t == "--":                  # PREDICT 259
                    prod = 259
                elif t == "Length":              # PREDICT 259
                    prod = 259
                elif t == "ToNumber":            # PREDICT 259
                    prod = 259
                elif t == "ToRational":          # PREDICT 259
                    prod = 259
                elif t == "flo_lit":             # PREDICT 259
                    prod = 259
                elif t == "id":                  # PREDICT 259
                    prod = 259
                elif t == "int_lit":             # PREDICT 259
                    prod = 259
                elif t == "~":                   # PREDICT 259
                    prod = 259
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "ToRational",
                                "flo_lit", "id", "int_lit", "~"]

            elif top == "<mul_tail>":
                # 260  <mul_tail> → <mul_op> <num_unary> <mul_tail>
                # 261  <mul_tail> → λ
                if t == "%":                     # PREDICT 260
                    prod = 260
                elif t == "*":                   # PREDICT 260
                    prod = 260
                elif t == "/":                   # PREDICT 260
                    prod = 260
                elif t == "!=":                  # PREDICT 261
                    prod = 261
                elif t == ")":                   # PREDICT 261
                    prod = 261
                elif t == "+":                   # PREDICT 261
                    prod = 261
                elif t == ",":                   # PREDICT 261
                    prod = 261
                elif t == "-":                   # PREDICT 261
                    prod = 261
                elif t == ";":                   # PREDICT 261
                    prod = 261
                elif t == "<":                   # PREDICT 261
                    prod = 261
                elif t == "<=":                  # PREDICT 261
                    prod = 261
                elif t == "==":                  # PREDICT 261
                    prod = 261
                elif t == ">":                   # PREDICT 261
                    prod = 261
                elif t == ">=":                  # PREDICT 261
                    prod = 261
                elif t == "And":                 # PREDICT 261
                    prod = 261
                elif t == "Or":                  # PREDICT 261
                    prod = 261
                elif t == "]":                   # PREDICT 261
                    prod = 261
                elif t == "{":                   # PREDICT 261
                    prod = 261
                else:
                    expected = ["!=", "%", ")", "*", "+", ",", "-", "/", ";", "<", "<=",
                                "==", ">", ">=", "And", "Or", "]", "{"]

            elif top == "<num_unary>":
                # 262  <num_unary> → ~ <num_unary>
                # 263  <num_unary> → <num_operand> <pow_tail>
                if t == "~":                     # PREDICT 262
                    prod = 262
                elif t == "(":                   # PREDICT 263
                    prod = 263
                elif t == "++":                  # PREDICT 263
                    prod = 263
                elif t == "--":                  # PREDICT 263
                    prod = 263
                elif t == "Length":              # PREDICT 263
                    prod = 263
                elif t == "ToNumber":            # PREDICT 263
                    prod = 263
                elif t == "ToRational":          # PREDICT 263
                    prod = 263
                elif t == "flo_lit":             # PREDICT 263
                    prod = 263
                elif t == "id":                  # PREDICT 263
                    prod = 263
                elif t == "int_lit":             # PREDICT 263
                    prod = 263
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "ToRational",
                                "flo_lit", "id", "int_lit", "~"]

            elif top == "<pow_tail>":
                # 264  <pow_tail> → ^ <num_unary>
                # 265  <pow_tail> → λ
                if t == "^":                     # PREDICT 264
                    prod = 264
                elif t == "!=":                  # PREDICT 265
                    prod = 265
                elif t == "%":                   # PREDICT 265
                    prod = 265
                elif t == ")":                   # PREDICT 265
                    prod = 265
                elif t == "*":                   # PREDICT 265
                    prod = 265
                elif t == "+":                   # PREDICT 265
                    prod = 265
                elif t == ",":                   # PREDICT 265
                    prod = 265
                elif t == "-":                   # PREDICT 265
                    prod = 265
                elif t == "/":                   # PREDICT 265
                    prod = 265
                elif t == ";":                   # PREDICT 265
                    prod = 265
                elif t == "<":                   # PREDICT 265
                    prod = 265
                elif t == "<=":                  # PREDICT 265
                    prod = 265
                elif t == "==":                  # PREDICT 265
                    prod = 265
                elif t == ">":                   # PREDICT 265
                    prod = 265
                elif t == ">=":                  # PREDICT 265
                    prod = 265
                elif t == "And":                 # PREDICT 265
                    prod = 265
                elif t == "Or":                  # PREDICT 265
                    prod = 265
                elif t == "]":                   # PREDICT 265
                    prod = 265
                elif t == "{":                   # PREDICT 265
                    prod = 265
                else:
                    expected = ["!=", "%", ")", "*", "+", ",", "-", "/", ";", "<", "<=",
                                "==", ">", ">=", "And", "Or", "]", "^", "{"]

            elif top == "<num_operand>":
                # 266  <num_operand> → <num_value>
                # 267  <num_operand> → <incdec_value>
                # 268  <num_operand> → <untyped_num_operand>
                if t == "Length":                # PREDICT 266
                    prod = 266
                elif t == "ToNumber":            # PREDICT 266
                    prod = 266
                elif t == "ToRational":          # PREDICT 266
                    prod = 266
                elif t == "flo_lit":             # PREDICT 266
                    prod = 266
                elif t == "int_lit":             # PREDICT 266
                    prod = 266
                elif t == "++":                  # PREDICT 267
                    prod = 267
                elif t == "--":                  # PREDICT 267
                    prod = 267
                elif t == "(":                   # PREDICT 268
                    prod = 268
                elif t == "id":                  # PREDICT 268
                    prod = 268
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "ToRational",
                                "flo_lit", "id", "int_lit"]

            elif top == "<num_value>":
                # 269  <num_value> → int_lit
                # 270  <num_value> → flo_lit
                # 271  <num_value> → ToNumber ( <expression> )
                # 272  <num_value> → ToRational ( <expression> )
                # 273  <num_value> → Length ( <length_arg> )
                if t == "int_lit":               # PREDICT 269
                    prod = 269
                elif t == "flo_lit":             # PREDICT 270
                    prod = 270
                elif t == "ToNumber":            # PREDICT 271
                    prod = 271
                elif t == "ToRational":          # PREDICT 272
                    prod = 272
                elif t == "Length":              # PREDICT 273
                    prod = 273
                else:
                    expected = ["Length", "ToNumber", "ToRational", "flo_lit", "int_lit"]

            elif top == "<incdec_value>":
                # 274  <incdec_value> → <incdec_op> id <accessor>
                if t == "++":                    # PREDICT 274
                    prod = 274
                elif t == "--":                  # PREDICT 274
                    prod = 274
                else:
                    expected = ["++", "--"]

            elif top == "<length_arg>":
                # 275  <length_arg> → <word_literal_exp>
                # 276  <length_arg> → <untyped_operand> <word_tail>
                if t == "ToWord":                # PREDICT 275
                    prod = 275
                elif t == "str_lit":             # PREDICT 275
                    prod = 275
                elif t == "(":                   # PREDICT 276
                    prod = 276
                elif t == "id":                  # PREDICT 276
                    prod = 276
                else:
                    expected = ["(", "ToWord", "id", "str_lit"]

            elif top == "<harvest_value>":
                # 277  <harvest_value> → <int_literal_exp>
                # 278  <harvest_value> → <word_literal_exp>
                # 279  <harvest_value> → id <harvest_name_tail>
                # 280  <harvest_value> → ( <expression> ) <harvest_result_tail>
                if t == "++":                    # PREDICT 277
                    prod = 277
                elif t == "--":                  # PREDICT 277
                    prod = 277
                elif t == "Length":              # PREDICT 277
                    prod = 277
                elif t == "ToNumber":            # PREDICT 277
                    prod = 277
                elif t == "int_lit":             # PREDICT 277
                    prod = 277
                elif t == "~":                   # PREDICT 277
                    prod = 277
                elif t == "ToWord":              # PREDICT 278
                    prod = 278
                elif t == "str_lit":             # PREDICT 278
                    prod = 278
                elif t == "id":                  # PREDICT 279
                    prod = 279
                elif t == "(":                   # PREDICT 280
                    prod = 280
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "ToWord", "id",
                                "int_lit", "str_lit", "~"]

            elif top == "<harvest_name_tail>":
                # 281  <harvest_name_tail> → ( <arguments> ) <harvest_result_tail>
                # 282  <harvest_name_tail> → <accessor> <harvest_var_tail>
                if t == "(":                     # PREDICT 281
                    prod = 281
                elif t == "%":                   # PREDICT 282
                    prod = 282
                elif t == "*":                   # PREDICT 282
                    prod = 282
                elif t == "+":                   # PREDICT 282
                    prod = 282
                elif t == "++":                  # PREDICT 282
                    prod = 282
                elif t == "-":                   # PREDICT 282
                    prod = 282
                elif t == "--":                  # PREDICT 282
                    prod = 282
                elif t == ".":                   # PREDICT 282
                    prod = 282
                elif t == "[":                   # PREDICT 282
                    prod = 282
                elif t == "^":                   # PREDICT 282
                    prod = 282
                elif t == "{":                   # PREDICT 282
                    prod = 282
                else:
                    expected = ["%", "(", "*", "+", "++", "-", "--", ".", "[", "^", "{"]

            elif top == "<harvest_var_tail>":
                # 283  <harvest_var_tail> → <incdec_op> <int_pow_tail> <int_mul_tail> <int_add_tail>
                # 284  <harvest_var_tail> → <harvest_result_tail>
                if t == "++":                    # PREDICT 283
                    prod = 283
                elif t == "--":                  # PREDICT 283
                    prod = 283
                elif t == "%":                   # PREDICT 284
                    prod = 284
                elif t == "*":                   # PREDICT 284
                    prod = 284
                elif t == "+":                   # PREDICT 284
                    prod = 284
                elif t == "-":                   # PREDICT 284
                    prod = 284
                elif t == "^":                   # PREDICT 284
                    prod = 284
                elif t == "{":                   # PREDICT 284
                    prod = 284
                else:
                    expected = ["%", "*", "+", "++", "-", "--", "^", "{"]

            elif top == "<harvest_result_tail>":
                # 285  <harvest_result_tail> → ^ <int_unary> <int_mul_tail> <int_add_tail>
                # 286  <harvest_result_tail> → <int_mul_op> <int_unary> <int_mul_tail> <int_add_tail>
                # 287  <harvest_result_tail> → - <int_term> <int_add_tail>
                # 288  <harvest_result_tail> → + <harvest_value>
                # 289  <harvest_result_tail> → λ
                if t == "^":                     # PREDICT 285
                    prod = 285
                elif t == "%":                   # PREDICT 286
                    prod = 286
                elif t == "*":                   # PREDICT 286
                    prod = 286
                elif t == "-":                   # PREDICT 287
                    prod = 287
                elif t == "+":                   # PREDICT 288
                    prod = 288
                elif t == "{":                   # PREDICT 289
                    prod = 289
                else:
                    expected = ["%", "*", "+", "-", "^", "{"]

            elif top == "<int_literal_exp>":
                # 290  <int_literal_exp> → <int_literal_start> <int_mul_tail> <int_add_tail>
                if t == "++":                    # PREDICT 290
                    prod = 290
                elif t == "--":                  # PREDICT 290
                    prod = 290
                elif t == "Length":              # PREDICT 290
                    prod = 290
                elif t == "ToNumber":            # PREDICT 290
                    prod = 290
                elif t == "int_lit":             # PREDICT 290
                    prod = 290
                elif t == "~":                   # PREDICT 290
                    prod = 290
                else:
                    expected = ["++", "--", "Length", "ToNumber", "int_lit", "~"]

            elif top == "<int_literal_start>":
                # 291  <int_literal_start> → ~ <int_unary>
                # 292  <int_literal_start> → <int_value> <int_pow_tail>
                # 293  <int_literal_start> → <incdec_value> <int_pow_tail>
                if t == "~":                     # PREDICT 291
                    prod = 291
                elif t == "Length":              # PREDICT 292
                    prod = 292
                elif t == "ToNumber":            # PREDICT 292
                    prod = 292
                elif t == "int_lit":             # PREDICT 292
                    prod = 292
                elif t == "++":                  # PREDICT 293
                    prod = 293
                elif t == "--":                  # PREDICT 293
                    prod = 293
                else:
                    expected = ["++", "--", "Length", "ToNumber", "int_lit", "~"]

            elif top == "<int_exp>":
                # 294  <int_exp> → <int_term> <int_add_tail>
                if t == "(":                     # PREDICT 294
                    prod = 294
                elif t == "++":                  # PREDICT 294
                    prod = 294
                elif t == "--":                  # PREDICT 294
                    prod = 294
                elif t == "Length":              # PREDICT 294
                    prod = 294
                elif t == "ToNumber":            # PREDICT 294
                    prod = 294
                elif t == "id":                  # PREDICT 294
                    prod = 294
                elif t == "int_lit":             # PREDICT 294
                    prod = 294
                elif t == "~":                   # PREDICT 294
                    prod = 294
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "id", "int_lit",
                                "~"]

            elif top == "<int_add_tail>":
                # 295  <int_add_tail> → + <int_term> <int_add_tail>
                # 296  <int_add_tail> → - <int_term> <int_add_tail>
                # 297  <int_add_tail> → λ
                if t == "+":                     # PREDICT 295
                    prod = 295
                elif t == "-":                   # PREDICT 296
                    prod = 296
                elif t == ")":                   # PREDICT 297
                    prod = 297
                elif t == ",":                   # PREDICT 297
                    prod = 297
                elif t == "]":                   # PREDICT 297
                    prod = 297
                elif t == "{":                   # PREDICT 297
                    prod = 297
                else:
                    expected = [")", "+", ",", "-", "]", "{"]

            elif top == "<int_term>":
                # 298  <int_term> → <int_unary> <int_mul_tail>
                if t == "(":                     # PREDICT 298
                    prod = 298
                elif t == "++":                  # PREDICT 298
                    prod = 298
                elif t == "--":                  # PREDICT 298
                    prod = 298
                elif t == "Length":              # PREDICT 298
                    prod = 298
                elif t == "ToNumber":            # PREDICT 298
                    prod = 298
                elif t == "id":                  # PREDICT 298
                    prod = 298
                elif t == "int_lit":             # PREDICT 298
                    prod = 298
                elif t == "~":                   # PREDICT 298
                    prod = 298
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "id", "int_lit",
                                "~"]

            elif top == "<int_mul_tail>":
                # 299  <int_mul_tail> → <int_mul_op> <int_unary> <int_mul_tail>
                # 300  <int_mul_tail> → λ
                if t == "%":                     # PREDICT 299
                    prod = 299
                elif t == "*":                   # PREDICT 299
                    prod = 299
                elif t == ")":                   # PREDICT 300
                    prod = 300
                elif t == "+":                   # PREDICT 300
                    prod = 300
                elif t == ",":                   # PREDICT 300
                    prod = 300
                elif t == "-":                   # PREDICT 300
                    prod = 300
                elif t == "]":                   # PREDICT 300
                    prod = 300
                elif t == "{":                   # PREDICT 300
                    prod = 300
                else:
                    expected = ["%", ")", "*", "+", ",", "-", "]", "{"]

            elif top == "<int_unary>":
                # 301  <int_unary> → ~ <int_unary>
                # 302  <int_unary> → <int_operand> <int_pow_tail>
                if t == "~":                     # PREDICT 301
                    prod = 301
                elif t == "(":                   # PREDICT 302
                    prod = 302
                elif t == "++":                  # PREDICT 302
                    prod = 302
                elif t == "--":                  # PREDICT 302
                    prod = 302
                elif t == "Length":              # PREDICT 302
                    prod = 302
                elif t == "ToNumber":            # PREDICT 302
                    prod = 302
                elif t == "id":                  # PREDICT 302
                    prod = 302
                elif t == "int_lit":             # PREDICT 302
                    prod = 302
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "id", "int_lit",
                                "~"]

            elif top == "<int_pow_tail>":
                # 303  <int_pow_tail> → ^ <int_unary>
                # 304  <int_pow_tail> → λ
                if t == "^":                     # PREDICT 303
                    prod = 303
                elif t == "%":                   # PREDICT 304
                    prod = 304
                elif t == ")":                   # PREDICT 304
                    prod = 304
                elif t == "*":                   # PREDICT 304
                    prod = 304
                elif t == "+":                   # PREDICT 304
                    prod = 304
                elif t == ",":                   # PREDICT 304
                    prod = 304
                elif t == "-":                   # PREDICT 304
                    prod = 304
                elif t == "]":                   # PREDICT 304
                    prod = 304
                elif t == "{":                   # PREDICT 304
                    prod = 304
                else:
                    expected = ["%", ")", "*", "+", ",", "-", "]", "^", "{"]

            elif top == "<int_operand>":
                # 305  <int_operand> → <int_value>
                # 306  <int_operand> → <incdec_value>
                # 307  <int_operand> → <untyped_num_operand>
                if t == "Length":                # PREDICT 305
                    prod = 305
                elif t == "ToNumber":            # PREDICT 305
                    prod = 305
                elif t == "int_lit":             # PREDICT 305
                    prod = 305
                elif t == "++":                  # PREDICT 306
                    prod = 306
                elif t == "--":                  # PREDICT 306
                    prod = 306
                elif t == "(":                   # PREDICT 307
                    prod = 307
                elif t == "id":                  # PREDICT 307
                    prod = 307
                else:
                    expected = ["(", "++", "--", "Length", "ToNumber", "id", "int_lit"]

            elif top == "<int_value>":
                # 308  <int_value> → int_lit
                # 309  <int_value> → ToNumber ( <expression> )
                # 310  <int_value> → Length ( <length_arg> )
                if t == "int_lit":               # PREDICT 308
                    prod = 308
                elif t == "ToNumber":            # PREDICT 309
                    prod = 309
                elif t == "Length":              # PREDICT 310
                    prod = 310
                else:
                    expected = ["Length", "ToNumber", "int_lit"]

            elif top == "<word_literal_exp>":
                # 311  <word_literal_exp> → <word_value> <word_tail>
                if t == "ToWord":                # PREDICT 311
                    prod = 311
                elif t == "str_lit":             # PREDICT 311
                    prod = 311
                else:
                    expected = ["ToWord", "str_lit"]

            elif top == "<word_exp>":
                # 312  <word_exp> → <word_operand> <word_tail>
                if t == "(":                     # PREDICT 312
                    prod = 312
                elif t == "ToWord":              # PREDICT 312
                    prod = 312
                elif t == "id":                  # PREDICT 312
                    prod = 312
                elif t == "str_lit":             # PREDICT 312
                    prod = 312
                else:
                    expected = ["(", "ToWord", "id", "str_lit"]

            elif top == "<word_tail>":
                # 313  <word_tail> → + <word_operand> <word_tail>
                # 314  <word_tail> → λ
                if t == "+":                     # PREDICT 313
                    prod = 313
                elif t == "!=":                  # PREDICT 314
                    prod = 314
                elif t == ")":                   # PREDICT 314
                    prod = 314
                elif t == ",":                   # PREDICT 314
                    prod = 314
                elif t == ";":                   # PREDICT 314
                    prod = 314
                elif t == "==":                  # PREDICT 314
                    prod = 314
                elif t == "And":                 # PREDICT 314
                    prod = 314
                elif t == "Or":                  # PREDICT 314
                    prod = 314
                elif t == "]":                   # PREDICT 314
                    prod = 314
                elif t == "{":                   # PREDICT 314
                    prod = 314
                else:
                    expected = ["!=", ")", "+", ",", ";", "==", "And", "Or", "]", "{"]

            elif top == "<word_operand>":
                # 315  <word_operand> → <word_value>
                # 316  <word_operand> → <untyped_operand>
                if t == "ToWord":                # PREDICT 315
                    prod = 315
                elif t == "str_lit":             # PREDICT 315
                    prod = 315
                elif t == "(":                   # PREDICT 316
                    prod = 316
                elif t == "id":                  # PREDICT 316
                    prod = 316
                else:
                    expected = ["(", "ToWord", "id", "str_lit"]

            elif top == "<word_value>":
                # 317  <word_value> → str_lit
                # 318  <word_value> → ToWord ( <expression> )
                if t == "str_lit":               # PREDICT 317
                    prod = 317
                elif t == "ToWord":              # PREDICT 318
                    prod = 318
                else:
                    expected = ["ToWord", "str_lit"]

            elif top == "<truth_literal_exp>":
                # 319  <truth_literal_exp> → <truth_value>
                # 320  <truth_literal_exp> → Not <truth_unary>
                if t == "ToTruth":               # PREDICT 319
                    prod = 319
                elif t == "boo_lit":             # PREDICT 319
                    prod = 319
                elif t == "Not":                 # PREDICT 320
                    prod = 320
                else:
                    expected = ["Not", "ToTruth", "boo_lit"]

            elif top == "<truth_unary>":
                # 321  <truth_unary> → Not <truth_unary>
                # 322  <truth_unary> → <truth_value>
                # 323  <truth_unary> → <untyped_operand>
                if t == "Not":                   # PREDICT 321
                    prod = 321
                elif t == "ToTruth":             # PREDICT 322
                    prod = 322
                elif t == "boo_lit":             # PREDICT 322
                    prod = 322
                elif t == "(":                   # PREDICT 323
                    prod = 323
                elif t == "id":                  # PREDICT 323
                    prod = 323
                else:
                    expected = ["(", "Not", "ToTruth", "boo_lit", "id"]

            elif top == "<truth_value>":
                # 324  <truth_value> → boo_lit
                # 325  <truth_value> → ToTruth ( <expression> )
                if t == "boo_lit":               # PREDICT 324
                    prod = 324
                elif t == "ToTruth":             # PREDICT 325
                    prod = 325
                else:
                    expected = ["ToTruth", "boo_lit"]

            elif top == "<untyped_exp>":
                # 326  <untyped_exp> → id <untyped_name_tail>
                # 327  <untyped_exp> → ( <expression> ) <untyped_result_tail>
                if t == "id":                    # PREDICT 326
                    prod = 326
                elif t == "(":                   # PREDICT 327
                    prod = 327
                else:
                    expected = ["(", "id"]

            elif top == "<untyped_name_tail>":
                # 328  <untyped_name_tail> → ( <arguments> ) <untyped_result_tail>
                # 329  <untyped_name_tail> → <accessor> <untyped_var_tail>
                if t == "(":                     # PREDICT 328
                    prod = 328
                elif t == "%":                   # PREDICT 329
                    prod = 329
                elif t == ")":                   # PREDICT 329
                    prod = 329
                elif t == "*":                   # PREDICT 329
                    prod = 329
                elif t == "+":                   # PREDICT 329
                    prod = 329
                elif t == "++":                  # PREDICT 329
                    prod = 329
                elif t == ",":                   # PREDICT 329
                    prod = 329
                elif t == "-":                   # PREDICT 329
                    prod = 329
                elif t == "--":                  # PREDICT 329
                    prod = 329
                elif t == ".":                   # PREDICT 329
                    prod = 329
                elif t == "/":                   # PREDICT 329
                    prod = 329
                elif t == ";":                   # PREDICT 329
                    prod = 329
                elif t == "And":                 # PREDICT 329
                    prod = 329
                elif t == "Or":                  # PREDICT 329
                    prod = 329
                elif t == "[":                   # PREDICT 329
                    prod = 329
                elif t == "]":                   # PREDICT 329
                    prod = 329
                elif t == "^":                   # PREDICT 329
                    prod = 329
                elif t == "{":                   # PREDICT 329
                    prod = 329
                else:
                    expected = ["%", "(", ")", "*", "+", "++", ",", "-", "--", ".", "/",
                                ";", "And", "Or", "[", "]", "^", "{"]

            elif top == "<untyped_var_tail>":
                # 330  <untyped_var_tail> → <incdec_op> <pow_tail> <mul_tail> <add_tail>
                # 331  <untyped_var_tail> → <untyped_result_tail>
                if t == "++":                    # PREDICT 330
                    prod = 330
                elif t == "--":                  # PREDICT 330
                    prod = 330
                elif t == "%":                   # PREDICT 331
                    prod = 331
                elif t == ")":                   # PREDICT 331
                    prod = 331
                elif t == "*":                   # PREDICT 331
                    prod = 331
                elif t == "+":                   # PREDICT 331
                    prod = 331
                elif t == ",":                   # PREDICT 331
                    prod = 331
                elif t == "-":                   # PREDICT 331
                    prod = 331
                elif t == "/":                   # PREDICT 331
                    prod = 331
                elif t == ";":                   # PREDICT 331
                    prod = 331
                elif t == "And":                 # PREDICT 331
                    prod = 331
                elif t == "Or":                  # PREDICT 331
                    prod = 331
                elif t == "]":                   # PREDICT 331
                    prod = 331
                elif t == "^":                   # PREDICT 331
                    prod = 331
                elif t == "{":                   # PREDICT 331
                    prod = 331
                else:
                    expected = ["%", ")", "*", "+", "++", ",", "-", "--", "/", ";",
                                "And", "Or", "]", "^", "{"]

            elif top == "<untyped_result_tail>":
                # 332  <untyped_result_tail> → ^ <num_unary> <mul_tail> <add_tail>
                # 333  <untyped_result_tail> → <mul_op> <num_unary> <mul_tail> <add_tail>
                # 334  <untyped_result_tail> → - <num_term> <add_tail>
                # 335  <untyped_result_tail> → + <non_truth_exp>
                # 336  <untyped_result_tail> → λ
                if t == "^":                     # PREDICT 332
                    prod = 332
                elif t == "%":                   # PREDICT 333
                    prod = 333
                elif t == "*":                   # PREDICT 333
                    prod = 333
                elif t == "/":                   # PREDICT 333
                    prod = 333
                elif t == "-":                   # PREDICT 334
                    prod = 334
                elif t == "+":                   # PREDICT 335
                    prod = 335
                elif t == ")":                   # PREDICT 336
                    prod = 336
                elif t == ",":                   # PREDICT 336
                    prod = 336
                elif t == ";":                   # PREDICT 336
                    prod = 336
                elif t == "And":                 # PREDICT 336
                    prod = 336
                elif t == "Or":                  # PREDICT 336
                    prod = 336
                elif t == "]":                   # PREDICT 336
                    prod = 336
                elif t == "{":                   # PREDICT 336
                    prod = 336
                else:
                    expected = ["%", ")", "*", "+", ",", "-", "/", ";", "And", "Or", "]",
                                "^", "{"]

            elif top == "<untyped_operand>":
                # 337  <untyped_operand> → id <name_tail>
                # 338  <untyped_operand> → ( <expression> )
                if t == "id":                    # PREDICT 337
                    prod = 337
                elif t == "(":                   # PREDICT 338
                    prod = 338
                else:
                    expected = ["(", "id"]

            elif top == "<name_tail>":
                # 339  <name_tail> → ( <arguments> )
                # 340  <name_tail> → <accessor>
                if t == "(":                     # PREDICT 339
                    prod = 339
                elif t == "!=":                  # PREDICT 340
                    prod = 340
                elif t == ")":                   # PREDICT 340
                    prod = 340
                elif t == "+":                   # PREDICT 340
                    prod = 340
                elif t == ",":                   # PREDICT 340
                    prod = 340
                elif t == ".":                   # PREDICT 340
                    prod = 340
                elif t == ";":                   # PREDICT 340
                    prod = 340
                elif t == "==":                  # PREDICT 340
                    prod = 340
                elif t == "And":                 # PREDICT 340
                    prod = 340
                elif t == "Or":                  # PREDICT 340
                    prod = 340
                elif t == "[":                   # PREDICT 340
                    prod = 340
                elif t == "]":                   # PREDICT 340
                    prod = 340
                elif t == "{":                   # PREDICT 340
                    prod = 340
                else:
                    expected = ["!=", "(", ")", "+", ",", ".", ";", "==", "And", "Or",
                                "[", "]", "{"]

            elif top == "<untyped_num_operand>":
                # 341  <untyped_num_operand> → id <untyped_num_tail>
                # 342  <untyped_num_operand> → ( <expression> )
                if t == "id":                    # PREDICT 341
                    prod = 341
                elif t == "(":                   # PREDICT 342
                    prod = 342
                else:
                    expected = ["(", "id"]

            elif top == "<untyped_num_tail>":
                # 343  <untyped_num_tail> → ( <arguments> )
                # 344  <untyped_num_tail> → <accessor> <postfix>
                if t == "(":                     # PREDICT 343
                    prod = 343
                elif t == "!=":                  # PREDICT 344
                    prod = 344
                elif t == "%":                   # PREDICT 344
                    prod = 344
                elif t == ")":                   # PREDICT 344
                    prod = 344
                elif t == "*":                   # PREDICT 344
                    prod = 344
                elif t == "+":                   # PREDICT 344
                    prod = 344
                elif t == "++":                  # PREDICT 344
                    prod = 344
                elif t == ",":                   # PREDICT 344
                    prod = 344
                elif t == "-":                   # PREDICT 344
                    prod = 344
                elif t == "--":                  # PREDICT 344
                    prod = 344
                elif t == ".":                   # PREDICT 344
                    prod = 344
                elif t == "/":                   # PREDICT 344
                    prod = 344
                elif t == ";":                   # PREDICT 344
                    prod = 344
                elif t == "<":                   # PREDICT 344
                    prod = 344
                elif t == "<=":                  # PREDICT 344
                    prod = 344
                elif t == "==":                  # PREDICT 344
                    prod = 344
                elif t == ">":                   # PREDICT 344
                    prod = 344
                elif t == ">=":                  # PREDICT 344
                    prod = 344
                elif t == "And":                 # PREDICT 344
                    prod = 344
                elif t == "Or":                  # PREDICT 344
                    prod = 344
                elif t == "[":                   # PREDICT 344
                    prod = 344
                elif t == "]":                   # PREDICT 344
                    prod = 344
                elif t == "^":                   # PREDICT 344
                    prod = 344
                elif t == "{":                   # PREDICT 344
                    prod = 344
                else:
                    expected = ["!=", "%", "(", ")", "*", "+", "++", ",", "-", "--", ".",
                                "/", ";", "<", "<=", "==", ">", ">=", "And", "Or", "[",
                                "]", "^", "{"]

            elif top == "<postfix>":
                # 345  <postfix> → <incdec_op>
                # 346  <postfix> → λ
                if t == "++":                    # PREDICT 345
                    prod = 345
                elif t == "--":                  # PREDICT 345
                    prod = 345
                elif t == "!=":                  # PREDICT 346
                    prod = 346
                elif t == "%":                   # PREDICT 346
                    prod = 346
                elif t == ")":                   # PREDICT 346
                    prod = 346
                elif t == "*":                   # PREDICT 346
                    prod = 346
                elif t == "+":                   # PREDICT 346
                    prod = 346
                elif t == ",":                   # PREDICT 346
                    prod = 346
                elif t == "-":                   # PREDICT 346
                    prod = 346
                elif t == "/":                   # PREDICT 346
                    prod = 346
                elif t == ";":                   # PREDICT 346
                    prod = 346
                elif t == "<":                   # PREDICT 346
                    prod = 346
                elif t == "<=":                  # PREDICT 346
                    prod = 346
                elif t == "==":                  # PREDICT 346
                    prod = 346
                elif t == ">":                   # PREDICT 346
                    prod = 346
                elif t == ">=":                  # PREDICT 346
                    prod = 346
                elif t == "And":                 # PREDICT 346
                    prod = 346
                elif t == "Or":                  # PREDICT 346
                    prod = 346
                elif t == "]":                   # PREDICT 346
                    prod = 346
                elif t == "^":                   # PREDICT 346
                    prod = 346
                elif t == "{":                   # PREDICT 346
                    prod = 346
                else:
                    expected = ["!=", "%", ")", "*", "+", "++", ",", "-", "--", "/", ";",
                                "<", "<=", "==", ">", ">=", "And", "Or", "]", "^", "{"]

            elif top == "<compare_op>":
                # 347  <compare_op> → <rel_op>
                # 348  <compare_op> → <equal_op>
                if t == "<":                     # PREDICT 347
                    prod = 347
                elif t == "<=":                  # PREDICT 347
                    prod = 347
                elif t == ">":                   # PREDICT 347
                    prod = 347
                elif t == ">=":                  # PREDICT 347
                    prod = 347
                elif t == "!=":                  # PREDICT 348
                    prod = 348
                elif t == "==":                  # PREDICT 348
                    prod = 348
                else:
                    expected = ["!=", "<", "<=", "==", ">", ">="]

            elif top == "<rel_op>":
                # 349  <rel_op> → >
                # 350  <rel_op> → <
                # 351  <rel_op> → >=
                # 352  <rel_op> → <=
                if t == ">":                     # PREDICT 349
                    prod = 349
                elif t == "<":                   # PREDICT 350
                    prod = 350
                elif t == ">=":                  # PREDICT 351
                    prod = 351
                elif t == "<=":                  # PREDICT 352
                    prod = 352
                else:
                    expected = ["<", "<=", ">", ">="]

            elif top == "<equal_op>":
                # 353  <equal_op> → ==
                # 354  <equal_op> → !=
                if t == "==":                    # PREDICT 353
                    prod = 353
                elif t == "!=":                  # PREDICT 354
                    prod = 354
                else:
                    expected = ["!=", "=="]

            elif top == "<mul_op>":
                # 355  <mul_op> → *
                # 356  <mul_op> → /
                # 357  <mul_op> → %
                if t == "*":                     # PREDICT 355
                    prod = 355
                elif t == "/":                   # PREDICT 356
                    prod = 356
                elif t == "%":                   # PREDICT 357
                    prod = 357
                else:
                    expected = ["%", "*", "/"]

            elif top == "<int_mul_op>":
                # 358  <int_mul_op> → *
                # 359  <int_mul_op> → %
                if t == "*":                     # PREDICT 358
                    prod = 358
                elif t == "%":                   # PREDICT 359
                    prod = 359
                else:
                    expected = ["%", "*"]

            # --- replace the non-terminal by the right side of production prod ----
            if prod is None:
                self._fail(stack_before, tok, t, expected, top)
                return False
            self.steps.append(prod)
            self._trace(stack_before, tok, t, "predict", prod, production_text(prod))
            stack.extend(reversed(PRODUCTIONS[prod - 1][1]))

    # --- error and trace ------------------------------------------------------------
    def _fail(self, stack_before, tok, name, expected, nonterminal=None):
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
        self._trace(stack_before, tok, name, "error", None, msg)

    def _trace(self, stack, tok, name, kind, production, action):
        """One row of the parse trace (like the lexer's state path)."""
        self.trace.append({
            "step": len(self.trace) + 1,
            "stack": stack,
            "lookahead": name,
            "lexeme": "" if name == END else tok.lexeme,
            "line": tok.line,
            "col": tok.col,
            "kind": kind,               # predict / match / accept / error
            "production": production,   # production number for predict
            "action": action,
        })


def parse(tokens):
    """Parse a token list.  Returns the Parser (check .errors)."""
    p = Parser(tokens)
    p.parse()
    return p
