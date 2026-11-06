from itertools import groupby
from typing import Dict, List, Set, NamedTuple
from BaseClasses import ItemClassification, Item

from .names import item_names as iname

class REPOItem(Item):
    game: str = "R.E.P.O"

item_base_id: int = 75912022        # not required anymore, but it doesn't hurt

class REPOItemData(NamedTuple):
    classification: ItemClassification
    quantity_in_item_pool: int
    item_id_offset: int
    item_group: str = ""


# a lot of quantities here will need to be adjusted later

base_shop_offset = 10

#Last used number - 60
item_table: Dict[str, REPOItemData] = {
    
    # ---- LEVELS ----
    #0-9 Reserved for Levels
    iname.swiftbroom_lvl: REPOItemData(ItemClassification.progression,1,0,"Level"),
    iname.headman_lvl: REPOItemData(ItemClassification.progression,1,1,"Level"),
    iname.mcjannek_lvl: REPOItemData(ItemClassification.progression,1,2,"Level"),
    iname.museum_lvl: REPOItemData(ItemClassification.progression,1,3,"Level"),
    iname.sunstone_lvl: REPOItemData(ItemClassification.progression,1,4,"Level"),

    # ---- AP Function Items ----
    iname.shop_stock: REPOItemData(ItemClassification.progression,0,base_shop_offset,"Progressive Shop"),

    # ---- UPGRADES ----
    iname.health_up: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.strength_up: REPOItemData(ItemClassification.progression_deprioritized_skip_balancing,13,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.range_up: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.sprint_up: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.stamina_up: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.player_count_up: REPOItemData(ItemClassification.filler,1,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.double_jump_up: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.tumble_up: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.crouch_rest: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.tumble_wings: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.tumble_climb: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),
    iname.death_head_battery: REPOItemData(ItemClassification.filler,3,(base_shop_offset:=base_shop_offset+1),"Upgrades"),

    # ---- SHOP UNLOCKS ----
    iname.small_health: REPOItemData(ItemClassification.filler,0,(base_shop_offset:=base_shop_offset+1),"Misc Filler"),
    #iname.medium_health: REPOItemData(ItemClassification.filler,2,(base_shop_offset:=base_shop_offset+1),"Health Pack"),   #these were meant to be filler but aren't implemented
    #iname.large_health: REPOItemData(ItemClassification.filler,2,(base_shop_offset:=base_shop_offset+1),"Health Pack"),
    iname.progressive_health: REPOItemData(ItemClassification.useful,3,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.baseball_bat: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Melee Shop Unlock"),
    iname.frying_pan: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Melee Shop Unlock"),
    iname.sledge_hammer: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Melee Shop Unlock"),
    iname.sword: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Melee Shop Unlock"),
    iname.inflatable_hammer: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.prodzap: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.gun: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Ranged Shop Unlock"),
    iname.shotgun: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Ranged Shop Unlock"),
    iname.tranq_gun: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.pulse_pistol: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.photon_blaster: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Ranged Shop Unlock"),
    iname.boltzap: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.cart_cannon: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Ranged Shop Unlock"),
    iname.cart_laser: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Ranged Shop Unlock"),
    iname.grenade: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Explosive Shop Unlock"),
    iname.shock_grenade: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.human_grenade: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Explosive Shop Unlock"),
    iname.stun_grenade: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.duct_taped_grenade: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Explosive Shop Unlock"),
    iname.shockwave_mine: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.stun_mine: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.explosive_mine: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Explosive Shop Unlock"),
    iname.rubber_duck: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.recharge_drone: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.indestructible_drone: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.roll_drone: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.feather_drone: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),       # todo: add to custom rule
    iname.zero_grav_drone: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),     # todo: add to custom rule
    iname.pocket_cart: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.cart: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.valuable_detector: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.extraction_detector: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.energy_crystal: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.zero_grav_orb: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),            # todo: add to custom rule
    iname.duck_bucket: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.phase_bridge: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),

    # ---- Traps ----
    iname.monster_trap: REPOItemData(ItemClassification.trap,0,(base_shop_offset:=base_shop_offset+1),"Traps"),
    iname.audit_trap: REPOItemData(ItemClassification.trap,0,(base_shop_offset:=base_shop_offset+1),"Traps"),
    iname.lure_trap: REPOItemData(ItemClassification.trap,0,(base_shop_offset:=base_shop_offset+1),"Traps"),
    iname.moon_phase_trap: REPOItemData(ItemClassification.trap,0,(base_shop_offset:=base_shop_offset+1),"Traps"),

    # ---- Cosmetic Update ----
    iname.roll_staff: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.void_staff: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.zero_grav_staff: REPOItemData(ItemClassification.progression_deprioritized,1,(base_shop_offset:=base_shop_offset+1),"Stun Shop Unlock"),
    iname.leaf_blower: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.scout_vehicle: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.hauler_vehicle: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Shop Unlock"),
    iname.defibro: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),
    iname.semibot_walkies: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),

    # ---- Sunstone Update ----
    iname.human_adventure_cable: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Melee Shop Unlock"),
    iname.human_gun: REPOItemData(ItemClassification.progression,1,(base_shop_offset:=base_shop_offset+1),"Ranged Shop Unlock"),
    iname.recharge_orb: REPOItemData(ItemClassification.useful,1,(base_shop_offset:=base_shop_offset+1),"Shop Unlock"),

    # ---- Event Items ----
    "Victory": REPOItemData(ItemClassification.progression,0,None,"Event"),
}

item_name_to_id: Dict[str, int] ={}#= {name: combine_item_id(data) for name, data in item_table.items()}

for name, data in item_table.items():
    if data.item_id_offset != None:
        item_name_to_id.update({name:data.item_id_offset + item_base_id})
    else:
        item_name_to_id.update({name:None})
        

def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group

filler_items: List[str] = [name for name, data in item_table.items() if data.classification == ItemClassification.filler]

trap_items: List[str] = [name for name, data in item_table.items() if data.classification == ItemClassification.trap]
event_items: List[str] = [name for name, data in item_table.items() if data.item_group == "Event"]

item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_table, key=get_item_group), get_item_group) if group != ""
}

#item_limited_group = [iname.umami_training1,iname.umami_training2,iname.umami_training3,iname.googly_eye,iname.used_bandage]