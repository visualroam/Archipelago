from BaseClasses import MultiWorld, Region, Entrance, Location, ItemClassification
from . import LHP2Options
from .Locations import LHP2Location, hub_event_loc_table, level_beaten_loc_table
from .Items import LHP2Item
from .Options import EndGoal
from .Data import RegionName


level_regions = [
    RegionName.dt,
    RegionName.da,
    RegionName.foc,
    RegionName.kd,
    RegionName.agv,
    RegionName.avt,
    RegionName.oor,
    RegionName.jd,
    RegionName.ansmc,
    RegionName.lh,
    RegionName.ff,
    RegionName.thath,
    RegionName.tsh,
    RegionName.mim,
    RegionName.igd,
    RegionName.sal,
    RegionName.ll,
    RegionName.dob,
    RegionName.ttd,
    RegionName.bts,
    RegionName.bb,
    RegionName.fiend,
    RegionName.st,
    RegionName.tfitp
]

hub_regions = [
    RegionName.diag,
    RegionName.knock,
    RegionName.www,
    RegionName.mm,
    RegionName.cust,
    RegionName.leaky,
    RegionName.lond,
    RegionName.cafe,
    RegionName.kcs,
    RegionName.tent,
    RegionName.wild,
    RegionName.hogstat,
    RegionName.hogspath,
    RegionName.hogs,
    RegionName.hogwpath,
    RegionName.quad,
    RegionName.tg,
    RegionName.herb,
    RegionName.ground,
    RegionName.qp,
    RegionName.thest,
    RegionName.lake,
    RegionName.foyer,
    RegionName.low_stair,
    RegionName.mid_stair,
    RegionName.dumble_office,
    RegionName.upper_stair,
    RegionName.dormlob,
    RegionName.slyth,
    RegionName.huff,
    RegionName.gryf,
    RegionName.raven,
    RegionName.lib,
    RegionName.ghl,
    RegionName.wc,
    RegionName.wcs,
    RegionName.gh,
    RegionName.ror,
    RegionName.cl,
    RegionName.y5c,
    RegionName.y6c,
    RegionName.dada,
    RegionName.pot,
    RegionName.divc,
    RegionName.div,
    RegionName.ast,
]


freeplay_regions = [
    RegionName.daf,
    RegionName.focf,
    RegionName.agvf,
    RegionName.oorf,
    RegionName.ansmcf,
    RegionName.lhf,
    RegionName.fff,
    RegionName.thathf,
    RegionName.tshf,
    RegionName.mimf,
    RegionName.igdf,
    RegionName.llf,
    RegionName.dobf,
    RegionName.ttdf,
    RegionName.btsf,
    RegionName.bbf,
    RegionName.fiendf,
    RegionName.stf,
    RegionName.tfitpf,
]


lhp2_all_regions = [
    *level_regions,
    *hub_regions,
    *freeplay_regions,
]


def create_regions(world: MultiWorld, options: LHP2Options, player: int, seed_locs):
    menu = Region("Menu", player, world)
    world.regions.append(menu)

    for region in lhp2_all_regions:
        create_regions_and_locations(region, player, world, seed_locs)

    connect_regions(world, player, "Menu", RegionName.diag)
    connect_regions(world, player, RegionName.diag, RegionName.knock)
    # connect_regions(world, player, RegionName.knock, RegionName.ror)
    connect_regions(world, player, RegionName.diag, RegionName.www)
    connect_regions(world, player, RegionName.diag, RegionName.mm)
    connect_regions(world, player, RegionName.mm, RegionName.cust)
    connect_regions(world, player, RegionName.diag, RegionName.leaky)
    connect_regions(world, player, RegionName.leaky, RegionName.lond)
    connect_regions(world, player, RegionName.lond, RegionName.cafe)
    connect_regions(world, player, RegionName.lond, RegionName.tent)
    connect_regions(world, player, RegionName.tent, RegionName.wild)
    connect_regions(world, player, RegionName.lond, RegionName.kcs)
    connect_regions(world, player, RegionName.kcs, RegionName.hogstat)
    connect_regions(world, player, RegionName.hogstat, RegionName.hogwpath)
    connect_regions(world, player, RegionName.hogwpath, RegionName.hogspath)
    connect_regions(world, player, RegionName.hogspath, RegionName.hogs)
    connect_regions(world, player, RegionName.hogwpath, RegionName.quad)
    connect_regions(world, player, RegionName.quad, RegionName.tg)
    connect_regions(world, player, RegionName.tg, RegionName.herb)
    connect_regions(world, player, RegionName.quad, RegionName.foyer)
    connect_regions(world, player, RegionName.foyer, RegionName.ground)
    connect_regions(world, player, RegionName.ground, RegionName.thest)
    connect_regions(world, player, RegionName.ground, RegionName.qp)
    connect_regions(world, player, RegionName.ground, RegionName.lake)
    connect_regions(world, player, RegionName.foyer, RegionName.lib)
    connect_regions(world, player, RegionName.foyer, RegionName.ghl)
    connect_regions(world, player, RegionName.ghl, RegionName.gh)
    connect_regions(world, player, RegionName.ghl, RegionName.wc)
    connect_regions(world, player, RegionName.wc, RegionName.wcs)
    connect_regions(world, player, RegionName.ghl, RegionName.ror)
    connect_regions(world, player, RegionName.ror, RegionName.upper_stair)
    connect_regions(world, player, RegionName.foyer, RegionName.low_stair)
    connect_regions(world, player, RegionName.low_stair, RegionName.dormlob)
    connect_regions(world, player, RegionName.low_stair, RegionName.mid_stair)
    connect_regions(world, player, RegionName.mid_stair, RegionName.dumble_office)
    connect_regions(world, player, RegionName.dumble_office, RegionName.upper_stair)
    connect_regions(world, player, RegionName.upper_stair, RegionName.dumble_office)
    connect_regions(world, player, RegionName.upper_stair, RegionName.ror)
    connect_regions(world, player, RegionName.dormlob, RegionName.slyth)
    connect_regions(world, player, RegionName.dormlob, RegionName.huff)
    connect_regions(world, player, RegionName.dormlob, RegionName.gryf)
    connect_regions(world, player, RegionName.dormlob, RegionName.raven)
    connect_regions(world, player, RegionName.foyer, RegionName.cl)
    connect_regions(world, player, RegionName.cl, RegionName.dada)
    connect_regions(world, player, RegionName.cl, RegionName.y5c)
    connect_regions(world, player, RegionName.cl, RegionName.y6c)
    connect_regions(world, player, RegionName.cl, RegionName.pot)
    connect_regions(world, player, RegionName.cl, RegionName.divc)
    connect_regions(world, player, RegionName.divc, RegionName.ast)
    connect_regions(world, player, RegionName.divc, RegionName.div)

    for region in level_regions:
        connect_regions(world, player, RegionName.leaky, region)

    connect_regions(world, player, RegionName.da, RegionName.daf)
    connect_regions(world, player, RegionName.foc, RegionName.focf)
    connect_regions(world, player, RegionName.agv, RegionName.agvf)
    connect_regions(world, player, RegionName.oor, RegionName.oorf)
    connect_regions(world, player, RegionName.ansmc, RegionName.ansmcf)
    connect_regions(world, player, RegionName.lh, RegionName.lhf)
    connect_regions(world, player, RegionName.ff, RegionName.fff)
    connect_regions(world, player, RegionName.thath, RegionName.thathf)
    connect_regions(world, player, RegionName.tsh, RegionName.tshf)
    connect_regions(world, player, RegionName.mim, RegionName.mimf)
    connect_regions(world, player, RegionName.igd, RegionName.igdf)
    connect_regions(world, player, RegionName.ll, RegionName.llf)
    connect_regions(world, player, RegionName.dob, RegionName.dobf)
    connect_regions(world, player, RegionName.ttd, RegionName.ttdf)
    connect_regions(world, player, RegionName.bts, RegionName.btsf)
    connect_regions(world, player, RegionName.bb, RegionName.bbf)
    connect_regions(world, player, RegionName.fiend, RegionName.fiendf)
    connect_regions(world, player, RegionName.st, RegionName.stf)
    connect_regions(world, player, RegionName.tfitp, RegionName.tfitpf)

    diag_region = world.get_region(RegionName.diag, player)
    tfitpf_region = world.get_region(RegionName.tfitpf, player)
    create_events(world, options, player)
    if options.EndGoal == EndGoal.option_defeat_voldemort:
        event: Location = create_event("Defeat Voldemort", "Voldemort Defeated", tfitpf_region, player)
        event.show_in_spoiler = True
    if options.EndGoal == EndGoal.option_levels_beaten:
        event: Location = create_event("All Required Levels Beaten", "All Required Levels Beaten", diag_region, player)
        event.show_in_spoiler = True


def connect_regions(world: MultiWorld, player: int, source: str, target: str) -> Entrance:
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)
    return source_region.connect(target_region)


def create_regions_and_locations(name: str, player: int, world: MultiWorld, seed_locations) -> Region:
    region = Region(name, player, world)

    for (key, data) in seed_locations.items():
        if data.region == name:
            location = LHP2Location(player, key, data.id, region)
            region.locations.append(location)

    world.regions.append(region)
    return region


def create_events(world: MultiWorld, options: LHP2Options, player: int):

    for (name, data) in hub_event_loc_table.items():
        item_name = name + " Cleared"
        event: Location = create_event(name, item_name, world.get_region(data.region, player), player)
        event.show_in_spoiler = True

    if options.EndGoal == EndGoal.option_levels_beaten:
        disabled = set(options.DisabledLevels.value)
        for (name, data) in level_beaten_loc_table.items():
            if data.region in disabled or data.region.endswith(" Freeplay") and data.region[:-9] in disabled:
                continue
            location_name = name + " Token"
            item_name = "Level Beaten"
            event: Location = create_event(location_name, item_name, world.get_region(data.region, player), player)
            event.show_in_spoiler = True


def create_event(name: str, item_name: str, region: Region, player: int) -> Location:
    event = LHP2Location(player, name, None, region)
    region.locations.append(event)
    event.place_locked_item(LHP2Item(item_name, ItemClassification.progression, None, player))
    return event
