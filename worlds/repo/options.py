from dataclasses import dataclass
from Options import OptionSet, Toggle, Range, Choice, PerGameCommonOptions, TextChoice,random,ItemDict,OptionCounter, DefaultOnToggle, DeathLink
from .names import item_names as iname

# class Goal(Choice):
#     """Choose your goal for the multiworld
#     - Pelly Hunt: Exctract each of the Pelly Statues from all level types
#     - Level Quota: Complete a certain number of levels in a single run"""
#     display_name: str = "Goal"
#     option_pelly_hunt = 0
#     option_level_quota = 1
#     default = 0

class PellyHunt(Range):
    """Choose how many Pellys will be required for victory."""
    display_name: str = "Pellys Required"
    range_start = 0
    range_end = 15
    default = 12

class LevelQuota(Range):
    """Choose how many levels must be completed for your goal, in addition to gathering enough Pellys."""
    display_name: str = "Level Quota"
    range_start = 1
    range_end = 20
    default = 8

class ValuableHunt(Toggle):
    """Determines if extracting all valuables (excluding pellys) is required for your goal."""
    display_name: str = "Valuable Hunt"

class MonsterHunt(Toggle):
    """Determines if extracting all monster souls is required for your goal."""
    display_name : str = "Monster Hunt"

class CombatLogic(Choice):
    """Determines what items are logically required to fight monsters.
    Easy: Guns or Explosives
    Medium: Strength Upgrades + Stun Items, Melee Weapons, Guns, or Explosives
    Hard: No combat logic. Player may have to kill monsters with valuables found in levels."""
    display_name: str = "Combat Logic"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    default = 1

class ShopPackCount(Range):
    """Choose how many Archipelago Shop Items are unlocked with each Progressive Shop Stock."""
    display_name: str = "Progressive Shop Stock Amount"
    range_start = 5
    range_end = 50
    default = 10

class ShopUpgradeLocationsTotal(Range):
    """Choose how many Archipelago Items show up in the Upgrades section of the Shop."""
    display_name: str = "Total Shop Upgrade Locations"
    range_start = 20
    range_end = 100
    default = 80

class ShopUpgradeLocationsInLogic(Range):
    """Choose how many shop upgrades will potentially be logically relevant.
    Items past this number will not have progression items.
    This number gets set to the Total Shop Upgrade Locations if it is greater.\n"""
    display_name: str = "Shop Upgrade Locations in Logic"
    range_start = 20
    range_end = 100
    default = 60

class StartingLevelType(TextChoice):
    """Choose which level type to start with."""
    display_name: str = "Starting Level Type"
    option_swiftbroom_academy = 0
    option_headman_manor = 1
    option_mcjannek_station = 2
    option_museum_of_human_art = 3
    option_sunstone_valley_resort = 4
    default = "random"

class FillerItemWeights(OptionCounter):
    """Choose the weights for adding filler and traps to the item pool.
    Each upgrade item will spawn one upgrade of that type in the truck.
    Each small health pack spawns one small health pack (25hp) in the truck.
    Traps:
        Extra Monster Trap - Spawns an extra enemy (or enemy group) from the tier 3 enemy pool.
        Audit Trap - Takes half of your money the next time you visit a shop.
        Monster Lure Trap - Lures monsters to your location for two minutes.
        Progressive Moon Phase Trap - Increases the moon phase by one stage FOR THE REST OF THE MULTIWORLD."""
    display_name: str = "Filler Item Weights"
    min = 0
    max = 1000
    valid_keys = {
        iname.health_up,
        iname.strength_up,
        iname.range_up,
        iname.sprint_up,
        iname.stamina_up, 
        iname.player_count_up,      # does nothing in singleplayer and you only need one in multiplayer
        iname.double_jump_up, 
        iname.tumble_up,
        iname.tumble_wings,
        iname.crouch_rest,
        iname.tumble_climb,
        iname.death_head_battery,    # does nothing in singleplayer
        iname.small_health,
        iname.monster_trap,
        iname.audit_trap,
        iname.lure_trap,
        iname.moon_phase_trap    # there will never be more than 4
    }
    default = {
        iname.health_up : 40,
        iname.strength_up : 30,
        iname.range_up : 40,
        iname.sprint_up: 30,
        iname.stamina_up : 50, 
        #iname.player_count_up : 10,      # does nothing in singleplayer and you only need one in multiplayer
        iname.double_jump_up : 20, 
        iname.tumble_up : 20,
        iname.tumble_wings : 20,
        iname.crouch_rest : 40,
        iname.tumble_climb : 20,
        #iname.death_head_battery : 10,    # does nothing in singleplayer
        iname.small_health: 20,
        iname.monster_trap: 8,
        iname.audit_trap: 6,
        iname.lure_trap: 15,
        iname.moon_phase_trap: 2    # there will never be more than 4
    }

class AuditTrapMoneyLost(Range):
    """The percentage of the player's money that an Audit Trap will take when triggered."""
    display_name: str = "Audit Trap Money Lost"
    range_start = 5
    range_end = 100
    default = 33
    


@dataclass
class REPOGameOptions(PerGameCommonOptions):
    #goal: Goal
    pellys_required: PellyHunt
    level_quota: LevelQuota 
    valuable_hunt: ValuableHunt
    monster_hunt: MonsterHunt
    combat_logic: CombatLogic
    shop_stock: ShopPackCount
    shop_upgrade_total: ShopUpgradeLocationsTotal
    shop_upgrade_logical: ShopUpgradeLocationsInLogic
    starting_level_type: StartingLevelType
    filler_item_weights: FillerItemWeights
    audit_trap_money_lost: AuditTrapMoneyLost
    death_link: DeathLink

    
