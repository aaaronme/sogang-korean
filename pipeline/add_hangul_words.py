"""Fill the gaps in the Hangul alphabet sections.

Source: the four class PowerPoints 초급1A_한글1..4 (박지연 선생님), which are the
materials the course actually teaches from. Unlike the rest of the pipeline
these are not photographs, so the word lists here are transcribed from the
slide scans rather than from the book — the workbook page reproduced on 한글2
slide 17 ("한글 2과 / Reading", workbook p.9, keyed to Student's Book p.18) is
the authoritative list for Hangul 2.

Three gaps, in order of size:

  Hangul2  did not exist at all. It teaches the plain consonants
           ㄱㄷㅂㅅㅈ and the five basic 받침 sounds, so the deck jumped
           from bare vowels (Hangul 1) straight to diphthongs (Hangul 3).

  Hangul1  had only the ten words from the 받아쓰기 dictation slide. The
           lesson's other exercise — the card-matching grid, which appears
           both in the 한글1 deck and again as review in 한글3 — has eighteen
           more, and the Student's Book reading page adds 우유/여우/아야/이/오.

  Hangul3  had only the [t]-final 받침 words. The workbook page on slides
           49-50 also drills [p]-finals (집 숲 잎) and [k]-finals (학교 부엌
           낚시), which were missing entirely. Plus 자다, the other half of
           the 자다/차다 minimal pair that teaches ㅈ against ㅊ.

Words the slides contain but this deliberately does NOT card:

  - bare drill syllables (카, 타, 파, 하) and minimal-pair sets (곰/공,
    반/밤, 문/물). They train an ear for one contrast; as flashcards they are
    just noise.
  - 히읗, which is the *name* of the letter ㅎ rather than a word.
  - the 한글3 bingo board, which mixes in vocabulary from much later units
    (교실, 안경, 수영장, 아이돌) that the student has not met yet.
  - anything already carded in another Hangul section. 우유 appears in both the
    한글1 reading page and the 한글2 word list and is carded in Hangul1; 의사
    appears in both 한글2 and 한글3 and stays in Hangul3, where it already
    shipped — under the freeze it cannot be moved to the lesson that
    introduces it.

That last rule is scoped to the Hangul sections on purpose. Deck-wide, a word
carded in more than one section is normal and pre-existing: 129 words were
already in that position before this script ran (칫솔 is in two Prep units,
김밥 in three sections), because a card belongs to the lesson that teaches it
and lessons genuinely re-teach words. Roughly 23 of the words added here also
exist as a Book1A card. That is the same pattern, not a new bug — but it does
mean a student with everything switched on meets 앞 and 공 twice, once as an
alphabet drill and once as unit vocabulary. The duplicate clip is a few hundred
bytes; deduplicating the cards would mean deleting one, which the freeze
forbids.

Safe under the post-launch freeze (see README): every card here is new, no
existing card's id, tag or Korean is touched, and Hangul2 is appended to
TAG_ORDER's *display* order only.

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
    with open(os.path.join(HERE, "hangul_words.json"), encoding="utf-8") as f:
        words = json.load(f)

    path = os.path.join(HERE, "master_cards.json")
    with open(path, encoding="utf-8") as f:
        master = json.load(f)

    before = [dict(c) for c in master]
    existing = {c["id"] for c in master}
    # A word already carded in any Hangul section stays where it is; the point
    # is one card per word, not one card per appearance.
    carded = {c["ko"] for c in master if any(t.startswith("Hangul") for t in c["tags"])}

    added = []
    for tag in ("Hangul1", "Hangul2", "Hangul3"):
        skipped, new = [], 0
        for ko, en, ja in words[tag]:
            if ko in carded:
                skipped.append(ko)
                continue
            cid = card_id(tag, ko)
            if cid in existing:
                continue
            master.append({"id": cid, "ko": ko, "en": en, "tags": [tag], "ja": ja})
            existing.add(cid)
            carded.add(ko)
            added.append((cid, ko))
            new += 1
        note = f" (skipped {', '.join(skipped)} — already carded)" if skipped else ""
        print(f"  {tag}: +{new}{note}")

    ids = [c["id"] for c in master]
    if len(ids) != len(set(ids)):
        raise SystemExit("ABORT: duplicate card id detected, refusing to write")

    # The freeze in one assertion: nothing that already shipped may move.
    by_id = {c["id"]: c for c in master}
    for old in before:
        now = by_id.get(old["id"])
        if now != old:
            raise SystemExit(f"ABORT: existing card changed or vanished: {old['id']} {old['ko']}")

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
