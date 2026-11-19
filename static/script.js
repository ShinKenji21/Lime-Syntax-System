/*
 * script.js - everything the LIME Lexical Analyzer page does in the browser.
 *
 * Keeps the line numbers next to the editor, sends the code to the server
 * (/analyze) when "Run" is clicked (lexical, then syntax analysis; both
 * results go to the log), draws the tokens in the table
 * (Line:Col, Lexeme, Token, Token Type) and the lexical errors in the
 * Error / Console Log.  "Clear" empties the editor and both outputs.  The "Show" checkboxes hide or show the newline,
 * whitespace, tab, comment and EOF tokens without asking the server again.
 */

// Tokens from the last run, so the Show checkboxes can redraw instantly.
let cachedTokens = [];
let shownTokenCount = 0;

// Parse trace from the last Run, and which tab is showing.
let cachedTrace = [];
let currentView = 'tokens';
const TRACE_EMPTY_MSG = "Click '▶ Run' to display the parse trace.";

// Which checkbox controls which token names.
const TOGGLE_GROUPS = {
    newline: ['newline'],
    whitespace: ['space'],
    tab: ['tab'],
    comment: ['single_comm', 'multi_comm'],
    EOF: ['EOF'],
};

// --- Line numbers ---------------------------------------------------------------
function updateLineNumbers() {
    const textarea = document.getElementById('code');
    const lines = textarea.value.split('\n').length;
    const lineNumDiv = document.getElementById('line-numbers');
    lineNumDiv.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('<br>');
    document.getElementById('char-count').innerText = `${textarea.value.length} chars`;
    syncScroll();
}

function syncScroll() {
    const textarea = document.getElementById('code');
    document.getElementById('line-numbers').scrollTop = textarea.scrollTop;
}

// --- Token table ----------------------------------------------------------------
// Token names hidden right now (from the unticked Show checkboxes).
function hiddenTokenNames() {
    const hidden = new Set();
    document.querySelectorAll('.show-toggle').forEach(box => {
        if (!box.checked) TOGGLE_GROUPS[box.value].forEach(n => hidden.add(n));
    });
    return hidden;
}

// Makes invisible lexemes readable in the table.
// Invisible lexemes get a grey label instead, e.g. "(space)".
function invisibleLabel(t) {
    switch (t.token) {
        case 'space': return '(space)';
        case 'tab': return '(tab)';
        case 'newline': return '(newline)';
        case 'EOF': return '(EOF)';
        default: return null;
    }
}

function renderTokenTable() {
    const tbody = document.getElementById('token-table');
    const hidden = hiddenTokenNames();
    const shown = cachedTokens.filter(t => !hidden.has(t.token));
    tbody.innerHTML = '';

    shownTokenCount = shown.length;
    updateCount();

    if (shown.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-table-msg">No tokens generated.</td></tr>';
        return;
    }

    shown.forEach(t => {
        const tr = document.createElement('tr');
        const label = invisibleLabel(t);
        const lexemeCell = label
            ? `<span style="color: var(--text-muted)">${label}</span>`
            : `<code style="white-space: pre">${escapeHtml(t.lexeme)}</code>`;
        tr.innerHTML = `
            <td>${t.line}:${t.col}</td>
            <td>${lexemeCell}</td>
            <td><code>${escapeHtml(t.token)}</code></td>
            <td>${escapeHtml(t.token_type)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Parse trace ------------------------------------------------------------------
// Each row is one step of the LL(1) parser: the stack before the step, the
// lookahead token, and what it did (Prod # = the production chosen from the
// PREDICT set, like the lexer's final state number).
function renderTraceTable(emptyMsg) {
    const tbody = document.getElementById('trace-table');
    tbody.innerHTML = '';
    if (cachedTrace.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="empty-table-msg">${escapeHtml(emptyMsg || TRACE_EMPTY_MSG)}</td></tr>`;
        updateCount();
        return;
    }
    cachedTrace.forEach(s => {
        const tr = document.createElement('tr');
        tr.className = `trace-${s.kind}`;
        const look = s.lookahead === '$'
            ? '<code>$</code>'
            : `<code>${escapeHtml(s.lookahead)}</code>` +
              (s.lexeme !== s.lookahead ? ` <span style="color: var(--text-muted)">${escapeHtml(s.lexeme)}</span>` : '') +
              ` <span style="color: var(--text-muted)">(${s.line}:${s.col})</span>`;
        tr.innerHTML = `
            <td>${s.step}</td>
            <td class="trace-stack">${escapeHtml(s.stack)}</td>
            <td>${look}</td>
            <td>${s.production !== null ? s.production : ''}</td>
            <td><code style="white-space: pre-wrap">${escapeHtml(s.action)}</code></td>
        `;
        tbody.appendChild(tr);
    });
    updateCount();
}

// Switches the right pane between the token table and the parse trace.
function showView(view) {
    currentView = view;
    document.getElementById('tokens-view').hidden = view !== 'tokens';
    document.getElementById('trace-view').hidden = view !== 'trace';
    document.querySelectorAll('.tab').forEach(t =>
        t.classList.toggle('active', t.dataset.view === view));
    updateCount();
}

function updateCount() {
    const predicts = cachedTrace.filter(s => s.kind === 'predict').length;
    document.getElementById('token-count').innerText = currentView === 'tokens'
        ? `${shownTokenCount} Tokens`
        : `${cachedTrace.length} Steps (${predicts} Productions)`;
}

// --- Run ------------------------------------------------------------------------------
// One button runs both phases: the lexical analysis, then the syntax analysis.
// The server skips the parser when there are lexical errors.
async function runAnalysis() {
    const code = document.getElementById('code').value;

    const res = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, syntax: true })
    });
    const data = await res.json();

    cachedTokens = data.tokens || [];
    renderTokenTable();

    // The trace belongs to this run only.  The page stays on the tab being viewed.
    cachedTrace = (data.syntax && data.syntax.trace) || [];
    renderTraceTable(data.syntax.ran ? null
        : 'Syntax analysis skipped — fix the lexical errors first.');

    const consoleLog = document.getElementById('console-log');
    const errStatus = document.getElementById('error-status');
    consoleLog.innerHTML = '';

    if (data.errors.length === 0) {
        consoleLog.innerHTML =
            `<div class="log-success">✔ Lexical analysis succeeded — 0 lexical errors. Recognized ${cachedTokens.length} total tokens.</div>`;
        appendSyntaxResult(data.syntax);
        return;
    }

    errStatus.innerText = `Status: ${data.errors.length} Lexical Error(s) — syntax skipped`;
    errStatus.style.color = 'var(--error-red)';

    data.errors.forEach((e, idx) => {
        const card = document.createElement('div');
        card.className = 'log-error-card';
        const state = (e.state !== null && e.state !== undefined) ? ` (stuck at state ${e.state})` : '';
        card.innerHTML = `
            <strong>[Error ${idx + 1}] ${escapeHtml(e.kind)} at ${e.line}:${e.col}${state}</strong><br>
            ${e.lexeme ? `<span>Invalid lexeme: <code>${escapeHtml(e.lexeme)}</code></span><br>` : ''}
            <span>Reason: ${escapeHtml(e.message)}</span><br>
            ${e.expected ? `<span style="color: var(--text-muted)">Expected: ${escapeHtml(e.expected)}</span>` : ''}
        `;
        consoleLog.appendChild(card);
    });

    const note = document.createElement('div');
    note.style.color = 'var(--text-muted)';
    note.innerText = 'Syntax analysis skipped — fix the lexical errors first.';
    consoleLog.appendChild(note);
}

// Adds the parser's result to the Error / Console Log and sets the status.
function appendSyntaxResult(syntax) {
    const consoleLog = document.getElementById('console-log');
    const errStatus = document.getElementById('error-status');

    if (syntax.errors.length === 0) {
        errStatus.innerText = 'Status: OK (0 Errors) — Syntax valid';
        errStatus.style.color = 'var(--primary-lime)';
        const ok = document.createElement('div');
        ok.className = 'log-success';
        ok.innerText = `✔ Syntax analysis succeeded — 0 syntax errors. ` +
            `The program follows the LIME grammar (${syntax.steps} productions applied).`;
        consoleLog.appendChild(ok);
        return;
    }

    errStatus.innerText = `Status: ${syntax.errors.length} Syntax Error(s)`;
    errStatus.style.color = 'var(--error-red)';
    syntax.errors.forEach((e, idx) => {
        const card = document.createElement('div');
        card.className = 'log-error-card';
        card.innerHTML = `
            <strong>[Syntax Error ${idx + 1}] ${escapeHtml(e.kind)} at ${e.line}:${e.col}</strong><br>
            <span>Reason: ${escapeHtml(e.message)}</span><br>
            <span style="color: var(--text-muted)">Expected: ${escapeHtml(e.expected)}</span>
        `;
        consoleLog.appendChild(card);
    });
}

// --- Clear ------------------------------------------------------------------------
// Empties the editor and puts the token table and the log back to "ready".
function clearEditor() {
    cachedTokens = [];
    shownTokenCount = 0;
    cachedTrace = [];
    renderTraceTable();
    showView('tokens');
    document.getElementById('code').value = '';
    updateLineNumbers();
    document.getElementById('token-table').innerHTML =
        '<tr><td colspan="4" class="empty-table-msg">Click \'▶ Run\' to display generated tokens.</td></tr>';
    document.getElementById('token-count').innerText = '0 Tokens';
    document.getElementById('console-log').innerHTML =
        '<span class="log-success">System initialized. Ready to analyze LIME code.</span>';
    const errStatus = document.getElementById('error-status');
    errStatus.innerText = 'Status: Ready';
    errStatus.style.color = '';
    document.getElementById('code').focus();
}

// --- Helper -----------------------------------------------------------------------
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// --- Page start-up -----------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('code');
    textarea.addEventListener('scroll', syncScroll);
    textarea.addEventListener('input', updateLineNumbers);

    // Tab key types a tab character instead of moving focus out of the editor.
    textarea.addEventListener('keydown', e => {
        if (e.key !== 'Tab' || e.ctrlKey || e.altKey || e.metaKey) return;
        e.preventDefault();
        textarea.setRangeText('\t', textarea.selectionStart, textarea.selectionEnd, 'end');
        updateLineNumbers();
    });

    document.querySelectorAll('.show-toggle').forEach(box => {
        box.addEventListener('change', renderTokenTable);
    });

    updateLineNumbers();
});
