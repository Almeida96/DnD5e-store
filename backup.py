import tkinter as tk
from tkinter import ttk
import sqlite3
import random

# Função para criar tabela de itens comuns
def create_common_items_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS common_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()

# Função para inserir itens comuns na tabela
def insert_common_item(conn, item_name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO common_items (name) VALUES (?)
    ''', (item_name,))
    conn.commit()

# Função para criar tabela de itens incomuns
def create_uncommon_items_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uncommon_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()

# Função para inserir itens incomuns na tabela
def insert_uncommon_item(conn, item_name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO uncommon_items (name) VALUES (?)
    ''', (item_name,))
    conn.commit()

# Função para criar tabela de tipos de lojas
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

# Função para inserir tipos de lojas na tabela
def insert_store_type(conn, name, ranges):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO store_types (name, mundane_min, mundane_max, common_min, common_max, uncommon_min, uncommon_max, rare_min, rare_max, very_rare_min, very_rare_max, legendary_min, legendary_max)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, *ranges))
    conn.commit()

# Função para gerar o inventário de uma loja
def generate_inventory(store_type):
    conn = sqlite3.connect('dnd_items.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM store_types WHERE name=?', (store_type,))
    store_info = cursor.fetchone()

    if store_info is None:
        print(f"Tipo de loja '{store_type}' não encontrado.")
        return

    _, mundane_min, mundane_max, common_min, common_max, uncommon_min, uncommon_max, rare_min, rare_max, very_rare_min, very_rare_max, legendary_min, legendary_max = store_info

    cursor.execute('SELECT * FROM common_items')
    common_items = cursor.fetchall()

    cursor.execute('SELECT * FROM uncommon_items')
    uncommon_items = cursor.fetchall()

    # Gerar inventário com base nas quantidades mínimas e máximas de cada raridade
    inventory = {
        "common": random.sample(common_items, random.randint(common_min, common_max)),
        "uncommon": random.sample(uncommon_items, random.randint(uncommon_min, uncommon_max)),
    }

    conn.close()

    return inventory

# Banco de dados
conn = sqlite3.connect('dnd_items.db')

# Criar tabelas
create_common_items_table(conn)
create_uncommon_items_table(conn)
create_store_types_table(conn)

# Inserir itens comuns e incomuns

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
    "Adamantine Armor", "Alchemy Jug", "All-Purpose Tool", "Ammunition +1, +2, or +3",
    "Amulet of Proof against Detection and Location", "Amulet of the Devout", "Arcane Grimoire", "Bag of Holding",
    "Bag of Tricks", "Barrier Tattoo", "Bloodwell Vial", "Boots of Elvenkind",
    "Boots of Striding and Springing", "Boots of the Winterlands", "Bracers of Archery", "Brooch of Shielding",
    "Broom of Flying", "Cap of Water Breathing", "Circlet of Blasting", "Cloak of Elvenkind",
    "Cloak of Protection", "Cloak of the Manta Ray", "Coiling Grasp Tattoo", "Decanter of Endless Water",
    "Deck of Illusions", "Dragonhide Belt +1, +2, or +3", "Driftglobe", "Dust of Disappearance",
    "Dust of Dryness", "Dust of Sneezing and Choking", "Eldritch Claw Tattoo", "Elemental Gem",
    "Emerald Pen", "Eversmoking Bottle", "Eyes of Charming", "Eyes of Minute Seeing",
    "Eyes of the Eagle", "Feywild Shard", "Figurine of Wondrous Power", "Gauntlets of Ogre Power",
    "Gem of Brightness", "Gloves of Missile Snaring", "Gloves of Swimming and Climbing", "Gloves of Thievery",
    "Goggles of Night", "Guardian Emblem", "Hat of Disguise", "Headband of Intellect",
    "Helm of Comprehending Languages", "Helm of Telepathy", "Immovable Rod", "Instrument of the Bards",
    "Javelin of Lightning", "Keoghtom's Ointment", "Lantern of Revealing", "Mariner's Armor",
    "Medallion of Thoughts", "Mithral Armor", "Moon Sickle", "Nature's Mantle",
    "Necklace of Adaptation", "Oil of Slipperiness", "Pearl of Power", "Periapt of Health",
    "Periapt of Wound Closure", "Philter of Love", "Pipes of Haunting", "Pipes of the Sewers",
    "Potion of Animal Friendship", "Potion of Fire Breath", "Potion of Giant Strength", "Potion of Growth",
    "Potion of Healing", "Potion of Poison", "Potion of Resistance", "Potion of Water Breathing",
    "Psi Crystal", "Quiver of Ehlonna", "Rhythm-Maker's Drum", "Ring of Jumping",
    "Ring of Mind Shielding", "Ring of Swimming", "Ring of Warmth", "Ring of Water Walking",
    "Robe of Useful Items", "Rod of the Pact Keeper", "Rope of Climbing", "Saddle of the Cavalier",
    "Sending Stones", "Sentinel Shield", "Shield, +1, +2, or +3", "Slippers of Spider Climbing",
    "Spell Scroll", "Spellwrought Tattoo", "Staff of the Adder", "Staff of the Python",
    "Stone of Good Luck (Luckstone)", "Sword of Vengeance", "Trident of Fish Command", "Wand of Magic Detection",
    "Wand of Magic Missiles", "Wand of Secrets", "Wand of the War Mage +1, +2, or +3", "Wand of Web",
    "Weapon +1, +2, or +3", "Weapon of Warning", "Wind Fan", "Winged Boots"
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


for item in common_items:
    insert_common_item(conn, item)

for item in uncommon_items:
    insert_uncommon_item(conn, item)

# Inserir tipos de lojas
store_types = {
    "Loja de Vila": (0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0),
    "Loja de Pequeno vilarejo": (0, 0, 1, 2, 0, 3, 0, 1, 0, 0, 0, 0),
    "Loja de Grande Vilarejo": (0, 0, 1, 8, 1, 6, 0, 1, 0, 1, 0, 1),
    "Loja de pequena cidade": (0, 0, 1, 10, 2, 8, 1, 4, 0, 1, 0, 1),
    "Loja de Grande Cidade": (0, 0, 3, 10, 5, 10, 3, 10, 0, 2, 0, 1),
    "Loja Geral": (10, 10, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
}

for store_name, ranges in store_types.items():
    insert_store_type(conn, store_name, ranges)

conn.close()

# Interface gráfica
app = tk.Tk()
app.title("Loja de Itens Mágicos D&D 5e")

store_types_combobox = ttk.Combobox(app, values=list(store_types.keys()))
store_types_combobox.grid(column=0, row=0)

generate_button = tk.Button(app, text="Gerar Inventário", command=lambda: print(generate_inventory(store_types_combobox.get())))
generate_button.grid(column=1, row=0)

app.mainloop()


uncommon_items = [
    "Adamantine Armor", "Alchemy Jug", "All-Purpose Tool", "Ammunition +1, +2, or +3",
    "Amulet of Proof against Detection and Location", "Amulet of the Devout", "Arcane Grimoire", "Bag of Holding",
    "Bag of Tricks", "Barrier Tattoo", "Bloodwell Vial", "Boots of Elvenkind",
    "Boots of Striding and Springing", "Boots of the Winterlands", "Bracers of Archery", "Brooch of Shielding",
    "Broom of Flying", "Cap of Water Breathing", "Circlet of Blasting", "Cloak of Elvenkind",
    "Cloak of Protection", "Cloak of the Manta Ray", "Coiling Grasp Tattoo", "Decanter of Endless Water",
    "Deck of Illusions", "Dragonhide Belt +1, +2, or +3", "Driftglobe", "Dust of Disappearance",
    "Dust of Dryness", "Dust of Sneezing and Choking", "Eldritch Claw Tattoo", "Elemental Gem",
    "Emerald Pen", "Eversmoking Bottle", "Eyes of Charming", "Eyes of Minute Seeing",
    "Eyes of the Eagle", "Feywild Shard", "Figurine of Wondrous Power", "Gauntlets of Ogre Power",
    "Gem of Brightness", "Gloves of Missile Snaring", "Gloves of Swimming and Climbing", "Gloves of Thievery",
    "Goggles of Night", "Guardian Emblem", "Hat of Disguise", "Headband of Intellect",
    "Helm of Comprehending Languages", "Helm of Telepathy", "Immovable Rod", "Instrument of the Bards",
    "Javelin of Lightning", "Keoghtom's Ointment", "Lantern of Revealing", "Mariner's Armor",
    "Medallion of Thoughts", "Mithral Armor", "Moon Sickle", "Nature's Mantle",
    "Necklace of Adaptation", "Oil of Slipperiness", "Pearl of Power", "Periapt of Health",
    "Periapt of Wound Closure", "Philter of Love", "Pipes of Haunting", "Pipes of the Sewers",
    "Potion of Animal Friendship", "Potion of Fire Breath", "Potion of Giant Strength", "Potion of Growth",
    "Potion of Healing", "Potion of Poison", "Potion of Resistance", "Potion of Water Breathing",
    "Psi Crystal", "Quiver of Ehlonna", "Rhythm-Maker's Drum", "Ring of Jumping",
    "Ring of Mind Shielding", "Ring of Swimming", "Ring of Warmth", "Ring of Water Walking",
    "Robe of Useful Items", "Rod of the Pact Keeper", "Rope of Climbing", "Saddle of the Cavalier",
    "Sending Stones", "Sentinel Shield", "Shield, +1, +2, or +3", "Slippers of Spider Climbing",
    "Spell Scroll", "Spellwrought Tattoo", "Staff of the Adder", "Staff of the Python",
    "Stone of Good Luck (Luckstone)", "Sword of Vengeance", "Trident of Fish Command", "Wand of Magic Detection",
    "Wand of Magic Missiles", "Wand of Secrets", "Wand of the War Mage +1, +2, or +3", "Wand of Web",
    "Weapon +1, +2, or +3", "Weapon of Warning", "Wind Fan", "Winged Boots"
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


def generate_inventory(store_type):
    conn = sqlite3.connect('dnd_items.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM store_types WHERE name=?', (store_type,))
    store_info = cursor.fetchone()

    if store_info is None:
        print(f"Tipo de loja '{store_type}' não encontrado.")
        return

    _, mundane_min, mundane_max, common_min, common_max, uncommon_min, uncommon_max, rare_min, rare_max, very_rare_min, very_rare_max, legendary_min, legendary_max = store_info

    cursor.execute('SELECT * FROM common_items')
    common_items = cursor.fetchall()

    cursor.execute('SELECT * FROM uncommon_items')
    uncommon_items = cursor.fetchall()

    cursor.execute('SELECT * FROM rare_items')
    rare_items = cursor.fetchall()

    cursor.execute('SELECT * FROM very_rare_items')
    very_rare_items = cursor.fetchall()

    cursor.execute('SELECT * FROM legendary_items')
    legendary_items = cursor.fetchall()

    inventory = {
        "common": random.sample(common_items, random.randint(common_min, common_max)),
        "uncommon": random.sample(uncommon_items, random.randint(uncommon_min, uncommon_max)),
        "rare": random.sample(rare_items, random.randint(rare_min, rare_max)),
        "very rare": random.sample(very_rare_items, random.randint(very_rare_min, very_rare_max)),
        "legendary": random.sample(legendary_items, random.randint(legendary_min, legendary_max))
    }

    conn.close()
    return inventory

# Interface gráfica
app = tk.Tk()
app.title("Loja de Itens Mágicos D&D 5e")

store_types_combobox = ttk.Combobox(app, values=list(store_types.keys()))
store_types_combobox.grid(column=0, row=0)

text_area = tk.Text(app, font=("JMH Typewriter", 12))
text_area.grid(column=0, row=1)

def show_inventory():
    inventory = generate_inventory(store_types_combobox.get())
    text_area.delete('1.0', tk.END)  # limpar o conteúdo existente
    for category, items in inventory.items():
        text_area.insert(tk.END, f"{category.capitalize()} Items:\n")
        for _, item_name in items:
            text_area.insert(tk.END, f"{item_name}\n")
        text_area.insert(tk.END, "\n")

generate_button = tk.Button(app, text="Gerar Inventário", command=show_inventory)
generate_button.grid(column=1, row=0)

app.mainloop()

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
    "Adamantine Armor", "Alchemy Jug", "All-Purpose Tool", "Ammunition +1, +2, or +3",
    "Amulet of Proof against Detection and Location", "Amulet of the Devout", "Arcane Grimoire", "Bag of Holding",
    "Bag of Tricks", "Barrier Tattoo", "Bloodwell Vial", "Boots of Elvenkind",
    "Boots of Striding and Springing", "Boots of the Winterlands", "Bracers of Archery", "Brooch of Shielding",
    "Broom of Flying", "Cap of Water Breathing", "Circlet of Blasting", "Cloak of Elvenkind",
    "Cloak of Protection", "Cloak of the Manta Ray", "Coiling Grasp Tattoo", "Decanter of Endless Water",
    "Deck of Illusions", "Dragonhide Belt +1, +2, or +3", "Driftglobe", "Dust of Disappearance",
    "Dust of Dryness", "Dust of Sneezing and Choking", "Eldritch Claw Tattoo", "Elemental Gem",
    "Emerald Pen", "Eversmoking Bottle", "Eyes of Charming", "Eyes of Minute Seeing",
    "Eyes of the Eagle", "Feywild Shard", "Figurine of Wondrous Power", "Gauntlets of Ogre Power",
    "Gem of Brightness", "Gloves of Missile Snaring", "Gloves of Swimming and Climbing", "Gloves of Thievery",
    "Goggles of Night", "Guardian Emblem", "Hat of Disguise", "Headband of Intellect",
    "Helm of Comprehending Languages", "Helm of Telepathy", "Immovable Rod", "Instrument of the Bards",
    "Javelin of Lightning", "Keoghtom's Ointment", "Lantern of Revealing", "Mariner's Armor",
    "Medallion of Thoughts", "Mithral Armor", "Moon Sickle", "Nature's Mantle",
    "Necklace of Adaptation", "Oil of Slipperiness", "Pearl of Power", "Periapt of Health",
    "Periapt of Wound Closure", "Philter of Love", "Pipes of Haunting", "Pipes of the Sewers",
    "Potion of Animal Friendship", "Potion of Fire Breath", "Potion of Giant Strength", "Potion of Growth",
    "Potion of Healing", "Potion of Poison", "Potion of Resistance", "Potion of Water Breathing",
    "Psi Crystal", "Quiver of Ehlonna", "Rhythm-Maker's Drum", "Ring of Jumping",
    "Ring of Mind Shielding", "Ring of Swimming", "Ring of Warmth", "Ring of Water Walking",
    "Robe of Useful Items", "Rod of the Pact Keeper", "Rope of Climbing", "Saddle of the Cavalier",
    "Sending Stones", "Sentinel Shield", "Shield, +1, +2, or +3", "Slippers of Spider Climbing",
    "Spell Scroll", "Spellwrought Tattoo", "Staff of the Adder", "Staff of the Python",
    "Stone of Good Luck (Luckstone)", "Sword of Vengeance", "Trident of Fish Command", "Wand of Magic Detection",
    "Wand of Magic Missiles", "Wand of Secrets", "Wand of the War Mage +1, +2, or +3", "Wand of Web",
    "Weapon +1, +2, or +3", "Weapon of Warning", "Wind Fan", "Winged Boots"
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