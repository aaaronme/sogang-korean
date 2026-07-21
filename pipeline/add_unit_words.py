"""Add the Prep/Unit vocabulary taught in the class speaking slides.

Source: the publisher's class decks at koreanteachers.org/ppt/3rd_1/, decks
`1A_P1_S` .. `1A_P4_S` and `1A_1_S` .. `1A_6_S` — 264 slides, read the same way
as `add_slide_words.py` reads the Hangul decks (Toast e-learning packages,
content baked into background JPGs).

What the sweep was for, and what it actually found. The point was to check the
Prep and Unit sections, which were built from photographs of the book, against
a second independent source. Across all ten decks it found **zero
misattributions** — not one card filed under the wrong unit. That negative
result is the valuable part; these additions are a by-product.

Two things the sweep could NOT do, recorded so nobody later mistakes silence
for confirmation:

  - No slide in any of the fourteen decks prints a translation in any
    language. Korean, pictures and the occasional romanization, nothing else.
    So the entire English and Japanese side of the deck remains unattested by
    the publisher. Every gloss here is ours, dictionary-checked only.

  - Each checker agent saw only its own unit's cards, so it flagged as
    "missing" anything carded under a different unit. 64 of 132 flags were
    that artifact — 책 and 우산 sit in 준비 2 and were flagged by 준비 3.
    Everything below is deduplicated against the WHOLE deck, not per unit.

Of the 66 genuinely-new items the sweep surfaced, this cards 42. The 24 left
out, and why:

  - 12 해요-form verbs (공부해요, 일해요, 요리해요 …). We already card 공부하다.
    A conjugated form of a lexeme we teach is a grammar drill, not new
    vocabulary, and the 해요 pattern has its own grammar cards.
  - 8 shop names from a Unit 1 worksheet (옷 가게, 신발 가게, 꽃 가게 …).
    Worksheet scaffolding built from 가게/식당 plus a noun the student already
    knows. Transparent compounds do not need cards.
  - 4 있어요/없어요 drill sentences (컴퓨터 있어요. 시계 없어요. …). Pattern
    substitutions; the pattern is already carded.

A card here can duplicate a word carded elsewhere in the deck, and that is
fine — see the note in `add_hangul_words.py`. 해운대 is already a Unit 6 card;
해운대에 가다 is the phrase the slides drill, and both stay.

Japanese glosses follow the Book1A convention rather than the Hangul one:
furigana in full-width parens after each kanji run, and Korean place names as
hanja plus the Korean reading in katakana (海雲台（ヘウンデ）). Book1A is 96%
furigana'd; the Hangul sections, added 2026-07-21, are only 17% and should be
brought into line separately.

Safe under the post-launch freeze (see README): every card is new, no existing
card's id, tag, Korean or gloss is touched.

Idempotent: ids are sha1(tag|ko).
"""
import hashlib
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

import strip_m4a_padding

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.abspath(os.path.join(HERE, "..", "audio"))
VOICE = "Yuna"


def card_id(tag, ko):
    return hashlib.sha1(f"{tag}|{ko}".encode("utf-8")).hexdigest()[:10]


def make_audio(cid, ko):
    dest = os.path.join(AUDIO, f"{cid}.m4a")
    if os.path.exists(dest):
        return False
    tmp = f"/tmp/say_{cid}.m4a"
    subprocess.run(["say", "-v", VOICE, "-o", tmp, ko], check=True)
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac@22050", "-b", "32000",
                    "-c", "1", tmp, dest], check=True)
    os.remove(tmp)
    strip_m4a_padding.strip(dest)
    return True


def main():
    with open(os.path.join(HERE, "unit_words.json"), encoding="utf-8") as f:
        words = json.load(f)

    path = os.path.join(HERE, "master_cards.json")
    with open(path, encoding="utf-8") as f:
        master = json.load(f)

    before = [dict(c) for c in master]
    existing = {c["id"] for c in master}
    added = []

    for tag, entries in words.items():
        if not any(tag in c["tags"] for c in before):
            raise SystemExit(f"ABORT: unknown tag {tag!r} — refusing to invent a section")
        n = 0
        for ko, en, ja in entries:
            cid = card_id(tag, ko)
            if cid in existing:
                continue
            master.append({"id": cid, "ko": ko, "en": en, "tags": [tag], "ja": ja})
            existing.add(cid)
            added.append((cid, ko))
            n += 1
        print(f"  {tag}: +{n}")

    ids = [c["id"] for c in master]
    if len(ids) != len(set(ids)):
        raise SystemExit("ABORT: duplicate card id detected, refusing to write")

    # The freeze in one assertion: nothing that already shipped may move.
    by_id = {c["id"]: c for c in master}
    for old in before:
        if by_id.get(old["id"]) != old:
            raise SystemExit(f"ABORT: existing card changed or vanished: "
                             f"{old['id']} {old['ko']}")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"master_cards.json: {len(before)} -> {len(master)} ({len(added)} added)")

    with ThreadPoolExecutor(max_workers=8) as pool:
        made = sum(bool(x) for x in pool.map(lambda a: make_audio(*a), added))
    print(f"audio: {made} clips generated")

    missing = [ko for cid, ko in added
               if not os.path.exists(os.path.join(AUDIO, f"{cid}.m4a"))]
    if missing:
        raise SystemExit(f"ABORT: {len(missing)} cards have no audio: {missing[:5]}")
    print("every new card has audio")


if __name__ == "__main__":
    main()
