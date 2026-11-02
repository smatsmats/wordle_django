"""Wordle solver logic, ported from the original wordle.py CLI."""
import re
import string
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
LETTERS = string.ascii_lowercase
MAX_LISTED = 500


@lru_cache(maxsize=None)
def load_words(use_ww=True):
    name = "answers.txt" if use_ww else "words.txt"
    return tuple((DATA / name).read_text().split())


def _clean(value):
    """Reduce free text to a sorted set of lowercase letters."""
    return sorted({c for c in (value or "").lower() if c in LETTERS})


def build_regex(known, notpos):
    """known: 5 single letters or ''; notpos: 5 iterables of excluded letters."""
    parts = []
    for k, nots in zip(known, notpos):
        if k:
            parts.append("[" + k + "]")
        else:
            parts.append("[" + "".join(l for l in LETTERS if l not in nots) + "]")
    return "^" + "".join(parts) + "$"


def solve(use_ww=True, exclude="", include="", known=None, notpos=None,
          no_repeats=False, regex=None):
    exclude, include = _clean(exclude), _clean(include)
    known = [(k or "").lower()[:1] if (k or "").lower()[:1] in LETTERS else ""
             for k in (known or [""] * 5)]
    notpos = [_clean(n) for n in (notpos or [""] * 5)]

    pattern = re.compile(regex) if regex else re.compile(build_regex(known, notpos))

    results = []
    for w in load_words(use_ww):
        if any(x in w for x in exclude):
            continue
        if any(r not in w for r in include):
            continue
        if not pattern.search(w):
            continue
        if no_repeats and len(set(w)) < 5:
            continue
        results.append(w)

    # letter frequency over candidates, ignoring already-known letters
    freqs = {}
    for l in LETTERS:
        if l in include or l in exclude:
            continue
        c = sum(r.count(l) for r in results)
        if c:
            freqs[l] = c
    sorted_f = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    weights = {l: len(sorted_f) - i for i, (l, _) in enumerate(sorted_f)}
    for l in include:
        weights[l] = 0

    scored = sorted(
        ((w, sum(weights.get(l, 0) for l in w)) for w in results),
        key=lambda x: x[1], reverse=True,
    )
    return {
        "count": len(results),
        "words": results[:MAX_LISTED],
        "truncated": len(results) > MAX_LISTED,
        "top_letters": sorted_f[:5],
        "best": scored[:6],
    }
