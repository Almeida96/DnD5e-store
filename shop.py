"""Seeded shop inventories from an editable local catalogue."""

import argparse
import json
import random
import sys
from pathlib import Path

RARITIES = ("mundane", "common", "uncommon", "rare", "very_rare", "legendary")
PROFILES = {
    "hamlet": ((0, 0), (0, 1), (0, 1), (0, 0), (0, 0), (0, 0)),
    "village": ((0, 0), (1, 2), (0, 3), (0, 1), (0, 0), (0, 0)),
    "large-village": ((0, 0), (1, 8), (1, 6), (0, 1), (0, 1), (0, 1)),
    "town": ((0, 0), (1, 10), (2, 8), (1, 4), (0, 1), (0, 1)),
    "city": ((0, 0), (3, 10), (5, 10), (3, 10), (0, 2), (0, 1)),
    "general": ((10, 10), (0, 1), (0, 0), (0, 0), (0, 0), (0, 0)),
    "potions": ((0, 0), (1, 10), (1, 10), (1, 10), (1, 10), (1, 10)),
}


def load_catalog(path=None):
    path = Path(path) if path else Path(__file__).with_name("catalog.json")
    with path.open("rb") as stream:
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("Catalog exceeds 1 MiB.")
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Catalog schema_version must be 1.")
    categories = data.get("categories")
    if not isinstance(categories, dict) or set(categories) != set(RARITIES):
        raise ValueError("Catalog must contain all six rarity categories.")
    result = {}
    for rarity, items in categories.items():
        if not isinstance(items, list) or len(items) > 5000:
            raise ValueError(
                "Each category must contain a list of at most 5,000 names."
            )
        if any(
            not isinstance(name, str)
            or not name.strip()
            or len(name) > 200
            or any(ord(c) < 32 for c in name)
            for name in items
        ):
            raise ValueError(
                "Item names must contain 1–200 characters without control characters."
            )
        result[rarity] = sorted(set(name.strip() for name in items))
    return result


def generate_inventory(store_type, seed=None, catalog_path=None):
    if store_type not in PROFILES:
        raise ValueError(f"Unknown store type: {store_type}.")
    if seed is not None and type(seed) is not int:
        raise ValueError("Seed must be an integer.")
    if seed is None:
        seed = random.SystemRandom().randrange(2**63)
    rng = random.Random(seed)
    catalog = load_catalog(catalog_path)
    inventory, warnings = {}, []
    for rarity, bounds in zip(RARITIES, PROFILES[store_type], strict=True):
        items = catalog[rarity]
        if store_type == "potions":
            items = [name for name in items if name.lower().startswith("potion")]
        requested = rng.randint(*bounds)
        if requested > len(items):
            warnings.append(
                f"{rarity}: requested {requested}; only {len(items)} unique items available."
            )
        inventory[rarity] = sorted(rng.sample(items, min(requested, len(items))))
    return {
        "schema_version": 1,
        "store_type": store_type,
        "seed": seed,
        "categories": inventory,
        "warnings": warnings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate an editable D&D shop inventory."
    )
    parser.add_argument("store_type", choices=PROFILES)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--catalog", type=Path)
    args = parser.parse_args(argv)
    try:
        print(
            json.dumps(
                generate_inventory(args.store_type, args.seed, args.catalog),
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
