"""Append Student's Book 1A cards to master_cards.json.

Covers 준비1과-준비4과 and 1과-6과.

Source: 서강한국어 STUDENT'S BOOK 1A (3rd ed., Hawoo) pp.16-167, transcribed from
photographs of the physical book, with English glosses taken from the companion
문법·단어 참고서 (Grammar and Vocabulary Handbook 1A, English edition) pp.36-47.

Reads the per-unit JSON produced by the transcription pass (see UNITS below) and
appends any card not already present. Idempotent: ids are sha1(tag|ko), so
re-running never invents a new id for a card that already shipped.

Naming follows the book's own English Table of Contents — 준비n과 is
"Preparatory Unit n" and n과 is "Unit n". They are different units, which is why
PrepUnit4 and Unit1 can both exist. See pipeline/README.md.
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys

import strip_m4a_padding

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/private/tmp/claude-501/-Users-aaron-sogang-korean/e97bafd5-f601-49d8-92cd-504b315807ec/scratchpad/out"

# json basename -> tag stem, in book order
UNITS = [
    ("prepunit1.json", "Book1A::PrepUnit1"),
    ("prepunit2.json", "Book1A::PrepUnit2"),
    ("prepunit3.json", "Book1A::PrepUnit3"),
    ("prepunit4.json", "Book1A::PrepUnit4"),
    ("unit1.json", "Book1A::Unit1"),
    ("unit2.json", "Book1A::Unit2"),
    ("unit3.json", "Book1A::Unit3"),
    ("unit4.json", "Book1A::Unit4"),
    ("unit5.json", "Book1A::Unit5"),
    ("unit6.json", "Book1A::Unit6"),
]

VOICE = "Yuna"  # same voice as the existing cards; a mid-deck voice change is jarring


def card_id(tag, ko):
    """Stable id from (tag, ko). Never recomputed for a card that already shipped."""
    return hashlib.sha1(f"{tag}|{ko}".encode("utf-8")).hexdigest()[:10]


def normalise(ko, en, ja):
    """Match the house style of the cards already shipped.

    The transcription pass is split across one worker per unit, so small style
    drifts (lowercase glosses, 。 on a question) are inevitable and are cheaper to
    fix mechanically here than to police in seven separate prompts.
    """
    if en and en[0].islower():
        en = en[0].upper() + en[1:]
    # A question in Korean gets a question mark in Japanese too.
    if ko.endswith("?") and ja.endswith("。"):
        ja = ja[:-1] + "？"
    return ko, en, ja


def collect():
    """Read the per-unit transcriptions into (tag, ko, en, ja) tuples, in book order."""
    out = []
    for fname, stem in UNITS:
        path = os.path.join(SRC, fname)
        if not os.path.exists(path):
            print(f"  ! {fname} missing, skipping")
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for kind, tag in (("vocab", f"{stem}::Vocab"), ("sentences", f"{stem}::Sentences")):
            seen = set()
            for e in data.get(kind, []):
                ko, en, ja = normalise(e.get("ko", "").strip(), e.get("en", "").strip(), e.get("ja", "").strip())
                if not (ko and en and ja):
                    print(f"  ! {fname} {kind}: incomplete entry {e!r}, skipping")
                    continue
                if ko in seen:  # the same word can be printed twice within one unit
                    continue
                seen.add(ko)
                out.append((tag, ko, en, ja))
        print(f"  {stem}: {len(data.get('vocab', []))} vocab, {len(data.get('sentences', []))} sentences")
    return out


def make_audio(cid, ko):
    """say -> AAC -> strip padding.

    All three steps matter. `say` writes uncompressed PCM (~8x too big), and
    afconvert then pads the header to a 4 KB boundary (~a third of a short clip).
    Skipping either leaves bytes that every student downloads.
    """
    dest = os.path.join(HERE, "..", "audio", f"{cid}.m4a")
    if os.path.exists(dest):
        return False
    tmp = f"/tmp/say_{cid}.m4a"
    subprocess.run(["say", "-v", VOICE, "-o", tmp, ko], check=True)
    subprocess.run(
        ["afconvert", "-f", "m4af", "-d", "aac@22050", "-b", "32000", "-c", "1", tmp, dest],
        check=True,
    )
    os.remove(tmp)
    strip_m4a_padding.strip(dest)
    return True


def main():
    cards = collect()
    if not cards:
        raise SystemExit("ABORT: no transcriptions found, nothing to do")

    path = os.path.join(HERE, "master_cards.json")
    with open(path, encoding="utf-8") as f:
        master = json.load(f)

    existing = {c["id"] for c in master}
    before = len(master)
    added = []
    for tag, ko, en, ja in cards:
        cid = card_id(tag, ko)
        if cid in existing:
            continue
        master.append({"id": cid, "ko": ko, "en": en, "tags": [tag], "ja": ja})
        existing.add(cid)
        added.append((cid, ko))

    # An id collision against a previously shipped card would silently rewrite a
    # student's progress onto the wrong card, so fail loudly instead.
    ids = [c["id"] for c in master]
    if len(ids) != len(set(ids)):
        raise SystemExit("ABORT: duplicate card id detected, refusing to write")

    # Ids come from the exact Korean string, so a re-transcription that differs by
    # one space or one comma silently becomes a *second* card for the same phrase
    # rather than matching the one already shipped. Exact-match dedup can't see
    # that; this can. Report rather than abort — the book does legitimately print
    # e.g. 학생 and 학생. separately — but these are worth eyeballing.
    def squash(s):
        return re.sub(r"[\s.,?!·]", "", s)

    by_tag = collections.defaultdict(dict)
    for c in master:
        by_tag[c["tags"][0]].setdefault(squash(c["ko"]), []).append(c["ko"])
    near = [(tag, variants) for tag, groups in by_tag.items()
            for variants in groups.values() if len(set(variants)) > 1]
    if near:
        print(f"\nNOTE: {len(near)} near-duplicate string(s) within a section — "
              f"these are separate cards, check they should be:")
        for tag, variants in near[:15]:
            print(f"  {tag.split('::')[-2]}: {sorted(set(variants))}")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"\nmaster_cards.json: {before} -> {len(master)} ({len(added)} added)")

    # say+afconvert is ~1s per clip and entirely I/O-bound on the TTS engine, so
    # a thread pool turns half an hour into a couple of minutes.
    from concurrent.futures import ThreadPoolExecutor
    made = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        for i, ok in enumerate(pool.map(lambda a: make_audio(*a), added), 1):
            made += bool(ok)
            if i % 200 == 0:
                print(f"  audio {i}/{len(added)}")
    print(f"audio: {made} clips generated")

    missing = [c["id"] for c in master
               if not os.path.exists(os.path.join(HERE, "..", "audio", f'{c["id"]}.m4a'))]
    if missing:
        raise SystemExit(f"ABORT: {len(missing)} cards have no audio: {missing[:5]}")
    print("every card has audio")


if __name__ == "__main__":
    main()
