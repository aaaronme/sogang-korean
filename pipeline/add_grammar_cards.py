"""Append grammar cards for Student's Book 1A to master_cards.json.

A grammar card is a different shape from a vocabulary card: the front is a
pattern (명이에요/예요), the back is a rule plus two to four worked examples. It
carries `type: "grammar"` and an `examples` array; `build.py` passes both
through and the app renders them specially.

Grammar cards have no audio clip of their own — a pattern is not a speakable
phrase. Their *examples* do, and where an example sentence is already a card in
its own right, this reuses that card's existing clip rather than synthesising a
second identical one.

Idempotent: ids are sha1(tag|pattern), so re-running never mints a new id for a
card that already shipped.
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
    "e97bafd5-f601-49d8-92cd-504b315807ec/scratchpad/out/grammar.json")

VOICE = "Yuna"


def card_id(tag, key):
    return hashlib.sha1(f"{tag}|{key}".encode("utf-8")).hexdigest()[:10]


def example_clip_id(ko):
    """Clip id for an example sentence that isn't already a card."""
    return hashlib.sha1(f"grammar-example|{ko}".encode("utf-8")).hexdigest()[:10]


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
        entries = json.load(f)["grammar"]

    path = os.path.join(HERE, "master_cards.json")
    with open(path, encoding="utf-8") as f:
        master = json.load(f)

    # Any existing card with this exact Korean already has a clip; reuse it.
    clip_for_ko = {}
    for c in master:
        clip_for_ko.setdefault(c["ko"], c["id"])

    existing = {c["id"] for c in master}
    before = len(master)
    to_speak = []
    added = 0

    for e in entries:
        tag = f'Book1A::{e["unit"]}::Grammar'
        cid = card_id(tag, e["pattern"])
        if cid in existing:
            continue
        examples = []
        for eg in e.get("examples", []):
            ko = eg["ko"]
            clip = clip_for_ko.get(ko)
            if not clip:
                clip = example_clip_id(ko)
                to_speak.append((clip, ko))
                clip_for_ko[ko] = clip
            examples.append({"ko": ko, "en": eg["en"], "ja": eg["ja"], "audio": clip})
        master.append({
            "id": cid,
            "ko": e["pattern"],
            "en": e["rule_en"],
            "tags": [tag],
            "ja": e["rule_ja"],
            "type": "grammar",
            "examples": examples,
        })
        existing.add(cid)
        added += 1

    ids = [c["id"] for c in master]
    if len(ids) != len(set(ids)):
        raise SystemExit("ABORT: duplicate card id detected, refusing to write")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"master_cards.json: {before} -> {len(master)} ({added} grammar cards added)")

    reused = sum(len(c.get("examples", [])) for c in master if c.get("type") == "grammar") - len(to_speak)
    print(f"examples: {reused} reused an existing card's clip, {len(to_speak)} need new audio")

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda a: make_audio(*a), to_speak))

    missing = [eg["audio"] for c in master if c.get("type") == "grammar"
               for eg in c.get("examples", [])
               if not os.path.exists(os.path.join(AUDIO, f'{eg["audio"]}.m4a'))]
    if missing:
        raise SystemExit(f"ABORT: {len(missing)} example clips missing: {missing[:5]}")
    print("every grammar example has audio")


if __name__ == "__main__":
    main()
