"""Append Culture Corner cards (문화 1-4) to master_cards.json.

Source: 서강한국어 STUDENT'S BOOK 1A (3rd ed., Hawoo) pp.56-57, 94-95, 132-133,
170-171, transcribed from photographs.

Unlike the teaching units these are one section each rather than a vocab/
sentences pair — a Culture Corner is two pages and splitting it would produce
sections of three cards. Culture 1 in particular has no sentences at all: the
spread contains no finite verb, only holiday names, hotlines and app labels.

There is no handbook word list covering these pages, so the English is ours
except where the book prints its own, which the transcription preserved.

Idempotent: ids are sha1(tag|ko).
"""
import hashlib
import json
import os
import subprocess

import strip_m4a_padding

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.abspath(os.path.join(HERE, "..", "audio"))
SRC = os.path.join(
    "/private/tmp/claude-501/-Users-aaron-sogang-korean",
    "e97bafd5-f601-49d8-92cd-504b315807ec/scratchpad/out/culture.json")

VOICE = "Yuna"
SECTIONS = ["Culture1", "Culture2", "Culture3", "Culture4"]


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
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)

    path = os.path.join(HERE, "master_cards.json")
    with open(path, encoding="utf-8") as f:
        master = json.load(f)
    existing = {c["id"] for c in master}
    before = len(master)

    # Group by section so cards land in book order rather than vocab-then-sentences
    # across the whole file.
    by_section = {s: [] for s in SECTIONS}
    for kind in ("vocab", "sentences"):
        for e in data.get(kind, []):
            sec = e.get("section")
            if sec in by_section:
                by_section[sec].append(e)

    added = []
    for sec in SECTIONS:
        tag = f"Book1A::{sec}"
        seen = set()
        for e in by_section[sec]:
            ko = e.get("ko", "").strip()
            en = e.get("en", "").strip()
            ja = e.get("ja", "").strip()
            if not (ko and en and ja) or ko in seen:
                continue
            seen.add(ko)
            if en[0].islower():
                en = en[0].upper() + en[1:]
            cid = card_id(tag, ko)
            if cid in existing:
                continue
            master.append({"id": cid, "ko": ko, "en": en, "tags": [tag], "ja": ja})
            existing.add(cid)
            added.append((cid, ko))
        print(f"  {tag}: {len(by_section[sec])} entries transcribed")

    ids = [c["id"] for c in master]
    if len(ids) != len(set(ids)):
        raise SystemExit("ABORT: duplicate card id detected, refusing to write")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"master_cards.json: {before} -> {len(master)} ({len(added)} added)")

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as pool:
        made = sum(bool(x) for x in pool.map(lambda a: make_audio(*a), added))
    print(f"audio: {made} clips generated")

    missing = [cid for cid, _ in added
               if not os.path.exists(os.path.join(AUDIO, f"{cid}.m4a"))]
    if missing:
        raise SystemExit(f"ABORT: {len(missing)} cards have no audio")
    print("every new card has audio")


if __name__ == "__main__":
    main()
