---
name: decision-proposals
description: Use when the user makes or states a decision ("we do X", "I choose Y", "decided", "lo hacemos", "wir machen"), or when you notice one in the conversation. Captures it as a proposal with the user's exact words, for the user to confirm.
---

# Decision proposals

A decision belongs to the human who made it. You only capture it.

## When the user decides something

1. Call `proposal_create` with:
   - `question`: what was decided, as a question.
   - `proposal`: the choice.
   - `options`: the alternatives, if they were named.
   - `quote`: the user's sentence, **word for word**, copied from their message. Never paraphrase, never invent.
   - `ref`: where it was said, as `claude-code:<session>@<time>` (use today's date and time if you have no session id).
   - `expected_outcome` and `review_date` if the user said what they expect and when to look again.
   - `language`: the language of the user's message.
2. Only with both `quote` and `ref` is the user named as the decider. If you cannot quote the user exactly, leave both
   out: it then stays your proposal.
3. Tell the user in one line: "Saved as proposal B-... for you to confirm." It is not a decision until they confirm it.

## Never

- Never give a decision a number (E-1, E-2, ...). Numbers come only from the decision log tool after confirmation.
- Never write a decision with `card_write`.
- Never capture your own suggestion as the user's decision.
