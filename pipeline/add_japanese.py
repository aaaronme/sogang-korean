# Adds Japanese translations to master_cards.json, keyed by the existing
# stable `id` (never by array order) so this can be re-run safely and never
# touches the ids that already have saved student progress against them.
import json

JA = {
    # Hangul1
    "2eee030e27": "きゅうり",
    "cc73c2b7a9": "アヒル",
    "a3071b779e": "額（ひたい）",
    "a1bf92ebb4": "木（き）",
    "e5b7109f3d": "母（はは）",
    "50c3391986": "世界（詩的な言い方）",
    "3b9f2d23f9": "私たちの国",
    "ee969c1f23": "姉（弟から見て）",
    "50c79801fe": "年齢（ねんれい）",
    "8500936151": "子供（こども）",
    # Hangul3
    "fa8530fe14": "ブランコ",
    "c9d1e73b2f": "アリ",
    "74311982d3": "豚（ぶた）",
    "26e97b27e1": "教会（きょうかい）",
    "22f75390a2": "洗顔（せんがん）",
    "1d50a83601": "数える（かぞえる）",
    "a6ced25d6e": "虹（にじ）",
    "c5786cb98c": "ひまわり",
    "87d89bd37a": "会社（かいしゃ）",
    "c2194459ac": "鍵（かぎ）",
    "cb1e84d650": "医者（いしゃ）",
    "5360aed727": "セーター",
    "3fd032109b": "蹴る（ける）／寒い（さむい）",
    "9bbadf2435": "スカート",
    "110ea3deb9": "汽車（きしゃ）",
    "abe3348185": "記者（きしゃ）",
    "b9cc606e1a": "お茶／車（ちゃ／くるま）",
    "e49ee70749": "背（せ）",
    "dd0f1a89dc": "大きい（おおきい）",
    "07d736f954": "コート",
    "06b2d89317": "コーヒー",
    "deca95d5b3": "乗る（のる）",
    "dd2541e2f1": "投手（とうしゅ）",
    "a15c90214b": "Tシャツ",
    "d1691e0fcb": "痛い／具合が悪い",
    "3a77b696ad": "ぶどう",
    "558136bd17": "一つ（ひとつ）",
    "2800d15994": "地下（ちか）",
    "b2a5547280": "歩く（あるく）",
    "31bfb61435": "聞く（きく）",
    "014ad5d030": "スプーン",
    "cc4b6965c0": "虫眼鏡（むしめがね）",
    "4fe0d88661": "畑（はたけ）",
    "3d9bc8a062": "五つ（いつつ）",
    "5db3959475": "歯ブラシ（はブラシ）",
    "f901bc32bb": "きのこ",
    "dbd1d5148a": "箸（はし）",
    "ce360031a2": "昼（ひる）",
    "442dbc217a": "昼寝（ひるね）",
    "916de1c113": "日差し（ひざし）",
    "e6344f6567": "花（はな）",
    # Hangul4
    "960ebc65e1": "時計（とけい）",
    "7a56f5adb6": "りんご",
    "c0a25774b7": "画家（がか）",
    "b8039ba05c": "シャワー",
    "c87d1961ef": "走る（はしる）",
    "4d2341fc90": "ねずみ",
    "e6a9913447": "はさみ",
    "2cda3f7dc6": "高い（たかい）",
    "b6aa6119fa": "書く／苦い／使う",
    "57fb892ae9": "しょっぱい",
    "8133043384": "象（ぞう）",
    "f5498f890a": "ヘアバンド",
    "309044ad4e": "根（ね）",
    "e3f820b59e": "忙しい（いそがしい）",
    "0c62455ea0": "喧嘩する（けんかする）",
    "58fe5a84ca": "偽物（にせもの）",
    # Expressions: To Be
    "e0e0f248aa": "私は医者です。",
    "ef2233e8a0": "私は画家です。",
    "9bfbc5a818": "これは時計です。",
    "f955ffdb23": "これははさみです。",
    # Expressions: Adjectives
    "44c84bce1b": "コーヒーが高いです。",
    "ebc0e38564": "セーターが高いです。",
    "60c4dbeb48": "花がきれいです。（きれい = pretty, new）",
    "b536a4320a": "ぶどうがおいしいです。（おいしい = delicious, new）",
    "debf562004": "この食べ物はしょっぱいです。（食べ物 = food, new）",
    "4f397dfea8": "私は忙しいです。",
    "3e38c99009": "私は具合が悪いです。",
    "f60cbb4156": "背が高いです。（直訳：「背が大きい」）",
    # Expressions: Verbs
    "969714ad2f": "汽車に乗ります。",
    "cf3176e10c": "ブランコに乗ります。",
    "629a49140a": "会社に行きます。",
    "7243806c3e": "教会に行きます。",
    "7efc281b7d": "歩いて行きます。",
    "1d3b80b7a8": "よく聞きます。",
    "368ed4c75a": "私は喧嘩しません。",
    "64d0a0079a": "洗顔をします。",
    # Expressions: Requests
    "580a1497e1": "コーヒーをください。",
    "c77a12e186": "はさみをください。",
    "7e515f6153": "スプーンと箸をください。",
    # Numbers
    "eca74f1000": "二つ（ふたつ、new）",
    "e4e5c4c3bf": "三つ（みっつ、new）",
    "c94b9f1fab": "四つ（よっつ、new）",
    "ce804e32cc": "五歳です。（歳 = age counter, new）",
}

with open("master_cards.json", encoding="utf-8") as f:
    cards = json.load(f)

missing = []
for c in cards:
    if c["id"] in JA:
        c["ja"] = JA[c["id"]]
    else:
        missing.append((c["id"], c["ko"]))

if missing:
    print("MISSING JAPANESE FOR:", missing)
else:
    print(f"All {len(cards)} cards have Japanese translations")

with open("master_cards.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
