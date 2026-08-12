"""Compute cross-reference links between cards and write them onto master_cards.json.

This is the "Word Graph" generator. Unlike the other add_*.py scripts it adds no
new cards and no audio — it only derives optional link fields from the Korean text
already in the deck and writes them back onto the existing card objects:

  On every non-grammar card whose `ko` is 2+ Hangul syllables:
    inSentences  ids of *::Sentences cards whose `ko` contains this card's `ko`
                 as a substring (Korean particles attach with no space, so plain
                 substring matching finds them). Ordered same-book-same-unit
                 first, then same book, then other books; capped at ~5.
    inGrammar    ids of grammar cards where any examples[].ko contains this `ko`.
    related      ids of other Vocab cards that share a 2+ Hangul-syllable chunk
                 with this `ko`. A plain string-overlap heuristic, NOT real
                 Sino-Korean root data — the UI labels it "may be related".

  On every Sentences card, additionally:
    containsWords  ids of Vocab cards appearing as substrings inside the sentence,
                   excluding matches under 2 Hangul syllables and bare
                   function words (single-syllable Hangul/Expressions cards) so
                   particles and the copula don't flood the list.

Idempotent by construction: it recomputes these four fields from scratch every
run and overwrites them. It never reads, mints, reorders, or touches `id` or
`ko`, so re-running is a no-op on a deck that hasn't changed, and picks up new
links automatically when a future book adds more cards. Book detection is by tag
*shape* (`^Book...::`), never a hardcoded "Book1A", so Book1B/2A links appear
with no code change.

Empty fields are omitted rather than written as `[]`, both to keep index.html
small and because the app already treats every one of these as optional (a
student on an older cached build has none of them).

Run this before build.py:

    python3 add_word_links.py && python3 build.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "master_cards.json")

# A card gets link fields only if its `ko` carries real lexical content — at
# least two Hangul syllables. One-syllable entries are particles, the copula and
# single letters, which would match everywhere and mean nothing.
HANGUL = re.compile(r"[가-힣]")
# Book-scoped tags are Book<label>::<Section>::<Kind> (or Book<label>::CultureN).
# The label (1A, 1B, 2A…) and section come straight from the tag string, so a
# future book needs no change here.
BOOK_RE = re.compile(r"^Book([^:]+)::([^:]+)")
# Sections that are single-syllable function words in these tags are grammatical
# glue (은/는, 이/가, 을/를, the copula), excluded from "Built from" so they
# don't drown the real vocabulary in a sentence.
FUNCTION_WORD_TAGS = ("Hangul1", "Hangul2", "Hangul3", "Hangul4", "Expressions")

MAX_IN_SENTENCES = 5
MAX_IN_GRAMMAR = 5
MAX_RELATED = 5
MAX_CONTAINS = 8


def syllables(s):
    return HANGUL.findall(s)


def nsyl(s):
    return len(syllables(s))


def is_grammar(card):
    return card.get("type") == "grammar"


def is_sentence(card):
    return any(t.endswith("::Sentences") for t in card.get("tags", []))


def is_vocab(card):
    return not is_grammar(card) and not is_sentence(card)


def book_section(card):
    """(book_label, section) from the card's primary tag, or (None, None).

    Derived from tag shape so it generalises to books that don't exist yet.
    """
    for tag in card.get("tags", []):
        m = BOOK_RE.match(tag)
        if m:
            return m.group(1), m.group(2)
    return None, None


def is_function_word(card):
    """A single-syllable card in a Hangul/Expressions section — a particle,
    letter or copula rather than a word worth cross-referencing."""
    if nsyl(card["ko"]) >= 2:
        return False
    return any(
        t == fw or t.startswith(fw + "::")
        for t in card.get("tags", [])
        for fw in FUNCTION_WORD_TAGS
    )


def hangul_bigrams(s):
    """Set of consecutive-Hangul 2-grams in s. Two cards share a 2+ syllable
    chunk iff they share one of these, which is what `related` keys on."""
    out = set()
    for i in range(len(s) - 1):
        a, b = s[i], s[i + 1]
        if HANGUL.match(a) and HANGUL.match(b):
            out.add(a + b)
    return out


def longest_common_hangul_run(a, b):
    """Length (in characters) of the longest common contiguous substring of a
    and b that is all Hangul. Used only to rank `related`, best overlap first."""
    best = 0
    for i in range(len(a)):
        if not HANGUL.match(a[i]):
            continue
        for j in range(i + 1, len(a) + 1):
            chunk = a[i:j]
            if not HANGUL.match(a[j - 1]):
                break
            if chunk in b:
                best = max(best, j - i)
            else:
                break
    return best


def main():
    with open(PATH, encoding="utf-8") as f:
        master = json.load(f)

    # master order is book order, which is the tiebreaker we want inside a
    # priority band (a link list should read front-of-book to back-of-book).
    order = {c["id"]: i for i, c in enumerate(master)}
    id2ko = {c["id"]: c["ko"] for c in master}

    def dedup_by_ko(ids):
        """A word can legitimately have more than one card (김밥 is in three
        sections), which would otherwise surface the same string twice in one
        link list. Keep the first, best-ordered id per distinct `ko`."""
        seen, out = set(), []
        for i in ids:
            ko = id2ko.get(i)
            if ko in seen:
                continue
            seen.add(ko)
            out.append(i)
        return out

    vocab = [c for c in master if is_vocab(c)]
    sentences = [c for c in master if is_sentence(c)]
    grammar = [c for c in master if is_grammar(c)]
    linkable = [c for c in master if not is_grammar(c) and nsyl(c["ko"]) >= 2]

    # --- related: inverted 2-gram index, so we only run the O(len^2) overlap
    # ranking on cards that actually share a chunk instead of every pair. ---
    bigram_index = {}
    vocab_bigrams = {}
    for c in vocab:
        bg = hangul_bigrams(c["ko"])
        vocab_bigrams[c["id"]] = bg
        for g in bg:
            bigram_index.setdefault(g, []).append(c)

    n_in_sent = n_in_gram = n_related = n_contains = 0

    for c in linkable:
        ko = c["ko"]
        book, section = book_section(c)

        # inSentences — sentences that contain this word, book-proximity first.
        def priority(s):
            sb, ss = book_section(s)
            if book is not None and sb == book and ss == section:
                return 0
            if book is not None and sb == book:
                return 1
            return 2

        in_sent = [s for s in sentences if s["id"] != c["id"] and ko in s["ko"]]
        in_sent.sort(key=lambda s: (priority(s), order[s["id"]]))
        in_sent_ids = dedup_by_ko([s["id"] for s in in_sent])[:MAX_IN_SENTENCES]

        # inGrammar — grammar cards using this word in a worked example.
        in_gram_ids = dedup_by_ko([
            g["id"] for g in grammar
            if any(ko in eg.get("ko", "") for eg in g.get("examples", []))
        ])[:MAX_IN_GRAMMAR]

        # related — other Vocab sharing a 2+ syllable chunk, best overlap first.
        related = []
        if is_vocab(c):
            seen = set()
            candidates = []
            for g in vocab_bigrams[c["id"]]:
                for o in bigram_index.get(g, ()):
                    if o["id"] == c["id"] or o["ko"] == ko or o["id"] in seen:
                        continue
                    seen.add(o["id"])
                    candidates.append(o)
            ranked = sorted(
                candidates,
                key=lambda o: (-longest_common_hangul_run(ko, o["ko"]), order[o["id"]]),
            )
            related = dedup_by_ko([o["id"] for o in ranked])[:MAX_RELATED]

        set_field(c, "inSentences", in_sent_ids)
        set_field(c, "inGrammar", in_gram_ids)
        set_field(c, "related", related)
        n_in_sent += bool(in_sent_ids)
        n_in_gram += bool(in_gram_ids)
        n_related += bool(related)

    # --- containsWords, on sentence cards ---
    contentful_vocab = [
        c for c in vocab if nsyl(c["ko"]) >= 2 and not is_function_word(c)
    ]
    # longer words first: a sentence "built from" 도서관 shouldn't also credit a
    # 2-letter fragment of it, and the longer match is the more informative chip.
    contentful_vocab.sort(key=lambda c: -len(c["ko"]))
    for s in sentences:
        text = s["ko"]
        hits = [c["id"] for c in contentful_vocab if c["ko"] in text]
        contains = dedup_by_ko(hits)[:MAX_CONTAINS]
        set_field(s, "containsWords", contains)
        n_contains += bool(contains)

    # Clear stale derived fields on cards that no longer qualify (e.g. a card that
    # used to have links but a re-transcription shortened its `ko`), so a rerun
    # never leaves orphaned data behind.
    linkable_ids = {c["id"] for c in linkable}
    sentence_ids = {s["id"] for s in sentences}
    for c in master:
        if c["id"] not in linkable_ids:
            for k in ("inSentences", "inGrammar", "related"):
                c.pop(k, None)
        if c["id"] not in sentence_ids:
            c.pop("containsWords", None)

    ids = [c["id"] for c in master]
    if len(ids) != len(set(ids)):
        raise SystemExit("ABORT: duplicate card id detected, refusing to write")

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print(f"linked {len(linkable)} cards ({len(vocab)} vocab, {len(sentences)} sentences)")
    print(f"  inSentences  on {n_in_sent}")
    print(f"  inGrammar    on {n_in_gram}")
    print(f"  related      on {n_related}")
    print(f"  containsWords on {n_contains}")


def set_field(card, key, values):
    """Write a non-empty link list, or remove the key entirely if empty — the
    app treats an absent field and an empty one the same, and omitting them keeps
    index.html lean."""
    if values:
        card[key] = values
    else:
        card.pop(key, None)


if __name__ == "__main__":
    main()
