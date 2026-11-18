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

The syntax analyzer is the `parser/` package, an LL(1) table-driven
(predictive) parser:

- `parser/grammar.py` is the paper's Context Free Grammar, production by
  production (359 productions).
- `parser/ll1.py` computes the FIRST, FOLLOW and PREDICT sets from that
  grammar and builds the parse table. Run `python -m parser.ll1` to print the
  sets and check the grammar for LL(1) conflicts (there are none).
- `parser/parser.py` runs the stack-based parser over the lexer's tokens
  (newline, whitespace and comment tokens are skipped) and reports the first
  syntax error with every token that was expected there.

In the page, **▶ Run Lexer** only tokenizes. **▶ Run Syntax** tokenizes and then
parses; if there are lexical errors, the parser is skipped.
