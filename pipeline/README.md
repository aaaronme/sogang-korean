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
- `../audio/<id>.m4a` — one Korean-language audio clip per card, named by that
  card's id. This directory lives at the **repo root**, not under `pipeline/`,
  because GitHub Pages serves it directly: the app fetches `audio/<id>.m4a` at
  play time.
- `app_template.html` — the actual app (HTML/CSS/JS). Contains
  `__CARDS_JSON__` as a placeholder that `build.py` fills in.
- `sw_template.js` — service worker source. `__VERSION__` is substituted by
  `build.py` with a hash of the built `index.html`.
- `build.py` — reads `master_cards.json` + `audio/`, writes `index.html` (card
  text only, no audio bytes) and `sw.js`, and prunes clips in `audio/` that no
  longer belong to any card.

## Rebuilding after any change

```bash
python3 build.py
```

It writes straight to the repo root — `index.html`, `sw.js`, and any pruning of
`audio/`. Commit those together: a new `index.html` without its new clips is a
deploy where half the cards are silent.

## Adding new cards

1. Generate Korean audio for each new phrase — on a Mac, the built-in
   `say` command works well and is completely free/offline:
   ```bash
   say -v Yuna -o /tmp/raw.m4a "새로운 단어"
   afconvert -f m4af -d aac@22050 -b 32000 -c 1 /tmp/raw.m4a ../audio/<new-id>.m4a
   python3 strip_m4a_padding.py
   ```
   (Run `say -v '?' | grep -i ko_KR` to see what Korean voices are
   installed; prefer an Enhanced/Premium one if available — noticeably
   more natural than the default compact voice.)

   **The `afconvert` step is not optional.** `say -o foo.m4a` writes
   *uncompressed* 16-bit PCM into the m4a container — 352 kbps, roughly 8x
   larger than it needs to be, and every one of those bytes is downloaded by a
   student on mobile data. AAC mono 32 kbps is transparent for a TTS voice; the
   1259-clip library is 11.5 MB encoded and would be near 90 MB as PCM.
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

**Name units the way the book's English Table of Contents does**, so a tag can
be checked against the physical book without a decoder ring: 준비n과 is
"Preparatory Unit n" (`Book1A::PrepUnitN::*`) and n과 is "Unit n"
(`Book1A::UnitN::*`). They are different units — 준비 1 and 1과 both exist —
so `Unit1` must stay reserved for 1과.

Renaming a tag after it ships is possible but has two catches, both handled for
the `Prep{n}` → `PrepUnit{n}` rename in commit `bb6d00d`'s successor:

1. Card ids are `sha1(tag|ko)`. Re-deriving them from the new tag would give
   every card a new id and orphan every student's progress, so
   `add_book1a_prep.py` keeps an `ID_TAG` map and mints ids from the *original*
   tag string forever.
2. Section-visibility prefs are keyed by tag, so `RENAMED_TAGS` in
   `app_template.html` migrates a student's old on/off choice to the new key on
   load. An explicit choice under the new name always wins.

The old strings stay in `TAG_ORDER` as retired entries. `tagHasCards()` filters
them out of every list once no card carries them.

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

**1259 cards.**

The original 94, from the "서강한국어 1A 한글" (Sogang Korean 1A Hangul) intro
unit slide decks — Hangul 1 (10 basics), Hangul 3 (41, diphthongs/aspirated),
Hangul 4 (16, tense consonants), Expressions (23, across To-Be/Adjectives/
Verbs/Requests), Numbers (6). These eight are the only sections that default
to **on**; every Book 1A section below defaults to off.

Preparatory Units 1–4 and Units 1–6, book pp.16–167 — 1205 cards:

| Tag | Vocab / Sentences | Book pages |
|---|---|---|
| `Book1A::PrepUnit1::Vocab` / `::Sentences` | 28 / 39 | 16–25 |
| `Book1A::PrepUnit2::Vocab` / `::Sentences` | 31 / 17 | 26–35 |
| `Book1A::PrepUnit3::Vocab` / `::Sentences` | 48 / 22 | 36–45 |
| `Book1A::PrepUnit4::Vocab` / `::Sentences` | 56 / 22 | 46–55 |
| `Book1A::Unit1::Vocab` / `::Sentences` | 70 / 74 | 58–75 |
| `Book1A::Unit2::Vocab` / `::Sentences` | 72 / 95 | 76–93 |
| `Book1A::Unit3::Vocab` / `::Sentences` | 51 / 85 | 96–113 |
| `Book1A::Unit4::Vocab` / `::Sentences` | 70 / 117 | 114–131 |
| `Book1A::Unit5::Vocab` / `::Sentences` | 58 / 102 | 134–151 |
| `Book1A::Unit6::Vocab` / `::Sentences` | 97 / 51 | 152–167 |

`add_book1a_units.py` generates all of it from the per-unit transcription JSON.
(`add_book1a_prep.py` produced the first pass at Preparatory Units 1–3 and is
kept for provenance; its cards are a subset of what the unit generator now
emits.) Both are idempotent: ids are `sha1(tag|ko)`, so re-running never mints a
new id for a card that already shipped — and the unit generator additionally
reports *near*-duplicate strings within a section, since a re-transcription
differing by one space would otherwise become a silent second card for the same
phrase rather than matching the first. English glosses come from the
companion 문법·단어 참고서 (Grammar and Vocabulary Handbook 1A, English edition)
pp.36–47 wherever the word appears there; the rest, and all Japanese, are ours.

Grammar points per unit are recorded in `GRAMMAR_NOTES.md`.

**Known gaps**, both missing photographs rather than missing work:

- pp.16–17, the 준비 1과 opener. The PDF sample shows this spread is the unit
  contents map only — no vocabulary, no example sentences — so nothing appears
  lost, but it is not visually verified.
- pp.168–169, the tail of 6과 (its 과제 and 단원 마무리 pages).

Everything else from pp.16–167 is covered.

Note on the photo set: shots 040–043 are **single pages** (18, 19, 20, 21);
from 044 on they are two-page spreads, where the left page is `2 × seq − 66`.
Shots 110 and 111 are the same spread (p.154–155) taken twice, which is why the
sequence runs two pages short at the end.

### Note on file size

`index.html` is **0.21 MB** for 1299 cards — card text only. The 8.1 MB of
audio sits in `audio/` and is fetched one clip at a time, so a student studying
two sections pays for roughly 100 clips (~600 KB), not the library.

Three separate fixes got it there, in this order, and the order matters:

1. **Codec.** `say -o out.m4a` writes uncompressed PCM. Re-encoding to AAC mono
   32 kbps shrank the library ~8x. Every clip in `audio/` should be AAC — check
   with `afinfo ../audio/*.m4a | grep -c lpcm`, which should print 0.
2. **Splitting audio out of the HTML.** Even after the codec fix, inlining 1259
   clips made `index.html` 15.6 MB, every byte of it downloaded before a student
   saw a single card. Now the shell is 0.20 MB and `sw.js` caches each clip
   permanently the first time it plays.
3. **Stripping container padding** (`strip_m4a_padding.py`). afconvert aligns
   the media data to a 4096-byte boundary with a `free` atom; on a 1-second clip
   that padding is a quarter of the file. Removing it is lossless — the `mdat`
   bitstream is copied byte for byte and only `stco`'s chunk offsets are fixed
   up — and took `audio/` from 11.5 MB to 7.8 MB. Run it after generating clips;
   it is idempotent.

   Do **not** extend it to strip `udta`. That looks like free bytes but holds
   the `iTunSMPB` priming-delay tag; without it decoders replay the encoder's
   priming samples, shifting every sample and lengthening the clip ~23 ms.

Doing (2) without (1) would have meant serving PCM forever, one wasteful request
at a time — splitting hides a bad codec rather than fixing it.

Further compression was measured and rejected: dropping to 24 kbps saves another
~11% for audible quality loss on a voice that is already synthetic, and an ADTS
container saves about what padding-stripping already did but changes the file
format, which risks iOS playback for no additional gain.

The trade-off: the app is no longer a single self-contained file, and "works
offline" now means "works offline for what you've already played" rather than
everything at once. That fits how the app is used — students carry two or three
sections at a time, and nobody needs 6과's audio in week two.
