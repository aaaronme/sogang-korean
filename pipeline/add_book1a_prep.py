"""Append Student's Book 1A preparatory-unit cards to master_cards.json.

Source: 서강한국어 STUDENT'S BOOK 1A (3rd ed., Hawoo) pp.16-45, cross-checked
against the companion 문법·단어 참고서 (Grammar and Vocabulary Handbook 1A,
English edition) pp.36-38, which is where the English glosses come from.

Idempotent: ids are derived from (tag, ko) so re-running never invents a new id
for a card that already shipped, and entries already present are skipped.
Japanese glosses are written here by hand — the handbook we photographed is the
English edition.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

P1V = "Book1A::Prep1::Vocab"
P1S = "Book1A::Prep1::Sentences"
P2V = "Book1A::Prep2::Vocab"
P2S = "Book1A::Prep2::Sentences"
P3V = "Book1A::Prep3::Vocab"
P3S = "Book1A::Prep3::Sentences"

# (tag, ko, en, ja)
CARDS = [
    # ---- 준비 1 반갑습니다 (pp.16-25) · 어휘: 국적 p.18, 직업 p.19 ----
    (P1V, "미국", "United States", "アメリカ"),
    (P1V, "한국", "Korea", "韓国（かんこく）"),
    (P1V, "중국", "China", "中国（ちゅうごく）"),
    (P1V, "태국", "Thailand", "タイ"),
    (P1V, "일본", "Japan", "日本（にほん）"),
    (P1V, "독일", "Germany", "ドイツ"),
    (P1V, "베트남", "Vietnam", "ベトナム"),
    (P1V, "프랑스", "France", "フランス"),
    (P1V, "몽골", "Mongolia", "モンゴル"),
    (P1V, "브라질", "Brazil", "ブラジル"),
    (P1V, "학생", "Student", "学生（がくせい）"),
    (P1V, "선생님", "Teacher", "先生（せんせい）"),
    (P1V, "회사원", "Office worker", "会社員（かいしゃいん）"),
    (P1V, "의사", "Doctor", "医者（いしゃ）"),
    (P1V, "간호사", "Nurse", "看護師（かんごし）"),
    (P1V, "요리사", "Cook", "料理人（りょうりにん）"),
    (P1V, "가수", "Singer", "歌手（かしゅ）"),
    (P1V, "배우", "Actor", "俳優（はいゆう）"),
    (P1V, "작가", "Writer, artist", "作家（さっか）"),
    (P1V, "패션 디자이너", "Fashion designer", "ファッションデザイナー"),
    (P1V, "군인", "Soldier", "軍人（ぐんじん）"),
    (P1V, "경찰", "Police officer", "警察官（けいさつかん）"),
    (P1V, "일본어 선생님", "Japanese language teacher", "日本語（にほんご）の先生"),
    (P1V, "가이드", "Tour guide", "ガイド"),
    (P1V, "프로그래머", "Programmer", "プログラマー"),
    (P1V, "운동", "Exercise", "運動（うんどう）"),
    (P1V, "드라마", "TV drama", "ドラマ"),
    (P1V, "공부", "Studying", "勉強（べんきょう）"),
    # ---- 준비 1 · 대화1 p.20, 대화2 p.21, 문법 p.18, 읽고 말하기 p.23 ----
    (P1S, "안녕하세요? 미나예요.", "Hello? I'm Mina.", "こんにちは。ミナです。"),
    (P1S, "이름이 뭐예요?", "What's your name?", "名前（なまえ）は何（なん）ですか？"),
    (P1S, "앤디예요.", "I'm Andy.", "アンディです。"),
    (P1S, "앤디 씨, 어느 나라 사람이에요?", "Andy, what country are you from?",
     "アンディさん、どこの国（くに）の人（ひと）ですか？"),
    (P1S, "저는 미국 사람이에요.", "I'm American.", "私（わたし）はアメリカ人（じん）です。"),
    (P1S, "아, 그래요? 반갑습니다.", "Oh, really? Nice to meet you.",
     "あ、そうですか？お会（あ）いできてうれしいです。"),
    (P1S, "안녕하세요? 수잔이에요.", "Hello? I'm Susan.", "こんにちは。スーザンです。"),
    (P1S, "수잔 씨, 안녕하세요?", "Hello, Susan.", "スーザンさん、こんにちは。"),
    (P1S, "저는 앤디예요.", "I'm Andy.", "私（わたし）はアンディです。"),
    (P1S, "앤디 씨는 무슨 일을 하세요?", "Andy, what work do you do?",
     "アンディさんは何（なん）のお仕事（しごと）をされていますか？"),
    (P1S, "학생이에요.", "I'm a student.", "学生（がくせい）です。"),
    (P1S, "이분이 누구예요?", "Who is this?", "この方（かた）はどなたですか？"),
    (P1S, "가브리엘 씨예요.", "This is Gabriel.", "ガブリエルさんです。"),
    (P1S, "만나서 반갑습니다.", "It's nice to meet you.", "お会（あ）いできてうれしいです。"),
    (P1S, "좋아해요.", "I like it.", "好（す）きです。"),

    # ---- 준비 2 한국어 책이에요 (pp.26-35) · 어휘: 사물 pp.28-29 ----
    (P2V, "책", "Book", "本（ほん）"),
    (P2V, "공책", "Notebook", "ノート"),
    (P2V, "필통", "Pencil case", "筆箱（ふでばこ）"),
    (P2V, "연필", "Pencil", "鉛筆（えんぴつ）"),
    (P2V, "샤프", "Mechanical pencil", "シャープペンシル"),
    (P2V, "볼펜", "Ballpoint pen", "ボールペン"),
    (P2V, "지우개", "Eraser", "消（け）しゴム"),
    (P2V, "수정 테이프", "Correction tape", "修正（しゅうせい）テープ"),
    (P2V, "가위", "Scissors", "はさみ"),
    (P2V, "가방", "Bag", "かばん"),
    (P2V, "우산", "Umbrella", "傘（かさ）"),
    (P2V, "달력", "Calendar", "カレンダー"),
    (P2V, "책상", "Desk", "机（つくえ）"),
    (P2V, "의자", "Chair", "椅子（いす）"),
    (P2V, "시계", "Clock", "時計（とけい）"),
    (P2V, "노트북", "Laptop computer", "ノートパソコン"),
    (P2V, "텔레비전", "Television", "テレビ"),
    (P2V, "에어컨", "Air conditioner", "エアコン"),
    # 듣고 말하기 p.33
    (P2V, "거울", "Mirror", "鏡（かがみ）"),
    (P2V, "비누", "Soap", "石（せっ）けん"),
    (P2V, "수건", "Towel", "タオル"),
    (P2V, "휴지", "Toilet paper", "トイレットペーパー"),
    (P2V, "칫솔", "Toothbrush", "歯（は）ブラシ"),
    (P2V, "치약", "Toothpaste", "歯磨（はみが）き粉（こ）"),
    (P2V, "접시", "Dish, plate", "皿（さら）"),
    (P2V, "컵", "Cup", "コップ"),
    (P2V, "숟가락", "Spoon", "スプーン"),
    (P2V, "젓가락", "Chopsticks", "箸（はし）"),
    # 대화 어휘
    (P2V, "충전기", "Charger", "充電器（じゅうでんき）"),
    (P2V, "핸드폰", "Mobile phone", "携帯電話（けいたいでんわ）"),
    (P2V, "그럼", "Then, in that case", "それでは"),
    # ---- 준비 2 · 문법 pp.28-29, 대화1 p.30, 대화2 p.31, 듣고 말하기 p.33 ----
    (P2S, "이게 뭐예요?", "What's this?", "これは何（なん）ですか？"),
    (P2S, "연필이에요.", "It's a pencil.", "鉛筆（えんぴつ）です。"),
    (P2S, "그럼 저게 뭐예요?", "Then what's that?", "では、あれは何（なん）ですか？"),
    (P2S, "시계예요.", "It's a clock.", "時計（とけい）です。"),
    (P2S, "저게 뭐예요?", "What's that?", "あれは何（なん）ですか？"),
    (P2S, "책이에요.", "It's a book.", "本（ほん）です。"),
    (P2S, "가방이에요.", "It's a bag.", "かばんです。"),
    (P2S, "우산 누구 거예요?", "Whose umbrella is this?", "この傘（かさ）は誰（だれ）のですか？"),
    (P2S, "제 거예요.", "It's mine.", "私（わたし）のです。"),
    (P2S, "여기 있어요.", "Here you go.", "どうぞ。"),
    (P2S, "고마워요.", "Thanks.", "ありがとうございます。"),
    (P2S, "아니에요.", "Don't mention it.", "いいえ、どういたしまして。"),
    (P2S, "이게 한국어로 뭐예요?", "What's this in Korean?",
     "これは韓国語（かんこくご）で何（なん）ですか？"),
    (P2S, "사라 씨 거예요.", "It's Sarah's.", "サラさんのです。"),

    # ---- 준비 3 핸드폰 있어요? (pp.36-45) · 어휘: 숫자① p.39 ----
    (P3V, "공", "Zero (0)", "ゼロ（0）"),
    (P3V, "일", "One (1)", "1（いち）"),
    (P3V, "이", "Two (2)", "2（に）"),
    (P3V, "삼", "Three (3)", "3（さん）"),
    (P3V, "사", "Four (4)", "4（よん）"),
    (P3V, "오", "Five (5)", "5（ご）"),
    (P3V, "육", "Six (6)", "6（ろく）"),
    (P3V, "칠", "Seven (7)", "7（なな）"),
    (P3V, "팔", "Eight (8)", "8（はち）"),
    (P3V, "구", "Nine (9)", "9（きゅう）"),
    (P3V, "십", "Ten (10)", "10（じゅう）"),
    (P3V, "이십", "Twenty (20)", "20（にじゅう）"),
    (P3V, "삼십", "Thirty (30)", "30（さんじゅう）"),
    (P3V, "사십", "Forty (40)", "40（よんじゅう）"),
    (P3V, "오십", "Fifty (50)", "50（ごじゅう）"),
    (P3V, "육십", "Sixty (60)", "60（ろくじゅう）"),
    (P3V, "칠십", "Seventy (70)", "70（ななじゅう）"),
    (P3V, "팔십", "Eighty (80)", "80（はちじゅう）"),
    (P3V, "구십", "Ninety (90)", "90（きゅうじゅう）"),
    (P3V, "백", "One hundred (100)", "100（ひゃく）"),
    # 날짜 (월) p.39
    (P3V, "일월", "January", "1月（いちがつ）"),
    (P3V, "이월", "February", "2月（にがつ）"),
    (P3V, "삼월", "March", "3月（さんがつ）"),
    (P3V, "사월", "April", "4月（しがつ）"),
    (P3V, "오월", "May", "5月（ごがつ）"),
    (P3V, "유월", "June", "6月（ろくがつ）"),
    (P3V, "칠월", "July", "7月（しちがつ）"),
    (P3V, "팔월", "August", "8月（はちがつ）"),
    (P3V, "구월", "September", "9月（くがつ）"),
    (P3V, "시월", "October", "10月（じゅうがつ）"),
    (P3V, "십일월", "November", "11月（じゅういちがつ）"),
    (P3V, "십이월", "December", "12月（じゅうにがつ）"),
    # 문법·대화 어휘 pp.38, 40-41
    (P3V, "지금", "Now", "今（いま）"),
    (P3V, "안경", "Glasses", "めがね"),
    (P3V, "컴퓨터", "Computer", "コンピューター"),
    (P3V, "선글라스", "Sunglasses", "サングラス"),
    (P3V, "교통카드", "Transportation card", "交通（こうつう）カード"),
    (P3V, "여권", "Passport", "パスポート"),
    (P3V, "전화번호", "Phone number", "電話番号（でんわばんごう）"),
    (P3V, "생일", "Birthday", "誕生日（たんじょうび）"),
    # ---- 준비 3 · 문법 p.38, 대화1 p.40, 대화2 p.41 ----
    (P3S, "우산 있어요?", "Do you have an umbrella?", "傘（かさ）はありますか？"),
    (P3S, "네, 있어요.", "Yes, I do.", "はい、あります。"),
    (P3S, "아니요, 없어요.", "No, I don't.", "いいえ、ありません。"),
    (P3S, "책 있어요.", "I have a book.", "本（ほん）があります。"),
    (P3S, "안경 없어요.", "I don't have glasses.", "めがねはありません。"),
    (P3S, "지금 핸드폰 있어요?", "Do you have your phone now?",
     "今（いま）、携帯電話（けいたいでんわ）はありますか？"),
    (P3S, "네, 핸드폰 있어요.", "Yes, I have my phone.",
     "はい、携帯電話（けいたいでんわ）があります。"),
    (P3S, "아니요, 핸드폰 없어요.", "No, I don't have my phone.",
     "いいえ、携帯電話（けいたいでんわ）はありません。"),
    (P3S, "수잔 씨, 한국 전화번호 있어요?", "Susan, do you have a Korean phone number?",
     "スーザンさん、韓国（かんこく）の電話番号（でんわばんごう）はありますか？"),
    (P3S, "전화번호가 몇 번이에요?", "What's your phone number?",
     "電話番号（でんわばんごう）は何番（なんばん）ですか？"),
    (P3S, "010-4948-1287이에요.", "It's 010-4948-1287.", "010-4948-1287です。"),
    (P3S, "네, 맞아요.", "Yes, that's right.", "はい、そうです。"),
    (P3S, "완 씨, 렌핑 씨 생일 알아요?", "Wan, do you know Lenping's birthday?",
     "ワンさん、レンピンさんの誕生日（たんじょうび）を知（し）っていますか？"),
    (P3S, "네, 알아요.", "Yes, I do.", "はい、知（し）っています。"),
    (P3S, "렌핑 씨 생일이 며칠이에요?", "What date is Lenping's birthday?",
     "レンピンさんの誕生日（たんじょうび）は何日（なんにち）ですか？"),
    (P3S, "7월 15일이에요.", "It's July 15th.", "7月（しちがつ）15日（じゅうごにち）です。"),
]


def card_id(tag, ko):
    """Stable id from (tag, ko). Never recomputed for a card that already shipped."""
    return hashlib.sha1(f"{tag}|{ko}".encode("utf-8")).hexdigest()[:10]


def main():
    path = os.path.join(HERE, "master_cards.json")
    with open(path, encoding="utf-8") as f:
        master = json.load(f)

    existing_ids = {c["id"] for c in master}
    added = 0
    for tag, ko, en, ja in CARDS:
        cid = card_id(tag, ko)
        if cid in existing_ids:
            continue
        master.append({"id": cid, "ko": ko, "en": en, "tags": [tag], "ja": ja})
        existing_ids.add(cid)
        added += 1

    # An id collision against a previously shipped card would silently rewrite a
    # student's progress onto the wrong card, so fail loudly instead.
    ids = [c["id"] for c in master]
    if len(ids) != len(set(ids)):
        raise SystemExit("ABORT: duplicate card id detected, refusing to write")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=1)

    print(f"Added {added} cards; master_cards.json now has {len(master)}.")


if __name__ == "__main__":
    main()
