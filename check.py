#!/usr/bin/env python3
"""Re-fetch Anthropic's Claude Cowork page and diff it against facts.json.

No dependencies. Exit 0 when every recorded fact is still present, 1 when one
moved, 2 when the page could not be fetched.

    python3 check.py            # report only
    python3 check.py --save     # also write reports/<date>.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = "claude-cowork-plan-tracker/1.0 (+https://github.com/ArtemShatokhin/claude-cowork-plan-tracker)"


def fetch(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                              "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def normalize(raw: str) -> str:
    body = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", body)
    text = html.unescape(text)
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--save", action="store_true")
    args = ap.parse_args()

    spec = json.loads((HERE / "facts.json").read_text(encoding="utf-8"))
    url = spec["source"]
    print(url)
    try:
        status, raw = fetch(url)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print(f"  fetch failed: {type(exc).__name__}: {exc}")
        return 2
    text = normalize(raw)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    digest = hashlib.sha256(text.encode()).hexdigest()
    print(f"  fetched {stamp}  {len(raw):,} bytes  {len(text.split()):,} words")
    print(f"  text sha256 {digest[:12]}...\n")

    squash = re.sub(r"\s+", "", text)
    changed, unchanged, missing = [], 0, []
    for fact in spec["facts"]:
        needle = fact["text"].replace("\u2019", "'")
        if needle in text or re.sub(r"\s+", "", needle) in squash:
            unchanged += 1
        else:
            missing.append(fact)
    for price in spec.get("prices", []):
        if price in text:
            unchanged += 1
        else:
            missing.append({"id": f"price-{price}", "text": price})

    print(f"  {len(spec['facts']) + len(spec.get('prices', []))} facts checked")
    print(f"  {unchanged} unchanged")
    print(f"  {len(missing)} changed or missing")
    for fact in missing:
        print(f"     {fact['id']}: {fact['text']!r}")
        words = fact["text"].split()[:4]
        if words:
            probe = re.search(r"\s+".join(re.escape(w) for w in words), text)
            if probe:
                start = max(0, probe.start() - 60)
                print(f"       nearby: ...{text[start:probe.start() + 200]}...")

    prices_seen = sorted(set(re.findall(r"\$\d[\d,]*", text)))
    print(f"\n  price tokens seen: {' '.join(prices_seen) or 'none'}")

    if args.save:
        out = HERE / "reports" / f"{stamp[:10]}.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps({
            "source": url, "fetched_at": stamp, "text_sha256": digest,
            "bytes": len(raw), "missing": missing,
            "prices_seen": prices_seen,
        }, indent=2) + "\n", encoding="utf-8")
        print(f"  wrote {out.relative_to(HERE)}")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
