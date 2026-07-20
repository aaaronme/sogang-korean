# Sogang Korean Flashcards — source pipeline

`index.html` (deployed at the repo root, served by GitHub Pages) is a
**generated file**. Never hand-edit it directly — edit the source files
below and rebuild.

## Files

- `master_cards.json` — the single source of truth for every card. Each
  entry: `{id, ko, en, ja, tags}`. `id` is permanent once shipped — it's
  the key each student's browser uses to remember review progress for that
  card, so **never change or reuse an existing id**, even if you fix a typo
  in `ko`/`en`/`ja`. Just add new entries with new ids.
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

## Things that must never change (backward compatibility)

- `STORAGE_KEY` in `app_template.html` (currently `"sogangKoreanProgress_v1"`)
  — this is the localStorage key holding every student's review history.
- Any existing card's `id` in `master_cards.json`.
- `DEFAULT_STATE`'s existing fields (`ef`, `interval`, `reps`, `due`) — new
  fields can be *added* to it (older saved progress will pick up sane
  defaults for a new field automatically via the merge in `getState()`),
  but don't rename or remove the current ones.

## Current content (as of this file)

94 cards across: Hangul 1 (10 basics), Hangul 3 (41, diphthongs/aspirated),
Hangul 4 (16, tense consonants), Expressions (23, across To-Be/Adjectives/
Verbs/Requests), Numbers (4). All are single words or short phrases drawn
from the "서강한국어 1A 한글" (Sogang Korean 1A Hangul) intro unit slide
decks — not yet from the Student's Book itself.
