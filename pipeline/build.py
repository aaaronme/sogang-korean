"""Build the deployed app from master_cards.json + audio/.

Writes three things into the repo root:

  index.html   the app, with every card's text but NO audio bytes
  audio/       one .m4a per card, fetched on demand by id
  sw.js        a service worker that caches the shell and every clip it sees

Audio used to be base64'd inline, which kept the app a single self-contained
file. That stopped being viable at 1259 cards: index.html hit 15.6 MB, and a
student on mobile data paid all of it before seeing a single card. Now the
shell is a few hundred KB and a clip is fetched the first time it is played,
then served from the service-worker cache forever after — so the app still
works offline, but only for the sections someone has actually studied.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
# Clips live in the repo root as audio/, which is both the working store and
# what GitHub Pages serves. There used to be a second copy under pipeline/
# audio_store/; keeping 14 MB of identical bytes twice in one repo bought
# nothing, so the served directory is now the only one.
AUDIO = os.path.join(ROOT, "audio")

with open(os.path.join(HERE, "master_cards.json"), encoding="utf-8") as f:
    master = json.load(f)

cards = []
missing_audio = []
total_audio = 0
for c in master:
    card = {
        "id": c["id"],
        "ko": c["ko"],
        "en": c["en"],
        "ja": c.get("ja", c["en"]),  # fall back to English if a translation is ever missing
        "tags": c["tags"],
    }
    # Optional fields, present only on grammar cards. Passed through rather than
    # hardcoded so a future card kind doesn't need build.py changed again.
    for key in ("type", "examples"):
        if key in c:
            card[key] = c[key]
    cards.append(card)

    # A grammar card has no clip of its own — its pattern isn't a speakable
    # phrase — but each of its examples does.
    if c.get("type") == "grammar":
        for eg in c.get("examples", []):
            if eg.get("audio"):
                src = os.path.join(AUDIO, f'{eg["audio"]}.m4a')
                if not os.path.exists(src):
                    missing_audio.append(eg["audio"])
        continue

    src = os.path.join(AUDIO, f'{c["id"]}.m4a')
    if not os.path.exists(src):
        missing_audio.append(c["id"])

for name in os.listdir(AUDIO):
    if name.endswith(".m4a"):
        total_audio += os.path.getsize(os.path.join(AUDIO, name))

if missing_audio:
    print(f"WARNING: missing audio for {len(missing_audio)} clips: {missing_audio[:5]}")

# --- audio/ ---------------------------------------------------------------
# Delete clips that no longer belong to any card, so retired audio doesn't
# linger in the deploy.
# Must include grammar examples' clip ids, not just card ids — those clips are
# referenced from inside a card rather than being named after one, so a card-id-only
# set would class every example clip as stale and delete it.
wanted = {f'{c["id"]}.m4a' for c in cards}
wanted |= {f'{eg["audio"]}.m4a' for c in cards for eg in c.get("examples", []) if eg.get("audio")}
stale = [n for n in os.listdir(AUDIO) if n.endswith(".m4a") and n not in wanted]
for name in stale:
    os.remove(os.path.join(AUDIO, name))

# --- index.html -----------------------------------------------------------
with open(os.path.join(HERE, "app_template.html"), encoding="utf-8") as f:
    template = f.read()

output = template.replace("__CARDS_JSON__", json.dumps(cards, ensure_ascii=False))
out_path = os.path.join(ROOT, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(output)

# --- sw.js ----------------------------------------------------------------
# The cache name embeds a hash of the shell, so publishing a new build makes
# every client drop the old shell instead of serving a stale app forever.
version = hashlib.sha1(output.encode("utf-8")).hexdigest()[:12]
with open(os.path.join(HERE, "sw_template.js"), encoding="utf-8") as f:
    sw = f.read().replace("__VERSION__", version)
with open(os.path.join(ROOT, "sw.js"), "w", encoding="utf-8") as f:
    f.write(sw)

print(f"index.html : {len(output)/1024/1024:.2f} MB, {len(cards)} cards")
print(f"audio/     : {len(wanted)} clips, {total_audio/1024/1024:.1f} MB "
      f"({len(stale)} stale removed)")
print(f"sw.js      : cache version {version}")
