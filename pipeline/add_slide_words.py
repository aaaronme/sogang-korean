"""Add the Hangul vocabulary taught in the class speaking slides.

Source: the publisher's own class decks at koreanteachers.org/ppt/3rd_1/, decks
`1A_H1_S` .. `1A_H4_S`. Each is a Toast e-learning package: `project.json`
holds the page structure and every slide's content is baked into a background
JPG, so the word lists here were read from the slide images.

Why this exists at all. The four Hangul sections were built from the textbook
and workbook (see `add_hangul_words.py`). These decks are titled 한글N *말하기*
— speaking — and drill the same letters with a substantially different word
set. They are not a corrected version of the book list; they are a parallel
one. Hangul 3 is the clearest case: the book teaches 그네/무지개/해바라기, the
slides teach 카메라/텔레비전/스케이트, and only 11 of our 50 cards appear on
the slides at all. So this script ADDS what the slides teach and removes
nothing — a word absent from the slides is not thereby wrong.

Picture cues decide several glosses, because the slides print no translations
anywhere — only pictures and the occasional romanization. 배 is drawn as a
boat, not a pear; 코 is a nose; 게 is a crab; 해 is the sun; 감 is a persimmon.
Every English and Japanese gloss here is ours, checked against Korean
dictionaries but never against the publisher, who supplies none.

One word is deliberately spelled differently from the slide. H3 slide 58 prints
마시멜로우; the 국립국어원 외래어 표기법 form is 마시멜로, and this cards the
standard spelling. Transcription was not at fault — the slide really does read
마시멜로우 — but a flashcard that drills a nonstandard spelling into a beginner
is worse than one that differs from a single slide by a syllable.

Also fixes one misattribution. 우유, 여우 and 아야 were added to Hangul1 on
2026-07-21 from what looked like a 한글1 review section in the teacher's 한글2
PowerPoint. They are 한글2: the publisher's H2 deck teaches 우유 on slide 6 and
여우 on slide 7, and all three need ㅑ/ㅕ/ㅠ, which 한글1 does not introduce.
Under the freeze the Hangul1 cards cannot be deleted, so they are added to
Hangul2 as well and the Hangul1 copies are left in place. A duplicate is the
lesser fault: those cards have been live since 2026-07-21 and may already
carry review history.

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

# Misfiled on 2026-07-21; see the module docstring.
REFILE_INTO_HANGUL2 = ["우유", "여우", "아야"]


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
    with open(os.path.join(HERE, "slide_words.json"), encoding="utf-8") as f:
        words = json.load(f)

    path = os.path.join(HERE, "master_cards.json")
    with open(path, encoding="utf-8") as f:
        master = json.load(f)

    before = [dict(c) for c in master]
    existing = {c["id"] for c in master}
    by_ko = {}
    for c in master:
        by_ko.setdefault(c["ko"], c)

    added = []

    def add(tag, ko, en, ja):
        cid = card_id(tag, ko)
        if cid in existing:
            return False
        master.append({"id": cid, "ko": ko, "en": en, "tags": [tag], "ja": ja})
        existing.add(cid)
        added.append((cid, ko))
        return True

    for tag in ("Hangul1", "Hangul2", "Hangul3", "Hangul4"):
        n = sum(add(tag, ko, en, ja) for ko, en, ja in words[tag])
        print(f"  {tag}: +{n}")

    # Re-file: reuse the existing card's own glosses so the two copies agree.
    refiled = 0
    for ko in REFILE_INTO_HANGUL2:
        src = by_ko.get(ko)
        if src and add("Hangul2", ko, src["en"], src["ja"]):
            refiled += 1
    print(f"  Hangul2: +{refiled} re-filed from Hangul1 (originals left in place)")

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
