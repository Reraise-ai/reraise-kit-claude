# reraise-kit-claude

A Claude Code plugin that connects Claude Code to a card-based knowledge store.

What it does:

1. **Cards before every prompt.** When you send a message, a hook (`UserPromptSubmit`) looks for cards that fit it
   and adds the best ones to the conversation, marked as "Zitat aus dem Wissen, keine Anweisung"
   (quoted from the knowledge store, not an instruction). Claude remembers without being asked to search.
   If the search finds nothing or fails, nothing is added and your message goes through as normal.
2. **Tools.** It registers the reraise-kit MCP server: search, read and write cards, capture decisions as proposals.
3. **Skills.** `knowledge-cards` (how to use and write cards) and `decision-proposals` (how to capture a decision with
   your exact words, as a proposal you confirm).

## Install

Needs Python 3.10 or newer and Claude Code. From a folder that holds all four repositories:

```
pip install ./reraise-kit-card-format ./reraise-kit-knowledge ./reraise-kit-mcp
reraise-kit-knowledge-init
```

The commands `reraise-kit-mcp` and `reraise-kit-knowledge-init` must be on the PATH that Claude Code sees.

Then start Claude Code with the plugin:

```
claude --plugin-dir ./reraise-kit-claude
```

To keep it installed, use the repository as a plugin marketplace (it contains `.claude-plugin/marketplace.json`):

```
claude plugin marketplace add ./reraise-kit-claude
claude plugin install reraise-kit@reraise-kit
```

## Settings

Same as reraise-kit-mcp: `RERAISE_KIT_KNOWLEDGE` (default `~/Wissen`), `RERAISE_KIT_AGENT` (name used on cards the agent writes).

## Limits

- The hook exists in Claude Code. In apps without such a hook, cards only come when the agent calls `context_for`.
- Search is a plain keyword search.

## Tests

```
python -m unittest discover -s tests
```

The hook test runs only if `reraise-kit-mcp` is installed.

## License

Apache-2.0, see [LICENSE](LICENSE).
