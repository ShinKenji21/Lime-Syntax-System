# Lime-Syntax-System (Lime Lexical Analyzer + Syntax)

Web-based lexical analyzer and tokenizer for the LIME compiler.

## Run locally on Windows

From this project directory, create a virtual environment, install the
dependencies, and start the Flask development server:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000> in your browser. Stop the server with `Ctrl+C`.

The lexer is the `lexer/` package. Each scanner follows the paper's transition
diagrams state by state.

The syntax analyzer is the `parser/` package, an LL(1) predictive parser
written as one if / elif branch per production, the same way the lexer is
written as one branch per state:

- `parser/grammar.py` is the paper's Context Free Grammar, production by
  production (359 productions).
- `parser/parser.py` is the parser. Its loop has an
  `if top == "<non_terminal>":` branch for every non-terminal, and inside it
  one `elif t == "token":  # PREDICT k` branch per token of each production's
  PREDICT set, setting `prod = k` the way the lexer sets `state`. It skips
  newline, whitespace and comment tokens, stops at the first syntax error,
  and records the parse trace shown in the page.
- `parser/ll1.py` computes the FIRST, FOLLOW and PREDICT sets from the
  grammar, to check the paper's tables. Run `python -m parser.ll1` to print
  them and check the grammar for LL(1) conflicts (there are none).

In the page, **▶ Run Lexer** only tokenizes. **▶ Run Syntax** tokenizes and then
parses; if there are lexical errors, the parser is skipped.
