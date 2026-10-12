"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from generate import ModelUnavailable
from mcp_client import call_tool
from tools import create_fit_card, suggest_outfit


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """Fresh session for one user interaction."""
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


def _parse_query(query: str) -> dict:
    cleaned = (query or "").strip()
    if not cleaned:
        return {"description": "", "size": None, "max_price": None}

    size_match = re.search(r"(?:size|in size|sz)\s*([A-Za-z0-9/]+)", cleaned, flags=re.I)
    size = size_match.group(1).strip() if size_match else None
    if size_match:
        cleaned = re.sub(r"(?:size|in size|sz)\s*[A-Za-z0-9/]+", "", cleaned, flags=re.I)

    price_match = re.search(r"(?:under|below|budget|up to|max(?:imum)?|\$)\s*\$?(\d+(?:\.\d+)?)", cleaned, flags=re.I)
    max_price = float(price_match.group(1)) if price_match else None
    if price_match:
        cleaned = re.sub(r"(?:under|below|budget|up to|max(?:imum)?|\$)\s*\$?(\d+(?:\.\d+)?)", "", cleaned, flags=re.I)

    description = re.sub(r"\s+", " ", cleaned).strip(" ,.-")
    if not description:
        description = (query or "").strip()
    return {"description": description, "size": size, "max_price": max_price}


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """Run the loop once and return the finished session."""
    trace.start_trace()
    session = new_session(query, wardrobe)
    iteration = 0

    parsed = _parse_query(query)
    session["parsed"] = parsed
    description = parsed["description"]
    size = parsed["size"]
    max_price = parsed["max_price"]

    while True:
        iteration += 1
        trace.check_iterations(iteration)

        if not description:
            session["error"] = "I couldn't tell what item you want. Try adding a clearer description like 'vintage graphic tee' or 'denim jacket'."
            break

        results = call_tool("search_listings", {
            "description": description,
            "size": size,
            "max_price": max_price,
        })
        session["search_results"] = results
        trace.step(
            "search_listings (via MCP)",
            inputs={"description": description, "size": size, "max_price": max_price},
            returned=results,
            note="branch: empty search stops here" if not results else "results found, continue",
        )

        if not results:
            session["error"] = (
                f"No items matched '{description}'"
                + (f" in size {size}" if size else "")
                + (f" under ${max_price}" if max_price is not None else "")
                + ". Try broadening the description, changing the size, or raising the budget."
            )
            break

        selected = results[0]
        session["selected_item"] = selected
        trace.step(
            "select_first_result",
            inputs={"search_results_count": len(results)},
            returned=selected,
        )

        try:
            outfit = suggest_outfit(selected, wardrobe)
            session["outfit_suggestion"] = outfit
            trace.step(
                "suggest_outfit",
                inputs={"item": selected.get("title"), "wardrobe_items": len((wardrobe or {}).get("items") or [])},
                returned=outfit,
            )
        except ModelUnavailable as exc:
            session["error"] = str(exc)
            trace.step("suggest_outfit", inputs={"item": selected.get("title")}, returned=None, note=str(exc))
            break

        try:
            card = create_fit_card(outfit, selected)
            session["fit_card"] = card
            trace.step(
                "create_fit_card",
                inputs={"item": selected.get("title")},
                returned=card,
            )
        except ModelUnavailable as exc:
            session["error"] = str(exc)
            trace.step("create_fit_card", inputs={"item": selected.get("title")}, returned=None, note=str(exc))
            break

        return session

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
