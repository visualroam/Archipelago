"""E1 boss and stat adapters. Encounter identities come from generated project tables.

Keys are objective families from docs/specs/bingo-catalogue-ledger.tsv.
Generic boss families resolve to one concrete encounter on this AP board.
"""
# family -> exact advisory names in our generated encounter table.
BOSSES = {
 "boss/morgott": ("Morgott, the Omen King",),
 "boss/rykard": ("Rykard, Lord of Blasphemy",),
 "boss/ancestor-spirit": ("Ancestor Spirit", "Regal Ancestor Spirit"),
 "boss/magma-wyrm-makar": ("Magma Wyrm Makar",),
 "boss/mohg-lord-of-blood": ("Mohg, Lord of Blood",),
 "boss/leonine-misbegotten": ("Leonine Misbegotten",),
 "boss/godskin-apostle": ("Godskin Apostle",),
 "boss/godfrey-shade": ("Godfrey, First Elden Lord",),
 "roster/gargoyle": ("Valiant Gargoyle",),
 "boss/fias-champions": ("Fia's Champion",),
 "boss/mohg-the-omen": ("Mohg, the Omen",),
 "boss/loretta-caria": ("Royal Knight Loretta",),
 "boss/commander-oneil": ("Commander O'Neil",),
 "boss/grafted-scion-chapel": ("Grafted Scion",),
 "boss/tree-sentinel-pair": ("Tree Sentinel",),
 "boss/crucible-misbegotten-pair": ("Crucible Knight",),
 "boss/elemer": ("Elemer of the Briar",),
 "boss/putrid-crystalian-trio": ("Crystalian (Spear)", "Putrid Crystalian (Spear)"),
 "boss/wormface": ("Wormface",),
 "boss/dragonkin-soldier": ("Dragonkin Soldier", "Dragonkin Soldier of Nokstella"),
 "boss/black-blade-kindred": ("Black Blade Kindred",),
 "boss/fire-giant": ("Fire Giant",),
 "boss/lansseax": ("Ancient Dragon Lansseax",),
 "boss/malenia": ("Malenia, Blade of Miquella",),
 "boss/borealis": ("Borealis the Freezing Fog",),
 "boss/misbegotten-crusader": ("Misbegotten Crusader",),
 "boss/vyke": ("Roundtable Knight Vyke",),
}
DLC_BOSSES = {
 "boss/golden-hippopotamus": ("Golden Hippopotamus",),
 "boss/bayle": ("Bayle the Dread",),
 "boss/midra": ("Midra, Lord of Frenzied Flame",),
 "boss/consort-radahn": ("Radahn, Consort of Miquella",),
 "boss/senessax": ("Ancient Dragon Senessax",),
 "roster/curseblade": ("Curseblade Labirith",),
 "boss/jori": ("Jori, Elder Inquisitor",),
 "boss/lamenter": ("Lamenter",),
 "boss/death-knight": ("Death Knight",),
 "boss/chief-bloodfiend": ("Chief Bloodfiend",),
 "boss/putrescent-knight": ("Putrescent Knight",),
 "boss/scadutree-avatar": ("Scadutree Avatar",),
 "boss/rellana": ("Rellana, Twin Moon Knight",),
 "boss/metyr": ("Metyr, Mother of Fingers",),
 "boss/messmer": ("Base Serpent Messmer",),
 "boss/dlc-fallingstar-beast": ("Fallingstar Beast",),
 "boss/romina": ("Romina, Saint of the Bud",),
 "boss/ancient-dragon-man": ("Ancient Dragon-Man",),
 "boss/dlc-death-rite-bird": ("Death Rite Bird",),
 "boss/rakshasa": ("Rakshasa",),
}
BOSSES.update(DLC_BOSSES)
# Fixed encounter qualifiers from boss_healthbars/boss_sweeps and their EMEVD events.
# Duo/trio terminal flags wait for every member; Lansseax uses the final Altus encounter.
EXACT = {"boss/godfrey-shade": {11000850},
         "boss/loretta-caria": {1035500800},
         "boss/grafted-scion-chapel": {10010800},
         "boss/tree-sentinel-pair": {1041510800},
         "boss/crucible-misbegotten-pair": {1051360800},
         "boss/putrid-crystalian-trio": {31110800},
         "boss/lansseax": {1041520800}}
# (metric, ((target, adapter), ...), label, region)
STATE_GOALS = (
 ("flask_potency", ((7, "stat/flask-potency"),), "Flask potency", "Limgrave"),
 ("flask_charges", ((10, "stat/flask-charges"),), "Flask charges", "Limgrave"),
 ("level", ((55, "stat/rune-level/55"), (60, "stat/rune-level/60"), (65, "stat/rune-level/65"),), "Rune level", "Limgrave"),
 ("faith", ((30, "stat/faith"),), "Base Faith", "Limgrave"),
 ("arcane", ((30, "stat/arcane"),), "Base Arcane", "Limgrave"),
 ("intelligence", ((30, "stat/intelligence"),), "Base Intelligence", "Limgrave"),
 ("scadutree", ((9, "stat/scadutree/9"), (10, "stat/scadutree/10"), (11, "stat/scadutree/11"),), "Scadutree blessing", "Gravesite"),
 ("spirit_ash", ((5, "stat/revered-spirit-ash"),), "Revered Spirit Ash blessing", "Gravesite"),
 ("level", ((80, "stat/dlc-rune-level/80"), (85, "stat/dlc-rune-level/85"),), "Rune level", "Gravesite"),
)


def candidates(healthbars, arenas, eligible, *, progressive_flasks=True, blessing_mode=0, sweep_regions=None):
    out = []
    for source, names in BOSSES.items():
        dlc = source in DLC_BOSSES
        for flag, info in healthbars.items():
            region = arenas.get(flag)
            # These overworld E1 encounters have no arena row; their own sweep has
            # a generated single-region owner. Do not extend this fallback to other bosses.
            if source in {"boss/commander-oneil", "boss/lansseax", "boss/borealis"}:
                region = (sweep_regions or {}).get(flag)
            # The intro map belongs to Stormveil's grouping; revisiting needs the Belfries key.
            if source == "boss/grafted-scion-chapel" and flag == 10010800:
                region = "Stormveil"
            if info[3] not in names or region not in eligible:
                continue
            if source in EXACT and flag not in EXACT[source]:
                continue
            if not dlc and str(info[0]).startswith(("m20", "m21", "m22", "m25", "m28", "m61", "m40", "m41", "m43")):
                continue
            if dlc and not str(info[0]).startswith(("m20", "m21", "m22", "m25", "m28", "m61", "m40", "m41", "m43")):
                continue
            cell = {"flag": flag, "region": region, "label": f"Defeat {info[3]} ({region})",
                    "family": source, "adapter": source, "requirements": []}
            encounter_labels = {"boss/tree-sentinel-pair": "Tree Sentinel duo", "boss/crucible-misbegotten-pair": "Crucible Knight and Misbegotten Warrior",
                                "boss/putrid-crystalian-trio": "Putrid Crystalian trio", "roster/gargoyle": "Valiant Gargoyle duo"}
            if source in encounter_labels:
                cell["label"] = f"Defeat {encounter_labels[source]} ({region})"
            if source == "boss/grafted-scion-chapel":
                cell.update(regions=[region, "Liurnia"], requirements=[["Imbued Sword Key", 1]])
                if "Liurnia" not in eligible:
                    continue
            if source == "boss/metyr":
                # Both Finger Ruins bells: Rhia in Cerulean, Dheo behind Shadow Keep.
                cell["regions"] = [region, "Cerulean", "Shadow Keep"]
                if not set(cell["regions"]) <= set(eligible):
                    continue
            out.append(cell)
    for metric, targets, label, region in STATE_GOALS:
        if region not in eligible or (metric.startswith("flask") and not progressive_flasks):
            continue
        # Catch-up floors also manufacture blessing observations; only the earned vanilla mode.
        if metric == "scadutree" and blessing_mode != 0:
            continue
        for target, adapter in targets:
            requirements = []
            if metric == "flask_potency": requirements = [["Progressive Flask Upgrade", target * 2]]
            if metric == "flask_charges": requirements = [["Progressive Flask Upgrade", (target - 4) * 2 - 1]]
            if metric == "scadutree":
                units = {9: 17, 10: 20, 11: 23}[target]
                requirements = [["Scadutree Fragment x2", (units + 1) // 2]]
            if metric == "spirit_ash": requirements = [["Revered Spirit Ash", 9]]
            out.append({"flag": 0, "region": region, "label": f"Reach {label} {target}",
                        "state": {"metric": metric, "target": target}, "family": "state:" + metric,
                        "adapter": adapter, "requirements": requirements,
                        "supply_goal": bool(requirements)})
    return out


def select(candidates, seed, *, region_limit, parents, start_pool=(), starts=1, size=5):
    """E1 draw: distinct encounters/source families, one upgrade supply goal, full closure."""
    import hashlib
    import random
    from .bingo_board import BINGO_LOCATION_BASE, board_area
    area = board_area(size)
    rng = random.Random(hashlib.sha256(str(seed).encode()).digest())
    candidates = sorted(candidates, key=lambda c: (c.get("adapter", ""), c["flag"], c["label"]))
    capacity = len({c.get("family", f"boss:{c['flag']}") for c in candidates})
    if capacity < area:
        raise ValueError(f"bingo E1 needs {area} distinct objective families; only {capacity} remain")
    def closure(cell):
        regions = set(cell.get("regions", [cell["region"]]))
        for owner in tuple(regions):
            seen = {owner}
            while owner in parents:
                owner = parents[owner]
                if owner in seen:
                    raise ValueError("bingo region parents contain a cycle")
                seen.add(owner)
                regions.add(owner)
        return regions
    for _ in range(256):
        order = rng.sample(candidates, len(candidates))
        opening = []
        for cell in order:
            if cell["region"] in start_pool and cell["region"] not in {c["region"] for c in opening}:
                opening.append(cell)
                if len(opening) == starts:
                    break
        if start_pool and len(opening) != starts:
            raise ValueError("bingo start_region_pool needs enough distinct objective regions")
        selected, regions, families, flags = [], set(), set(), set()
        supply = False
        hits, counters = {}, 0
        for cell in opening + [c for c in order if c not in opening]:
            family = cell.get("family", f"boss:{cell['flag']}")
            needed = regions | closure(cell)
            from .features.bingo import evidence_flags
            evidence = evidence_flags(cell)
            if (family in families or (cell["flag"] and cell["flag"] in flags)
                    or (supply and cell.get("supply_goal")) or len(needed) > region_limit
                    or (cell.get("counter") and counters >= 3)
                    or any(hits.get(f, 0) >= 2 for f in evidence)):

                continue
            selected.append(cell)
            regions, supply = needed, supply or cell.get("supply_goal", False)
            families.add(family)
            counters += bool(cell.get("counter"))
            for f in evidence: hits[f] = hits.get(f, 0) + 1
            flags.add(cell["flag"])
            if len(selected) == area:
                break
        if len(selected) == area and all(c in selected for c in opening):
            rng.shuffle(selected)
            return [dict(c, location=BINGO_LOCATION_BASE + i) for i, c in enumerate(selected)]
    raise ValueError(f"bingo E1 cannot fit {area} distinct objectives in {region_limit} regions")
