# Sogang Korean Flashcards — source pipeline

`index.html` (deployed at the repo root, served by GitHub Pages) is a
**generated file**. Never hand-edit it directly — edit the source files
below and rebuild.

## Files

- `master_cards.json` — the single source of truth for every card. Each
  entry: `{id, ko, en, ja, tags}`. `id` is permanent once shipped — it's
  the key each student's browser uses to remember review progress for that
  card, so **never change or reuse an existing id**, even if you fix a typo
  in `ko`/`en`/`ja`. Just add new entries with new ids. (Editing the text of a
  shipped card in place is fine and keeps its progress — that's how the
  "Hello? I'm Mina." → "Hello, I'm Mina." gloss fix was made. Only the `id` is
  frozen. Note that changing `ko` also means regenerating that id's audio file.)
- `audio_store/<id>.m4a` — one Korean-language audio clip per card, named
  by that card's id.
- `app_template.html` — the actual app (HTML/CSS/JS). Contains
  `__CARDS_JSON__` as a placeholder that `build.py` fills in.
- `build.py` — reads `master_cards.json` + `audio_store/`, embeds the audio
  as base64 into each card, and writes the final `index.html` (one
  self-contained file, no external requests, works offline once loaded).

## Rebuilding after any change

```bash
python3 build.py
cp index.html ../index.html   # or wherever the repo root actually is
```

Then commit/push `index.html` as usual.

## Adding new cards

1. Generate Korean audio for each new phrase — on a Mac, the built-in
   `say` command works well and is completely free/offline:
   ```bash
   say -v Yuna -o audio_store/<new-id>.m4a "새로운 단어"
   ```
   (Run `say -v '?' | grep -i ko_KR` to see what Korean voices are
   installed; prefer an Enhanced/Premium one if available — noticeably
   more natural than the default compact voice.)
2. Append new entries to `master_cards.json` with a **new, never-before-used
   id** (a short random/hash string is fine — just needs to be stable and
   unique), the Korean text, English + Japanese translations, and a
   `tags` array.
3. Run `python3 build.py` and commit the regenerated `index.html`.

## Tags / sections

The deck-picker screen groups cards by tag. `TAG_ORDER` and `TAG_LABELS`
(per-language) live in `app_template.html` — add a new tag there (in both
the `en` and `ja` blocks of `TAG_LABELS`, plus `TAG_ORDER`) whenever you
introduce a new section, alongside giving the relevant cards that tag in
`master_cards.json`. Only ever *append* to `TAG_ORDER` — don't reorder or
remove existing entries, since that would rearrange sections students
already have bookmarked mentally.

## Section visibility

The deck picker only shows sections the student has switched on. The switches
live on the deck picker itself — tap **Edit** next to the heading and every
section with cards turns into a labelled toggle row, on ones bright, off ones
dimmed; tap **Done** to go back to studying. Which sections you're carrying is
the thing that changes week to week, so it deliberately isn't buried in the ⋯
menu. That preference lives in its own localStorage key,
`SECTIONS_KEY` (`"sogangKoreanSections_v1"`), as a plain `{tag: bool}` map —
it is a **display preference, never progress data**, so it must stay separate
from `STORAGE_KEY`. Hiding a section leaves its review history untouched.

The rule that makes this safe to ship content into:

- A tag listed in `DEFAULT_VISIBLE_TAGS` is on for a student who has never
  opened the sheet. That list is the original eight sections, and **new tags
  should not be added to it**.
- Every other tag defaults to **off**. So adding a unit never changes what an
  existing student sees; they switch it on when their class gets there.
- An explicit choice in `SECTIONS_KEY` always beats the default, in both
  directions.
- Hidden sections are excluded from "All cards" too, and the header due-count
  only counts visible cards.

A corrupt or missing `SECTIONS_KEY` value falls back to the defaults rather
than throwing.

## Browse mode

The ☰ button on each deck row opens that section as a plain scrollable list —
every card at once, Korean plus translation, with a 🔊 button per row. It is
read-only on purpose: **browsing never writes progress**, because counting a
skim as a review would push cards out to intervals they haven't earned.

## Card order

`SHUFFLE_KEY` (`"sogangKoreanShuffle_v1"`) holds a single `"1"`/`"0"`, toggled
under ⋯ → *Shuffle card order*, **defaulting to on**. When on, a session's due
cards are shuffled; when off they come back in due-date order, which is the
original behaviour. Also a display preference, also separate from `STORAGE_KEY`.
It applies at `startSession()` only — flipping it mid-session doesn't reorder
the queue under the student's current card.

## Things that must never change (backward compatibility)

- `STORAGE_KEY` in `app_template.html` (currently `"sogangKoreanProgress_v1"`)
  — this is the localStorage key holding every student's review history.
- Any existing card's `id` in `master_cards.json`.
- `DEFAULT_STATE`'s existing fields (`ef`, `interval`, `reps`, `due`) — new
  fields can be *added* to it (older saved progress will pick up sane
  defaults for a new field automatically via the merge in `getState()`),
  but don't rename or remove the current ones.

## Current content (as of this file)

**238 cards.**

The original 94, from the "서강한국어 1A 한글" (Sogang Korean 1A Hangul) intro
unit slide decks — Hangul 1 (10 basics), Hangul 3 (41, diphthongs/aspirated),
Hangul 4 (16, tense consonants), Expressions (23, across To-Be/Adjectives/
Verbs/Requests), Numbers (6).

Plus 144 from the Student's Book itself (서강한국어 STUDENT'S BOOK 1A, 3rd ed.),
preparatory units 1–3, pp.16–45 — all default to **off** in Manage sections:

| Tag | Cards | Book pages |
|---|---|---|
| `Book1A::Prep1::Vocab` | 28 | 18–19, 23 (국적, 직업) |
| `Book1A::Prep1::Sentences` | 15 | 18, 20–21, 23 |
| `Book1A::Prep2::Vocab` | 31 | 28–29, 33 (사물) |
| `Book1A::Prep2::Sentences` | 14 | 28–31, 33 |
| `Book1A::Prep3::Vocab` | 40 | 38–39 (숫자①, 날짜) |
| `Book1A::Prep3::Sentences` | 16 | 38, 40–41 |

`add_book1a_prep.py` is the generator that produced them — idempotent, ids
derived from `sha1(tag|ko)`, safe to re-run. English glosses come from the
companion 문법·단어 참고서 (Grammar and Vocabulary Handbook 1A, English
edition) pp.36–38; Japanese glosses were written by hand, since the handbook
we have is the English edition.

Grammar points per unit are recorded in `GRAMMAR_NOTES.md`. Units 준비 4 and
1과–6과 are not carded yet.

### Note on file size

`index.html` is now **10.6 MB** (was 3.9 MB), because every clip is base64'd
inline to keep the app a single offline-capable file. That is a one-time load
per student, cached afterwards, but it is worth watching — carding all ten
remaining units at this rate would land somewhere north of 40 MB. If it gets
uncomfortable, the fix is re-encoding the clips at a lower bitrate rather than
splitting the file, which would cost the offline behaviour.
