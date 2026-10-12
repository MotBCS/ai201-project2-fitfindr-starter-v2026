"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
import re
from collections import Counter

from generate import generate
from utils.data_loader import load_listings


SIZE_ALIASES = {"xs": "xs", "s": "s", "m": "m", "l": "l", "xl": "xl", "xxl": "xxl"}


def _normalise(text: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _size_matches(query_size: str | None, listing_size: str | None) -> bool:
    if query_size is None:
        return True
    q = _normalise(query_size)
    if not q or not listing_size:
        return False
    listing = _normalise(listing_size)
    if not listing:
        return False
    # size strings often escape with separators like "S/M", "W30 L30", or "XL (oversized)"
    candidate_tokens = set(re.findall(r"[a-z]+|\d+", listing))
    # Direct match for common clothing sizes and slash ranges.
    if q in candidate_tokens:
        return True
    if re.search(rf"(?<![a-z]){re.escape(q)}(?![a-z])", listing):
        return True
    if q in SIZE_ALIASES and any(token in SIZE_ALIASES for token in candidate_tokens):
        return q in candidate_tokens or q in listing.replace("/", " ").split()
    return False


def _score_item(description: str, item: dict) -> int:
    search_terms = [t for t in re.findall(r"[a-z0-9]+", (description or "").lower()) if len(t) > 2]
    if not search_terms:
        return 1
    haystack = " ".join(
        [
            item.get("title", ""),
            item.get("description", ""),
            item.get("category", ""),
            " ".join(item.get("style_tags") or []),
            " ".join(item.get("colors") or []),
            item.get("brand") or "",
            item.get("size") or "",
        ]
    ).lower()
    counts = Counter(re.findall(r"[a-z0-9]+", haystack))
    score = 0
    for term in search_terms:
        score += counts.get(term, 0)
        if term in {"tee", "shirt", "dress", "jacket", "jeans", "pants", "sneaker"}:
            score += 1
    return score


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    Returns a list of listing dicts in descending relevance order.
    """
    if not description or not description.strip():
        return []

    matches = []
    for item in load_listings():
        if max_price is not None and item.get("price") is not None and float(item["price"]) > float(max_price):
            continue
        if not _size_matches(size, item.get("size")):
            continue
        score = _score_item(description, item)
        if score <= 0:
            continue
        matches.append((score, item))

    matches.sort(key=lambda pair: (-pair[0], float(pair[1].get("price", 0))))
    results = [item for _, item in matches[: config.SEARCH_RESULT_LIMIT]]
    return results


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.
    """
    if not new_item:
        return "Choose an item first, then I can suggest an outfit."

    if not wardrobe or not wardrobe.get("items"):
        prompt = (
            "You are a helpful fashion stylist. Give 2 concise outfit ideas for this thrifted item: "
            f"{new_item.get('title')} ({new_item.get('category')}, {new_item.get('color', '')}). "
            "The user has no saved wardrobe pieces, so keep the advice general and wearable."
        )
        return generate(prompt, system="You are a fashion stylist.", cache=True)

    wardrobe_items = wardrobe["items"]
    wardrobe_lines = []
    for idx, item in enumerate(wardrobe_items[:10], 1):
        wardrobe_lines.append(
            f"{idx}. {item.get('name') or item.get('category') or 'Wardrobe item'} "
            f"({item.get('category')}, colors: {', '.join(item.get('colors') or [])})"
        )

    prompt = (
        "You are a helpful fashion stylist. Suggest 2 outfit combinations using the user's existing wardrobe and this new item. "
        f"New item: {new_item.get('title')} ({new_item.get('category')}, price ${new_item.get('price')}, size {new_item.get('size')}).\n"
        "Wardrobe:\n" + "\n".join(wardrobe_lines) + "\nGive specific pairing suggestions that mention the existing items by name."
    )
    return generate(prompt, system="You are a fashion stylist.", cache=True)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.
    """
    if not outfit or not str(outfit).strip():
        return (
            f"Found this {new_item.get('title', 'piece')} for ${new_item.get('price')} on {new_item.get('platform', 'the marketplace')} — "
            "a perfect thrift score for a casual outfit."
        )

    title = new_item.get("title", "this piece")
    price = new_item.get("price")
    platform = new_item.get("platform", "the marketplace")
    brand = new_item.get("brand") or ""
    prompt = (
        "Write a short social post caption, 2-4 sentences long, in a lively thrift-shopping voice. "
        f"Item: {title}. Brand: {brand or 'unknown'}. Price: ${price}. Platform: {platform}. "
        f"Outfit idea: {outfit}. Mention the vibe and the item, price, and platform once each."
    )
    return generate(prompt, system="You write short, natural social captions.", cache=True)
