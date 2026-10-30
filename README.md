# D&D 5e shop inventories

Generate a shop's stock from a settlement profile and a local item catalogue. Inventories can be reproduced with a seed and exported as JSON.

## Run

Requires Python 3.11+. The desktop interface also requires Tkinter.

```sh
python db.py
python shop.py city --seed 42
python shop.py potions --seed 42 > inventory.json
```

Profiles: `hamlet`, `village`, `large-village`, `town`, `city`, `general`, and `potions`. The output includes the seed even when one was generated automatically. Reuse it with the same catalogue and version to reproduce the selection.

## Inventory rules

Each profile defines minimum and maximum quantities for six categories: mundane, common, uncommon, rare, very rare and legendary. Selection is without replacement within each category. If a catalogue has fewer items than requested, all available items are returned and a shortage warning is included.

The general store now includes mundane supplies. The potion profile filters every rarity to potion names; it cannot accidentally produce weapons or armor.

Settlement quantities are **house-rule presets**, not an official D&D purchasing table. The legacy catalogue contains item names from multiple sources and some names shared across rarity variants. It does not provide stat blocks, authoritative rarity validation, prices, attunement checks or rules text. Confirm a selected item's exact variant with your game reference.

## Custom catalogue

Edit a copy of [catalog.json](catalog.json), then run:

```sh
python shop.py village --seed 42 --catalog campaign-catalog.json
```

The file needs `schema_version: 1` and a `categories` object containing all six categories. Each category is a list of names. Repeated names are deduplicated before selection; empty categories are allowed. Files are limited to 1 MiB and each category to 5,000 names.

## Changes from the original script

The original app inserted its catalogue into SQLite on every start, which accumulated duplicate rows and biased future rolls. Catalogue loading is now read-only and independent of the working directory. An existing `dnd_items.db` is left untouched and is no longer required. To retain manual additions from that database, copy their names into a custom catalogue.

`db.py` remains the desktop entry point; `backup.py` delegates to it. Neither opens a window or database on import.

## Development

```sh
python -m unittest discover -s tests -v
```

Tests cover every profile, seed replay, duplicate prevention, potion filtering, small catalogues, CLI output and imports. [CI](https://github.com/Almeida96/DnD5e-store/actions/workflows/ci.yml) runs on Windows and Linux.

See [contributing](CONTRIBUTING.md) and [changes](CHANGELOG.md). No application-source license has been declared.
