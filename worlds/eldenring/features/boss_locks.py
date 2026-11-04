"""SPEC-PARITY Phase 3 -- region bosses (+ future dungeon sweeps).

Region bosses: the 25 major bosses (method=boss_arena) joined to greenfield ap-ids by FLAG,
pre-generated into boss_data.py (matt-free). Emitted as bossLocations {region: [ap_ids]} for kept
regions -- the data a boss-based ending goal / region-boss tracker reads.

Dungeon SWEEPS (kill a dungeon boss -> auto-grant its other checks) need a per-dungeon boss-kill
flag the backbone does NOT carry: only 22/39 minidungeons have any emevd row, and those aren't
reliably boss rewards. That trigger set requires an EMEVD enrichment pass (SPEC-PARITY.md P3); the boss-defeat FLAG per dungeon is now derived from the DarkScript EMEVD (boss_sweeps.py) and
emitted as dungeonSweepFlags {boss_flag: [member_ap_ids]}; a small client flag-watch handler
(P3b-client) grants the members on boss kill. The location-keyed dungeonSweeps variant additionally
needs a boss-reward-location join (ItemLotParam) and stays empty for now.
"""
from Options import Choice, Removed, Toggle, Visibility
from BaseClasses import ItemClassification
from ..registry import Feature, register
from .. import contract
from ..region_spine import DLC_REGIONS   # canonical base/DLC partition (also used by core.py)

try:
    from ..tables.boss_data import REGION_BOSSES
except Exception:  # not yet generated
    REGION_BOSSES = {}
try:
    from ..tables.boss_sweeps import DUNGEON_SWEEPS, SWEEP_REGION
except Exception:
    DUNGEON_SWEEPS, SWEEP_REGION = {}, {}
try:
    from ..tables.boss_sweeps import SWEEP_ARENA_REGION   # trigger -> region the BOSS is fought in (#445)
except Exception:
    SWEEP_ARENA_REGION = {}
try:
    from ..tables.boss_healthbars import BOSS_HEALTHBARS   # flag -> (map, tile, CLASS, name)
except Exception:
    BOSS_HEALTHBARS = {}
try:
    from ..tables.location_tags import LOCATION_TAGS       # ap id -> [surface class, ...]
except Exception:  # not yet generated -> the per-seed surface cut is a no-op
    LOCATION_TAGS = {}
try:
    from ..tables.region_gating_boss import REGION_GATING_BOSS  # hand-curated, see the module docstring
except Exception:
    REGION_GATING_BOSS = {}


# The half of contract.SURFACE_CLASSES that gen_data ADMITS into a sweep and this side cuts PER
# SEED. Its complement (gen_data._SWEEP_NEVER_TAGS) is the permanent floor -- boss drops,
# remembrances, great runes, key items and merchant stock are never sweep members in any seed and no
# option restores them. See gen_data's comment for why the split falls where it does; the two halves
# PARTITION the vocabulary and test_gf_boss_sweeps asserts exactly that, so a new premium class has
# to be filed on one side deliberately.
_SWEEP_SURFACE_CUTTABLE = frozenset({"Seedtree", "Church", "Fragment", "Revered", "Basin",
                                     "Legendary"})


def seed_surface_classes(world):
    """The surface classes THIS seed says may hold progression, as a plain set.

    Not `progression_surface.selected_surface()`: that returns a canonically ORDERED list because
    the feasibility ladder's determinism depends on the order, and nothing here iterates -- this is
    a membership test only, so importing the feature (and its Options dependency) buys nothing and
    costs a cycle. Falls back to contract.SURFACE_DEFAULT_CLASSES when the option is absent, which
    is the conservative direction: the default surface is the widest cut of the six.

    Unfiltered by the valid vocabulary on purpose -- an unknown key cannot be in
    _SWEEP_SURFACE_CUTTABLE, so it can only ever fail to cut, and AP's VerifyKeys has already
    rejected it upstream anyway."""
    opt = getattr(getattr(world, "options", None), "progression_surface", None)
    if opt is None:
        return frozenset(contract.SURFACE_DEFAULT_CLASSES)
    return frozenset(getattr(opt, "value", None) or ())


def _full_area_sweeps_on(world):
    """Is this seed's `full_area_sweeps` on? Absent option (or no world) reads OFF, which is the
    default and the HEAD behaviour -- every synthetic-world unit test that predates the option
    therefore keeps measuring the surface cut it was written for."""
    opt = getattr(getattr(world, "options", None), "full_area_sweeps", None)
    return bool(opt is not None and getattr(opt, "value", 0))


def sweep_surface_cut(world, location_tags=None):
    """The member ap ids this seed must NOT sweep: the ones whose class its Progression Surface has
    claimed for progression.

    WHY THIS IS PER SEED AND NOT BAKED. Until 2026-08-13 gen_data cut the whole 16-class vocabulary,
    so a sweep was "filler-only" in the narrow sense of "holds nothing the surface could ever name".
    That is a corpus-wide answer to a per-seed question: `Legendary` and `Basin` are not in
    SURFACE_DEFAULT_CLASSES at all, so in a default seed those 51 checks were barred from a sweep to
    protect a placement that could not happen. The rule now matches what the seed actually decided --
    a class that cannot host progression here is ordinary area loot, and killing the boss pays it out.

    🛑 THE HONEST EDGE, stated rather than special-cased. An EMPTY surface turns confinement off
    entirely (progression scatters as vanilla AP fill decides) and this cut correctly returns
    nothing -- but that is not a hole this change opens. With no confinement, our own Locks and, at
    `confine_foreign_progression` 0, foreign advancement can already land on any of the 3731
    UNTAGGED filler members a sweep has always granted. The surface is the only statement a seed
    makes about where progression may go; when it says "nowhere in particular" there is nothing for
    a tag cut to act on, and DungeonSweep's docstring says so.

    ⚠️ progression_surface's feasibility LADDER can widen past the player's selection when the
    surface is too small to host every Lock (a few-region seed). If it reaches its +Legendary or
    +Seedtree,Church rung it can place a Lock on a check this cut has already released, and the
    sweep will hand it over. Not a soft-lock -- a sweep member's access rule is its region, so the
    Lock was reachable there anyway and the sweep only makes it earlier -- but it is the one way a
    sweep can pay out progression under a non-empty surface, and it is why this returns the BASE
    selection rather than pretending to predict the ladder.

    🛑 `full_area_sweeps` TURNS THIS OFF ENTIRELY (#1033, siffrin + bobler). It is checked HERE
    rather than in `enabled_sweeps` so that every reader of the cut agrees about what this seed
    grants -- a cut that two callers disagree about is the defect `enabled_sweeps` was written to
    prevent. When the option is on the cut is empty, the six cuttable classes stay in the payload
    whatever the surface says, and the honest edge above stops being an edge and becomes the
    behaviour: a boss kill CAN hand over this seed's own Locks, and at the default
    `confine_foreign_progression` another player's. That is not a soft-lock for the same reason the
    ladder case is not -- a sweep member's access rule is its own region and the trigger boss stands
    in a region this seed kept (#445) -- so the sweep only makes a reachable check arrive earlier.

    Pure over its inputs (module globals by default) so it unit-tests with synthetic data."""
    if _full_area_sweeps_on(world):
        return frozenset()
    tags = LOCATION_TAGS if location_tags is None else location_tags
    claimed = _SWEEP_SURFACE_CUTTABLE & seed_surface_classes(world)
    if not claimed:
        return frozenset()
    return frozenset(ap for ap, t in tags.items() if claimed.intersection(t))


def _boss_label(reward: str) -> str:
    """Derive a clean boss name from a REGION_BOSSES reward string (no separate boss-name table --
    locked decision). Strips the 'Remembrance of the '/'Remembrance of ' prefix and a trailing
    "'s Great Rune"/' Great Rune' suffix. Examples: 'Remembrance of the Dancing Lion' -> 'Dancing
    Lion'; "Radahn's Great Rune" -> 'Radahn'. Names that fit neither shape (e.g. 'Elden
    Remembrance') pass through unchanged."""
    s = reward.strip()
    for pre in ("Remembrance of the ", "Remembrance of "):
        if s.startswith(pre):
            s = s[len(pre):]
            break
    for suf in ("'s Great Rune", " Great Rune"):
        if s.endswith(suf):
            s = s[:-len(suf)]
            break
    return s.strip()


# Which boss CLASSES each rung sweeps -- MOVED TO contract.py 2026-08-13 so the AP-free wizard census
# tool can read it (it prices the SweepSlot box). Re-exported under the old private names so every
# reader in this module and its tests keeps working and there is still exactly one table.
_SWEEP_MINI = contract.SWEEP_MINI_CLASSES
_SWEEP_RUNGS = contract.SWEEP_RUNGS


class DungeonSweep(Choice):
    """Which boss kills also collect the rest of their area's checks for you (a "sweep").

    Kill such a boss and the other checks in its dungeon or area arrive at once, so you can
    skip walking to them. Nothing is lost or required either way. Never collected this way:
    boss rewards, quest keys, shop stock, and by default collectibles such as Golden Seeds
    and Sacred Tears (see full_area_sweeps). By default some checks in a sweep may hold
    progression; to reduce that, remove SweepSlot from Progression Surface (where
    progression can land). In a multiworld, other players' progression then has fewer of
    your checks to land on.
    none: no sweeps; pick up every check where it lies
    minidungeons: catacombs, caves, tunnels and other small dungeons
    all: minidungeons plus legacy dungeons, castles and DLC open-world bosses
    bosses: all plus base-game open-world bosses (default)
    """
    display_name = "Dungeon Sweep"
    option_none = 0
    option_minidungeons = 1
    option_all = 2
    option_bosses = 3
    default = 3


class FullAreaSweeps(Toggle):
    """Boss kills that sweep up an area also take the pickups they usually skip.

    A sweep skips what Progression Surface reserves for progression (by default Golden
    Seeds, Sacred Tears, Scadutree Fragments, Revered Spirit Ashes). On: it takes those too,
    so a kill may hand you an item that opens a region or another player's progression. It
    cannot strand you. Boss rewards, quest keys and shop stock are never swept. No effect if
    Dungeon Sweep is none.
    """
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Full Area Sweeps"


class RegionSweep(Toggle):
    """Kill a region's own gating boss and the rest of its checks arrive at once.

    Its gating boss is its Great Rune boss, else its biggest Remembrance boss, else its
    major boss. Adds to whatever Dungeon Sweep already grants. Never takes another boss's
    own reward, remembrance or rune, quest-gate keys, or merchant stock. Cannot strand you.
    No effect if Dungeon Sweep is none.
    """
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Region Sweep"


# The location tags a region-sweep grant never takes, regardless of full_area_sweeps -- the same
# three carve-outs full_area_sweeps documents (own-boss reward/remembrance/rune, quest keys, shop
# stock), read directly off LOCATION_TAGS rather than re-deriving them. GreatRune/Remembrance/
# MajorBoss cover "another boss's own reward"; KeyItem covers quest-gate keys; the Shop* tags cover
# merchant stock (TAG_COUNTS in location_tags.py: Shop, ShopNonSpell, ShopSlot, EniaShop).
_REGION_SWEEP_NEVER_TAGS = frozenset({
    "GreatRune", "Remembrance", "MajorBoss", "KeyItem",
    "Shop", "ShopNonSpell", "ShopSlot", "EniaShop",
})


def _region_sweep_on(world):
    """Is this seed's `region_sweep` on? Absent option (or no world) reads OFF -- same convention as
    `_full_area_sweeps_on`, so every pre-existing synthetic-world test keeps measuring HEAD."""
    opt = getattr(getattr(world, "options", None), "region_sweep", None)
    return bool(opt is not None and getattr(opt, "value", 0))


def region_sweep_groups(world, kept=None, location_tags=None, region_gating_boss=None):
    """{gating boss flag: [member ap ids]} for `region_sweep`, one group per KEPT region that has a
    `REGION_GATING_BOSS` entry.

    Members are every check `tables.locations` lists for the region, minus `_REGION_SWEEP_NEVER_TAGS`
    and minus this seed's `sweep_surface_cut` (the same per-seed progression-surface cut every other
    sweep obeys, so `full_area_sweeps` controls this exactly as it controls design 1's sweeps -- see
    that function's docstring). HUB is never a `REGION_GATING_BOSS` key, so it is excluded by
    construction rather than by a separate check.

    Empty (not merely absent) when the option is off, so a caller can `dict.update` the result
    unconditionally. Pure over its inputs (module globals by default) so it unit-tests with synthetic
    data injected, matching every other function in this file.
    """
    if not _region_sweep_on(world):
        return {}
    region_gating_boss = REGION_GATING_BOSS if region_gating_boss is None else region_gating_boss
    if not region_gating_boss:
        return {}
    kept = set(world._kept()) if kept is None else set(kept)
    tags = LOCATION_TAGS if location_tags is None else location_tags
    locations = getattr(getattr(world, "tables", None), "locations", None) or {}
    surface_cut = sweep_surface_cut(world, tags)
    runtime_skips = contract.runtime_sweep_skips()
    out = {}
    for region, fl in region_gating_boss.items():
        if region not in kept or fl in runtime_skips:
            # The runtime-skip guard should never fire given the curation in §2 of the spec -- kept
            # anyway so a future table edit cannot silently gate a region on a dead boss.
            continue
        members = [ap for (_name, ap, _flag) in locations.get(region, ())
                   if ap not in surface_cut
                   and not (_REGION_SWEEP_NEVER_TAGS & set(tags.get(ap, ())))]
        if members:
            out[fl] = members
    return out


class RevealSweepBossNames(Toggle):
    """The F6 tracker shows boss names for sweeps in regions that are still locked.

    Off by default, so the tracker does not spoil which bosses wait in locked regions. This
    changes only the display; checks, sweeps and item placement stay identical. On needs an
    up-to-date client; older ones refuse the seed.
    """
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Reveal Hidden Sweep Boss Names"
    default = 0


class BossKeys(Removed):
    """RETIRED 2026-10-06 (Alaric): Boss Keys ("mode B") is gone. It minted a progression
    'Boss Key: <Boss>' per kept boss and held that boss's own check and dungeon sweep until the key
    arrived. It was frozen OFF in defaults.FROZEN_OPTIONS from v0.2 until removal, so no seed ever
    ran it. Kept as a Removed stub so an old yaml that still names it loads instead of failing on
    an unknown option, the same way LocalItemOnly was retired (features/local_items.py)."""


class BossLockPlacement(Removed):
    """RETIRED 2026-10-06 with Boss Keys: it chose where boss-lock items were hosted and did nothing
    without them. Removed stub for the same old-yaml reason as BossKeys."""


# The 27 AP item ids the 'Boss Key: <Boss>' names held (7780316..7780342). registry.allocate_item_ids
# hands out feature item ids SEQUENTIALLY, so dropping the names would renumber every feature item
# allocated after this module -- 523 of them, from 'Progressive Flask Upgrade' (7780343) on. The band
# is burned instead, at this module's position, and never reissued. A literal on purpose: the names
# were derived from REGION_BOSSES, and a regen that changed that table must not move the band.
RETIRED_BOSS_KEY_ID_SLOTS = 27


def sweep_trigger_reachable(fl, kept, sweep_region=None, arena_region=None):
    """True iff this seed can ever FIRE sweep group `fl` -- issue #445.

    A group has two regions, and until 2026-08-07 only one of them was checked:

    * the MEMBERS' region (`SWEEP_REGION`) -- where the checks it grants live;
    * the ARENA region (`SWEEP_ARENA_REGION`) -- where the player must STAND to kill the trigger
      boss, read from PlayRegionParam's boss-area row.

    They are the same region for 106 of the 112 audited triggers and this predicate changes nothing
    there. For the other 6 they differ, and a seed that keeps the members' region WITHOUT the arena's
    ships a group whose trigger can never fire: `er_logic::region_lock::kick_decision` ejects the
    player from the arena's play_region bucket before the fight. The Golden Hippopotamus is the case
    that found it (issue #445) -- arena bucket 69000 = m61_48_45 = Scadu Altus, 104 members in Shadow
    Keep -- and boblerrr's 6-region seed kept Shadow Keep and not Scadu Altus.

    🛑 AN UNKNOWN ARENA IS TREATED AS REACHABLE, and that is a documented LOWER BOUND, not a clean
    bill. 113 of the 225 triggers have no `boss_area_regions.tsv` row, so this predicate cannot speak
    for them; refusing them instead would silently delete 1686 member links on missing evidence.
    `slot_data` logs the unaudited count on every seed and
    test_gf_boss_sweeps.test_sweep_arena_coverage_floor ratchets it, because a self-reported coverage
    number is not a safeguard unless something acts on it (CONTRIBUTING rule 11).

    Pure over its inputs (module globals by default) so it unit-tests with synthetic data injected."""
    sweep_region = SWEEP_REGION if sweep_region is None else sweep_region
    arena_region = SWEEP_ARENA_REGION if arena_region is None else arena_region
    kept = set(kept)
    if sweep_region.get(fl) not in kept:
        return False
    arena = arena_region.get(fl)
    return arena is None or arena in kept


def unreachable_sweeps(live, kept, sweep_region=None, arena_region=None):
    """The subset of `live` this seed keeps the members' region for but can never TRIGGER, as
    {flag: (members_region, arena_region)}. Split out from the filter so the drop can be COUNTED and
    named in the log rather than silently vanishing -- a filter with no tally is a lie
    (CONTRIBUTING rule 4). Groups whose members' region is simply not kept are not in here: those
    are ordinary out-of-scope groups, not a defect."""
    sweep_region = SWEEP_REGION if sweep_region is None else sweep_region
    arena_region = SWEEP_ARENA_REGION if arena_region is None else arena_region
    kept = set(kept)
    return {fl: (sweep_region.get(fl), arena_region.get(fl))
            for fl in live
            if sweep_region.get(fl) in kept
            and not sweep_trigger_reachable(fl, kept, sweep_region, arena_region)}


def rung_sweeps(world, _want_unjoined=False):
    """{boss flag: [member ap ids]} at this seed's RUNG, BEFORE the per-seed surface cut.

    Split out of `enabled_sweeps` so `progression_surface.sweep_slot_aps` can ask "which sweeps does
    this seed run?" without asking "which members did the surface claim?" -- because it is the thing
    that decides the surface. 🛑 Calling `enabled_sweeps` from the surface would be a cycle:
    enabled_sweeps -> sweep_surface_cut -> seed_surface_classes -> the surface -> sweep_slot_aps ->
    enabled_sweeps. The rung filter reads only `dungeon_sweep`, so it is safe from either side.
    """
    opt = getattr(getattr(world, "options", None), "dungeon_sweep", None)
    key = getattr(opt, "current_key", None) or "bosses"
    allowed = _SWEEP_RUNGS.get(key, _SWEEP_RUNGS["bosses"])
    out, unjoined = {}, []
    runtime_skips = contract.runtime_sweep_skips()
    if allowed:
        for fl, members in DUNGEON_SWEEPS.items():
            # #878: a trigger positively known not to fire is not a runtime sweep. Keep the baked
            # table as evidence, but never send this group to the client/tracker. Do NOT use the
            # wider sweep_slot_skips() set here: unnamed/unaudited groups are unsafe for required
            # progression, not proven dead at runtime.
            if fl in runtime_skips:
                continue
            info = BOSS_HEALTHBARS.get(fl)
            if info is None:
                # A sweep whose boss is not in boss_healthbars cannot be classified. Count it, say
                # so, and keep it only at the widest rung -- a filter with no tally is a lie.
                unjoined.append(fl)
                if key != "bosses":
                    continue
            elif info[2] not in allowed:
                continue
            out[fl] = members
    return (out, unjoined, key) if _want_unjoined else out


def enabled_sweeps(world):
    """The sweeps this seed actually grants: {boss flag: [member ap ids]} at the chosen rung.

    ONE definition, so every consumer (the slot_data emit below, the progression surface, bingo)
    agrees on which groups exist: a member treated as swept when its sweep is not emitted would be
    stranded behind a trigger that never fires."""
    rung, unjoined, key = rung_sweeps(world, _want_unjoined=True)
    if not rung:
        return {}
    # ...and the PER-SEED surface cut on top of the rung. gen_data admits the six cuttable classes
    # into the baked member lists; this seed takes back the ones its own Progression Surface claims.
    #
    # 🛑 SweepSlot (contract.SURFACE_DERIVED_CLASSES) is deliberately NOT consulted here. It is not
    # one of _SWEEP_SURFACE_CUTTABLE, so a seed that puts SweepSlot on its surface does NOT lose the
    # member it just nominated -- that is the whole point of the class, and it is why the cut reads
    # `_SWEEP_SURFACE_CUTTABLE & seed_surface_classes` rather than the raw selection. Were it
    # otherwise this would be self-referential: the surface would name the sweep, the cut would
    # remove it, and the surface would then be naming a member that no longer exists.
    surface_cut = sweep_surface_cut(world)
    out, cut_links, emptied = {}, 0, []
    bingo_reserved = (set(getattr(world, "gf_bingo_line_sweep", ())) | set(getattr(world, "gf_bingo_protected_checks", ())))
    for fl, members in rung.items():
        members = [ap for ap in members if ap not in bingo_reserved]
        if not members:
            continue
        if surface_cut:
            kept_members = [ap for ap in members if ap not in surface_cut]
            cut_links += len(members) - len(kept_members)
            if not kept_members:
                # Possible only now that a group's whole membership can be surface-claimed. An empty
                # group is not a sweep: the client would draw a group that can never grant anything.
                emptied.append(fl)
                continue
            out[fl] = kept_members
        else:
            out[fl] = members
    if unjoined:
        import warnings
        warnings.warn("dungeon_sweep: %d sweep(s) have no boss_healthbars class and were %s: %s"
                      % (len(unjoined), "kept (rung=bosses)" if key == "bosses" else "dropped",
                         sorted(unjoined)[:5]))
    if cut_links or emptied:
        # Rule 4: say the size of the cut out loud. A seed's sweep total moving because the player
        # ticked a surface class is intended; it moving for any other reason is not, and this is the
        # only number that can tell those apart after the fact.
        print("dungeon_sweep: progression-surface cut removed %d member link(s)%s"
              % (cut_links, ", emptying %d group(s)" % len(emptied) if emptied else ""))
    return out


@register
class BossLocks(Feature):
    def extend_hint_information(self, world, hint_data):
        from ..sweep_hints import instructions
        # Read the final wire payload, including region additions, arena filtering and bingo cuts.
        sweeps = self.slot_data(world).get(contract.DUNGEON_SWEEP_FLAGS, {})
        candidates = {aid for members in DUNGEON_SWEEPS.values() for aid in members}
        locations = {loc.address for loc in world.multiworld.get_locations(world.player)
                     if loc.address is not None}
        hints = instructions(locations, candidates, sweeps, BOSS_HEALTHBARS)
        for aid in set(getattr(world, "gf_bingo_line_sweep", ())) & locations:
            hints[aid] = "Collected by a bingo line"
        hint_data.setdefault(world.player, {}).update(hints)

    name = "boss_locks"
    OPTIONS = {"dungeon_sweep": DungeonSweep, "full_area_sweeps": FullAreaSweeps,
               "region_sweep": RegionSweep,
               "reveal_sweep_boss_names": RevealSweepBossNames,
               "boss_lock_placement": BossLockPlacement, "boss_keys": BossKeys}
    RETIRED_ITEM_SLOTS = RETIRED_BOSS_KEY_ID_SLOTS

    def slot_data(self, world):
        kept = set(world._kept())
        boss_locs = {r: [aid for (aid, _f, _n) in REGION_BOSSES[r]]
                     for r in REGION_BOSSES if r in kept}
        sd = {"bossLocations": boss_locs}
        if world.options.reveal_sweep_boss_names.value:
            # A client predating #1184 would silently ignore the chosen spoiler policy. Refuse that
            # pairing loudly only for opted-in seeds; the default remains compatible with old DLLs.
            sd[contract.REQUIRES_CLIENT_FEATURES] = ["reveal_sweep_boss_names"]
        # "Felled: <Boss>" trophy tracking (slot_data + client only; zero fill risk). The client
        # mints a 'Felled: <Boss>' trophy when the boss_flag fires; er-logic boss_felled / region.rs
        # read this map keyed by boss-defeat flag. BASE-game bosses only: the DLC entries existed to
        # carry the Boss Keys gate hint, and Boss Keys were deleted 2026-10-06.
        _items = {}
        for r in REGION_BOSSES:
            if r not in kept or r in DLC_REGIONS:
                continue
            for (aid, fl, reward) in REGION_BOSSES[r]:
                _items[str(fl)] = {"name": "Felled: " + _boss_label(reward), "region": r,
                                   "boss_ap_id": aid}
        sd[contract.BOSS_LOCK_ITEMS] = _items
        if world.options.dungeon_sweep.value != 0:
            # FLAG-KEYED sweeps (boss-defeat flag -> member ap-ids), scoped to kept regions. Derived
            # from DarkScript EMEVD (boss_sweeps.py). A small client handler that watches the
            # boss-defeat flag and grants the members activates these in-game (P3b-client).
            _live = enabled_sweeps(world)
            # region_sweep (SPEC-region-completion-release.md): the region's gating boss additionally
            # releases the REST of its region, unioned onto whatever design-1 sweep already sits on
            # that same trigger flag (most gating bosses already own a smaller group here). Only
            # widens an existing group or adds a new one -- never removes a member design 1 granted.
            for _fl, _region_members in region_sweep_groups(world, kept).items():
                _live[_fl] = sorted(set(_live.get(_fl, ())) | set(_region_members))
            # #445: a group is emitted only when BOTH its members' region and its trigger's ARENA
            # region are kept. Dropping it here is what stops the F6 tracker promising "0/104 checks
            # -- waiting on the boss" for a boss this seed can never let the player fight. The
            # members are unaffected: each is an ordinary location in `locationFlags` and is still
            # collected by walking to it. What is lost is the convenience the sweep was, and saying
            # so beats rendering a row that will never move.
            _dropped = unreachable_sweeps(_live, kept)
            reserved = (set(getattr(world, "gf_bingo_line_sweep", ())) | set(getattr(world, "gf_bingo_protected_checks", ())))
            sd[contract.DUNGEON_SWEEP_FLAGS] = {
                str(fl): members for fl in _live
                if sweep_trigger_reachable(fl, kept)
                and (members := [ap for ap in _live[fl] if ap not in reserved])}
            _unaudited = [fl for fl in _live if fl not in SWEEP_ARENA_REGION]
            print("[greenfield] dungeon sweeps: %d group(s) armed; %d dropped as UNFIREABLE "
                  "(trigger's arena region not kept, #445)%s; %d group(s) UNAUDITED (no arena row -- "
                  "not verified clean)"
                  % (len(sd[contract.DUNGEON_SWEEP_FLAGS]), len(_dropped),
                     (" -- " + ", ".join("%d %s members, arena %s (%d checks)"
                                         % (fl, _dropped[fl][0], _dropped[fl][1], len(_live[fl]))
                                         for fl in sorted(_dropped, key=lambda x: -len(_live[x]))))
                     if _dropped else "",
                     len(_unaudited)))
            # dungeonSweeps: NOT emitted (#1463). The location-keyed variant needs a
            # boss-reward-location join we never built, so this line only ever wrote `{}` -- which
            # reads identically to absent on the client (flagpoll.rs parse_dungeon_sweeps) while
            # making the contract claim greenfield produces a bedrock key. The key is now tagged
            # BEDROCK-only and emitting it here would fail validate_slot_data's foreign-key check.
        return sd
