"""E2 encounter rosters and vanilla-location objectives; identities from generated tables.

Rows name their adapter and family; labels come from the objective ledger. Native
healthbar members without a generated terminal owner are never counted separately.
Collection squares count physical pickups at the items' vanilla locations, never
possession: with randomized items the fixed place is what the square is about.
"""
import json
from importlib.resources import files
from itertools import combinations

CATALOGUE = json.loads(files(__package__).joinpath("bingo_e2_catalogue.json").read_text(encoding="utf-8"))

# Fight-level terminals, verified in boss_sweeps/EMEVD. Partner healthbars are not units.
DUOS = {12020800, 30100800, 30120800, 30140800, 31060800, 31070800,
        31100800, 31110800, 31150800, 31180800, 31200800, 31220800,
        32050800, 1041510800, 1048400800, 1049390800, 1051360800, 1248550800}
NPC_BASE_NAMES = {"Patches", "Adan, Thief of Fire", "Battlemage Hugues",
                  "Roundtable Knight Vyke", "Necromancer Garris", "Esgar, Priest of Blood",
                  "Sir Gideon Ofnir, the All-Knowing"}
NPC_DLC_NAMES = {"Knight of the Solitary Gaol", "Dancer of Ranah", "Red Bear", "Rakshasa", "Dryleaf Dane"}
DRAGON_HEART_NAMES = {"Flying Dragon Agheel", "Glintstone Dragon Smarag", "Glintstone Dragon Adula",
 "Decaying Ekzykes", "Flying Dragon Greyll", "Borealis the Freezing Fog", "Magma Wyrm",
 "Magma Wyrm Makar", "Great Wyrm Theodorix"}
LEGENDARY_TALISMANS = {"Radagon's Soreseal", "Marika's Soreseal", "Dragoncrest Greatshield Talisman",
 "Moon of Nokstella", "Old Lord's Talisman", "Radagon Icon", "Godfrey Icon", "Erdtree's Favor +2"}


def _roster(family, rows):
    n = lambda names: [r for r in rows if r["name"] in names]
    contains = lambda word: [r for r in rows if word.casefold() in r["name"].casefold()]
    return {
      "roster/red-wolf": lambda: contains("Red Wolf"),
      "roster/gargoyle": lambda: contains("Gargoyle") + n({"Black Blade Kindred"}),
      "roster/magma-wyrm": lambda: n({"Magma Wyrm", "Magma Wyrm Makar", "Great Wyrm Theodorix"}),
      "roster/fallingstar-beast": lambda: contains("Fallingstar Beast"),
      "roster/omenkiller": lambda: contains("Omenkiller") + [r for r in rows if r["flag"] == 31180800],
      "roster/cemetery-shade": lambda: n({"Cemetery Shade"}),
      "roster/misbegotten": lambda: contains("Misbegotten"),
      "roster/watchdog": lambda: contains("Watchdog"),
      "roster/duelist": lambda: contains("Duelist"),
      "roster/black-knife": lambda: n({"Black Knife Assassin", "Alecto, Black Knife Ringleader"}),
      "roster/dragon-heart": lambda: n(DRAGON_HEART_NAMES),
      "roster/avatar": lambda: n({"Erdtree Avatar", "Putrid Avatar"}),
      "roster/nights-cavalry": lambda: contains("Night's Cavalry"),
      "roster/tibia-mariner": lambda: n({"Tibia Mariner"}),
      "roster/bell-bearing-hunter": lambda: n({"Bell Bearing Hunter"}),
      "roster/multi-boss": lambda: [r for r in rows if r["flag"] in DUOS],
      "roster/name-god": lambda: contains("God"),
      "roster/mounted": lambda: contains("Night's Cavalry") + n({"Tree Sentinel", "Draconic Tree Sentinel"}),
      "roster/name-tree": lambda: contains("Tree"),
      "region/limgrave": lambda: [r for r in rows if r["region"] in {"Limgrave", "Weeping"}],
      "region/liurnia": lambda: [r for r in rows if r["region"] == "Liurnia"],
      "region/caelid": lambda: [r for r in rows if r["region"] == "Caelid"],
      "region/altus": lambda: [r for r in rows if r["region"] in {"Altus", "Mt. Gelmir"}],
      "dungeon/catacombs": lambda: [r for r in rows if r["map"].startswith("m30_") and r["flag"] != 30050850],
      "dungeon/caves": lambda: [r for r in rows if r["map"].startswith("m31_") and r["flag"] not in {31000800, 31190850}],
      "dungeon/tunnels": lambda: [r for r in rows if r["map"].startswith("m32_") or r["name"] == "Magma Wyrm Makar"],
      "dungeon/altus-heros-grave": lambda: [r for r in rows if r["map"] in {"m30_08", "m30_09", "m30_10"}],
      "dungeon/evergaols": lambda: [r for r in rows if r["flag"] in {1033420800,1033450800,1036500800,1038410800,
                       1042370800,1042330800,1044350800,1039500800,1049390850,1053560800}],
      "boss/astel-both": lambda: contains("Astel"),
      "roster/npc-bosses": lambda: n(NPC_BASE_NAMES),
      "dungeon/dlc-catacombs": lambda: [r for r in rows if r["map"].startswith("m40_")],
      "roster/dlc-dragons": lambda: n({"Ghostflame Dragon", "Jagged Peak Drake", "Ancient Dragon Senessax", "Bayle the Dread"}),
      "dungeon/gaols": lambda: [r for r in rows if r["map"].startswith("m41_")],
      "roster/dancing-lion": lambda: n({"Divine Beast Dancing Lion"}),
      "roster/red-bear": lambda: n({"Red Bear", "Ralva the Great Red Bear", "Rugalea the Great Red Bear"}),
      "roster/dlc-npc-bosses": lambda: n(NPC_DLC_NAMES),
      "dungeon/mausoleums": lambda: n(NPC_DLC_NAMES - {"Dryleaf Dane"}),
      "roster/base-bosses-in-dlc": lambda: n({"Death Rite Bird", "Tree Sentinel", "Fallingstar Beast"}),
      "roster/name-knight": lambda: contains("Knight"),
    }.get(family, lambda: [])()


def _collection(row, tables):
    cat, goods, dlc = tables.item_catalog, tables.modules["item_ids"].GOODS_TYPE, set(tables.dlc_item_names)
    names = sorted(cat)
    scoped = [n for n in names if (n in dlc) == (row["scope"] == "dlc")]
    key, target = row["family"], row["target"]
    explicit = {
      "check/somberstone-bells": ["Somberstone Miner's Bell Bearing [1]", "Somberstone Miner's Bell Bearing [2]"],
      "check/smithing-stone-bells": ["Smithing-Stone Miner's Bell Bearing [1]", "Smithing-Stone Miner's Bell Bearing [2]"],
      "check/glovewort-bells-1": ["Glovewort Picker's Bell Bearing [1]", "Ghost-Glovewort Picker's Bell Bearing [1]"],
      "check/glovewort-bells-2": ["Glovewort Picker's Bell Bearing [2]", "Ghost-Glovewort Picker's Bell Bearing [2]"],
      "check/cracked-pot": ["Cracked Pot"], "check/ritual-pot": ["Ritual Pot"],
      "check/scarseals": ["Radagon's Scarseal", "Marika's Scarseal"],
      "check/fingerslayer-blade": ["Fingerslayer Blade"], "check/memory-stone": ["Memory Stone"],
      "check/haligtree-medallion": ["Haligtree Secret Medallion (Left)", "Haligtree Secret Medallion (Right)"],
      "check/moon-of-nokstella": ["Moon of Nokstella"], "check/imbued-sword-key": ["Imbued Sword Key"],
      "check/gaius-greaves": ["Gaius's Greaves"], "check/jolan": ["Swordhand of Night Jolán"],
      "check/dragon-heart": ["Dragon Heart"],
      "check/talisman": ["Two-Handed Sword Talisman" if row["adapter"] == "check/talisman-two-handed-sword" else "Two-Headed Turtle Talisman"],
      "check/scorpion-stew": ["Scorpion Stew"], "check/golden-braid": ["Golden Braid"], "check/ledas-rune": ["Leda's Rune"],
      "check/hefty-pot": ["Hefty Cracked Pot"], "check/igons-finger": ["Igon's Furled Finger"],
      "check/gravebird-set": ["Gravebird Helm", "Gravebird Armor", "Gravebird Bracelets", "Gravebird Anklets"],
      "check/three-helms": ["Death Mask Helm", "Winged Serpent Helm", "Salza's Hood"],
      "check/blessing-of-marika": ["Blessing of Marika"],
    }
    qty = key in {"check/cracked-pot", "check/ritual-pot", "check/memory-stone", "check/imbued-sword-key",
                  "check/dragon-heart", "check/hefty-pot", "check/blessing-of-marika"}
    if key in explicit:
        chosen = explicit[key]
        if not all(n in cat for n in chosen): return None
        if not qty: target = len(chosen)
    elif key == "check/talismans":
        chosen = sorted(LEGENDARY_TALISMANS & set(cat)) if row["adapter"] == "check/talismans-3-legendary-talismans" else [n for n in scoped if cat[n] >> 28 == 2]
    elif key in {"check/sorceries", "check/incantations"}: chosen = [n for n in scoped if goods.get(n) == (5 if key == "check/sorceries" else 16)]
    elif key in {"check/staves", "check/seals"}: chosen = [n for n in scoped if cat[n] >> 28 == 0 and cat[n] // 1000000 == (33 if key == "check/staves" else 34)]
    elif key == "check/material-bells": chosen = [n for n in scoped if "Bell Bearing" in n and any(w in n for w in ["Mushroom-Seller", "String-Seller", "Greasemonger", "Moldmonger", "Herbalist"]) ]
    elif key == "check/dlc-ashes-of-war": chosen = [n for n in scoped if cat[n] >> 28 == 8]
    elif key == "check/dlc-spirit-ashes": chosen = [n for n in scoped if goods.get(n) == 7]
    elif key == "check/top-upgrade-materials": chosen = [n for n in names if n in {"Ancient Dragon Smithing Stone", "Somber Ancient Dragon Smithing Stone", "Great Grave Glovewort", "Great Ghost Glovewort"}]
    # Whetstone Knives have dual-use flags blocked by the delivery contract; full armor
    # sets are mostly repeatable enemy drops with no fixed check.
    else: return None
    return {"names": chosen, "target": target, "qty": qty, "named": key in explicit and not qty}


def _short(name):
    """'Region :: Item - where, may be sweep-granted by X (m..) [f123]' -> 'Item - where'."""
    name = name.split(" :: ", 1)[-1].rsplit(" [f", 1)[0]
    return name.split(", may be sweep-granted by ", 1)[0].replace(" (region unconfirmed)", "")


def _vanilla_rows(group, tables, eligible):
    """All physical vanilla locations, grouped by item for distinct goals. Hub-collapsed rows have no known
    place, so they cannot anchor a region footprint and are never members."""
    missable = set(tables.modules["missable_locations"].MISSABLE_LOCATIONS)
    where = {aid: (name, region, flag) for region, rows in tables.locations.items()
             for name, aid, flag in rows if flag and region in eligible and region != tables.hub}
    by_item = {}
    for aid, item in sorted(tables.location_item.items()):
        if aid in where:
            by_item.setdefault(item, []).append(aid)
    rows, seen = [], set()
    for item in group["names"]:
        aids = sorted(by_item.get(item, ()), key=lambda aid: (aid in missable or where[aid][0] in missable, aid))
        if not group["named"]:
            # A missable member could brick a count square that has alternatives.
            aids = [aid for aid in aids if aid not in missable and where[aid][0] not in missable]
        if group["named"] and not aids:
            return None
        for aid in aids:
            name, region, flag = where[aid]
            identity = (flag, 0 if group["qty"] else tables.item_catalog[item])
            if identity not in seen:
                seen.add(identity)
                rows.append({"flag": flag, "name": _short(name), "region": region, "weight": 1,
                             **({"unit": identity[1]} if identity[1] else {})})
    return rows


def candidates(tables, eligible, region_limit, *, global_rosters=False):
    from .region_spine import DLC_REGIONS, parent_chain
    hb = tables.modules["boss_healthbars"].BOSS_HEALTHBARS
    spine = tables.modules["boss_sweeps"]
    # Only flags with an owning generated terminal sweep can count; partner bars lack one.
    rows = [{"flag": f, "name": r[3] or f"Boss encounter ({spine.SWEEP_ARENA_REGION.get(f, spine.SWEEP_REGION.get(f))})", "map": r[0], "region": spine.SWEEP_ARENA_REGION.get(f, spine.SWEEP_REGION.get(f)), "weight": 2 if f == 12020800 else 1}
            for f,r in hb.items() if spine.SWEEP_ARENA_REGION.get(f, spine.SWEEP_REGION.get(f)) in eligible and f not in {31000800}]
    out, unavailable = [], []
    for row in CATALOGUE:
        label = row["label"]
        if row["kind"] == "collection":
            group = _collection(row, tables)
            members = _vanilla_rows(group, tables, eligible) if group else None
            if not members:
                unavailable.append(row["adapter"]); continue
            groups = [(group["target"], members)]
        else:
            scoped = [r for r in rows if (r["region"] in DLC_REGIONS) == (row["scope"] == "dlc")]
            if row["family"] == "roster/deathbirds":
                groups = [(2, [r for r in scoped if r["name"] == "Deathbird"]), (1, [r for r in scoped if r["name"] == "Death Rite Bird"])]
            elif row["family"] == "roster/bear-lion-hippo":
                groups = [(1, [r for r in scoped if r["name"] in names]) for names in [
                  {"Red Bear", "Ralva the Great Red Bear", "Rugalea the Great Red Bear"}, {"Divine Beast Dancing Lion"}, {"Golden Hippopotamus"}]]
            else: groups = [(row["target"], _roster(row["family"], scoped))]
        from .features.bingo import counter_total
        pair = row["family"] == "roster/gargoyle"  # the Valiant Gargoyle duo counts as two
        if any(counter_total([dict(r, weight=r["weight"] if pair else 1)
                              for r in members]) < target for target,members in groups):
            unavailable.append(row["adapter"]); continue
        if global_rosters or row["kind"] == "collection" or row.get("distinct"):
            # Optional contributors span all eligible regions. The board keeps those
            # regions; this is any N distinct units, not a selected local route.
            counter = [dict(target=target, members=[dict(flag=r["flag"], region=r["region"],
                label=r["name"], weight=r["weight"] if pair else 1,
                **({"unit": r["unit"]} if "unit" in r else {})) for r in members]) for target,members in groups]
            owners = sorted({m["region"] for g in counter for m in g["members"]})
            out.append(dict(flag=0, region=owners[0], regions=owners, label=label,
                family=row["family"], adapter=row["adapter"], counter=counter, requirements=[]))
            continue
        # Choose a sufficient contributor footprint within the region budget. Each viable
        # footprint is a candidate so a wider board can pick a compatible route after the draw.
        owners = sorted({r["region"] for _,members in groups for r in members})
        emitted = 0
        for size in range(1, min(len(owners), region_limit)+1):
            for footprint in combinations(owners, size):
                closure = set(footprint) | {p for r in footprint for p in parent_chain(r)}
                if len(closure) > region_limit: continue
                counter=[]
                for target,members in groups:
                    units=[dict(flag=r["flag"], region=r["region"], label=r["name"], weight=r["weight"] if pair else 1) for r in members if r["region"] in footprint]
                    if sum(u["weight"] for u in units) < target: break
                    counter.append(dict(target=target, members=units))
                else:
                    out.append(dict(flag=0, region=footprint[0], regions=list(footprint), label=label,
                        family=row["family"], adapter=row["adapter"], counter=counter, requirements=[]))
                    emitted += 1
            if emitted: break
        if not emitted: unavailable.append(row["adapter"])
    return out, unavailable
