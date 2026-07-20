import json, base64, os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "master_cards.json"), encoding="utf-8") as f:
    master = json.load(f)

cards = []
missing_audio = []
for c in master:
    audio_path = os.path.join(HERE, "audio_store", f'{c["id"]}.m4a')
    if not os.path.exists(audio_path):
        missing_audio.append(c["id"])
        audio_b64 = ""
    else:
        with open(audio_path, "rb") as af:
            audio_b64 = base64.b64encode(af.read()).decode("ascii")
    cards.append({
        "id": c["id"],
        "ko": c["ko"],
        "en": c["en"],
        "ja": c.get("ja", c["en"]),  # fall back to English if a translation is ever missing
        "tags": c["tags"],
        "audio": audio_b64,
    })

if missing_audio:
    print(f"WARNING: missing audio for {len(missing_audio)} cards: {missing_audio}")

with open(os.path.join(HERE, "..", "app_template.html"), encoding="utf-8") as f:
    template = f.read()

output = template.replace("__CARDS_JSON__", json.dumps(cards, ensure_ascii=False))

out_path = os.path.join(HERE, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Built {out_path}: {len(cards)} cards, {len(output)/1024/1024:.2f} MB")
