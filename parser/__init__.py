"""The LIME syntax analyzer: an LL(1) predictive parser built from the CFG of the paper."""

from .parser import Parser, parse, SyntaxError_

__all__ = ["Parser", "parse", "SyntaxError_"]
