"""
app.py - the web server for the LIME Lexical Analyzer.

  * Shows the page (templates/index.html).
  * /analyze receives LIME code, runs it through the lexer package, and sends
    back every token (including newline, whitespace, tab, comment and EOF
    tokens, which the page can hide) and every lexical error as JSON.
    With "syntax": true it also runs the LL(1) parser (parser package) on the
    tokens and adds the result under "syntax".
"""

from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import parse

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    lx = Lexer(data.get('code', ''))
    lx.tokenize()

    tokens_payload = [{
        'line': tok.line,
        'col': tok.col,
        'lexeme': tok.lexeme,
        'token': tok.label,          # id1, id2, ... for identifiers
        'token_type': tok.category,
        'final_state': tok.final_state,
    } for tok in lx.tokens]

    errors_payload = [{
        'line': err.line,
        'col': err.col,
        'kind': err.kind,
        'message': err.message,
        'found': err.found,
        'expected': err.expected,
        'lexeme': err.lexeme,
        'state': err.state,
    } for err in lx.errors]

    result = {'tokens': tokens_payload, 'errors': errors_payload}

    # Syntax analysis runs only on a lexically clean program (a bad token
    # stream would only give misleading errors).
    if data.get('syntax'):
        if lx.errors:
            result['syntax'] = {'ran': False, 'errors': []}
        else:
            p = parse(lx.tokens)
            result['syntax'] = {
                'ran': True,
                'steps': len(p.steps),
                'trace': p.trace,
                'errors': [{
                    'line': err.line,
                    'col': err.col,
                    'kind': err.kind,
                    'message': err.message,
                    'found': err.found,
                    'lexeme': err.lexeme,
                    'expected': err.expected_text,
                } for err in p.errors],
            }

    return jsonify(result)


if __name__ == '__main__':
    print("Starting Lime Web App on http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
