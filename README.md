# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr helps users find thrifted clothing items based on what they are looking for, their size, and their budget. The user enters a natural language request such as “vintage graphic tee under $30,” and FitFindr searches the listings for matching items. When it finds a match, it suggests an outfit using the selected item and the user's wardrobe. Finally, it creates a short fit card caption describing the outfit, item, price, platform, and overall vibe.



---

## Tool Inventory

### `search_listings`

- **What it does:** Searches the clothing listings for items matching the user's description and optionally filters them by size and maximum price.
- **Inputs:** `description` (`str`), `size` (`str | None`), `max_price` (`float | None`)
- **Returns:** A list of matching listing dictionaries, ordered from best match to lowest match, with fields including `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:** Returns an empty list `[]` when no listings match the search criteria.

### `suggest_outfit`

- **What it does:** Uses a new clothing item and the user's wardrobe to generate one or two outfit suggestions.
- **Inputs:** `new_item` (`dict`), `wardrobe` (`dict`)
- **Returns:** A non-empty string containing outfit suggestions. When the wardrobe has items, the suggestions should name pieces from the user's wardrobe.
- **When it has nothing:** If the wardrobe is empty, it returns general styling advice for the new item instead of returning an empty string or raising an error.

### `create_fit_card`

- **What it does:** Creates a short social-media-style caption describing the selected item and the suggested outfit.
- **Inputs:** `outfit` (`str`), `new_item` (`dict`)
- **Returns:** A two-to-four sentence string that mentions the item, its price, its platform, and the outfit's overall vibe.
- **When it has nothing:** If `outfit` is empty or contains only whitespace, it returns a descriptive message instead of raising an error.

### `search_listings`

- **What it does:**
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:**
- **When it has nothing:**

### `suggest_outfit`

- **What it does:**
- **Inputs:**
- **Returns:**
- **When it has nothing:**

### `create_fit_card`

- **What it does:**
- **Inputs:**
- **Returns:**
- **When it has nothing:**

---

## Planning Loop

**Branch rule:**

If `search_listings` returns an empty list, put a helpful message in `session["error"]` explaining what the user could change, then stop the run and return the session. If `search_listings` returns one or more listings, save the results in the session, select the first result, and continue to `suggest_outfit`. After that, save the outfit suggestion in the session, pass it to `create_fit_card` with the selected item, save the fit card in the session, and return the completed session.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:**  
Use regex/string parsing to extract the description, size, and maximum price from the user's query. The parsed values are stored in `session["parsed"]` before calling `search_listings`.

**What moves through the session:**  
The query is stored first, followed by the parsed description/size/max price. The search results are then stored in `session["search_results"]`. The first result becomes `session["selected_item"]`. That item and the wardrobe are used to produce `session["outfit_suggestion"]`. Finally, the outfit suggestion and selected item produce `session["fit_card"]`. If the search returns no results, `session["error"]` is populated and the later fields remain unset.

---

## Sample Run

<(.venv) myathomas@Myas-MacBook-Pro ai201-project2-fitfindr-starter-v2026 % python - <<'PY'
from tools import search_listings, suggest_outfit, create_fit_card print('search_listings ->, search_listings(graphic tee, max_price=30'))
print (suggest_outfit ->, suggest_outfit {'title:demo'}, {items: [1})) print(create_fit_card ->, create_fit_card({'title''demo'},
{'title':'demo}))
PY
  File "<stdin>", line 1
    from tools import search_listings, suggest_outfit, create_fit_card print('search_listings ->, search_listings(graphic tee, max_price=30'))
                                                                                                                                             ^
SyntaxError: unmatched ')'
(.venv) myathomas@Myas-MacBook-Pro ai201-project2-fitfindr-starter-v2026 % clear
(.venv) myathomas@Myas-MacBook-Pro ai201-project2-fitfindr-starter-v2026 % python app.py fields
A listing has these fields:

  id             str    lst_001
  title          str    Vintage Levi's 501 Jeans — Medium Wash
  description    str    Classic 501s in a perfect medium wash. Some light fading a…
  category       str    bottoms
  style_tags     list   ['vintage', 'classic', 'denim', 'streetwear']
  size           str    W30 L30
  condition      str    good
  price          float  38.0
  colors         list   ['blue', 'indigo']
  brand          str    Levi's
  platform       str    depop

A wardrobe item has these fields:

  id             str    w_001
  name           str    Baggy straight-leg jeans, dark wash
  category       str    bottoms
  colors         list   ['dark blue', 'indigo']
  style_tags     list   ['denim', 'streetwear', 'baggy']
  notes          str    High-waisted, sits above the hip

These are what search_listings can filter on. Read a few whole listings
with `python app.py listings` before you write it.
(.venv) myathomas@Myas-MacBook-Pro ai201-project2-fitfindr-starter-v2026 % python app.py listings --ful
l -n 6
{
  "id": "lst_001",
  "title": "Vintage Levi's 501 Jeans \u2014 Medium Wash",
  "description": "Classic 501s in a perfect medium wash. Some light fading at the knees which adds to the vintage look. No rips or stains.",
  "category": "bottoms",
  "style_tags": [
    "vintage",
    "classic",
    "denim",
    "streetwear"
  ],
  "size": "W30 L30",
  "condition": "good",
  "price": 38.0,
  "colors": [
    "blue",
    "indigo"
  ],
  "brand": "Levi's",
  "platform": "depop"
}

{
  "id": "lst_002",
  "title": "Y2K Baby Tee \u2014 Butterfly Print",
  "description": "Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.",
  "category": "tops",
  "style_tags": [
    "y2k",
    "vintage",
    "graphic tee",
    "cottagecore"
  ],
  "size": "S/M",
  "condition": "excellent",
  "price": 18.0,
  "colors": [
    "white",
    "pink",
    "purple"
  ],
  "brand": null,
  "platform": "depop"
}

{
  "id": "lst_003",
  "title": "Oversized Flannel Shirt \u2014 Plaid Red/Black",
  "description": "Classic oversized flannel. Great layering piece. A few tiny pulls in the fabric but nothing visible when worn.",
  "category": "tops",
  "style_tags": [
    "grunge",
    "vintage",
    "flannel",
    "streetwear",
    "layering"
  ],
  "size": "XL (oversized)",
  "condition": "good",
  "price": 22.0,
  "colors": [
    "red",
    "black"
  ],
  "brand": "Woolrich",
  "platform": "thredUp"
}

{
  "id": "lst_004",
  "title": "90s Track Jacket \u2014 Navy/White Stripe",
  "description": "Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight \u2014 great for layering.",
  "category": "outerwear",
  "style_tags": [
    "90s",
    "vintage",
    "athletic",
    "streetwear"
  ],
  "size": "M",
  "condition": "excellent",
  "price": 45.0,
  "colors": [
    "navy",
    "white"
  ],
  "brand": "Champion",
  "platform": "poshmark"
}

{
  "id": "lst_005",
  "title": "Corduroy Wide-Leg Pants \u2014 Rust",
  "description": "Beautiful rust-colored cords in a wide-leg silhouette. High-waisted. Minor pilling on the seat but otherwise great condition.",
  "category": "bottoms",
  "style_tags": [
    "vintage",
    "cottagecore",
    "70s",
    "earth tones"
  ],
  "size": "W28",
  "condition": "good",
  "price": 32.0,
  "colors": [
    "rust",
    "orange"
  ],
  "brand": null,
  "platform": "depop"
}

{
  "id": "lst_006",
  "title": "Graphic Tee \u2014 2003 Tour Bootleg Style",
  "description": "Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.",
  "category": "tops",
  "style_tags": [
    "graphic tee",
    "vintage",
    "grunge",
    "streetwear",
    "band tee"
  ],
  "size": "L",
  "condition": "good",
  "price": 24.0,
  "colors": [
    "black"
  ],
  "brand": null,
  "platform": "depop"
}

(.venv) myathomas@Myas-MacBook-Pro ai201-project2-fitfindr-starter-v2026 % python app.py ask 'vintage graphic tee under $30'

  The planning loop isn't built yet — see the TODO in agent.py.

0 model calls this session
(.venv) myathomas@Myas-MacBook-Pro ai201-project2-fitfindr-starter-v2026 % python - <<'PY'
from tools import search_listings, suggest_outfit, create_fit_card
print('search_listings ->', search_listings('graphic tee', max_price=30))
print('suggest_outfit ->', suggest_outfit({'title':'demo'}, {'items': []}))
print('create_fit_card ->', create_fit_card({'title':'demo'}, {'title':'demo'}))
PY

search_listings -> []
suggest_outfit -> 
create_fit_card -> 
(.venv) myathomas@Myas-MacBook-Pro ai201-project2-fitfindr-starter-v2026 % python app.py fields  
A listing has these fields:

  id             str    lst_001
  title          str    Vintage Levi's 501 Jeans — Medium Wash
  description    str    Classic 501s in a perfect medium wash. Some light fading a…
  category       str    bottoms
  style_tags     list   ['vintage', 'classic', 'denim', 'streetwear']
  size           str    W30 L30
  condition      str    good
  price          float  38.0
  colors         list   ['blue', 'indigo']
  brand          str    Levi's
  platform       str    depop

A wardrobe item has these fields:

  id             str    w_001
  name           str    Baggy straight-leg jeans, dark wash
  category       str    bottoms
  colors         list   ['dark blue', 'indigo']
  style_tags     list   ['denim', 'streetwear', 'baggy']
  notes          str    High-waisted, sits above the hip

These are what search_listings can filter on. Read a few whole listings
with `python app.py listings` before you write it.
(.venv) myathomas@Myas-MacBook-Pro ai201-project2-fitfindr-starter-v2026 % python app.py examples 
Queries worth trying:

  python app.py ask 'vintage graphic tee under $30'
  python app.py ask '90s track jacket in size M'
  python app.py ask 'silk slip dress in midi length under $40'
  python app.py ask 'platform sneakers size 8'
  python app.py ask 'denim jacket under $50'

**One full query**

```
 python app.py ask 'designer ballgown size XXS under $5'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

What I asked for: I asked AI to help me understand the requirements for the three FitFindr tools and turn the starter-code specifications into clear Tool Inventory descriptions.

What came back: AI explained what each tool takes as input, what it should return, and what should happen when there are no results or the wardrobe is empty.

What I changed: I used those explanations to write specific return values and empty cases in my README instead of using vague descriptions such as “returns a list.”

**Moment 2**
What I asked for: I asked AI to help me understand how the planning loop should branch when search_listings returns no results.

What came back: AI explained that the empty list should be checked before calling suggest_outfit, and that the session should contain an error message explaining what the user could change.

What I changed: I used that explanation to define my branch rule and make session["search_results"] the value the loop checks before deciding whether to continue or stop.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
