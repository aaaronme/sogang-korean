# Grammar points — Sogang Korean Student's Book 1A

Placeholder notes. **There is no grammar-card UI yet** — this file just records
what grammar each unit introduces so building one later is a matter of writing
the UI, not re-reading the book.

Source: 서강한국어 STUDENT'S BOOK 1A, 3rd ed., Hawoo Publishing. Unit titles and
page numbers come from the 목차 (Contents, p.8) and 내용 구성표 (pp.4–7).

## Unit map

Start pages are printed in the Contents; end pages were inferred as
next-start-minus-1 and then **confirmed against the physical book on
2026-07-20**.

The English names are the publisher's own, from the Table of Contents — 준비n과
is "Preparatory Unit n" and n과 is "Unit n". They are distinct units, which is
why the tags are `PrepUnit1..4` and `Unit1..6` rather than one run of numbers.

| Unit | Title | Pages | Grammar introduced | Cards? |
|---|---|---|---|---|
| 준비 1 | 반갑습니다 · It's Nice to Meet You | 16–25 | `명이에요/예요` | ✅ |
| 준비 2 | 한국어 책이에요 · It's a Korean Language Book | 26–35 | `이게`, `저게` | ✅ |
| 준비 3 | 핸드폰 있어요? · Do You Have a Cell Phone? | 36–45 | `명 있어요/없어요` | ✅ |
| 준비 4 | 커피 주세요 · I'd Like Some Coffee | 46–55 | `명 주세요` | — |
| 문화 1 | 유용한 정보 · Useful Information | 56–57 | (culture corner, no grammar) | — |
| 1과 | 앤디 씨가 식당에 있어요 · Andy Is in the Cafeteria | 58–75 | `명이/가`, `명에 있어요`, `명 명에 있어요` | — |
| 2과 | 여섯 시에 일어나요 · I Get Up at 6:00 | 76–93 | `명에`, `명에 가요`, `동-아/어요①` | — |
| 문화 2 | 서울 · Seoul | 94–95 | (culture corner, no grammar) | — |
| 3과 | 카페에서 친구를 만나요 · I Meet My Friend at the Café | 96–113 | `명을/를`, `동-아/어요②`, `명에서` | — |
| 4과 | 어제 핸드폰을 샀어요 · I Bought a Mobile Phone Yesterday | 114–131 | `동-았/었어요`, `안 동/형`, `명도` | — |
| 문화 3 | 한국의 관광지 · Korean Travel Destinations | 132–133 | (culture corner, no grammar) | — |
| 5과 | 지하철 2호선을 타세요 · Take Subway Line 2 | 134–151 | `동-고 싶어요`, `명(으)로①`, `동-(으)세요①` | — |
| 6과 | 내일 등산하러 갈 거예요 · I'm Going to Go Hiking Tomorrow | 152–169 | `동-(으)러 가요`, `명(이)나`, `동-(으)ㄹ 거예요` | — |
| 문화 4 | 대중교통 · Public Transportation | 170–171 | (culture corner, no grammar) | — |
| 부록 | Appendix (transcripts, answer key, translations) | 172+ | — | — |

`명` = noun, `동` = verb, `형` = adjective — the book's own shorthand.

## Detail for the units already carded

Only these three were read page by page; the rest of the table above is from
the contents pages only.

### 준비 1 — `명이에요/예요` (p.18)

Copula attached directly to a noun, no space. `-예요` after a vowel, `-이에요`
after a consonant.

- 앤디**예요**. / 수잔**이에요**.
- 미국 사람**이에요**. / 학생**이에요**.

Sentence structure introduced alongside it: subject precedes predicate
(이름이 뭐예요? → 앤디예요.). Intonation tip on p.20: questions rise, answers fall.

### 준비 2 — `이게` / `저게` (pp.28–29)

Demonstrative + subject marker. `이게` = this thing (near speaker), `저게` =
that thing (away from both).

- **이게** 뭐예요? → 책이에요.
- **저게** 뭐예요? → 가방이에요.

Also introduced in the dialogues: possessive `누구 거예요?` / `제 거예요.`

### 준비 3 — `명 있어요/없어요` (p.38)

Existence and possession. No particle on the noun in the book's examples.

- 우산 **있어요**? → 네, **있어요**. / 아니요, **없어요**.
- 책 **있어요**. / 안경 **없어요**.

Numbers ① (Sino-Korean) and dates are taught in the same unit (p.39), which is
what makes 전화번호가 몇 번이에요? and 생일이 며칠이에요? the unit's drill dialogues.

## When adding a grammar-card UI

Grammar cards would need a different shape from the current `{id, ko, en, ja}`
vocabulary card — at minimum a pattern, a rule note, and several example
sentences per card. Adding that means a new field on the card record rather
than a new tag; `build.py` passes through whatever keys it is given except that
it currently hardcodes the `id/ko/en/ja/tags/audio` set, so it would need
updating too.
