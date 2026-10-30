import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from shop import PROFILES, RARITIES, generate_inventory, load_catalog


class ShopTests(unittest.TestCase):
    def test_reproducible_and_unique(self):
        first = generate_inventory("city", 42)
        self.assertEqual(first, generate_inventory("city", 42))
        for items in first["categories"].values():
            self.assertEqual(len(items), len(set(items)))

    def test_all_profiles_generate_without_database(self):
        for profile in PROFILES:
            for seed in range(20):
                self.assertEqual(
                    set(generate_inventory(profile, seed)["categories"]), set(RARITIES)
                )

    def test_general_store_has_mundane_stock(self):
        self.assertEqual(
            len(generate_inventory("general", 1)["categories"]["mundane"]), 10
        )

    def test_potion_shop_contains_only_potions(self):
        result = generate_inventory("potions", 42)
        self.assertTrue(
            all(
                name.startswith("Potion")
                for items in result["categories"].values()
                for name in items
            )
        )

    def test_small_catalog_reports_shortage(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(
                json.dumps(
                    {"schema_version": 1, "categories": {key: [] for key in RARITIES}}
                )
            )
            result = generate_inventory("general", 1, path)
            self.assertEqual(result["categories"]["mundane"], [])
            self.assertTrue(result["warnings"])

    def test_unknown_profile_and_bad_catalog_rejected(self):
        with self.assertRaises(ValueError):
            generate_inventory("missing", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text('{"schema_version":1,"categories":{}}')
            with self.assertRaises(ValueError):
                load_catalog(path)

    def test_generated_seed_can_be_replayed(self):
        result = generate_inventory("town")
        self.assertEqual(result, generate_inventory("town", result["seed"]))

    def test_cli_works_outside_repository_and_import_is_safe(self):
        script = Path("shop.py").resolve()
        with tempfile.TemporaryDirectory() as directory:
            output = subprocess.check_output(
                [sys.executable, str(script), "village", "--seed", "42"],
                cwd=directory,
                text=True,
            )
            self.assertEqual(json.loads(output)["seed"], 42)
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import db, tkinter; assert tkinter._default_root is None",
            ]
        )
        self.assertEqual(result.returncode, 0)
