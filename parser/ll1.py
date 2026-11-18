"""
ll1.py - FIRST, FOLLOW and PREDICT sets (pp. 131-167) computed from the CFG,
and the LL(1) parse table built from the PREDICT sets.

The sets are computed, not typed in, so they always agree with grammar.py.
`python -m parser.ll1` prints them and any LL(1) conflicts, to compare with
the tables in the paper.
"""

from .grammar import PRODUCTIONS, START, END, EPSILON, is_nonterminal

NONTERMINALS = []
for _lhs, _ in PRODUCTIONS:
    if _lhs not in NONTERMINALS:
        NONTERMINALS.append(_lhs)

TERMINALS = sorted({s for _, rhs in PRODUCTIONS for s in rhs
                    if not is_nonterminal(s)})


def _first_of_seq(seq, first):
    """FIRST of a sequence of symbols (contains λ if the whole seq can vanish)."""
    out = set()
    for sym in seq:
        f = first[sym] if is_nonterminal(sym) else {sym}
        out |= f - {EPSILON}
        if EPSILON not in f:
            return out
    out.add(EPSILON)
    return out


def compute_first():
    first = {nt: set() for nt in NONTERMINALS}
    changed = True
    while changed:
        changed = False
        for lhs, rhs in PRODUCTIONS:
            f = _first_of_seq(rhs, first)
            if not f <= first[lhs]:
                first[lhs] |= f
                changed = True
    return first


def compute_follow(first):
    follow = {nt: set() for nt in NONTERMINALS}
    follow[START].add(END)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in PRODUCTIONS:
            for i, sym in enumerate(rhs):
                if not is_nonterminal(sym):
                    continue
                f = _first_of_seq(rhs[i + 1:], first)
                add = f - {EPSILON}
                if EPSILON in f:
                    add |= follow[lhs]
                if not add <= follow[sym]:
                    follow[sym] |= add
                    changed = True
    return follow


def compute_predict(first, follow):
    """PREDICT(k) = FIRST(rhs) - λ, plus FOLLOW(lhs) when rhs can vanish."""
    predict = []
    for lhs, rhs in PRODUCTIONS:
        f = _first_of_seq(rhs, first)
        p = f - {EPSILON}
        if EPSILON in f:
            p |= follow[lhs]
        predict.append(p)
    return predict


def build_table(predict):
    """table[nonterminal][terminal] = production number (1-based).
    A conflict keeps the lower-numbered production (paper order) and is
    recorded in `conflicts`."""
    table = {nt: {} for nt in NONTERMINALS}
    conflicts = []
    for k, ((lhs, _), p) in enumerate(zip(PRODUCTIONS, predict), start=1):
        for t in p:
            if t in table[lhs]:
                conflicts.append((lhs, t, table[lhs][t], k))
            else:
                table[lhs][t] = k
    return table, conflicts


FIRST = compute_first()
FOLLOW = compute_follow(FIRST)
PREDICT = compute_predict(FIRST, FOLLOW)
TABLE, CONFLICTS = build_table(PREDICT)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")   # λ on a Windows console

    def show(s):
        return ", ".join(sorted(s))
    print("FIRST SET")
    for nt in NONTERMINALS:
        print("  %-26s %s" % (nt, show(FIRST[nt])))
    print("\nFOLLOW SET")
    for nt in NONTERMINALS:
        print("  %-26s %s" % (nt, show(FOLLOW[nt])))
    print("\nPREDICT SET")
    for k, p in enumerate(PREDICT, start=1):
        print("  %3d %s" % (k, show(p)))
    print("\n%d productions, %d non-terminals, %d terminals"
          % (len(PRODUCTIONS), len(NONTERMINALS), len(TERMINALS)))
    if CONFLICTS:
        print("LL(1) CONFLICTS:")
        for lhs, t, a, b in CONFLICTS:
            print("  %s on %r: productions %d and %d" % (lhs, t, a, b))
    else:
        print("No LL(1) conflicts.")
