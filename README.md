# claude-cowork-plan-tracker

Kortix is open source. This repository keeps a dated record of what Anthropic's Claude Cowork page says about plans, limits and where the work runs, plus a script that re-fetches the page and tells you which of those sentences changed.

It exists because comparison pages rot silently. A page that quoted "Claude Cowork consumes limits faster than Chat" was correct on the day it was written and wrong a month later when Anthropic rewrote the copy, and nobody noticed until a reader did. A quote with a date is a fact; the same quote without one is a liability.

## The record as of 21 October 2026

Source: <https://claude.com/product/cowork>, fetched 2026-10-21.

**Plans and prices on the Cowork page**

| Plan | What the page says | Price shown |
|---|---|---|
| Pro | "Claude Cowork is included in your Pro plan." | $17 |
| Max 5x | "Claude Cowork is included in your Max plan." | $100 |
| Max 20x | "Even more Claude Cowork included in your Max plan." | $200 |
| Team | "Claude Cowork and the Slack connector are included in your Team plan standard and premium seats." | $20 |
| Enterprise | "Claude Cowork is included in your Enterprise plan." | none shown |

**Availability**

- "Available in Pro, Max, and Team plans automatically. Enterprise plans can opt in."
- "Usage limits (opens in new tab) apply." appears under the Max and Enterprise blocks.
- "Prices shown don't include applicable tax. Price and plans are subject to change at Anthropic's discretion."

**Where the work runs**

- "Claude Cowork runs on web, desktop, and mobile and is the same Claude, wherever you work."
- "Close your laptop, it keeps going."
- "Start a task from your phone, and Claude keeps working in the cloud even when your laptop is closed."
- "Use a Claude account or your own cloud provider: Access Claude through Amazon Bedrock, Gemini Enterprise Agent Platform, or Microsoft Foundry."

The last line is the one that moves most often. It read "Amazon Bedrock, Google Cloud, or Microsoft Foundry" earlier in 2026, and pages that copied it verbatim are now quoting a product name Anthropic no longer prints.

## Run the check

```sh
python3 check.py                 # fetch, compare, print a report
python3 check.py --save          # also write reports/<date>.json
```

```
$ python3 check.py
https://claude.com/product/cowork
  fetched 2026-10-21T04:12:32Z  1,310,162 bytes  2,889 words
  text sha256 d3488005643f...

  22 facts checked
  22 unchanged
  0 changed or missing

  price tokens seen: $100 $17 $20 $200
```

Exit code is 0 when every recorded fact is still on the page, 1 when one moved, and 2 when the page could not be fetched. Before a fact is reported as moved the script retries it with whitespace removed, so a tag placed inside a sentence is not mistaken for a rewording. A moved fact is not automatically wrong in your copy: it means a human has to read the current sentence and decide.

## Why this matters for the buying decision

Cowork's plans are seat subscriptions whose usage limits are drawn from the same allowance as chat, and Anthropic reserves the right to change both. A team pricing agent work for a year cannot read its unit cost off that page. The alternative worth comparing against is a platform whose model layer takes a key you hold: Kortix's gateway calls your provider, charges no credits for a custom endpoint, and applies budgets, logs, access rules and routing per project ([Kortix's model documentation](https://kortix.com/docs/project/models)).

[Kortix on GitHub](https://github.com/kortix-ai/suna) · [kortix.com](https://kortix.com) · companion: [Claude Cowork pricing, checked](https://opensourceclaudecowork.com/claude-cowork-pricing).
