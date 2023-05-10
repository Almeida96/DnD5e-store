#Projeto desenvolvido por Igor Almeida, qualquer modificação sem autorização terá implicações legais

import tkinter as tk
from tkinter import ttk
import sqlite3
import random


def create_common_items_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS common_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()


def insert_common_item(conn, item_name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO common_items (name) VALUES (?)
    ''', (item_name,))
    conn.commit()


def get_common_items(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM common_items')
    return [row[0] for row in cursor.fetchall()]


def create_uncommon_items_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uncommon_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()


def insert_uncommon_item(conn, item_name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO uncommon_items (name) VALUES (?)
    ''', (item_name,))
    conn.commit()


def get_uncommon_items(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM uncommon_items')
    return [row[0] for row in cursor.fetchall()]


def create_rare_items_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rare_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()


def insert_rare_item(conn, item_name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rare_items (name) VALUES (?)
    ''', (item_name,))
    conn.commit()


def get_rare_items(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM rare_items')
    return [row[0] for row in cursor.fetchall()]


def create_very_rare_items_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS very_rare_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()


def insert_very_rare_item(conn, item_name):
    c = conn.cursor()
    c.execute('''
        INSERT INTO very_rare_items (name)
        VALUES (?)
    ''', (item_name,))
    conn.commit()


def get_very_rare_items(conn):
    c = conn.cursor()
    c.execute('SELECT name FROM very_rare_items')
    return [row[0] for row in c.fetchall()]


def create_legendary_items_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS legendary_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()


def insert_legendary_item(conn, item_name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO legendary_items (name) VALUES (?)
    ''', (item_name,))
    conn.commit()


def get_legendary_items(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM legendary_items')
    return [row[0] for row in cursor.fetchall()]


def create_store_types_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS store_types (
            name TEXT PRIMARY KEY,
            mundane_min INTEGER,
            mundane_max INTEGER,
            common_min INTEGER,
            common_max INTEGER,
            uncommon_min INTEGER,
            uncommon_max INTEGER,
            rare_min INTEGER,
            rare_max INTEGER,
            very_rare_min INTEGER,
            very_rare_max INTEGER,
            legendary_min INTEGER,
            legendary_max INTEGER
        )
    ''')
    conn.commit()


def insert_store_type(conn, name, ranges):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO store_types (name, mundane_min, mundane_max, common_min, common_max, uncommon_min, uncommon_max, rare_min, rare_max, very_rare_min, very_rare_max, legendary_min, legendary_max)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, *ranges))
    conn.commit()


def generate_inventory(store_type):
    conn = sqlite3.connect('dnd_items.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM store_types WHERE name=?', (store_type,))
    store_info = cursor.fetchone()

    if store_info is None:
        print(f"Tipo de loja '{store_type}' não encontrado.")
        return

    _, mundane_min, mundane_max, common_min, common_max, uncommon_min, uncommon_max, rare_min, rare_max, very_rare_min, very_rare_max, legendary_min, legendary_max = store_info

    if store_type == "Potion Store":
        common_items = get_potion_items(conn, "common_items")
        uncommon_items = get_potion_items(conn, "uncommon_items")
        rare_items = get_potion_items(conn, "rare_items")
        very_rare_items = get_potion_items(conn, "very_rare_items")
        legendary_items = get_potion_items(conn, "legendary_items")
    else:
        cursor.execute('SELECT * FROM common_items')
        common_items = cursor.fetchall()

        cursor.execute('SELECT * FROM uncommon_items')
        uncommon_items = cursor.fetchall()

        cursor.execute('SELECT * FROM rare_items')
        rare_items = cursor.fetchall()

        cursor.execute('SELECT * FROM very_rare_items')  # Adicione esta linha
        very_rare_items = cursor.fetchall()  # Adicione esta linha

        cursor.execute('SELECT * FROM legendary_items')
        legendary_items = cursor.fetchall()

    inventory = {
        "common": random.sample(common_items, random.randint(common_min, common_max)),
        "uncommon": random.sample(uncommon_items, random.randint(uncommon_min, uncommon_max)),
        "rare": random.sample(rare_items, random.randint(rare_min, rare_max)),
        "very rare": random.sample(very_rare_items, random.randint(very_rare_min, very_rare_max)),
        "legendary": random.sample(legendary_items, random.randint(legendary_min, legendary_max))
    }

    # Print the inventory grouped by item type
    for item_type, items in inventory.items():
        print(f"\n{item_type.title()} Items:")
        for item in items:
            print(item[1])  # item[1] is the item name

    conn.close()

    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, "Lojinha da Baderna\n\n")
    for item_type, items in inventory.items():
        text_area.insert(tk.END, f"{item_type.capitalize()} Items:\n")
        for item in items:
            text_area.insert(tk.END, f"{item[1]}\n")
        text_area.insert(tk.END, "\n")
    return inventory

def get_potion_items(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name} WHERE name LIKE "%Potion%"')
    return cursor.fetchall()


# Banco de dados
conn = sqlite3.connect('dnd_items.db')

# Criar tabelas
create_common_items_table(conn)
create_uncommon_items_table(conn)
create_rare_items_table(conn)
create_very_rare_items_table(conn)
create_legendary_items_table(conn)
create_store_types_table(conn)

# Inserir itens comuns, incomuns e raros
common_items = [
    "Armor of Gleaming", "Bead of Nourishment", "Bead of Refreshment",
    "Boots of False Tracks", "Candle of the Deep", "Cast-off Armor",
    "Charlatan's Die", "Cloak of Billowing", "Cloak of Many Fashions",
    "Clockwork Amulet", "Clothes of Mending", "Dark Shard Amulet",
    "Dread Helm", "Ear Horn of Hearing", "Enduring Spellbook", "Ersatz Eye",
    "Hat of Vermin", "Hat of Wizardry", "Heward's Handy Spice Pouch",
    "Horn of Silent Alarm", "Illuminator's Tattoo", "Instrument of Illusions",
    "Instrument of Scribing", "Lock of Trickery", "Masquerade Tattoo",
    "Moon-touched Sword", "Mystery Key", "Orb of Direction",
    "Orb of Time", "Perfume of Bewitching", "Pipe of Smoke Monsters",
    "Pole of Angling", "Pole of Collapsing", "Pot of Awakening",
    "Potion of Climbing", "Potion of Healing", "Prosthetic Limb",
    "Rope of Mending", "Ruby of the War Mage", "Shield of Expression",
    "Smoldering Armor", "Spell Scroll", "Spellwrought Tattoo",
    "Staff of Adornment", "Staff of Birdcalls", "Staff of Flowers",
    "Talking Doll", "Tankard of Sobriety", "Unbreakable Arrow",
    "Veteran's Cane", "Walloping Ammunition", "Wand of Conducting",
    "Wand of Pyrotechnics", "Wand of Scowls", "Wand of Smiles"
]

uncommon_items = [
    "Adamantine Chain shirt - Armor - 550 gp",
    "Adamantine Armor - 700 gp",
    "Alchemy Jug - Wondrous - 6000 gp",
    "Ammunition +1",
    "Amulet of Proof Against Detection and Location - Wondrous - 20.000 gp",
    "Amulet of the Devout",
    "Amulet of the Drunkard",
    "Arcane Grimoire",
    "Bag of Bounty",
    "Bag of Holding - Wondrous - 4.000 gp",
    "Bag of Tricks",
    "Balance of Harmony",
    "Ballon Pack",
    "Barrier Tattoo",
    "Blood of the Lycanthrope Antidote",
    "Blood Spear",
    "Bloodwell Vial",
    "Boomerang +1",
    "Boots of Elvenkind - Wondrous - 2.500 gp",
    "Boots of Striding and Springing - Wondrous - 5.000 gp",
    "Boots of the Winterlands - Wondrous - 10.000 gp",
    "Bottle Breath",
    "Bracers of Archery - Wondrous - 1.500 gp",
    "Brooch of Living Essence",
    "Brooch of Shielding - Wondrous - 7.500 gp",
    "Broom of Flying - Wondrous - 8.000 gp",
    "Cap of Water Breathing - Wondrous - 1.000 gp",
    "Circlet of Blasting - Wondrous - 1.500 gp",
    "Circlet of Human Perfection",
    "Cloak of Elvenkind - Wondrous - 5.000 gp",
    "Cloak of Protection - Wondrous - 3.500 gp",
    "Cloak of the Manta Ray - Wondrous - 6.000 gp",
    "Coiling Grasp Tattoo",
    "Cracked Driftglobe",
    "Crown of the Forest",
    "Cursed Luckstone",
    "Dagger of Warning - Weapon - 60.100 gp",
    "Decanter of Endless Water - Wondrous - 135.000 gp",
    "Deck of Illusions - Wondrous - 6.120 gp",
    "Dragon Vessel",
    "Dragon's Wrath Weapon",
    "Dragonhide Belt",
    "Dragon-Touched Focus",
    "Driftglobe - Wondrous - 750 gp",
    "Dust of Corrosion",
    "Dust of Deliciousness",
    "Dust of Disappearance - Wondrous - 300 gp",
    "Dust of Dryness (1 pellet) - Wondrous - 120 gp",
    "Dust of Sneezing and Choking - Wondrous - 480 gp",
    "Earworm",
    "Efficient Quiver",
    "Elder Cartographer's Glossography",
    "Eldritch Claw Tattoo",
    "Elemental Gem - Wondrous - 950 gp",
    "Emerald Pen",
    "Eversmoking Bottle - Wondrous - 1.000 gp",
    "Eyes of Charming - Wondrous - 3.000 gp",
    "Eyes of Minute Seeing - Wondrous - 2.500 gp",
    "Eyes of the Eagle - Wondrous - 2.500 gp",
    "Feywild Shard",
    "Figurine of Wondrous Power",
    "Finder's Goggles",
    "Gauntlets of Ogre Power - Wondrous - 8.000 gp",
    "Gem of Brightness",
    "Gloves of Missile Snaring - Wondrous - 3.000 gp",
    "Gloves of Swimming and Climbing - Wondrous - 2.000 gp",
    "Gloves of Thievery - Wondrous - 5.000 gp",
    "Greatsword +1 - Weapon - 1.050 gp",
    "Greatsword of Warning - Weapon - 60.100 gp",
    "Greatclub of Warning - Weapon - 60.000 gp",
    "Goggles of Night - Wondrous - 1.500 gp",
    "Goggles of Object Reading",
    "Guardian Emblem",
    "Guild Keyrune",
    "Guild Signet",
    "Harkon's Bite",
    "Hat of Disguise",
    "Headband of Intellect - Wondrous - 8.000 gp",
    "Hellfire Weapon",
    "Helm of Comprehend Languages - Wondrous - 500 gp",
    "Helm of Telepathy - Wondrous - 12.000 gp",
    "Helm of Underwater Action",
    "Hew",
    "Immovable Rod - Rod - 5.000 gp",
    "Infernal Puzzle Box",
    "Inquisitive's Goggles",
    "Insignia of Claws",
    "Instrument of the Bards - Mac-Fuirmidh Cittern - Wondrous - 27.000 gp",
    "Instrument of the Bards - Fochlucan Bandore - Wondrous - 26.500 gp",
    "Instrument of the Bards - Doss Lute - Wondrous - 28.500 gp",
    "Javelin of Lightning - Weapon - 1.500 gp",
    "Keoghtom's Ointment (per dose) - Wondrous - 120 gp",
    "Lantern of Revealing - Wondrous - 5.000 gp",
    "+1 Lance - Weapon - 1.010 gp",
    "Lightbringer",
    "Light Hammer of Warning - Weapon - 60.100 gp",
    "Living Gloves",
    "Lorehold Primer",
    "Mace +1 - Weapon - 1.010 gp",
    "Mariner's Chain shirt - Armor - 1.550 gp",
    "Mask of the Beast",
    "Medallion of Thoughts - Wondrous - 3.000 gp",
    "Mind Carapace Armor",
    "Mithral Chain shirt - Armor - 850 gp",
    "Mithral Scale mail - Armor - 850 gp",
    "Mizzium Apparatus",
    "Moon Sickle",
    "Mummy Rot Antidote",
    "Nature's Mantle",
    "Necklace of Adaption - Wondrous - 1.500 gp",
    "Night Caller",
    "Oil of Slipperiness",
    "Orc Stone",
    "Paper Bird",
    "Pearl of Power - Wondrous - 6.000 gp",
    "Periapt of Health - Wondrous - 5.000 gp",
    "Periapt of Wound Closure - Wondrous - 5.000 gp",
    "Philter of Love - Wondrous - 90 gp",
    "Pipes of Haunting - Wondrous - 6.000 gp",
    "Pipes of the Sewers - Wondrous - 2.000 gp",
    "Piwafwi (Cloak of Elvenkind)",
    "Pixie Dust",
    "Potion of Advantage",
    "Potion of Animal Friendship - Potion - 200 gp",
    "Potion of Fire Breath - Potion - 150 gp",
    "Potion of Giant Strength",
    "Potion of Growth - Potion - 270 gp",
    "Potion of Healing - Potion - 50 gp",
    "Potion of Poison - Potion - 100 gp",
    "Potion of Resistance against Cold - Potion - 300 gp",
    "Potion of Water Breathing - Potion - 180 gp",
    "Prismari Primer",
    "Propeller Helm",
    "Psi Crystal",
    "Pyroconverger",
    "Quandrix Primer",
    "Quiver of Ehlonna - Wondrous - 1.000 gp",
    "Restorative Ointment",
    "Rhythm-Maker's Drum",
    "Ring of Jumping - Ring - 2.500 gp",
    "Ring of Mind Shielding - Ring - 16.000 gp",
    "Ring of Obscuring",
    "Ring of Swimming - Ring - 3.000 gp",
    "Ring of Truth Telling",
    "Ring of Warmth - Ring - 1.000 gp",
    "Ring of Water Walking - Ring - 1.500 gp",
    "Rings of Shared Suffering",
    "Robe os Serpents",
    "Robe of Useful Items (13 special patches) - Wondrous - 13.200 gp",
    "Rod of Retribution",
    "Rod of the Pact Keeper",
    "Rope of Climbing - Wondrous - 2.000 gp",
    "Saddle of the Cavalier - Wondrous - 2.000 gp",
    "Scaled Ornament",
    "Seeker Dart",
    "Sending Stones - Wondrous - 2.000 gp",
    "Sentinel Shield - Armor - 20.000 gp",
    "Serpent Scale Armor",
    "Scroll of Crusader’s Mantle - Scroll - 400 gp",
    "Scroll of Hunger of Hadar - Scroll - 400 gp",
    "Scroll of Hypnotic Pattern - Scroll - 400 gp",
    "Scroll of Scorching Ray - Scroll - 240 gp",
    "Scroll of Spike Growth - Scroll - 240 gp",
    "Scroll of Catnap - Scroll - 400 gp",
    "Scroll of Conjure Animals - Scroll - 400 gp",
    "Scroll of Haste - Scroll - 400 gp",
    "Scroll of Branding Smite - Scroll - 240 gp",
    "Scroll of Meld into Stone - Scroll - 400 gp",
    "Scroll of Nondetection - Scroll - 400 gp",
    "Scroll of Bestow Curse - Scroll - 400 gp",
    "Scroll of Prayer of Healing - Scroll - 240 gp",
    "Scroll of Sending - Scroll - 400 gp",
    "Shatterspike",
    "+1 Shield - Armor - 1.500 gp",
    "Shortsword +1 - Weapon - 1.010 gp",
    "Shortsword of Warning - Weapon - 60.100 gp",
    "Silverquill Primer",
    "Skyblinder Staff",
    "Sling of Warning - Weapon - 60.000 gp",
    "Slippers of Spider Climbing - Wondrous - 5.000 gp",
    "Smokepowder",
    "Soul Coin",
    "Spear +1 - Weapon - 1.010 gp",
    "Spear of Warning - Weapon - 60.100 gp",
    "Spell Gem (Lapis Lazuli)",
    "Spell Gem (Obsidian)",
    "Spellwrought Tattoo",
    "Spies' Murmur",
    "Staff of the Adder - Staff - 1.800 gp",
    "Staff of the Python - Staff - 2.000 gp",
    "Luckstone - Wondrous - 4.200 gp",
    "Stone of ill luck",
    "Storm Boomerang",
    "Sword of Vengeance",
    "Thessaltoxin Antidote",
    "Travel Alchemical Kit",
    "Trident +1 - Weapon - 1.010 gp",
    "Trident of Fish Command - Wondrous - 800 gp",
    "Uncommon Glamerweave",
    "Wand of Entangle",
    "Wand of Magic Detection - Wand - 1.500 gp",
    "Wand of Magic Missiles - Wand - 8.000 gp",
    "Wand of Secrets - Wand - 1.500 gp",
    "Wand of the War Mage +1 - Wand - 1.200 gp",
    "Wand of Web - Wand - 8.000 gp",
    "Weapon of Warning",
    "Wheel of Wind and Water",
    "Wildspace Orrery",
    "Wand of the War Mage +1 - Wand - 1.200 gp",
    "Winged Boots - Wondrous - 8.000 gp",
    "Wingwear",
    "Winter's Dark Bite",
    "Whiterbloom Primer",
    "Yklwa +1"
]

rare_items = [
    "Alchemical Compendium", "All-Purpose Tool", "Ammunition +1, +2, or +3", "Amulet of Health", "Amulet of the Devout",
    "Arcane Grimoire", "Armor +1, +2, or +3", "Armor of Resistance", "Armor of Vulnerability", "Arrow-Catching Shield",
    "Astral Shard", "Astromancy Archive", "Atlas of Endless Horizons", "Bag of Beans", "Barrier Tattoo",
    "Bead of Force", "Bell Branch", "Belt of Dwarvenkind", "Belt of Giant Strength", "Berserker Axe",
    "Bloodwell Vial", "Boots of Levitation", "Boots of Speed", "Bowl of Commanding Water Elementals", "Bracers of Defense",
    "Brazier of Commanding Fire Elementals", "Cape of the Mountebank", "Censer of Controlling Air Elementals", "Chime of Opening", "Cloak of Displacement",
    "Cloak of the Bat", "Cube of Force", "Daern's Instant Fortress", "Dagger of Venom", "Devotee's Censer",
    "Dimensional Shackles", "Dragon Slayer", "Duplicitous Manuscript", "Elemental Essence Shard", "Elixir of Health",
    "Elven Chain", "Far Realm Shard", "Figurine of Wondrous Power", "Flame Tongue", "Folding Boat",
    "Fulminating Treatise", "Gem of Seeing", "Giant Slayer", "Glamoured Studded Leather", "Heart Weaver's Primer",
    "Helm of Teleportation", "Heward's Handy Haversack", "Horn of Blasting", "Horn of Valhalla", "Horseshoes of Speed",
    "Instrument of the Bards", "Ioun Stone", "Iron Bands of Bilarro", "Libram of Souls and Flesh", "Lyre of Building",
    "Mace of Disruption", "Mace of Smiting", "Mace of Terror", "Mantle of Spell Resistance", "Moon Sickle",
    "Necklace of Fireballs", "Necklace of Prayer Beads", "Oil of Etherealness", "Outer Essence Shard", "Periapt of Proof against Poison",
    "Planecaller's Codex", "Portable Hole", "Potion of Clairvoyance", "Potion of Diminution", "Potion of Gaseous Form",
    "Potion of Giant Strength", "Potion of Healing", "Potion of Heroism", "Potion of Invulnerability", "Potion of Mind Reading",
    "Protective Verses", "Quaal's Feather Token", "Reveler's Concertina", "Rhythm-Maker's Drum", "Ring of Animal Influence",
    "Ring of Evasion", "Ring of Feather Falling", "Ring of Free Action", "Ring of Poison Resistance", "Ring of Protection",
    "Ring of Resistance", "Ring of Spell Storing", "Ring of the Ram", "Ring of X-ray Vision", "Robe of Eyes",
    "Rod of Rulership", "Rod of the Pact Keeper", "Rope of Entanglement", "Scroll of Protection", "Shadowfell Brand Tattoo",
    "Shadowfell Shard", "Shield of Missile Attraction", "Shield, +1, +2, or +3", "Spell Scroll", "Spellwrought Tattoo", "Staff of Charming", "Staff of Healing",
    "Staff of Swarming Insects", "Staff of the Woodlands", "Staff of Withering", "Stone of Controlling Earth Elementals", "Sun Blade",
    "Sword of Life Stealing", "Sword of Wounding", "Tentacle Rod", "Vicious Weapon", "Wand of Binding",
    "Wand of Enemy Detection", "Wand of Fear", "Wand of Fireballs", "Wand of Lightning Bolts", "Wand of Paralysis",
    "Wand of the War Mage +1, +2, or +3", "Wand of Wonder", "Weapon +1, +2, or +3", "Wings of Flying"
]

very_rare_items = [
    "Absorbing Tattoo", "All-Purpose Tool", "Amethyst Lodestone",
    "Ammunition +1, +2, or +3", "Amulet of the Devout", "Amulet of the Planes",
    "Animated Shield", "Arcane Grimoire", "Armor +1, +2, or +3",
    "Arrow of Slaying", "Bag of Devouring", "Barrier Tattoo",
    "Belt of Giant Strength", "Bloodwell Vial", "Candle of Invocation",
    "Carpet of Flying", "Cauldron of Rebirth", "Cloak of Arachnida",
    "Crystal Ball", "Crystalline Chronicle", "Dancing Sword",
    "Demon Armor", "Dragon Scale Mail", "Dwarven Plate", "Dwarven Thrower",
    "Efreeti Bottle", "Figurine of Wondrous Power", "Frost Brand",
    "Ghost Step Tattoo", "Helm of Brilliance", "Horn of Valhalla",
    "Horseshoes of a Zephyr", "Instrument of the Bards", "Ioun Stone",
    "Lifewell Tattoo", "Manual of Bodily Health", "Manual of Gainful Exercise",
    "Manual of Golems", "Manual of Quickness of Action",
    "Mirror of Life Trapping", "Moon Sickle", "Nine Lives Stealer",
    "Nolzur's Marvelous Pigments", "Oathbow", "Oil of Sharpness",
    "Potion of Flying", "Potion of Giant Strength", "Potion of Healing",
    "Potion of Invisibility", "Potion of Longevity", "Potion of Speed",
    "Potion of Vitality", "Rhythm-Maker's Drum", "Ring of Regeneration",
    "Ring of Shooting Stars", "Ring of Telekinesis",
    "Robe of Scintillating Colors", "Robe of Stars", "Rod of Absorption",
    "Rod of Alertness", "Rod of Security", "Rod of the Pact Keeper",
    "Sapphire Buckler", "Scimitar of Speed", "Shield, +1, +2, or +3",
    "Spell Scroll", "Spellguard Shield", "Staff of Fire", "Staff of Frost",
    "Staff of Power", "Staff of Striking", "Staff of Thunder and Lightning",
    "Sword of Sharpness", "Tome of Clear Thought",
    "Tome of Leadership and Influence", "Tome of Understanding",
    "Wand of Polymorph", "Wand of the War Mage +1, +2, or +3",
    "Weapon +1, +2, or +3"
]

legendary_items = [
    "Apparatus of Kwalish",
    "Armor +1, +2, or +3",
    "Armor of Invulnerability",
    "Belt of Giant Strength",
    "Blackrazor",
    "Blood Fury Tattoo",
    "Cloak of Invisibility",
    "Crystal Ball",
    "Cubic Gate",
    "Deck of Many Things",
    "Defender",
    "Efreeti Chain",
    "Flail of Tiamat",
    "Gold Canary Figurine of Wondrous Power",
    "Hammer of Thunderbolts",
    "Holy Avenger",
    "Horn of Valhalla",
    "Instrument of the Bards",
    "Ioun Stone",
    "Iron Flask",
    "Luck Blade",
    "Moonblade",
    "Plate Armor of Etherealness",
    "Platinum Scarf",
    "Potion of Dragon's Majesty",
    "Potion of Giant Strength",
    "Ring of Djinni Summoning",
    "Ring of Elemental Command",
    "Ring of Invisibility",
    "Ring of Spell Turning",
    "Ring of Three Wishes",
    "Robe of the Archmagi",
    "Rod of Lordly Might",
    "Rod of Resurrection",
    "Ruby Weave Gem",
    "Scarab of Protection",
    "Sovereign Glue",
    "Spell Scroll",
    "Sphere of Annihilation",
    "Staff of the Magi",
    "Sword of Answering",
    "Talisman of Pure Good",
    "Talisman of the Sphere",
    "Talisman of Ultimate Evil",
    "Tome of the Stilled Tongue",
    "Topaz Annihilator",
    "Universal Solvent",
    "Vorpal Sword",
    "Wave",
    "Well of Many Worlds",
    "Whelm"
]

for item in common_items:
    insert_common_item(conn, item)

for item in uncommon_items:
    insert_uncommon_item(conn, item)

for item in rare_items:
    insert_rare_item(conn, item)

for item in very_rare_items:
    insert_very_rare_item(conn, item)

for item in legendary_items:
    insert_legendary_item(conn, item)

# Inserir tipos de lojas
store_types = {
    "Loja de Vila": (0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0),
    "Loja de Pequeno vilarejo": (0, 0, 1, 2, 0, 3, 0, 1, 0, 0, 0, 0),
    "Loja de Grande Vilarejo": (0, 0, 1, 8, 1, 6, 0, 1, 0, 1, 0, 1),
    "Loja de pequena cidade": (0, 0, 1, 10, 2, 8, 1, 4, 0, 1, 0, 1),
    "Loja de Grande Cidade": (0, 0, 3, 10, 5, 10, 3, 10, 0, 2, 0, 1),
    "Loja Geral": (10, 10, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    "Potion Store": (0, 0, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10)  # Adicionando a Potion Store aqui.
}

for store_name, ranges in store_types.items():
    insert_store_type(conn, store_name, ranges)

conn.close()


# Interface gráfica
app = tk.Tk()
app.title("Loja de Itens Mágicos D&D 5e")

# Configurar colunas e linhas para expandir
app.grid_rowconfigure(0, weight=0)  # Não permita que a linha 0 (botões) expanda
app.grid_rowconfigure(1, weight=1)  # Permita que a linha 1 (texto e scrollbar) expanda
for i in range(2):
    app.grid_columnconfigure(i, weight=1)

store_types_combobox = ttk.Combobox(app, values=list(store_types.keys()))
store_types_combobox.grid(column=0, row=0, sticky="new")

scrollbar = tk.Scrollbar(app)  # Crie a barra de rolagem
scrollbar.grid(column=2, row=1, sticky="nsw")

text_area = tk.Text(app, font=("JMH Typewriter", 12), yscrollcommand=scrollbar.set)  # Configure o comando de rolagem
text_area.grid(column=0, row=1, sticky="nsew", columnspan=2)

scrollbar.config(command=text_area.yview)  # Configure o comando de visualização da barra de rolagem

# Definir a tag 'bold'
text_area.tag_configure('bold', font=("JMH Typewriter", 12, 'bold'))

def show_inventory():
    inventory = generate_inventory(store_types_combobox.get())
    text_area.delete('1.0', tk.END)  # limpar o conteúdo existente
    for category, items in inventory.items():
        start_index = text_area.index(tk.END)  # pegar o índice de início antes de inserir o texto
        text_area.insert(tk.END, f"{category.capitalize()} Items:\n", 'bold')  # aplicar a tag 'bold'
        for _, item_name in items:
            text_area.insert(tk.END, f"{item_name}\n")
        text_area.insert(tk.END, "\n")

generate_button = tk.Button(app, text="Gerar Inventário", command=show_inventory)
generate_button.grid(column=1, row=0, sticky="new")

app.mainloop()
