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
| 준비 4 | 커피 주세요 · I'd Like Some Coffee | 46–55 | `명 주세요` | ✅ |
| 문화 1 | 유용한 정보 · Useful Information | 56–57 | (culture corner, no grammar) | — |
| 1과 | 앤디 씨가 식당에 있어요 · Andy Is in the Cafeteria | 58–75 | `명이/가`, `명에 있어요`, `명 명에 있어요` | ✅ |
| 2과 | 여섯 시에 일어나요 · I Get Up at 6:00 | 76–93 | `명에`, `명에 가요`, `동-아/어요①` | ✅ |
| 문화 2 | 서울 · Seoul | 94–95 | (culture corner, no grammar) | — |
| 3과 | 카페에서 친구를 만나요 · I Meet My Friend at the Café | 96–113 | `명을/를`, `동-아/어요②`, `명에서` | ✅ |
| 4과 | 어제 핸드폰을 샀어요 · I Bought a Mobile Phone Yesterday | 114–131 | `동-았/었어요`, `안 동/형`, `명도` | ✅ |
| 문화 3 | 한국의 관광지 · Korean Travel Destinations | 132–133 | (culture corner, no grammar) | — |
| 5과 | 지하철 2호선을 타세요 · Take Subway Line 2 | 134–151 | `동-고 싶어요`, `명(으)로①`, `동-(으)세요①` | ✅ |
| 6과 | 내일 등산하러 갈 거예요 · I'm Going to Go Hiking Tomorrow | 152–169 | `동-(으)러 가요`, `명(이)나`, `동-(으)ㄹ 거예요` | ✅ |
| 문화 4 | 대중교통 · Public Transportation | 170–171 | (culture corner, no grammar) | — |
| 부록 | Appendix (transcripts, answer key, translations) | 172+ | — | — |

`명` = noun, `동` = verb, `형` = adjective — the book's own shorthand.

## Detail for the units already carded

Every unit except the culture corners has now been read page by page.

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


## Detail for 준비 4과 and 1과–6과

Transcribed from the book alongside the handbook's English grammar pages.
Cards for these units exist; the notes below are still documentation only —
there is no grammar-card UI.

### 준비 4과 · Preparatory Unit 4

- **`명 주세요`** (p.48) — Attach 주세요 directly after a noun to order or request that thing: 'Please give me N / I'd like N.' No particle is needed. The natural reply from the server is 여기 있어요. ('Here you are.'). To order a quantity, put the counted phrase before 주세요: 된장찌개 한 개, 비빔밥 두 개 주세요. Examples: 커피 주세요. (Coffee, please.) / 김밥 주세요. (Gimbap, please.) / 물 좀 주세요. (Could I have some water?) — 좀 softens the request.
- **`숫자② — pure Korean numbers 하나~열`** (p.49) — Korean has two number systems. The pure Korean numbers 하나, 둘, 셋, 넷, 다섯, 여섯, 일곱, 여덟, 아홉, 열 are used mostly for counting things. Sino-Korean numbers (일, 이, 삼 …) are used for money, dates, phone numbers. Examples: 사과 하나 (one apple), 열 (ten).
- **`수 + 개 (counter) / 몇 개`** (p.49) — When a pure Korean number is used with a counter such as 개 (things), the first four (and 스물) change shape: 하나→한 개, 둘→두 개, 셋→세 개, 넷→네 개; 다섯 onward is unchanged (다섯 개). 몇 is the question word 'how many' and is used with a counter. Examples: A: 몇 개 있어요? (How many do you have?) B: 한 개 있어요. (I have one.) / 비빔밥 두 개 주세요.
- **`얼마예요?`** (p.49) — 얼마예요? asks the price of something ('How much is it?'). Prices are answered with Sino-Korean numbers plus 원, using 십 / 백 / 천 / 만 for 10 / 100 / 1,000 / 10,000; large numbers are grouped by 만 (10,000), not by thousands. Examples: A: 얼마예요? B: 이만 삼천팔백오십 원이에요. (It's 23,850 won.) / 3,000원이에요. / 모두 얼마예요? (How much is it altogether?)

### 1과 · Unit 1

- **`명이/가`** (p.60) — The subject marker 이/가 attaches to a noun to mark it as the subject of a verb or adjective. Use 이 after a noun ending in a consonant (집이, 대사관이, 한국이) and 가 after a noun ending in a vowel (미나 씨가, 앤디 씨가, 학교가). Examples: 이름이 뭐예요? (What's your name?) / 선생님이 도서관에 있어요. (My teacher is in the library.) / 미나 씨가 여기 있어요. (Mina is here.) Note that 있어요 can mean both existence and possession, so context decides which reading applies (집이 있어요. = I have a house.).
- **`명에 있어요`** (p.62) — (장소)에 있어요 = 'be at / in (a place)'. 에 is the location marker: attach it to a place noun to say where someone or something is. The verb used with it is always 있어요/없어요. Examples: 앤디 씨가 학교에 있어요. (Andy is at school.) / 앤디 씨가 집에 없어요. (Andy is not at home.) / 은행이 1층에 있어요. The question word is 어디 ('where'), which asks for the location of a person or object: A: 스터디 카페가 어디에 있어요? B: A빌딩에 있어요.
- **`명 명에 있어요`** (p.63) — Position nouns are used with the location marker 에 to say where something is relative to another thing: 위 (on/above), 아래 (under), 앞 (in front of), 뒤 (behind), 옆 (beside), 왼쪽 (left), 오른쪽 (right), 안 (inside), 밖 (outside), 사이 (between). The pattern is [thing]이/가 [reference noun] [position word]에 있어요, with no particle between the reference noun and the position word. Examples: 가방이 책상 위에 있어요. (There is a bag on the desk.) / 가방이 책상 아래에 있어요. (There is a bag under the desk.) / 강아지가 침대 위에 있어요. (The puppy is on the bed.) / 가방이 앤디 씨 가방하고 미나 씨 가방 사이에 있어요. (There is a bag between Andy's bag and Mina's bag.) Related: the marker 으로 expresses direction — 오른쪽으로 가세요. (Go to the right, please.)

### 2과 · Unit 2

- **`명에 ((시간)에)`** (p.78) — The particle 에 attaches to a time noun to mark when something happens ('at ...'). Hours use pure Korean numbers with 시 (한 시, 두 시, 세 시, 네 시 ...), minutes use Sino-Korean numbers with 분 (십 분, 삼십 분 ...); 반 means 'half past'. 몇 시 asks 'what time'. Examples: 몇 시에 일어나요? / 일곱 시에 일어나요. / 한 시 삼십 분이에요. = 한 시 반이에요.
- **`몇 시`** (p.78) — The interrogative 몇 attaches to 시 to ask the time. 지금 몇 시예요? = 'What time is it now?'; the answer is 한 시예요. / 오전 다섯 시 이십 분이에요. With a verb it becomes 몇 시에 …?: 몇 시에 공항에 가요? – 오후 다섯 시에 공항에 가요.
- **`명에 가요 ((장소)에 가요)`** (p.79) — 에 also marks a destination when used with 가다 and 오다, expressing where someone goes or comes. 어디에 가요? – 회사에 가요. / 지금 어디에 가요? – 도서관에 가요. / 9시에 학교에 와요. Time and place can be combined: 한 시에 학생 식당에 가요.
- **`동-아/어요①`** (p.81) — The informal polite (해요체) present-tense ending. Korean has three speech styles — informal polite, formal polite and plain — and adult speakers use the informal polite style, ending in 요, in everyday conversation. This unit covers 가다 → 가요 and 하다 verbs → 해요 (공부하다 → 공부해요, 일하다 → 일해요). The present tense covers current states, ongoing actions and near-future plans: 저는 여섯 시에 일어나요. / 어디에 가요? – 학교에 가요. / 오늘은 뭐 해요? When speaking to someone, use their name or title rather than a word for 'you': 앤디 씨, 뭐 해요? – 운동해요.
- **`뭐 해요?`** (p.80) — 뭐 ('what') combines with -해요 to ask about an action: 뭐 해요? = 'What are you doing?' Examples: 렌핑 씨, 오늘 오후에 공부해요? – 아니요. 그럼 뭐 해요? – 명동에 가요. / 오후에 뭐 해요? – 영화관에 가요. Note that 뭐 해요? sounds close to 뭐예요? ('What is it?') because ㅎ weakens between vowels; context distinguishes them.
- **`은/는`** (p.82) — 은/는 is the topic particle; it has no direct English equivalent and introduces or emphasises the topic that the rest of the sentence is about. 은 follows a consonant, 는 follows a vowel. Examples: 체육관에 가요. 수잔 씨는 어디에 가요? – 저도 체육관에 가요. / 오늘은 날씨가 좋아요. / 서울은 공원이 많아요. Compare 이/가, which highlights the attached noun as new or focal information: 저 사람이 앤디예요. vs 앤디 씨는 대학생이에요.

### 3과 · Unit 3

- **`명을/를`** (p.98) — Object marker. Attached to a noun, it marks that noun as the direct object of a transitive verb. Use -을 after a noun ending in a consonant and -를 after a noun ending in a vowel: 운동 + 을 → 운동을, 아메리카노 + 를 → 아메리카노를. Examples: 아메리카노를 좋아해요? / 네, 아메리카노를 좋아해요. / 아니요, 운동을 싫어해요. In colloquial speech native speakers often drop the object marker, but beginners are encouraged to practise using it.
- **`동-아/어요②`** (p.100) — Informal polite (해요체) sentence ending on verbs, used to ask and answer about actions. A Korean verb is stem + 다; drop 다 and add the ending. (1) If the stem's final vowel is ㅏ or ㅗ, add -아요: 살다 → 살아요, 오다 → 와요, 가다 → 가요, 받다 → 받아요. (2) If the final vowel is anything else, add -어요: 먹다 → 먹어요, 주다 → 줘요, 마시다 → 마셔요, 읽다 → 읽어요. (3) If the verb ends in -하다, it becomes -해요: 말하다 → 말해요, 공부하다 → 공부해요, 피곤하다 → 피곤해요. The same ending covers declarative, interrogative, imperative and propositive sentences; intonation and context distinguish them. Examples: 지금 뭐 해요? / 드라마를 봐요. / 커피를 마셔요.
- **`명에서`** (p.101) — Place marker meaning 'at, in'. Attached to a place noun to show where an action takes place (school, office, restaurant, etc.). Contrast it with 에, which simply indicates a location where someone or something exists (used with 있다). Examples: 어디에서 책을 빌려요? / 도서관에서 빌려요. / 학교에서 한국어를 공부해요. / 요리 교실에서 한국 요리를 배워요. Compare: 집에서 공부해요. (I study at home.) vs 오늘 집에 있어요. (I am at home today.)

### 4과 · Unit 4

- **`동-았/었어요`** (p.117) — Past-tense sentence ending for verbs and adjectives. It marks a completed action or a past state; the attachment rules are the same as for the present tense -아/어요. 1) If the stem's final vowel is ㅏ or ㅗ, add -았어요 (살다 → 살았어요, 오다 → 왔어요, 가다 → 갔어요, 앉다 → 앉았어요). 2) With any other final vowel, add -었어요 (먹다 → 먹었어요, 주다 → 줬어요, 마시다 → 마셨어요, 찍다 → 찍었어요). 3) Verbs/adjectives in -하다 become 했어요 (말하다 → 말했어요, 공부하다 → 공부했어요, 피곤하다 → 피곤했어요). Examples: 어제 뭐 했어요? — 운동했어요. / 친구를 만났어요. / 3일 전에 샀어요.
- **`안 동/형`** (p.118) — 안 is the negation adverb, placed directly before the verb or adjective: 안 + verb/adjective. Examples: 밥을 안 먹어요. / 아니요, 안 갔어요. / 앤디 씨가 오늘 학교에 안 가요. With 하다 compounds made of noun + 하다, 안 goes between the noun and 하다: 운동해요 → 운동을 안 해요 = 운동 안 해요; 매일 요리 안 해요.
- **`명도`** (p.119) — The particle 도 means 'also, too'. It attaches to a noun and replaces the subject markers 이/가 and the object markers 을/를 rather than stacking with them. Examples: 사과를 사요. 그리고 우유도 사요. / 요리했어요. 그리고 청소도 했어요. / 그리고 주스도 샀어요. / 앤디 씨가 김치를 좋아해요. 미나 씨도 김치를 좋아해요.
- **`'으' 불규칙 ('으' irregular)`** (p.121) — Stems ending in the vowel 'ㅡ' drop that vowel when a vowel ending is attached. 1) If the vowel before 'ㅡ' is ㅏ or ㅗ, -아요/-아어요 is used; otherwise -어요/-었어요 is used. 2) If the stem is a single syllable, -어요 is added. Examples: 바쁘다 → 바빠요 / 바빴어요 (미나 씨가 바빠요. / 어제 바빴어요.); 예쁘다 → 예뻐요 (미나 씨가 예뻐요.).

### 5과 · Unit 5

- **`동-고 싶어요`** (p.136) — Attached to a verb stem to express the subject's desire to do something: 'would like to / want to (do something)'. The form never changes, whether the verb stem ends in a consonant or a vowel: 만나다 → 만나고 싶어요, 먹다 → 먹고 싶어요. Examples: 안나 씨를 만나고 싶어요. (I would like to meet Anna.) / 빵을 먹고 싶어요. (I would like to eat some bread.) / 부산에 가고 싶어요. (I want to go to Busan.)
- **`명(으)로①`** (p.137) — A marker attached to a noun to indicate the method or means by which something is done. In this unit it is used with means of transportation. Use -으로 after nouns ending in a consonant (except ㄹ), and -로 after nouns ending in a vowel or in ㄹ: 버스로 (by bus), 지하철로 (by subway). Example: 스티브 씨는 어떻게 학교에 와요? — 지하철로 와요. (I come to school by subway.) Note the irregular set phrase 걸어서 가요 for going on foot.
- **`동-(으)세요①`** (p.138) — Attached to a verb stem to make a polite request or command: 'Please do (something)'. Use -으세요 after verb stems ending in a consonant and -세요 after stems ending in a vowel: 가다 → 가세요 (Please go.), 읽다 → 읽으세요 (Please read.). Examples: 지하철 2호선을 타세요. (Take subway line 2.) / 그리고 을지로3가 역에서 3호선으로 갈아타세요. (Then transfer to line 3 at Euljiro 3-ga Station.)
- **`동-지 마세요`** (p.138) — Attached to a verb stem to indicate prohibition of an action: 'Please do not (do something)'. It is used mainly in imperative or request sentences. Example: 집에 가지 마세요. (Please don't go home.) / 교실에서 음식을 먹지 마세요. (Please don't eat food in the classroom.)
- **`에서 까지`** (p.137) — The marker 에서 marks the starting point and 까지 marks the destination; used together they mean 'from A to B'. Both attach directly to place nouns. Example: 학교에서 집까지 걸어서 왔어요. (I walked from school to my house.) / 인천 공항에서 나리타 공항까지 비행기로 가요. Compare 부터 ... 까지, which is used with time words: 마이클 씨가 아침부터 저녁까지 일을 해요.
- **`어떻게`** (p.137) — The interrogative equivalent of English 'how', used to ask how to do something. Examples: 어떻게 가요? (How do I get there?) / 김치는 어떻게 만들어요? (How do I make kimchi?) / 명동에 어떻게 가요? (How do I get to Myeongdong?)

### 6과 · Unit 6

- **`동-(으)러 가요`** (p.154) — Attaches to a verb stem to express the purpose of going somewhere: 'go in order to (do something)'. Use -으러 after stems ending in a consonant (except ㄹ) and -러 after stems ending in a vowel or in ㄹ. The main verb is usually a movement verb such as 가다, 오다, 다니다. Examples: 책을 사러 서점에 가요. (I go to the bookstore to buy a book.) 점심을 먹으러 식당에 가요. (I go to a restaurant to eat lunch.) 공원에 놀러 왔어요. (I came to the park to play.)
- **`명(이)나`** (p.155) — Joins two nouns to mean 'or': attach -이나 after a noun ending in a consonant and -나 after a noun ending in a vowel. Examples: 커피나 차 (coffee or tea), 책이나 신문 (a book or a newspaper), 비빔밥이나 김치찌개를 먹어요. (I eat bibimbap or kimchi stew.) The related form -거나 does the same job for verbs and adjectives, but 명(이)나 is used only for connecting nouns.
- **`동-(으)ㄹ 거예요`** (p.157) — The future tense: expresses an action the speaker is going to do. Attach -을 거예요 after a verb stem ending in a consonant and -ㄹ 거예요 after a stem ending in a vowel (or a ㄹ stem, which drops nothing extra). Used with verbs, not adjectives. Examples: 안나 씨, 언제 부산에 갈 거예요? (Anna, when are you going to go to Busan?) 다음 주에 갈 거예요. (I'm going to go there next week.) 오늘 친구하고 점심을 먹을 거예요. (I'm going to eat lunch with my friend today.)

**Gap:** pp.168–169 (end of 6과) were never photographed — see README.


## Additional grammar found in the full re-read of 준비 1–3

The first pass at these units worked from a 12-page publisher sample. Reading
the real pages surfaced these, which the sample did not contain:

- **준비 1과** `명이에요/예요` (p.18) — The copula 'to be (am/is/are)'. It attaches directly to a noun with no space. Use -이에요 after a noun ending in a consonant (미국 사람이에요, 회사원이에요) and -예요 after a noun ending in a vowel (앤디 씨예요, 의사예요). Examples: A: 이름이 뭐예요? B: 수잔이에요. / 저는 앤디예요. / 미국 사람이에요. Basic Korean sentence structure is subject + predicate, as in 이분이(subject) 앤디 씨예요(predicate). Pronunciation TIP on p.18: questions end on a rising tone while answers end on a falling tone — A: 이름이 뭐예요?↗ B: 앤디예요.↘
- **준비 1과** `누구` (p.22) — '누구' is the interrogative pronoun 'who', used to ask about a person. With the copula it becomes 누구예요? Example: A: 이분이 누구예요? B: 앤디 씨예요. / B: 가브리엘 씨예요. Presented in the textbook through the 과제 (p.22) and 읽고 말하기 (p.23) sections.
- **준비 2과** `이게/저게` (p.28) — '이게' (this thing) points to an object close to the speaker; '저게' (that thing over there) points to an object far from both speaker and listener. Both are used only as the subject of a sentence. e.g. 이게 의자예요. (This is a chair.) / 저게 가방이에요. (That is a bag.)
- **준비 2과** `뭐예요?` (p.30) — The interrogative pronoun '뭐' means 'what'; the ending '-예요' attaches directly to it. When answering '이게/저게 뭐예요?', the subject '이게/저게' is usually omitted. e.g. A: 이게 뭐예요? B: 연필이에요. / A: 그럼 저게 뭐예요? B: 시계예요.
- **준비 2과** `누구 거예요?` (p.31) — Used to ask who an object belongs to: '누구' (who) + '거' (thing, from 것) + '-예요'. The answer uses 제 거예요 (it's mine) or a name plus 씨 거예요. e.g. A: 우산 누구 거예요? B: 제 거예요. / 사라 씨 거예요.
- **준비 3과** `명 있어요/없어요` (p.38) — 있어요 = 'to have / there is'; 없어요 = 'to not have / there isn't'. Attach directly after a noun with no particle at this level: [noun] 있어요/없어요. Question and statement share the same form, distinguished by intonation. Examples: 우산 있어요? – 네, 있어요. / 지우개 있어요? – 아니요, 없어요. / 책 있어요. / 안경 없어요.
- **준비 3과** `숫자① (Sino-Korean numbers)` (p.39) — Korean has two number systems; this unit teaches the Sino-Korean set (일, 이, 삼 … 십, 이십 … 백). Sino-Korean numbers are used for prices, phone numbers, bus numbers and dates: 10원, 02-925-3857, 34번, 2월 14일. Zero is normally 영, but in telephone numbers 공 is used instead. Pure Korean numbers (taught later) are used mostly for counting.
- **준비 3과** `몇 번` (p.40) — 몇 usually means 'how many', but with 번 (number) it means 'what/which number' and asks for a numerical value such as a phone number, bus number or room number. A: 전화번호가 몇 번이에요? B: 010-4948-1287이에요. / A: 몇 번 버스예요? B: 701번 버스예요. When reading a phone number aloud, the dash is read 에. Answers to 몇 번이에요? always use Sino-Korean numbers (unlike 몇 개 있어요?, which takes pure Korean numbers).
- **준비 3과** `몇 월 며칠` (p.41) — 몇 combines with 월 (month) and 일 (day) to ask a date. A: 오늘이 몇 월 며칠이에요? B: 7월 5일이에요. Write 며칠, not 몇 일, even though the two sound alike. Month names use Sino-Korean numbers plus 월, with two irregular forms: 6월 is 유월 (not 육월) and 10월 is 시월 (not 십월).
