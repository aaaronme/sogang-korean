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
   student on mobile data. AAC mono 32 kbps is transparent for a TTS voice.
2. Append new entries to `master_cards.json` with a **new, never-before-used
   id** (a short random/hash string is fine — just needs to be stable and
   unique), the Korean text, English + Japanese translations, and a
   `tags` array. In practice you want one of the generators rather than doing
   this by hand — see *Generators* below.
3. Run `python3 build.py` and commit the regenerated `index.html`, `sw.js` and
   `audio/` together.

## Generators

All are idempotent — ids derive from content, so re-running never mints a new id
for a card that already shipped — and all read transcription JSON produced by
reading the book photographs.

| Script | Produces |
|---|---|
| `add_book1a_prep.py` | first pass at Preparatory Units 1–3; superseded, kept for provenance |
| `add_book1a_units.py` | vocabulary + sentence cards for all ten units |
| `add_culture_cards.py` | the four Culture Corner sections |
| `add_grammar_cards.py` | grammar cards (see below) |
| `strip_m4a_padding.py` | post-processes `audio/`; run after any clip generation |

`add_book1a_units.py` also reports **near-duplicate** strings within a section:
because ids come from the exact Korean, a re-transcription differing by a single
space would otherwise become a silent second card for the same phrase instead of
matching the first. It squashes whitespace and punctuation to spot those. It
reports rather than aborts, since the book does legitimately print e.g. a
statement and a question that differ only in punctuation.

## Grammar cards

A grammar card has a different shape from a vocabulary card and is the reason
`build.py` passes unknown keys through instead of hardcoding a field list:

```json
{"id": "...", "ko": "명이/가", "en": "<rule>", "ja": "<rule>",
 "tags": ["Book1A::Unit1::Grammar"], "type": "grammar",
 "examples": [{"ko": "...", "en": "...", "ja": "...", "audio": "<clip id>"}]}
```

The pattern is the front, the rule and 2–4 worked examples the back. Two things
to know:

- **A grammar card has no clip of its own** — a pattern like 명이에요/예요 is not
  a speakable phrase. Its *examples* have audio instead, and the app hides the
  card's speaker button rather than leaving a dead control. Everything in the
  app guards on `type === "grammar"` and on the fields being absent, because a
  student may be running a cached `index.html` from before grammar existed.
- **Example clips are referenced from inside a card, not named after one.**
  `build.py`'s stale-clip pruner must therefore include example ids in its
  wanted set — without that it classes every example clip as orphaned and
  deletes it.

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

**Renaming a tag is no longer an option** now that the app is shared: ids are
`sha1(tag|ko)`, so a rename re-derives every id in that section and orphans the
progress attached to it. Get the name right the first time. (The `Prep{n}` →
`PrepUnit{n}` rename happened before release, when the deck could still be
reshaped freely; the migration code that supported it has been removed.)

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

**The app was shared with students on 2026-07-20. From that date real people
have review history saved in their browsers, and there is no server-side copy of
it — if a change orphans their progress, it is gone.** Everything in this
section is now load-bearing. Before this date the deck was reshaped freely
(ids reminted, a duplicate card deleted, tags renamed); none of that is
acceptable any more.

In particular, and in addition to the list below:

- **Never delete a card.** Hide it by switching its section off if you must;
  removing it discards whatever a student had learned about it.
- **Never edit a card's `ko`.** The id is derived from it in the generators, so
  changing `ko` and re-running mints a *new* card and abandons the old one's
  progress. Fixing `en`/`ja` in place is still fine and keeps progress.
- **Only append to `TAG_ORDER`**, and keep `DEFAULT_VISIBLE_TAGS` as it is, so
  new content never appears in someone's deck uninvited.
- New fields on a card record are fine — `build.py` passes them through and the
  app must treat them as optional, because a student's cached `index.html` may
  be a build old enough not to have them.

- `STORAGE_KEY` in `app_template.html` (currently `"sogangKoreanProgress_v1"`)
  — this is the localStorage key holding every student's review history.
- Any existing card's `id` in `master_cards.json`.
- `DEFAULT_STATE`'s existing fields (`ef`, `interval`, `reps`, `due`) — new
  fields can be *added* to it (older saved progress will pick up sane
  defaults for a new field automatically via the merge in `getState()`),
  but don't rename or remove the current ones.

## Current content (as of this file)

**1496 cards.**

The original 94, from the "서강한국어 1A 한글" (Sogang Korean 1A Hangul) intro
unit slide decks — Hangul 1 (10 basics), Hangul 3 (41, diphthongs/aspirated),
Hangul 4 (16, tense consonants), Expressions (23, across To-Be/Adjectives/
Verbs/Requests), Numbers (6). These eight are the only sections that default
to **on**; every Book 1A section below defaults to off.

Preparatory Units 1–4 and Units 1–6, book pp.16–169:

| Tag | Vocab / Sentences / Grammar | Book pages |
|---|---|---|
| `Book1A::PrepUnit1::*` | 28 / 39 / 2 | 16–25 |
| `Book1A::PrepUnit2::*` | 31 / 17 / 3 | 26–35 |
| `Book1A::PrepUnit3::*` | 48 / 22 / 4 | 36–45 |
| `Book1A::PrepUnit4::*` | 56 / 22 / 4 | 46–55 |
| `Book1A::Unit1::*` | 70 / 74 / 3 | 58–75 |
| `Book1A::Unit2::*` | 72 / 95 / 6 | 76–93 |
| `Book1A::Unit3::*` | 51 / 85 / 3 | 96–113 |
| `Book1A::Unit4::*` | 70 / 117 / 4 | 114–131 |
| `Book1A::Unit5::*` | 58 / 102 / 6 | 134–151 |
| `Book1A::Unit6::*` | 104 / 64 / 3 | 152–169 |

The four Culture Corners are one section each rather than a vocab/sentences
pair — each is a two-page spread, and splitting would give sections of three
cards. 문화 1 has **no sentence cards at all**: that spread contains no finite
verb, only holiday names, hotline numbers and app labels.

| Tag | Cards | Book pages |
|---|---|---|
| `Book1A::Culture1` | 39 | 56–57 |
| `Book1A::Culture2` | 34 | 94–95 |
| `Book1A::Culture3` | 49 | 132–133 |
| `Book1A::Culture4` | 17 | 170–171 |

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

**Known gap:** pp.16–17, the 준비 1과 opener, is the only spread never
photographed. The PDF sample shows it is the unit contents map — no vocabulary,
no example sentences — so nothing appears lost, but that is not visually
verified. Everything else from pp.16–171 is covered.

**Do not trust arithmetic on the photo sequence.** It is irregular in three
places and every one of them caused a wrong page assignment at some point:

- shots 040–043 are **single pages** (18, 19, 20, 21); from 044 on they are
  two-page spreads
- shots 110 and 111 are the same spread (pp.154–155) photographed twice
- so `left page = 2 × seq − 66` holds only for 044–110, and everything after
  111 is shifted by one

pp.168–169 were reported missing twice on the strength of that formula. They
are not missing; they are shot 118. Always confirm against the printed folio.

Both hazards for a future pass: this copy has a previous owner's **handwritten
English glosses** next to the p.169 word list and handwritten answers in
fill-in-the-blank exercises throughout. They are not book content and must not
be transcribed as if they were.

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
