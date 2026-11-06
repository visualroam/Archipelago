import math
import time
from typing import Dict, List, Any
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from BaseClasses import LocationProgressType, Region, ItemClassification, CollectionState, Tutorial
from Fill import fill_restrictive

from .items import item_table, item_name_groups, item_name_to_id, filler_items, trap_items, REPOItem, REPOItemData,event_items
from .locations import location_table, location_name_groups, location_name_to_id, location_total, REPOLocation, REPOLocationData,event_locations
from .regions import REPO_regions
from .rules import set_location_rules, set_region_rules
from .options import REPOGameOptions
from .names import location_names as lname, item_names as iname, region_names as rname


class REPOWeb(WebWorld):
    theme: str = "stone"
    game: str = "R.E.P.O"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago randomizer for R.E.P.O.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Automagic00"]
    )

    tutorials = [setup_en]

class REPOWorld(World):
    
    """
    R.E.P.O. is an online co-op horror game where you are tasked with extracting valuables from monster-filled locations.
    """
    game: str = "R.E.P.O"
    web = REPOWeb()

    options_dataclass = REPOGameOptions
    options: REPOGameOptions
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    location_total = location_total

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    
    
    
    def generate_output(self, output_directory: str):
        #visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}.puml", show_entrance_names=False ) #regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player]
        pass

    #def generate_early(self):
        #GenEarly
        

    def get_locations(self):
        return self.multiworld.get_locations(self.player)

    def pre_fill(self):
        #state = CollectionState(self.multiworld)
        #victory_loc = REPOLocation(self.player,shell_locations[i],None,region)
        return super().pre_fill()

    def create_item(self, name: str) -> REPOItem:
        item_data = item_table[name]
        if item_data.item_id_offset != None:
            return REPOItem(name, item_data.classification, self.item_name_to_id[name], self.player)
        else:
            return REPOItem(name, item_data.classification, None, self.player)

    def create_event(self, event: str) -> REPOItem:
        return REPOItem(event, True, None, self.player)

    def create_items(self) -> None:
        REPO_items: List[REPOItem] = []
        self.slot_data_items = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}


        # ---- YAML Options ----
        # -- Starting Level --
        if self.options.starting_level_type == self.options.starting_level_type.option_swiftbroom_academy:
            self.multiworld.push_precollected(self.create_item(iname.swiftbroom_lvl))
            items_to_create[iname.swiftbroom_lvl] = 0

        if self.options.starting_level_type == self.options.starting_level_type.option_mcjannek_station:
            self.multiworld.push_precollected(self.create_item(iname.mcjannek_lvl))
            items_to_create[iname.mcjannek_lvl] = 0

        if self.options.starting_level_type == self.options.starting_level_type.option_headman_manor:
            self.multiworld.push_precollected(self.create_item(iname.headman_lvl))
            items_to_create[iname.headman_lvl] = 0

        if self.options.starting_level_type == self.options.starting_level_type.option_museum_of_human_art:
            self.multiworld.push_precollected(self.create_item(iname.museum_lvl))
            items_to_create[iname.museum_lvl] = 0

        if self.options.starting_level_type == self.options.starting_level_type.option_sunstone_valley_resort:
            self.multiworld.push_precollected(self.create_item(iname.sunstone_lvl))
            items_to_create[iname.sunstone_lvl] = 0
        # -- Shop Stock --
        items_to_create[iname.shop_stock] = math.ceil((self.options.shop_upgrade_total / self.options.shop_stock) - 1)


        #Create Victory Event
        region = self.multiworld.get_region(rname.menu, self.player) 
        victory_loc = REPOLocation(self.player,"Victory",None,region)
        victory_loc.place_locked_item(REPOItem("Victory",ItemClassification.progression,None,self.player))
        region.locations.append(victory_loc)

        # fill empty locations with filler and traps
        ## I've had some issues with strange generation cases due to this way of handling filler items
        items_total: int = 0

        for item in items_to_create:
            items_total += items_to_create[item]

        total_filler = self.location_total - items_total

        available_filler: List[str] = [upgrade for upgrade in items_to_create if 
                                         (item_table[upgrade].item_group == "Upgrades" or 
                                                                            item_table[upgrade].item_group == "Misc Filler" or
                                                                            item_table[upgrade].item_group == "Traps")]
        print(available_filler)
        #print(trap_items)
        print("Loaction Count: " + str(self.location_total))
        print("Item Count: " + str(items_total))
        print("Total Filler: " + str(total_filler))
        if total_filler < 0:
            total_filler = 0

        #traps_needed = total_filler * self.options.trapamount.value / 100
        #print("Traps needed: " + str(math.floor(traps_needed)))

        #Trap Order for Weights: ['Extra Monster Trap', 'Monster Lure Trap', 'Audit Trap', 'Progressive Moon Phase Trap']
        #for counter in range(0, math.floor(traps_needed)):
        #    trap_item = self.random.choices(trap_items, weights=[3,3,2],k=1)
        #    items_to_create[trap_item[0]] += 1

        #filler_needed = total_filler - traps_needed
        filler_needed = total_filler
        print("Filler needed: " + str(math.ceil(filler_needed)))

        #Upgrade Order for Weights [Health Up, Strength Up, Range Up, Sprint Up, Stamina Up, Player Count Up, Double Jump Up, Tumble Launch Up] weights=[5,3,2,3,5,1,2,2]
        filler_weights = []

        for filler_item in available_filler:
            if filler_item in self.options.filler_item_weights:
                filler_weights.append(self.options.filler_item_weights[filler_item])
            else:
                filler_weights.append(0)

        for counter in range(0, math.ceil(filler_needed)):
            filler_item = self.random.choices(available_filler,weights= filler_weights,k=1)
            items_to_create[filler_item[0]] += 1
            if items_to_create[iname.moon_phase_trap] >= 4: 
                filler_weights[available_filler.index(iname.moon_phase_trap)] = 0

        # add items to item pool
        for item, quantity in items_to_create.items():
            print("Creating " + str(quantity) + " " + item)
            for i in range(quantity):
                REPO_item: REPOItem = self.create_item(item)
                REPO_items.append(REPO_item)

        self.multiworld.itempool += REPO_items

    def create_regions(self):

        for region_name in REPO_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name, exits in REPO_regions.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exits)

        for location_name, location_id in location_name_to_id.items():
            if location_id is not None:

                #Check that item doesnt fall out of options ranges
                if (location_table[location_name].location_group == "Shop Upgrade Purchase" and location_table[location_name].location_id_offset > self.options.shop_upgrade_total):
                    self.location_total -= 1
                    continue
                elif(location_table[location_name].location_group.__contains__("Pelly") and self.options.pellys_required == 0):
                    self.location_total -= 1
                    print(f"Pelly Removed: {location_name}")
                    continue
                else:
                    region = self.multiworld.get_region(location_table[location_name].region, self.player) 
                    location = REPOLocation(self.player, location_name, location_id, region)

                if (location_table[location_name].location_group == "Shop Upgrade Purchase" and location_table[location_name].location_id_offset > self.options.shop_upgrade_logical):
                    location.progress_type = LocationProgressType.EXCLUDED
                elif(location_table[location_name].location_group == "Shop Upgrade Purchase"and location_table[location_name].location_id_offset % 20 == 0):
                    location.progress_type = LocationProgressType.PRIORITY
                region.locations.append(location)

        # for i in range(len(shell_items)):
        #     region = self.multiworld.get_region(location_table[shell_locations[i]].region,self.player)
        #     location = self.placed_shells[i]
        #     region.locations.append(location)

        

    def set_rules(self) -> None:
        set_region_rules(self)
        set_location_rules(self)
    

    def fill_slot_data(self) -> Dict[str, Any]:
        #Sleep for if im trying to read the output log
        #time.sleep(3)
        slot_data: Dict[str, Any] = {
            "world_version": self.world_version.as_simple_string(),
            #"goal": int(self.options.goal.value)
            "level_quota": int(self.options.level_quota.value),
            "pellys_required": int(self.options.pellys_required.value),
            "upgrade_locations": int(self.options.shop_upgrade_total.value),
            "shop_stock" : int(self.options.shop_stock.value),
            "valuable_hunt": bool(self.options.valuable_hunt.value),
            "monster_hunt": bool(self.options.monster_hunt.value),
            "audit_trap_money_lost": int(self.options.audit_trap_money_lost.value),
            "death_link": bool(self.options.death_link.value)
        }
        return slot_data