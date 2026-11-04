"""E3 admission: native persistent deaths, never reward/pickup flags.

Each ordinary enemy below has an audited EMEVD death setter. The existing
client protects these flags from AP writers, including first-line sweeps.
Quest transactions, source pickups and enemies without such evidence stay out.
"""
from itertools import combinations
from collections import Counter

# (death flag, actual entity, map, owner). common_func events 90005300/1 wait
# for CharacterRatioDead(entity) BEFORE setting its first argument. LOD entity
# IDs deliberately differ from flags at several Furnace Golem placements.
DEATHS = {
    "roster/crucible-knight": [
        (10000498, 10000498, "m10_00_00_00", "Stormveil"),
        (11000495, 11000495, "m11_00_00_00", "Leyndell"),
        (11000496, 11000496, "m11_00_00_00", "Leyndell"),
        (13000295, 13000295, "m13_00_00_00", "Farum Azula"),
        (13000296, 13000296, "m13_00_00_00", "Farum Azula"),
    ],
    "roster/tree-spirit": [
        (10000291, 10000291, "m10_00_00_00", "Stormveil"),
        (11000497, 11000497, "m11_00_00_00", "Leyndell"),
        (12010420, 12010420, "m12_01_00_00", "Ainsel River"),
        (15000398, 15000398, "m15_00_00_00", "Haligtree"),
        (1042500300, 1042500300, "m60_42_50_00", "Altus"),
    ],
    "boss/preceptor-miriam": [
        (34110710, 34110710, "m34_11_00_00", "Liurnia"),
        (34110711, 34110711, "m34_11_00_00", "Liurnia"),
    ],
    "roster/elder-lion": [
        (10000289, 10000289, "m10_00_00_00", "Stormveil"),
        (11000399, 11000399, "m11_00_00_00", "Leyndell"),
        (1049370299, 1049370299, "m60_49_37_00", "Caelid"),
        (1051360291, 1051360291, "m60_51_36_00", "Caelid"),
        (1051360292, 1051360292, "m60_51_36_00", "Caelid"),
        (1051570310, 1051570310, "m60_51_57_00", "Mountaintops of the Giants"),
        (1051570311, 1051570311, "m60_51_57_00", "Mountaintops of the Giants"),
    ],
    "roster/furnace-golem": [
        (2045460200, 2045460200, "m61_45_46_00", "Ancient Ruins"),
        (2046390200, 2246390200, "m61_46_39_00", "Cerulean"),
        (2046420300, 2246420300, "m61_46_42_00", "Gravesite"),
        (2048400200, 2248400200, "m61_48_40_00", "Cerulean"),
        (2248460291, 2248460291, "m61_48_46_00", "Scadu Altus"),
        (2050460300, 2050460300, "m61_50_46_00", "Scadu Altus"),
        (2050460310, 2050460310, "m61_50_46_00", "Scadu Altus"),
        (2251450280, 2251450280, "m61_51_45_00", "Scadu Altus"),
    ],
    "roster/hippopotamus": [
        (2046460290, 2046460290, "m61_46_46_00", "Ancient Ruins"),
        (2047390300, 2047390400, "m61_47_39_00", "Cerulean"),
        (2051440300, 2051440300, "m61_51_44_00", "Scadu Altus"),
        (2051440310, 2051440310, "m61_51_44_00", "Scadu Altus"),
    ],
    "roster/dlc-tree-spirit": [
        (20000410, 20000410, "m20_00_00_00", "Belurat"),
        (21000470, 21000470, "m21_00_00_00", "Shadow Keep"),
        (21000471, 21000471, "m21_00_00_00", "Shadow Keep"),
        (2047430300, 2047430300, "m61_47_43_00", "Gravesite"),
    ],
    "boss/madding-hand": [(2052420300, 2052420300, "m61_52_42_00", "Abyssal")],
}

# Bespoke death setters, not the item-lot acquisition flags.
SINGLES = {
    "boss/black-knight-garrew": (2047450800, "Scadu Altus"),  # 90005860 native boss terminal
    "boss/moonrithyll": (2047440360, "Ensis"),  # m61_47_44 event 2047442360
    "boss/madding-hand": (2052420300, "Abyssal"),
}

OBJECTIVES = [
    ("roster/crucible-knight", "roster/crucible-knight/2", "Defeat 2 different Crucible Knights", 2),
    ("roster/crucible-knight", "roster/crucible-knight/3", "Defeat 3 different Crucible Knights", 3),
    ("roster/crucible-knight", "roster/crucible-knight/4", "Defeat 4 different Crucible Knights", 4),
    ("boss/preceptor-miriam", "boss/preceptor-miriam", "Defeat Preceptor Miriam", 1),
    ("roster/tree-spirit", "roster/tree-spirit", "Defeat 3 different Tree Spirits", 3),
    ("roster/elder-lion", "roster/elder-lion/2", "Defeat 2 different Elder Lions", 2),
    ("roster/elder-lion", "roster/elder-lion/3", "Defeat 3 different Elder Lions", 3),
    ("roster/elder-lion", "roster/elder-lion/4", "Defeat 4 different Elder Lions", 4),
    ("roster/furnace-golem", "roster/furnace-golem/1", "Defeat 1 Furnace Golem", 1),
    ("roster/furnace-golem", "roster/furnace-golem/2", "Defeat 2 Furnace Golems", 2),
    ("roster/hippopotamus", "roster/hippopotamus", "Defeat 2 hippopotamuses", 2),
    ("roster/dlc-tree-spirit", "roster/dlc-tree-spirit", "Defeat 3 Ulcerated Tree Spirits in the Shadow Realm", 3),
    ("boss/black-knight-garrew", "boss/black-knight-garrew", "Defeat Black Knight Garrew", 1),
    ("boss/moonrithyll", "boss/moonrithyll", "Defeat Moonrithyll, Carian Knight", 1),
    ("boss/madding-hand", "boss/madding-hand", "Defeat the Madding Hand", 1),
]

MEMBER_NAMES = {
    "roster/crucible-knight": "Crucible Knight", "boss/preceptor-miriam": "Preceptor Miriam",
    "roster/tree-spirit": "Tree Spirit", "roster/elder-lion": "Elder Lion",
    "roster/furnace-golem": "Furnace Golem", "roster/hippopotamus": "Hippo",
    "roster/dlc-tree-spirit": "Ulcerated Tree Spirit",
}

# Corresponding getItemFlagId from flag_lots.tsv, joined through each native
# 90005301 itemLotId. Used ONLY for inheriting the native reward's access rules;
# the client earns the square from the death flag, never these pickup flags.
REWARD_DEATH = {
    34117700: 34110710, 34117710: 34110711,
    10007085: 10000289, 10007195: 10000291, 10007295: 10000498,
    11007185: 11000399, 11007993: 11000497, 12017997: 12010420,
    15001200: 15000398, 1042507020: 1042500300,
    1049377700: 1049370299, 1051367700: 1051360291,
    1051367800: 1051360292, 1051577800: 1051570310,
    1051577810: 1051570311,
    20007991: 20000410, 21007991: 21000470, 21007993: 21000471,
    2045467500: 2045460200, 2046397060: 2046390200,
    2046427980: 2046420300, 2046467000: 2046460290,
    2047397070: 2047390300, 2047437980: 2047430300,
    2048407020: 2048400200, 65410: 2248460291,
    2050467500: 2050460300, 2050467510: 2050460310,
    2051447500: 2051440300, 2051447510: 2051440310,
    2051457700: 2251450280, 2052427500: 2052420300,
    530865: 2047440360,
}


def candidates(tables, eligible, region_limit, *, global_rosters=False):
    from .region_spine import parent_chain
    out = []
    for family, adapter, label, target in OBJECTIVES:
        if family in SINGLES:
            flag, region = SINGLES[family]
            if region in eligible:
                out.append(dict(flag=flag, region=region, label=label, family=family,
                                adapter=adapter, requirements=[]))
            continue
        placements = [p for p in DEATHS[family] if p[3] in eligible and p[3] != "Leyndell"]
        totals, seen, members = Counter(p[3] for p in placements), Counter(), []
        for flag, _entity, _map, region in placements:
            seen[region] += 1
            suffix = f", encounter {seen[region]}" if totals[region] > 1 else ""
            member_label = f"{MEMBER_NAMES[family]} ({region}{suffix})"
            if family == "boss/preceptor-miriam":
                member_label = "Preceptor Miriam (normal hall)" if flag == 34110710 else "Preceptor Miriam (inverted hall)"
            members.append(dict(flag=flag, region=region, label=member_label, weight=1))
        # Native Leyndell is erased by Maliketh. Its ordinary placements are
        # audited above but not admitted as required contributors to a board.
        if family in {"roster/crucible-knight", "roster/tree-spirit"}:
            hb = tables.modules["boss_healthbars"].BOSS_HEALTHBARS
            spine = tables.modules["boss_sweeps"]
            names = {"Crucible Knight", "Crucible Knight Ordovis", "Crucible Knight Siluria"} if family == "roster/crucible-knight" else {"Ulcerated Tree Spirit", "Putrid Tree Spirit"}
            for flag, info in hb.items():
                region = spine.SWEEP_ARENA_REGION.get(flag, spine.SWEEP_REGION.get(flag))
                if info[3] in names and region in eligible and not info[0].startswith(("m61", "m20", "m21")):
                    members.append(dict(flag=flag, region=region, label=info[3], weight=2 if flag == 30100800 else 1))
        if family == "roster/hippopotamus":
            # Golden Hippopotamus is a fifth independent encounter; its partner
            # entities are not additional kills.
            flag = 21000850
            spine = tables.modules["boss_sweeps"]
            region = spine.SWEEP_ARENA_REGION.get(flag, spine.SWEEP_REGION.get(flag))
            if region in eligible:
                members.append(dict(flag=flag, region=region, label="Golden Hippopotamus", weight=1))
        owners = sorted({m["region"] for m in members})
        if global_rosters:
            if sum(m["weight"] for m in members) >= target:
                out.append(dict(flag=0, region=owners[0], regions=owners,
                    label=label, family=family, adapter=adapter,
                    counter=[dict(target=target, members=members)], requirements=[]))
            continue
        if "unique" in label.casefold():
            if sum(m["weight"] for m in members) >= target:
                out.append(dict(flag=0, region=owners[0], regions=owners,
                    label=label, family=family, adapter=adapter,
                    counter=[dict(target=target, members=members)], requirements=[]))
            continue
        for size in range(1, min(len(owners), region_limit) + 1):
            emitted = False
            for footprint in combinations(owners, size):
                closure = set(footprint) | {p for r in footprint for p in parent_chain(r)}
                units = [m for m in members if m["region"] in footprint]
                if len(closure) > region_limit or sum(m["weight"] for m in units) < target:
                    continue
                out.append(dict(flag=0, region=footprint[0], regions=list(footprint),
                    label=label, family=family, adapter=adapter,
                    counter=[dict(target=target, members=units)], requirements=[]))
                emitted = True
            if emitted:
                break
    return out
