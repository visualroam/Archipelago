from typing import TYPE_CHECKING, Dict, List
from worlds.generic.Rules import set_rule
from BaseClasses import CollectionState

from .options import REPOGameOptions
from .names import location_names as lname
from .names import item_names as iname
from .names import region_names as rname

if TYPE_CHECKING:
    from . import REPOWorld


#world: ACTWorld  #= ACTWorld()
# regions_to_exclude = []

# def set_options (options: ACTGameOptions):
#     if options.goal == "roland":
#         regions_to_exclude = [rname.unfathom,rname.plains,rname.old_ocean,rname.drain_bottom,rname.trash_island,rname.carcinia_ruins]

#     if options.goal == "voltai":
#         regions_to_exclude = [rname.pinbarge,rname.unfathom,rname.plains,rname.old_ocean,rname.drain_bottom,rname.trash_island,rname.carcinia_ruins]

#     if options.goal == "magista":
#         regions_to_exclude = [rname.reefs_edge,rname.new_carcinia,rname.sands_between,rname.post_pag,rname.secluded_ridge,rname.expired_grove,rname.grove_main,rname.grove_village,rname.flotsam_vale,rname.scuttleport,rname.pinbarge,rname.unfathom,rname.plains,rname.old_ocean,rname.drain_bottom,rname.trash_island,rname.carcinia_ruins]





#Checks to see if the player can logically consistently deal damage
#def can_deal_damage_hard(state: CollectionState,player:int) -> bool:
#    return can_rolling_attack(state,player) | can_magic_damage(state,player) | can_atk_damage_shell(state,player) | has_summon(state,player)  | state.has(iname.fork,player)
