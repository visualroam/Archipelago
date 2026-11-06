from typing import Dict, List, NamedTuple, Set, Optional
from BaseClasses import Location

from .names import location_names as lname, region_names as rname
from .options import REPOGameOptions

class REPOLocation(Location):
    game: str = "R.E.P.O"

location_base_id: int = 75912022

class REPOLocationData(NamedTuple):
    region: str
    location_id_offset: int
    location_group: Optional[str] = None


level_types = ["Swiftbroom Academy ","Headman Manor ","McJannek Station ","Museum of Human Art ","Sunstone Valley Resort "]
pelly_types = [lname.standard_pelly,lname.glass_pelly,lname.gold_pelly]

v = 200 # Valuable Base ID
e = 500 # Monster Base ID
location_table: Dict[str, REPOLocationData] = { 
    # ---- Shop Upgrade Purchases ----
    # Reserved 1 - 100 for shop
    # lname.upgrade_pur + " 1": REPOLocationData(rname.shop,1,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 2": REPOLocationData(rname.shop,2,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 3": REPOLocationData(rname.shop,3,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 4": REPOLocationData(rname.shop,4,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 5": REPOLocationData(rname.shop,5,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 6": REPOLocationData(rname.shop,6,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 7": REPOLocationData(rname.shop,7,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 8": REPOLocationData(rname.shop,8,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 9": REPOLocationData(rname.shop,9,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 10": REPOLocationData(rname.shop,10,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 11": REPOLocationData(rname.shop,11,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 12": REPOLocationData(rname.shop,12,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 13": REPOLocationData(rname.shop,13,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 14": REPOLocationData(rname.shop,14,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 15": REPOLocationData(rname.shop,15,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 16": REPOLocationData(rname.shop,16,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 17": REPOLocationData(rname.shop,17,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 18": REPOLocationData(rname.shop,18,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 19": REPOLocationData(rname.shop,19,"Shop Upgrade Purchase"),
    # lname.upgrade_pur + " 20": REPOLocationData(rname.shop,20,"Shop Upgrade Purchase"),

    # ---- Pellys ----
    # -- Swiftbroom --
    level_types[0] + lname.standard_pelly: REPOLocationData(rname.swiftbroom,101,"Standard Pelly"),
    level_types[0] + lname.glass_pelly:    REPOLocationData(rname.swiftbroom,102,"Glass Pelly"),
    level_types[0] + lname.gold_pelly:     REPOLocationData(rname.swiftbroom,103,"Gold Pelly"),

    # -- Headman --
    level_types[1] + lname.standard_pelly: REPOLocationData(rname.headman,104,"Standard Pelly"),
    level_types[1] + lname.glass_pelly:    REPOLocationData(rname.headman,105,"Glass Pelly"),
    level_types[1] + lname.gold_pelly:     REPOLocationData(rname.headman,106,"Gold Pelly"),

    # -- McJannek --
    level_types[2] + lname.standard_pelly: REPOLocationData(rname.mcjannek,107,"Standard Pelly"),
    level_types[2] + lname.glass_pelly:    REPOLocationData(rname.mcjannek,108,"Glass Pelly"),
    level_types[2] + lname.gold_pelly:     REPOLocationData(rname.mcjannek,109,"Gold Pelly"),

    # -- Museum --
    level_types[3] + lname.standard_pelly: REPOLocationData(rname.museum,110,"Standard Pelly"),
    level_types[3] + lname.glass_pelly:    REPOLocationData(rname.museum,111,"Glass Pelly"),
    level_types[3] + lname.gold_pelly:     REPOLocationData(rname.museum,112,"Gold Pelly"),

    # -- Sunstone --
    level_types[4] + lname.standard_pelly: REPOLocationData(rname.sunstone,113,"Standard Pelly"),
    level_types[4] + lname.glass_pelly:    REPOLocationData(rname.sunstone,114,"Glass Pelly"),
    level_types[4] + lname.gold_pelly:     REPOLocationData(rname.sunstone,115,"Gold Pelly"),

    # ---- Valuables ----
    # -- Headman Manor --
    lname.goblet:	            REPOLocationData(rname.headman,v,       "Light Valuable"),
    lname.uranium_mug:	        REPOLocationData(rname.headman,(v:=v+1),"Light Valuable"),
    lname.emerald_bracelet:	    REPOLocationData(rname.headman,(v:=v+1),"Light Valuable"),
    lname.ocarina:	            REPOLocationData(rname.headman,(v:=v+1),"Light Valuable"),
    lname.pocket_watch:	        REPOLocationData(rname.headman,(v:=v+1),"Light Valuable"),
    lname.music_box:	        REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.instrument:	        REPOLocationData(rname.headman,(v:=v+1),"Medium+ Valuable"),
    lname.doll:	                REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.uranium_plate:	    REPOLocationData(rname.headman,(v:=v+1),"Light Valuable"),
    lname.globe:	            REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.frog:	                REPOLocationData(rname.headman,(v:=v+1),"Light Valuable"),
    lname.toy_monkey:	        REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.money:	            REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.small_vase:	        REPOLocationData(rname.headman,(v:=v+1),"Light Valuable"),
    lname.radio:	            REPOLocationData(rname.headman,(v:=v+1),"Medium+++ Valuable"),
    lname.gramophone:	        REPOLocationData(rname.headman,(v:=v+1),"Medium++ Valuable"),
    lname.ship_in_a_bottle:	    REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.kettle:	            REPOLocationData(rname.headman,(v:=v+1),"Light+ Valuable"),
    lname.old_camera:	        REPOLocationData(rname.headman,(v:=v+1),"Medium++ Valuable"),
    lname.magnifying_glass:	    REPOLocationData(rname.headman,(v:=v+1),"Light++ Valuable"),
    lname.map:	                REPOLocationData(rname.headman,(v:=v+1),"Light++ Valuable"),
    lname.vase:	                REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.bottle:	            REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.clown_doll:	        REPOLocationData(rname.headman,(v:=v+1),"Medium++ Valuable"),
    lname.trophy:	            REPOLocationData(rname.headman,(v:=v+1),"Medium Valuable"),
    lname.television:	        REPOLocationData(rname.headman,(v:=v+1),"Heavy Valuable"),
    lname.diamond_display:	    REPOLocationData(rname.headman,(v:=v+1),"Medium+++ Valuable"),
    lname.scream_doll:	        REPOLocationData(rname.headman,(v:=v+1),"Medium++ Valuable"),
    lname.telescope:	        REPOLocationData(rname.headman,(v:=v+1),"Medium++ Valuable"),
    lname.chunky_vase:	        REPOLocationData(rname.headman,(v:=v+1),"Heavy++ Valuable"),
    lname.big_vase:	            REPOLocationData(rname.headman,(v:=v+1),"Heavy Valuable"),
    lname.piano:	            REPOLocationData(rname.headman,(v:=v+1),"Very Heavy Valuable"),
    lname.animal_crate:	        REPOLocationData(rname.headman,(v:=v+1),"Heavy Valuable"),
    lname.harp:	                REPOLocationData(rname.headman,(v:=v+1),"Heavy Valuable"),
    lname.painting:	            REPOLocationData(rname.headman,(v:=v+1),"Heavy Valuable"),
    lname.grandfather_clock:	REPOLocationData(rname.headman,(v:=v+1),"Heavy Valuable"),
    lname.dinosaur:	            REPOLocationData(rname.headman,(v:=v+1),"Heavy Valuable"),
    lname.golden_statue:	    REPOLocationData(rname.headman,(v:=v+1),"Heavy+ Valuable"),
    lname.coffin:	            REPOLocationData(rname.headman,(v:=v+1),"Very Heavy Valuable"),

    # -- McJannek Station --
    lname.keycard:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Light++ Valuable"),
    lname.uranium_petri_dish:	REPOLocationData(rname.mcjannek,(v:=v+1),"Light Valuable"),
    lname.eraser:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Light++ Valuable"),
    lname.pills:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Light Valuable"),
    lname.stapler:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Light Valuable"),
    lname.usb_stick:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Light Valuable"),
    lname.coffee_cup:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Light+ Valuable"),
    lname.smartwatch:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Light++ Valuable"),
    lname.phone:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Light Valuable"),
    lname.bonsai:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.hdd:	                REPOLocationData(rname.mcjannek,(v:=v+1),"Medium++ Valuable"),
    lname.calculator:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.vhs:	                REPOLocationData(rname.mcjannek,(v:=v+1),"Light++ Valuable"),
    lname.camera:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.laptop:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.sample:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.sample_pack:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Medium++ Valuable"),
    lname.fan:	                REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.computer:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium++ Valuable"),
    lname.printer_3d:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Medium+++ Valuable"),
    lname.propane_tank:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.scale:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium++ Valuable"),
    lname.flashlight:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Medium+ Valuable"),
    lname.fire_extinguisher:	REPOLocationData(rname.mcjannek,(v:=v+1),"Medium+ Valuable"),
    lname.icepick:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium++ Valuable"),
    lname.explosive_barrel:	    REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy Valuable"),
    lname.sample_cooler:	    REPOLocationData(rname.mcjannek,(v:=v+1),"Medium+++ Valuable"),
    lname.big_sample:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.creature_leg:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy+ Valuable"),
    lname.guitar:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium+++ Valuable"),
    lname.ice_saw:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Medium Valuable"),
    lname.flamethrower:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy Valuable"),
    lname.ice_block:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy+ Valuable"), 
    lname.snow_bike:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy+ Valuable"),
    lname.centrifuge:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy++ Valuable"),
    lname.sample_cooler_wide:	REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy++ Valuable"),
    lname.science_station:	    REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy+ Valuable"),
    lname.heavy_water:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Very Heavy Valuable"),
    lname.jackhammer:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Medium++++ Valuable"),
    lname.server_rack:	        REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy+ Valuable"),
    lname.cryo_pod:	            REPOLocationData(rname.mcjannek,(v:=v+1),"Heavy+ Valuable"),

    # -- Swiftbroom Academy --
    lname.eye_ball:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Light+ Valuable"),
    lname.diamond:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Light Valuable"),
    lname.bird_skull:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Light+ Valuable"),
    lname.bug:	                REPOLocationData(rname.swiftbroom,(v:=v+1),"Light Valuable"),
    lname.glowing_jar:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Light Valuable"),
    lname.small_gem:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium Valuable"),
    lname.small_potion:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Light Valuable"),
    lname.chomp_book:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Light Valuable"),
    lname.love_potion:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium Valuable"),
    lname.red_mushroom:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Light+ Valuable"),
    lname.pendant:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium++ Valuable"),
    lname.fortune_card:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Light+ Valuable"),
    lname.levitation_potion:	REPOLocationData(rname.swiftbroom,(v:=v+1),"Light+ Valuable"),
    lname.gem_box:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium Valuable"),
    lname.crown:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Light Valuable"),
    lname.power_crystal:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium Valuable"),
    lname.time_glass:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium Valuable"),
    lname.goblin_head:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium+++ Valuable"),
    lname.tentacle:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium Valuable"),
    lname.star_wand:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Light Valuable"),
    lname.poison_chalice:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium++ Valuable"),
    lname.crystal:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Light Valuable"),
    lname.crystal_ball:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium+++ Valuable"),
    lname.eye_of_orpigox:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium++++ Valuable"),
    lname.cube_of_knowledge:	REPOLocationData(rname.swiftbroom,(v:=v+1),"Heavy++ Valuable"),
    lname.master_potion:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium+++ Valuable"),
    lname.unicorn_horn:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium+ Valuable"),
    lname.forever_candle:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Heavy Valuable"),
    lname.cauldron_box:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Heavy Valuable"),
    lname.spider_potion:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium+++ Valuable"),
    lname.griffin_statue:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Very Heavy Valuable"),
    lname.dragon_skull:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Heavy++ Valuable"),
    lname.alchemy_staion:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Heavy Valuable"),
    lname.goblin_arm:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Heavy+ Valuable"),
    lname.dumgolfs_staff:	    REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium++++ Valuable"),
    lname.sword:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium+++ Valuable"),
    lname.broom:	            REPOLocationData(rname.swiftbroom,(v:=v+1),"Medium++++ Valuable"),
    lname.troll_finger:	        REPOLocationData(rname.swiftbroom,(v:=v+1),"Very Heavy Valuable"),

    # -- Museum of Human Art --
    lname.tooth:	            REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.silverfish:	        REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.rubendoll:	        REPOLocationData(rname.museum,(v:=v+1),"Medium Valuable"),
    lname.goldfish:	            REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.fish:	                REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.cool_brain:	        REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.toast:	            REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.goldtooth:	        REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.wire_figure:	        REPOLocationData(rname.museum,(v:=v+1),"Light+ Valuable"),
    lname.flesh_blob:	        REPOLocationData(rname.museum,(v:=v+1),"Medium Valuable"),
    lname.banana_bow:	        REPOLocationData(rname.museum,(v:=v+1),"Light++ Valuable"),
    lname.cubic_tower:	        REPOLocationData(rname.museum,(v:=v+1),"Light+ Valuable"),
    lname.car:	                REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.ladybug:	            REPOLocationData(rname.museum,(v:=v+1),"Medium++ Valuable"),
    lname.duck_man:	            REPOLocationData(rname.museum,(v:=v+1),"Light+ Valuable"),
    lname.cube_ball:	        REPOLocationData(rname.museum,(v:=v+1),"Light+ Valuable"),
    lname.cocktail:	            REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.pimpleguy:	        REPOLocationData(rname.museum,(v:=v+1),"Medium Valuable"),
    lname.plane:	            REPOLocationData(rname.museum,(v:=v+1),"Light Valuable"),
    lname.pacifier:	            REPOLocationData(rname.museum,(v:=v+1),"Medium+++ Valuable"),
    lname.monkeybox:	        REPOLocationData(rname.museum,(v:=v+1),"Medium++ Valuable"),
    lname.gumball:	            REPOLocationData(rname.museum,(v:=v+1),"Medium++ Valuable"),
    lname.handface:	            REPOLocationData(rname.museum,(v:=v+1),"Medium+++ Valuable"),
    lname.cubic_sculpture:	    REPOLocationData(rname.museum,(v:=v+1),"Medium+++ Valuable"),
    lname.teeth_bot:	        REPOLocationData(rname.museum,(v:=v+1),"Medium+ Valuable"),
    lname.uranium_mug_deluxe:	REPOLocationData(rname.museum,(v:=v+1),"Medium++++ Valuable"),
    lname.golden_swirl:	        REPOLocationData(rname.museum,(v:=v+1),"Heavy++ Valuable"),
    lname.boombox:	            REPOLocationData(rname.museum,(v:=v+1),"Medium Valuable"),
    lname.gem_burger:	        REPOLocationData(rname.museum,(v:=v+1),"Medium++++ Valuable"),
    lname.baby_head:	        REPOLocationData(rname.museum,(v:=v+1),"Medium+++ Valuable"),
    lname.egg:	                REPOLocationData(rname.museum,(v:=v+1),"Medium+++ Valuable"),
    lname.horse:	            REPOLocationData(rname.museum,(v:=v+1),"Very Heavy Valuable"),
    lname.worm:	                REPOLocationData(rname.museum,(v:=v+1),"Heavy+ Valuable"),
    lname.vinyl:	            REPOLocationData(rname.museum,(v:=v+1),"Heavy++ Valuable"),
    lname.tray:	                REPOLocationData(rname.museum,(v:=v+1),"Heavy Valuable"),
    lname.milk:	                REPOLocationData(rname.museum,(v:=v+1),"Heavy Valuable"),
    lname.tall_guy:	            REPOLocationData(rname.museum,(v:=v+1),"Heavy+ Valuable"),
    lname.blender:	            REPOLocationData(rname.museum,(v:=v+1),"Medium+++ Valuable"),
    lname.traffic_light:	    REPOLocationData(rname.museum,(v:=v+1),"Heavy+ Valuable"),

    # Sunstone Valley Resort
    lname.golden_coin:          REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.golden_horse_shoe:    REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.golden_lock:          REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.lighter:              REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.magnet:               REPOLocationData(rname.sunstone,(v:=v+1),"Light++ Valuable"),
    lname.snow_globe:           REPOLocationData(rname.sunstone,(v:=v+1),"Light++ Valuable"),
    lname.mouth_harp:           REPOLocationData(rname.sunstone,(v:=v+1),"Light Valuable"),
    lname.fossil:               REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.gold_bar:             REPOLocationData(rname.sunstone,(v:=v+1),"Medium++ Valuable"),
    lname.horse_on_wheels:      REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.lunch_box:            REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.post_card:            REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.sippy_cup:            REPOLocationData(rname.sunstone,(v:=v+1),"Light++ Valuable"),
    lname.snake_in_a_can:       REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.harmonica:            REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.pan_flute:            REPOLocationData(rname.sunstone,(v:=v+1),"Medium Valuable"),
    lname.backpack:             REPOLocationData(rname.sunstone,(v:=v+1),"Light++ Valuable"),
    lname.cowboy_action_figure: REPOLocationData(rname.sunstone,(v:=v+1),"Medium+ Valuable"),
    lname.cowboy_boot_trophy:   REPOLocationData(rname.sunstone,(v:=v+1),"Medium+++ Valuable"),
    lname.fluffy_buddy:         REPOLocationData(rname.sunstone,(v:=v+1),"Light++ Valuable"),
    lname.mineral_case:         REPOLocationData(rname.sunstone,(v:=v+1),"Medium+++ Valuable"),
    lname.rattlesnake:          REPOLocationData(rname.sunstone,(v:=v+1),"Light+ Valuable"),
    lname.suitcase:             REPOLocationData(rname.sunstone,(v:=v+1),"Medium++ Valuable"),
    lname.banjo:                REPOLocationData(rname.sunstone,(v:=v+1),"Medium+++ Valuable"),
    lname.golden_shovel:        REPOLocationData(rname.sunstone,(v:=v+1),"Medium++ Valuable"),
    lname.golden_wheel:         REPOLocationData(rname.sunstone,(v:=v+1),"Medium+++ Valuable"),
    lname.energy_crystal_chunk: REPOLocationData(rname.sunstone,(v:=v+1),"Heavy+ Valuable"),
    lname.rocking_chair:        REPOLocationData(rname.sunstone,(v:=v+1),"Medium+++ Valuable"),
    lname.distillery:           REPOLocationData(rname.sunstone,(v:=v+1),"Heavy++ Valuable"),
    lname.popcorn_stand:        REPOLocationData(rname.sunstone,(v:=v+1),"Heavy++ Valuable"),
    lname.golfcart:             REPOLocationData(rname.sunstone,(v:=v+1),"Heavy++ Valuable"),
    lname.shooting_cowboy:      REPOLocationData(rname.sunstone,(v:=v+1),"Medium+++ Valuable"),
    lname.bird_cage:            REPOLocationData(rname.sunstone,(v:=v+1),"Heavy Valuable"),
    lname.explosive_tower:      REPOLocationData(rname.sunstone,(v:=v+1),"Heavy+ Valuable"),
    lname.zero_grav_crystal:    REPOLocationData(rname.sunstone,(v:=v+1),"Heavy+ Valuable"),


    # ---- Enemy Souls ----
    lname.animal_soul   	    : REPOLocationData(rname.menu,e,       "Monster Soul"),
    lname.apex_predator_soul    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.bella_soul    	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.birthday_boy_soul	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.bowtie_soul   	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.chef_soul     	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.cleanup_crew_soul	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.clown_soul    	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.elsa_soul     	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.gambit_soul   	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.headgrab_soul 	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.headman_soul  	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.heart_hugger_soul	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.hidden_soul   	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.huntsman_soul 	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.loom_soul     	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.mentalist_soul	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.oogly_soul    	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.peeper_soul    	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.reaper_soul   	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.robe_soul     	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.rugrat_soul   	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.shadow_child_soul	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.spewer_soul   	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.tick_soul    	        : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),      # only drops if the tick absorbs enough health from the player to reach 100hp
    lname.trudge_soul   	    : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.upscream_soul	        : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),
    lname.pony_soul	            : REPOLocationData(rname.menu,(e:=e+1),"Monster Soul"),

    # ---- Event Locations ----
    "Victory": REPOLocationData(rname.menu,None,"Event")

}

for i in range(100):
    location_table[lname.upgrade_pur + " " + str(i+1)] = REPOLocationData(rname.shop,i+1,"Shop Upgrade Purchase")

location_name_to_id: Dict[str, int] = {}

for name, data in location_table.items():
    if data.location_id_offset != None:
        location_name_to_id.update({name:data.location_id_offset + location_base_id})
    else:
        location_name_to_id.update({name:None})

def get_location_group(location_name: str) -> str:
    return location_table[location_name].location_group

event_locations: List[str] = [name for name, data in location_table.items() if data.location_group == "Event"]

temp_loc_total: int = 0

location_name_groups: Dict[str, Set[str]] = {}
pelly_list: list[REPOLocationData] = []

for loc_name, loc_data in location_table.items():
    if loc_data.location_id_offset != None:
        temp_loc_total += 1

    if loc_data.location_group:
        location_name_groups.setdefault(loc_data.location_group, set()).add(loc_name)

    if loc_name.__contains__("Pelly"):
        pelly_list.append(loc_name)

location_total: int = temp_loc_total