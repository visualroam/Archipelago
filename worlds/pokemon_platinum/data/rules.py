# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/rules.py
#
# Copyright (C) 2025-2026 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from typing import Tuple, TYPE_CHECKING
from BaseClasses import CollectionState
from collections.abc import Callable, Mapping, MutableMapping, MutableSequence, Sequence
from rule_builder.rules import Has, HasAll, HasAny, Rule, True_, False_, HasFromListUnique, Or, And
import operator

from . import Hm, items, locations, species

if TYPE_CHECKING:
    from ..options import PokemonPlatinumOptions

def create_hm_badge_rule(hm: Hm) -> Rule:
    badge_item = hm.badge_item()
    if badge_item is not None:
        return Has(badge_item)
    else:
        return True_()

class Rules:
    exit_rules: Mapping[Tuple[str, str], Rule]
    location_rules: Mapping[str, Rule]
    encounter_type_rules: Mapping[str, Rule]
    location_type_rules: Mapping[str, Rule]
    common_rules: MutableMapping[str, Callable[..., Rule] | Rule]
    trainer_rules: Mapping[str, Rule]
    opts: "PokemonPlatinumOptions"
    cached_enc_accessibility_rules: MutableMapping[frozenset[str], Rule]
    
    def __init__(self, common_rules: MutableMapping[str, Callable[..., Rule] | Rule], opts: "PokemonPlatinumOptions"):
        self.opts = opts
        self.common_rules = common_rules
        self.cached_enc_accessibility_rules = {}
        def see_regional_mons(n: int) -> Rule:
            return HasFromListUnique(*[f"see_mon_{spec}" for spec in species.regional_mons], count=n)
        def see_mons(n: int) -> Rule:
            return HasFromListUnique(*[f"see_mon_{spec}" for spec in species.species.keys()], count=n)
        def badges(n: int) -> Rule:
            badges = tuple(items.items[loc.original_item].label # type: ignore
                for loc in locations.locations.values() if loc.type == "badge")
            return HasFromListUnique(*badges, count=n)
        self.common_rules["see_regional_mons"] = see_regional_mons
        self.common_rules["see_mons"] = see_mons
        self.common_rules["badges"] = badges

    def fill_rules(self):
        self.common_rules["evo_item_shop"] = (Has("event_veilstone_store")) if self.opts.evo_items_shop_in_ap_helper.value == 0 else True_()
        self.common_rules["cut"] = (And(HasAll("use_cut", "HM01 Cut"), HasAny("HM Reader", "Bag"), self.common_rules["cut_badge"])) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(Has("HM01 Cut"), self.common_rules["cut_badge"], (Or(Has("HM Reader"), HasAll("use_cut", "Bag")))))
        self.common_rules["fly"] = (And(HasAll("HM02 Fly", "use_fly", "Bag"), self.common_rules["fly_badge"])) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(HasAll("HM02 Fly", "Bag"), HasAny("use_fly", "HM Reader"), self.common_rules["fly_badge"]))
        self.common_rules["surf"] = (And(HasAll("HM03 Surf", "use_surf"), self.common_rules["surf_badge"], HasAny("HM Reader", "Bag"))) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(Has("HM03 Surf"), self.common_rules["surf_badge"], (Or(Has("HM Reader"), HasAll("use_surf", "Bag")))))
        self.common_rules["strength"] = (And(HasAll("HM04 Strength", "use_strength"), HasAny("HM Reader", "Bag"), self.common_rules["strength_badge"])) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(Has("HM04 Strength"), self.common_rules["strength_badge"], (Or(Has("HM Reader"), HasAll("use_strength", "Bag")))))
        self.common_rules["defog"] = (And(HasAll("use_defog", "HM05 Defog", "Bag"), self.common_rules["defog_badge"])) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(HasAll("HM05 Defog", "Bag"), HasAny("use_defog", "HM Reader"), self.common_rules["defog_badge"]))
        self.common_rules["rock_smash"] = (And(HasAll("HM06 Rock Smash", "use_rock_smash"), HasAny("HM Reader", "Bag"), self.common_rules["rock_smash_badge"])) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(Has("HM06 Rock Smash"), (Or(Has("HM Reader"), HasAll("use_rock_smash", "Bag"))), self.common_rules["rock_smash_badge"]))
        self.common_rules["waterfall"] = (And(HasAll("HM07 Waterfall", "use_waterfall"), HasAny("HM Reader", "Bag"), self.common_rules["waterfall_badge"])) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(Has("HM07 Waterfall"), (Or(Has("HM Reader"), HasAll("use_waterfall", "Bag"))), self.common_rules["waterfall_badge"]))
        self.common_rules["down_waterfall"] = (And(HasAll("HM07 Waterfall", "use_waterfall"), HasAny("HM Reader", "Bag"))) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(Has("HM07 Waterfall"), (Or(Has("HM Reader"), HasAll("use_waterfall", "Bag")))))
        self.common_rules["rock_climb"] = (And(HasAll("HM08 Rock Climb", "use_rock_climb"), HasAny("HM Reader", "Bag"), self.common_rules["rock_climb_badge"])) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(Has("HM08 Rock Climb"), self.common_rules["rock_climb_badge"], (Or(Has("HM Reader"), HasAll("use_rock_climb", "Bag")))))
        self.common_rules["flash"] = (HasAll("TM70 Flash", "use_flash", "Bag")) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon and self.opts.reusable_tms.value != 0 else (And(HasAll("TM70 Flash", "use_flash", "Bag"), self.common_rules["evo_item_shop"])) if self.opts.hm_reader_mode.value == self.opts.hm_reader_mode.option_req_mon else (And(HasAll("TM70 Flash", "Bag"), HasAny("HM Reader", "use_flash"))) if self.opts.reusable_tms.value != 0 else (And(HasAll("TM70 Flash", "Bag"), HasAny("HM Reader", "use_flash"), self.common_rules["evo_item_shop"]))
        self.common_rules["national_dex"] = (Has("Upgradable Pokedex", count=3))
        self.common_rules["dowsingmachine_if_opt"] = (HasAll("Poketch", "DOWSING MACHINE")) if self.opts.dowsing_machine_logic.value != 0 else True_()
        self.common_rules["defog_if_opt"] = (self.common_rules["defog"]) if self.opts.visibility_hm_logic.value != 0 else True_()
        self.common_rules["flash_if_opt"] = (self.common_rules["flash"]) if self.opts.visibility_hm_logic.value != 0 else True_()
        self.common_rules["poketch_req"] = (HasAll("Coupon 3", "Coupon 1", "Coupon 2", "Parcel"))
        self.common_rules["route_210_south_to_route_210_junction"] = (Has("Bicycle")) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope else (self.common_rules["rock_climb"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb else (self.common_rules["surf"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf else (And(self.common_rules["surf"], self.common_rules["waterfall"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall else (False_()) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_impassable else (self.common_rules["cut"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_cut_tree else (self.common_rules["rock_smash"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_smash else (self.common_rules["strength"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_strength_boulder else (Has("SecretPotion")) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_psyduck else (And(Has("Bicycle"), self.common_rules["cut"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope_and_cut_tree else (And(Has("Bicycle"), self.common_rules["rock_smash"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope_and_rock_smash else (And(Has("Bicycle"), self.common_rules["strength"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope_and_strength_boulder else (HasAll("Bicycle", "SecretPotion")) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope_and_psyduck else (And(self.common_rules["rock_climb"], self.common_rules["cut"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb_and_cut_tree else (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["rock_climb"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["rock_climb"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb_and_psyduck else (And(self.common_rules["cut"], self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_cut_tree else (And(self.common_rules["surf"], self.common_rules["rock_smash"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_psyduck else (And(self.common_rules["cut"], self.common_rules["surf"], self.common_rules["waterfall"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_cut_tree else (And(self.common_rules["surf"], self.common_rules["waterfall"], self.common_rules["rock_smash"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["surf"], self.common_rules["waterfall"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["surf"], self.common_rules["waterfall"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_psyduck else True_()
        self.common_rules["bicycle_through_route_210_barricade"] = (Has("Bag")) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_impassable or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_cut_tree or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_rock_smash or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_strength_boulder or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_psyduck or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_cut_tree or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_rock_smash or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_strength_boulder or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_psyduck else (Or(Has("Bag"), self.common_rules["route_210_south_to_route_210_junction"]))
        self.common_rules["route_210_junction_to_route_215"] = (And(Has("Bicycle"), self.common_rules["bicycle_through_route_210_barricade"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge else (self.common_rules["rock_climb"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb else (self.common_rules["surf"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf else (And(self.common_rules["surf"], self.common_rules["waterfall"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall else (False_()) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_impassable else (self.common_rules["cut"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_cut_tree else (self.common_rules["rock_smash"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_smash else (self.common_rules["strength"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_strength_boulder else (Has("SecretPotion")) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_psyduck else (And(Has("Bicycle"), self.common_rules["cut"], self.common_rules["bicycle_through_route_210_barricade"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge_and_cut_tree else (And(Has("Bicycle"), self.common_rules["bicycle_through_route_210_barricade"], self.common_rules["rock_smash"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge_and_rock_smash else (And(Has("Bicycle"), self.common_rules["strength"], self.common_rules["bicycle_through_route_210_barricade"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge_and_strength_boulder else (And(HasAll("Bicycle", "SecretPotion"), self.common_rules["bicycle_through_route_210_barricade"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge_and_psyduck else (And(self.common_rules["rock_climb"], self.common_rules["cut"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb_and_cut_tree else (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["rock_climb"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["rock_climb"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb_and_psyduck else (And(self.common_rules["cut"], self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_cut_tree else (And(self.common_rules["surf"], self.common_rules["rock_smash"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_psyduck else (And(self.common_rules["cut"], self.common_rules["surf"], self.common_rules["waterfall"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_cut_tree else (And(self.common_rules["surf"], self.common_rules["waterfall"], self.common_rules["rock_smash"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["surf"], self.common_rules["waterfall"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["surf"], self.common_rules["waterfall"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_psyduck else True_()
        self.common_rules["bicycle_through_route_215_barricade"] = (Has("Bag")) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_impassable or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_cut_tree or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_rock_smash or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_strength_boulder or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_psyduck or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_cut_tree or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_rock_smash or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_strength_boulder or self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_psyduck else (Or(Has("Bag"), self.common_rules["route_210_junction_to_route_215"]))
        self.common_rules["veilstone_bicycle_from_solaceon"] = (And(self.common_rules["bicycle_through_route_215_barricade"], self.common_rules["bicycle_through_route_210_barricade"]))
        self.common_rules["amity_square"] = (Or(HasAny("mon_buneary", "mon_turtwig", "mon_pachirisu", "mon_infernape", "mon_happiny", "mon_drifloon", "mon_monferno", "mon_torterra", "mon_piplup", "mon_empoleon", "mon_chimchar", "mon_psyduck", "mon_grotle", "mon_clefairy", "mon_pikachu", "mon_prinplup"), And(HasAny("mon_jigglypuff", "mon_shroomish", "mon_torchic", "mon_skitty"), self.common_rules["national_dex"])))
        self.common_rules["boat_canalave_pastoria"] = (True_()) if self.opts.boat_canalave_pastoria.value == self.opts.boat_canalave_pastoria.option_on else (Has("S.S. Ticket")) if self.opts.boat_canalave_pastoria.value == self.opts.boat_canalave_pastoria.option_ss_ticket else (False_())
        self.common_rules["boat_canalave_snowpoint"] = (True_()) if self.opts.boat_canalave_snowpoint.value == self.opts.boat_canalave_snowpoint.option_on else (Has("S.S. Ticket")) if self.opts.boat_canalave_snowpoint.value == self.opts.boat_canalave_snowpoint.option_ss_ticket else (False_())
        self.common_rules["boat_pastoria_snowpoint"] = (True_()) if self.opts.boat_pastoria_snowpoint.value == self.opts.boat_pastoria_snowpoint.option_on else (Has("S.S. Ticket")) if self.opts.boat_pastoria_snowpoint.value == self.opts.boat_pastoria_snowpoint.option_ss_ticket else (False_())
        self.exit_rules = {
            ("lake_verity", "verity_cavern"): (self.common_rules["surf"]),
            ("valor_lakefront", "lake_valor_drained"): (Has("event_lake_explosion")),
            ("valor_lakefront", "route_222"): (Has("event_distortion_world")) if self.opts.early_sunyshore.value == 0 else True_(),
            ("valor_lakefront", "lake_valor"): (Has("event_distortion_world")),
            ("verity_lakefront", "lake_verity"): (Has("event_lake_valor_defeat_saturn")),
            ("acuity_lakefront", "lake_acuity"): (And(Has("event_lake_verity_defeat_mars"), self.common_rules["rock_climb"])),
            ("acuity_lakefront", "lake_acuity_low_water"): (self.common_rules["rock_climb"]),
            ("route_219", "route_220"): (self.common_rules["surf"]),
            ("route_221", "route_220"): (self.common_rules["surf"]),
            ("route_221", "pal_park_lobby"): (self.common_rules["national_dex"]),
            ("jubilife_city", "route_203"): (Has("Poketch")) if self.opts.poketch_route_203.value != 0 else True_(),
            ("jubilife_city", "jubilife_tv_1f"): (Has("event_coal_badge")),
            ("oreburgh_gate_1f", "oreburgh_gate_b1f"): (self.common_rules["rock_smash"]),
            ("route_207_south", "route_207"): (Has("Bicycle")) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope else (self.common_rules["rock_climb"]) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb else (False_()) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_impassable else (self.common_rules["cut"]) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_cut_tree else (self.common_rules["rock_smash"]) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_smash else (self.common_rules["strength"]) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_strength_boulder else (Has("SecretPotion")) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_psyduck else (And(Has("Bicycle"), self.common_rules["cut"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope_and_cut_tree else (And(Has("Bicycle"), self.common_rules["rock_smash"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope_and_rock_smash else (And(Has("Bicycle"), self.common_rules["strength"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope_and_strength_boulder else (HasAll("Bicycle", "SecretPotion")) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope_and_psyduck else (And(self.common_rules["rock_climb"], self.common_rules["cut"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb_and_cut_tree else (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["rock_climb"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["rock_climb"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb_and_psyduck else True_(),
            ("route_207", "route_207_south"): (self.common_rules["rock_climb"]) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb else (False_()) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_impassable else (self.common_rules["cut"]) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_cut_tree or self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope_and_cut_tree else (self.common_rules["rock_smash"]) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_smash or self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope_and_rock_smash else (self.common_rules["strength"]) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_strength_boulder or self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope_and_strength_boulder else (Has("SecretPotion")) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_psyduck or self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_bicycle_slope_and_psyduck else (And(self.common_rules["rock_climb"], self.common_rules["cut"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb_and_cut_tree else (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["rock_climb"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["rock_climb"])) if self.opts.route_207_barricade.value == self.opts.route_207_barricade.option_rock_climb_and_psyduck else True_(),
            ("route_210_south", "route_210_junction"): (self.common_rules["route_210_south_to_route_210_junction"]),
            ("route_210_junction", "route_210_south"): (self.common_rules["rock_climb"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb else (self.common_rules["surf"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf else (And(self.common_rules["down_waterfall"], self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall else (False_()) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_impassable else (self.common_rules["cut"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_cut_tree or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope_and_cut_tree else (self.common_rules["rock_smash"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_smash or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope_and_rock_smash else (self.common_rules["strength"]) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_strength_boulder or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope_and_strength_boulder else (Has("SecretPotion")) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_psyduck or self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_bicycle_slope_and_psyduck else (And(self.common_rules["rock_climb"], self.common_rules["cut"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb_and_cut_tree else (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["rock_climb"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["rock_climb"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_rock_climb_and_psyduck else (And(self.common_rules["cut"], self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_cut_tree else (And(self.common_rules["surf"], self.common_rules["rock_smash"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_surf_and_psyduck else (And(self.common_rules["cut"], self.common_rules["down_waterfall"], self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_cut_tree else (And(self.common_rules["down_waterfall"], self.common_rules["surf"], self.common_rules["rock_smash"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["down_waterfall"], self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["down_waterfall"], self.common_rules["surf"])) if self.opts.route_210_lower_barricade.value == self.opts.route_210_lower_barricade.option_waterfall_and_psyduck else True_(),
            ("route_210_junction", "route_215"): (self.common_rules["route_210_junction_to_route_215"]),
            ("route_210_junction", "route_210_south_upper"): (Has("SecretPotion")),
            ("route_215", "route_210_junction"): (HasAll("Bicycle", "Bag")) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge else (self.common_rules["rock_climb"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb else (self.common_rules["surf"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf else (And(self.common_rules["down_waterfall"], self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall else (False_()) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_impassable else (self.common_rules["cut"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_cut_tree else (self.common_rules["rock_smash"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_smash else (self.common_rules["strength"]) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_strength_boulder else (Has("SecretPotion")) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_psyduck else (And(HasAll("Bicycle", "Bag"), self.common_rules["cut"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge_and_cut_tree else (And(HasAll("Bicycle", "Bag"), self.common_rules["rock_smash"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge_and_rock_smash else (And(HasAll("Bicycle", "Bag"), self.common_rules["strength"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge_and_strength_boulder else (HasAll("Bicycle", "SecretPotion", "Bag")) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_bicycle_bridge_and_psyduck else (And(self.common_rules["rock_climb"], self.common_rules["cut"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb_and_cut_tree else (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["rock_climb"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["rock_climb"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_rock_climb_and_psyduck else (And(self.common_rules["cut"], self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_cut_tree else (And(self.common_rules["surf"], self.common_rules["rock_smash"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_surf_and_psyduck else (And(self.common_rules["cut"], self.common_rules["down_waterfall"], self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_cut_tree else (And(self.common_rules["down_waterfall"], self.common_rules["surf"], self.common_rules["rock_smash"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_rock_smash else (And(self.common_rules["strength"], self.common_rules["down_waterfall"], self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_strength_boulder else (And(Has("SecretPotion"), self.common_rules["down_waterfall"], self.common_rules["surf"])) if self.opts.route_215_barricade.value == self.opts.route_215_barricade.option_waterfall_and_psyduck else True_(),
            ("ravaged_path", "route_204_north"): (self.common_rules["rock_smash"]),
            ("route_205_south_bottom", "route_205_south"): (Or(Has("Works Key"), self.common_rules["surf"])),
            ("valley_windworks_outside", "valley_windworks_building"): (Has("Works Key")),
            ("route_205_south", "fuego_ironworks_outside"): (self.common_rules["surf"]),
            ("route_205_south", "eterna_forest_outside"): (self.common_rules["cut"]),
            ("route_205_north", "eterna_forest_outside"): (self.common_rules["cut"]),
            ("eterna_forest", "old_chateau"): (self.common_rules["cut"]),
            ("eterna_city", "team_galactic_eterna_building_1f"): (self.common_rules["cut"]),
            ("eterna_city", "eterna_city_south_house"): (Has("event_met_oak_pal_park")),
            ("mt_coronet_1f_north_room_1_left", "mt_coronet_1f_north_room_1_middle"): (self.common_rules["rock_smash"]),
            ("mt_coronet_1f_north_room_1_middle", "mt_coronet_1f_north_room_1_left"): (Or(self.common_rules["strength"], self.common_rules["rock_smash"])),
            ("mt_coronet_1f_north_room_1_middle", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_right", "mt_coronet_1f_north_room_1_middle"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_right", "mt_coronet_1f_north_room_1_top"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_top", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_top", "mt_coronet_b1f"): (And(self.common_rules["fly"], self.common_rules["defog_if_opt"])) if self.opts.north_sinnoh_fly.value != 0 else (self.common_rules["defog_if_opt"]),
            ("mt_coronet_1f_north_room_1_bottom", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("route_206_cycling_road_north_gate", "cycling_road"): (Has("Bicycle")),
            ("route_206_cycling_road_south_gate", "cycling_road"): (Has("Bicycle")),
            ("route_206", "route_206_upper"): (self.common_rules["cut"]),
            ("route_206_upper", "wayward_cave_1f"): (self.common_rules["flash_if_opt"]),
            ("route_206_upper", "wayward_cave_1f_secret"): (self.common_rules["flash_if_opt"]),
            ("wayward_cave_1f", "virt_wayward_cave_1f_red_shard"): (self.common_rules["rock_smash"]),
            ("mt_coronet_1f_south", "mt_coronet_2f_right"): (And(self.common_rules["rock_climb"], self.common_rules["surf"])),
            ("mt_coronet_2f_right", "mt_coronet_2f_left"): (self.common_rules["strength"]),
            ("route_209_lost_tower_2f", "route_209_lost_tower_3f"): (self.common_rules["defog_if_opt"]),
            ("maniac_tunnel", "solaceon_ruins_maniac_tunnel_room"): (Has("Unown File", count=26)) if self.opts.unown_option.value == self.opts.unown_option.option_item else (Has("event_solaceon_ruins")) if self.opts.unown_option.value == self.opts.unown_option.option_vanilla else True_(),
            ("route_210_south_upper", "route_210_junction"): (Has("SecretPotion")),
            ("route_210_south_upper", "route_210_north"): (self.common_rules["defog_if_opt"]),
            ("route_210_north", "route_210_grandma_wilma_house"): (self.common_rules["rock_climb"]),
            ("celestic_town", "route_210_north"): (self.common_rules["defog_if_opt"]),
            ("galactic_hq_wo_key", "veilstone_city_galactic_warehouse"): (HasAny("Storage Key", "event_lake_acuity_meet_jupiter")),
            ("veilstone_city_galactic_warehouse", "galactic_hq_wo_key"): (HasAny("Storage Key", "event_lake_acuity_meet_jupiter")),
            ("veilstone_city", "galactic_hq_w_key"): (Has("Galactic Key")),
            ("route_214", "spring_path"): (Has("event_distortion_world")),
            ("route_214", "route_214_top"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else True_(),
            ("sendoff_spring", "turnback_cave_entrance"): (self.common_rules["defog_if_opt"]),
            ("route_213", "route_213_honey_tree"): (self.common_rules["rock_smash"]),
            ("route_213", "grand_lake_route_213_northeast_house"): (self.common_rules["rock_climb"]),
            ("route_218_east", "route_218_west"): (self.common_rules["surf"]),
            ("route_218_west", "route_218_east"): (self.common_rules["surf"]),
            ("canalave_city", "fullmoon_island"): (And(Has("event_beat_cynthia"), self.common_rules["national_dex"])),
            ("canalave_city", "pastoria_city"): (self.common_rules["boat_canalave_pastoria"]),
            ("canalave_city", "snowpoint_city"): (And(self.common_rules["fly"], self.common_rules["boat_canalave_snowpoint"])) if self.opts.north_sinnoh_fly.value != 0 else (self.common_rules["boat_canalave_snowpoint"]),
            ("mt_coronet_1f_tunnel_room", "mt_coronet_1f_tunnel_room_base"): (self.common_rules["rock_climb"]),
            ("mt_coronet_1f_tunnel_room_base", "mt_coronet_1f_tunnel_room"): (self.common_rules["rock_climb"]),
            ("mt_coronet_1f_north_room_2", "mt_coronet_b1f"): (self.common_rules["defog_if_opt"]),
            ("mt_coronet_outside_south", "mt_coronet_outside_north_plat"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_south", "mt_coronet_outside_south_entrance"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_north_plat", "mt_coronet_outside_south"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_south_entrance", "mt_coronet_outside_south"): (self.common_rules["rock_climb"]),
            ("mt_coronet_4f_rooms_1_and_2_lower", "mt_coronet_4f_rooms_1_and_2"): (self.common_rules["rock_climb"]),
            ("mt_coronet_4f_rooms_1_and_2", "mt_coronet_4f_rooms_1_and_2_lower"): (self.common_rules["rock_climb"]),
            ("mt_coronet_2f_left", "mt_coronet_3f"): (Has("event_galactic_hq_defeat_cyrus")),
            ("lake_acuity", "acuity_cavern"): (self.common_rules["surf"]),
            ("snowpoint_city", "fight_area"): (Has("S.S. Ticket")),
            ("snowpoint_city", "snowpoint_temple_1f"): (And(Has("event_beat_cynthia"), self.common_rules["national_dex"])),
            ("snowpoint_city", "canalave_city"): (self.common_rules["boat_canalave_snowpoint"]),
            ("snowpoint_city", "pastoria_city"): (self.common_rules["boat_pastoria_snowpoint"]),
            ("victory_road_1f", "victory_road_1f_room_1"): (And(Has("event_beat_cynthia"), self.common_rules["national_dex"])),
            ("victory_road_1f_room_1", "victory_road_1f_room_2_entrance"): (self.common_rules["defog_if_opt"]),
            ("victory_road_1f_room_2_entrance", "victory_road_1f_room_2"): (self.common_rules["strength"]),
            ("sunyshore_city", "route_223"): (self.common_rules["surf"]),
            ("sunyshore_city", "sunyshore_city_east_house"): (self.common_rules["rock_climb"]),
            ("pokemon_league_south_south", "pokemon_league_south"): (And(self.common_rules["surf"], self.common_rules["waterfall"])),
            ("pokemon_league_south", "pokemon_league_south_south"): (And(self.common_rules["down_waterfall"], self.common_rules["surf"])),
            ("pokemon_league_north_pokecenter_1f", "pokemon_league_elevator_to_aaron_room"): (self.common_rules["badges"](8)),
            ("victory_road_1f_entrance", "victory_road_2f_entrance"): (self.common_rules["rock_climb"]),
            ("victory_road_2f_entrance", "victory_road_2f"): (And(self.common_rules["strength"], self.common_rules["rock_smash"])),
            ("pastoria_city_observatory_gate_1f", "virt_great_marsh"): (Has("Marsh Pass")) if self.opts.marsh_pass.value != 0 else True_(),
            ("virt_great_marsh", "virt_great_marsh_national_dex"): (self.common_rules["national_dex"]),
            ("route_212_north_top", "route_212_north"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else True_(),
            ("route_212_north", "route_212_north_top"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else True_(),
            ("route_214_top", "route_214"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else True_(),
            ("fight_area", "route_225_gate_to_fight_area"): (self.common_rules["national_dex"]),
            ("fight_area", "route_230"): (self.common_rules["national_dex"]),
            ("route_225_gate_to_fight_area", "fight_area"): (self.common_rules["national_dex"]),
            ("route_230", "route_229"): (self.common_rules["surf"]),
            ("route_230", "fight_area"): (And(self.common_rules["national_dex"], self.common_rules["surf"])),
            ("route_229", "route_230"): (self.common_rules["surf"]),
            ("route_228", "route_228_rock_peak_ruins"): (And(Has("Bag"), (Or(Has("Bicycle"), self.common_rules["fly"])))),
            ("route_226_east", "route_226_mid"): (And(self.common_rules["rock_climb"], self.common_rules["surf"])),
            ("route_226_mid", "route_226_east"): (self.common_rules["surf"]),
            ("route_226_west", "route_226_mid"): (self.common_rules["rock_climb"]),
            ("route_227_lower", "route_227"): (HasAll("Bicycle", "Bag")),
            ("route_227", "route_227_pit"): (self.common_rules["rock_climb"]),
            ("stark_mountain_room_1_entrance", "stark_mountain_room_1"): (self.common_rules["strength"]),
            ("stark_mountain_room_1", "stark_mountain_room_2"): (self.common_rules["rock_smash"]),
            ("trophy_garden", "trophy_garden_national_dex"): (self.common_rules["national_dex"]),
            ("mt_coronet_b1f", "mt_coronet_b1f_feebas"): (And(HasAll("Poketch", "DOWSING MACHINE", "PokeSonar", "Bag"), HasAny("Good Rod", "Super Rod", "Old Rod"), self.common_rules["surf"])),
            ("route_209", "route_209_odd_keystone"): (And(Has("Odd Keystone"), self.common_rules["evo_item_shop"])),
            ("virt_start", "virt_roamers"): (HasAll("Poketch", "MARKING MAP")) if self.opts.can_reset_legendaries_in_ap_helper.value != 0 else (HasAll("Poketch", "MARKING MAP", "event_beat_cynthia")),
            ("virt_start", "virt_dex"): (Has("Upgradable Pokedex")) if self.opts.dexsanity_mode.value >= self.opts.dexsanity_mode.option_req else True_(),
            ("virt_start", "virt_national_dex"): (self.common_rules["national_dex"]) if self.opts.dexsanity_mode.value >= self.opts.dexsanity_mode.option_req else True_(),
            ("virt_start", "virt_fly"): (self.common_rules["fly"]),
            ("hearthome_city_west_gate_to_amity_square", "amity_square"): (self.common_rules["amity_square"]),
            ("hearthome_city_east_gate_to_amity_square", "amity_square"): (self.common_rules["amity_square"]),
            ("pastoria_city", "canalave_city"): (self.common_rules["boat_canalave_pastoria"]),
            ("pastoria_city", "snowpoint_city"): (And(self.common_rules["fly"], self.common_rules["boat_pastoria_snowpoint"])) if self.opts.north_sinnoh_fly.value != 0 else (self.common_rules["boat_pastoria_snowpoint"]),
            ("virt_fly", "twinleaf_town"): (Has("Twinleaf Town Fly Region")),
            ("virt_fly", "sandgem_town"): (Has("Sandgem Town Fly Region")),
            ("virt_fly", "floaroma_town"): (Has("Floaroma Town Fly Region")),
            ("virt_fly", "solaceon_town"): (Has("Solaceon Town Fly Region")) if self.opts.require_fly_items_for_flight.value != 0 else (HasAny("solaceon_town_ledge", "Solaceon Town Fly Region")),
            ("virt_fly", "celestic_town"): (Has("Celestic Town Fly Region")),
            ("virt_fly", "jubilife_city"): (Has("Jubilife City Fly Region")),
            ("virt_fly", "canalave_city"): (Has("Canalave City Fly Region")),
            ("virt_fly", "oreburgh_city"): (Has("Oreburgh City Fly Region")),
            ("virt_fly", "eterna_city"): (Has("Eterna City Fly Region")),
            ("virt_fly", "hearthome_city"): (Has("Hearthome City Fly Region")),
            ("virt_fly", "pastoria_city"): (Has("Pastoria City Fly Region")),
            ("virt_fly", "veilstone_city"): (Has("Veilstone City Fly Region")),
            ("virt_fly", "sunyshore_city"): (Has("Sunyshore City Fly Region")),
            ("virt_fly", "snowpoint_city"): (Has("Snowpoint City Fly Region")),
            ("virt_fly", "pokemon_league_south"): (Has("Pokemon League South Fly Region")),
            ("virt_fly", "fight_area"): (Has("Fight Area Fly Region")),
            ("virt_fly", "survival_area"): (Has("Survival Area Fly Region")),
            ("virt_fly", "resort_area"): (Has("Resort Area Fly Region")),
            ("virt_fly", "pokemon_league"): (Has("Pokemon League Fly Region")),
            ("virt_fly", "route_221"): (Has("Route 221 Fly Region")),
            ("victory_road_1f_upper_entrance", "victory_road_1f"): (self.common_rules["rock_climb"]),
            ("pokemon_league", "victory_road_1f_upper_entrance"): (And(self.common_rules["down_waterfall"], self.common_rules["surf"])),
            ("victory_road_2f_from_1f", "victory_road_2f_from_1f_strength"): (self.common_rules["strength"]),
            ("victory_road_2f_from_1f_strength", "victory_road_2f"): (self.common_rules["rock_smash"]),
            ("victory_road_b1f", "victory_road_b1f_upper"): (And(self.common_rules["surf"], self.common_rules["waterfall"])),
            ("ravaged_path", "ravaged_path_water"): (self.common_rules["rock_smash"]),
            ("lake_acuity", "lake_acuity_land"): (self.common_rules["surf"]),
            ("route_230", "route_230_land"): (self.common_rules["surf"]),
            ("route_229", "route_229_water"): (self.common_rules["cut"]),
        }
        self.location_rules = {
            "Twinleaf Town - Hidden Item in Pond": (self.common_rules["surf"]),
            "Lake Verity - Item in Southwest Grass Patch": (self.common_rules["surf"]),
            "Sandgem Town Pokemon Research Lab - First Item from Prof Oak": (And(Has("Upgradable Pokedex"), self.common_rules["see_regional_mons"](self.opts.regional_dex_goal.value))),
            "Sandgem Town Pokemon Research Lab - Item from Prof Rowan (After Regional Dex)": (And(Has("Upgradable Pokedex"), self.common_rules["see_regional_mons"](self.opts.regional_dex_goal.value))),
            "Route 221 - Item on Corner of Land": (self.common_rules["surf"]),
            "Pal Park - Show Snorlax to Girl": (Has("mon_snorlax")),
            "Pal Park - Show Kecleon to Girl": (HasAll("mon_kecleon", "mon_snorlax")),
            "Jubilife Trainers' School - Item from Rival": (Has("Parcel")),
            "Jubilife City - Item from East Clown": (Has("Parcel")),
            "Jubilife City - Item from Clown in front of Poketch HQ": (Has("Parcel")),
            "Jubilife City - Item from Clown in front of Jubilife TV": (Has("Parcel")),
            "Jubilife City - First Item from CEO": (self.common_rules["poketch_req"]),
            "Jubilife City - Second Item from CEO": (self.common_rules["poketch_req"]),
            "Jubilife City - Third Item from CEO": (self.common_rules["poketch_req"]),
            "Jubilife City - Fourth Item from CEO": (self.common_rules["poketch_req"]),
            "Oreburgh Gate B1F - Item After Ramps": (Or(Has("Bicycle"), self.common_rules["surf"])),
            "Oreburgh Gate B1F - Item in Pit North": (And(self.common_rules["strength"], self.common_rules["surf"])),
            "Oreburgh Gate B1F - Item in Pit South": (And(self.common_rules["strength"], self.common_rules["surf"])),
            "Oreburgh City - Show Geodude to Overalls Man in North House": (Has("mon_geodude")),
            "Jubilife City - Item from Overalls Man After Grunts Battle After Oreburgh Gym": (Has("event_coal_badge")),
            "Route 204 South - Item Behind Southwest Pond": (self.common_rules["surf"]),
            "Route 204 South - Item Behind Eastern Pond": (self.common_rules["surf"]),
            "Ravaged Path - Item Left of Breakable Rocks": (self.common_rules["rock_smash"]),
            "Ravaged Path - Item at Water's End": (And(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Ravaged Path - Item Behind Long Boulder Trail": (And(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Route 204 North - Woman Behind Cut Tree": (self.common_rules["cut"]),
            "Valley Windworks - Item Behind Windworks": (self.common_rules["surf"]),
            "Valley Windworks - Item Beyond Fence": (self.common_rules["surf"]),
            "Valley Windworks - Hidden Item Beyond Fence": (self.common_rules["surf"]),
            "Eterna Forest - Hidden Item Next to Old Chateau": (self.common_rules["cut"]),
            "Eterna Forest - Item Next to Old Chateau": (self.common_rules["cut"]),
            "Eterna City - Item Behind Fence": (self.common_rules["cut"]),
            "Eterna City - Item from Rad Rickshaw": (Has("event_eterna_defeat_team_galactic")),
            "Eterna City - Hidden Item Above Pond": (self.common_rules["surf"]),
            "Route 206 North Gate - Reward For 35 Pokemon Seen": (And(Has("Upgradable Pokedex"), self.common_rules["see_mons"](35))),
            "Route 211 West - Item Under Bridge": (self.common_rules["rock_smash"]),
            "Mt. Coronet (Route 211 Tunnel Room) - Item Behind Two Breakable Rocks": (self.common_rules["rock_smash"]),
            "Mt. Coronet (Route 211 Tunnel Room) - Item in Corner Above Ledge": (self.common_rules["strength"]),
            "Wayward Cave - Item in Southwest Corner": (self.common_rules["rock_smash"]),
            "Wayward Cave - Item in Northwest Corner": (self.common_rules["rock_smash"]),
            "Wayward Cave - Item Next to Five Rocks": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Rock Next to Mira": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Rock Below Picnicker on East Side": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Center Boulder": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Corner With Breakable Rock": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden Item in Southeast Corner": (self.common_rules["rock_smash"]),
            "Wayward Cave Secret Basement - Item in Final Room": (Has("Bicycle")),
            "Wayward Cave Secret Basement - Item Between Bike Bridges": (Has("Bicycle")),
            "Wayward Cave Secret Basement - Item After Four Bike Jumps": (Has("Bicycle")),
            "Wayward Cave Secret Basement - Item Next to Bike Ramp on Ledges": (Has("Bicycle")),
            "Wayward Cave Secret Basement - Hidden Item Against Northwest Wall": (Has("Bicycle")),
            "Route 207 - Item Below Rock Climb Slope": (self.common_rules["rock_climb"]),
            "Mt. Coronet (Southern Room) - Item Across Upper Pond": (self.common_rules["surf"]),
            "Mt. Coronet (Southern Room) - Item Across Lower Pond": (self.common_rules["surf"]),
            "Route 208 - Hidden Item Above Rock Climb Slope": (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])),
            "Route 208 - Item Above Waterfall": (And(self.common_rules["surf"], self.common_rules["waterfall"])),
            "Route 208 - Item Behind Breakable Rocks": (self.common_rules["rock_smash"]),
            "Route 209 - Item Down River in Southeast": (self.common_rules["surf"]),
            "Route 209 - Item in Corner Past West Mud Slide Pit": (Has("Bicycle")),
            "Route 209 - Item Behind Cut Tree": (self.common_rules["cut"]),
            "Lost Tower 5F - Gift from Old Woman on Right": (self.common_rules["defog"]),
            "Lost Tower 5F - Gift from Old Woman on Left": (self.common_rules["defog"]),
            "Solaceon Town - Item from Ruin Maniac": (And(Has("Upgradable Pokedex"), self.common_rules["see_regional_mons"](50))),
            "Solaceon Ruins B1F - Gift for Lending Defog to Hiker": (Has("HM05 Defog")),
            "Route 210 South - Item in Northwest Corner": (HasAll("Bicycle", "Bag")),
            "Route 210 North - Item Behind Breakable Rocks": (And(Has("Bicycle"), (Or(Has("Bag"), self.common_rules["strength"])), self.common_rules["rock_smash"])),
            "Route 210 Center - Hidden Item on Ledge in Pit": (self.common_rules["rock_climb"]),
            "Route 210 North - Hidden Item up East Waterfall": (And(self.common_rules["surf"], self.common_rules["waterfall"])),
            "Route 210 North - Item Under West Bridge": (And(self.common_rules["surf"], self.common_rules["waterfall"])),
            "Route 210 Center - Item on Ledge Below Move Tutor": (self.common_rules["rock_climb"]),
            "Celestic Town Cave - Item from Cynthia's Grandmother": (Has("Old Charm")),
            "Celestic Town - Item Below Shrine Right Stairs": (Has("Old Charm")),
            "Celestic Town - Hidden Item Above Shrine Left Stairs": (Has("Old Charm")),
            "Route 211 East - Hidden Item Up Rock Climb Slope": (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])),
            "Route 211 East - Item Up Rock Climb Slope": (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])),
            "Route 215 - Item Next to Black Belt Behind Cut Tree": (self.common_rules["cut"]),
            "Route 215 - Item Behind Cut Trees Below Northeast Grass Patch": (self.common_rules["cut"]),
            "Veilstone City - Item on Rock Climb Platform": (self.common_rules["rock_climb"]),
            "Galactic Warehouse - Item in Many Generators Room": (Has("Galactic Key")),
            "Route 214 - Item Across Pond": (self.common_rules["surf"]),
            "Valor Lakefront - Second Item from Cynthia": (Has("event_fen_badge")),
            "Valor Lakefront - Hidden Item After Rock Climbing from Route 213": (self.common_rules["rock_climb"]),
            "Valor Lakefront - Bottom Item After Rock Climb Ledges": (self.common_rules["rock_climb"]),
            "Valor Lakefront - Top Item After Rock Climb Ledges": (self.common_rules["rock_climb"]),
            "Valor Lakefront - Gift from Locked Out Woman": (Has("Suite Key")),
            "Route 213 - Hidden Item Next to Honey Tree": (self.common_rules["rock_smash"]),
            "Route 213 - Hidden Item By Reception": (self.common_rules["dowsingmachine_if_opt"]),
            "Route 213 - Item on Sandy Island": (self.common_rules["surf"]),
            "Route 213 - Item Down East Rock Climb Slopes": (self.common_rules["rock_climb"]),
            "Route 213 - Hidden Item in Grass After Rock Climb Slope": (self.common_rules["rock_climb"]),
            "Route 213 - Hidden Item on Southeast White Rock": (self.common_rules["surf"]),
            "Route 213 - Hidden Item on Sandy Island": (self.common_rules["surf"]),
            "Route 213 - Item on Small Island Above Swimmers": (self.common_rules["surf"]),
            "Route 213 - Item By Grass After Rock Climb Slope": (self.common_rules["rock_climb"]),
            "Route 213 - Item Behind Breakable Rock on Beach": (self.common_rules["rock_smash"]),
            "Pastoria City - Item in Trees Above Boats": (self.common_rules["surf"]),
            "Route 212 South - Item By Grass Patch in Water": (self.common_rules["surf"]),
            "Route 212 South - Hidden Item Below Two Trees on Corner": (self.common_rules["surf"]),
            "Route 212 South - Item Near Scientist Between Cut Trees": (And(HasAll("Bicycle", "Bag"), self.common_rules["cut"])) if self.opts.pastoria_barriers.value != 0 else (And(Has("Bicycle"), self.common_rules["cut"], self.common_rules["veilstone_bicycle_from_solaceon"])),
            "Route 212 South - Item on Ledge Above Move Tutor": (And(HasAll("Bicycle", "Bag"), self.common_rules["cut"])) if self.opts.pastoria_barriers.value != 0 else (And(Has("Bicycle"), self.common_rules["cut"], self.common_rules["veilstone_bicycle_from_solaceon"])),
            "Route 212 North - Item on West Ledge": (Or(self.common_rules["cut"], self.common_rules["surf"])),
            "Route 212 North - Item in Flower Patch": (self.common_rules["surf"]),
            "Route 212 North - Item Next to North Pond": (self.common_rules["surf"]),
            "Route 212 South - Hidden Item on SW Bike Bridge Island": (And(HasAll("Bicycle", "Bag"), self.common_rules["cut"])) if self.opts.pastoria_barriers.value != 0 else (And(Has("Bicycle"), self.common_rules["cut"], self.common_rules["veilstone_bicycle_from_solaceon"])),
            "Route 212 South - Item on Northeast Island Past Bike Bridge": (HasAll("Bicycle", "Bag")) if self.opts.pastoria_barriers.value != 0 else (And(Has("Bicycle"), self.common_rules["veilstone_bicycle_from_solaceon"])),
            "Route 218 East - Item in Northeast Corner": (self.common_rules["surf"]),
            "Route 218 East - Item Below Fisherman": (self.common_rules["surf"]),
            "Canalave City - Item in Trees South of Canal": (self.common_rules["surf"]),
            "Iron Island - Gift from Byron": (self.common_rules["national_dex"]),
            "Mt. Coronet Tunnel to 1F - Hidden Item on Corner White Rock Before Exit": (self.common_rules["rock_smash"]),
            "Mt. Coronet Tunnel to 1F - Hidden Item Above Big White Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet Tunnel to 1F - Hidden Item Behind Breakable Rock on Left": (And(self.common_rules["rock_climb"], self.common_rules["rock_smash"])),
            "Mt. Coronet Tunnel to 1F - Hidden Item in White Rock on South Ledge": (self.common_rules["rock_climb"]),
            "Mt. Coronet Tunnel to 1F - Hidden Item on Right Path": (self.common_rules["rock_climb"]),
            "Mt. Coronet B1F - Item in SW Corner": (self.common_rules["rock_smash"]),
            "Mt. Coronet B1F - Item Behind West Boulder": (And(self.common_rules["strength"], self.common_rules["rock_smash"])),
            "Mt. Coronet B1F - Hidden Item Behind Breakable Rock West of Lake": (self.common_rules["rock_smash"]),
            "Mt. Coronet B1F - Hidden Item in SW White Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet B1F - Item in Middle of Lake": (self.common_rules["surf"]),
            "Mt. Coronet B1F - Item in Northeast Corner of Lake": (Or(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Mt. Coronet B1F - Item Behind Boulder": (self.common_rules["strength"]),
            "Mt. Coronet B1F - Item Against East Wall": (self.common_rules["rock_smash"]),
            "Mt. Coronet Outside North - Hidden Item in Corner Behind Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet Outside South - Hidden Item Behind Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet 4F Left - Hidden Item Behind NW Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet 4F Right - Hidden Item on Wall Behind Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet 4F Right - Hidden Item in Corner Behind Breakable Rock": (self.common_rules["rock_smash"]),
            "Mt. Coronet 4F Room Above Waterfall - Right Item": (And(self.common_rules["surf"], self.common_rules["waterfall"])),
            "Mt. Coronet 4F Room Above Waterfall - Left Item": (And(self.common_rules["surf"], self.common_rules["waterfall"])),
            "Mt. Coronet 4F Room Above Waterfall - Hidden Item in Rock": (And(self.common_rules["surf"], self.common_rules["waterfall"])),
            "Mt. Coronet 2F - Gift from Looker": (Has("event_galactic_hq_defeat_cyrus")),
            "Mt. Coronet 2F - Hidden Item on Rock Down East Staircase After Mural": (Has("event_galactic_hq_defeat_cyrus")),
            "Route 216 - Right Item on Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 216 - Bottom Item on Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 216 - Top Item on Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 216 - Left Item on Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Route 217 - Gift from Hiker": (Has("HM08 Rock Climb")),
            "Acuity Lakefront - Item East of Lake Entrance": (self.common_rules["rock_climb"]),
            "Lake Acuity - Item in NE Corner of Lake": (self.common_rules["surf"]),
            "Snowpoint Temple B4F - Item Past Ice Tile": (self.common_rules["strength"]),
            "Route 222 - Hidden Item in Grass Below Fence on the Left": (Or(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Route 222 - Item Behind Cut Tree": (self.common_rules["cut"]),
            "Route 222 - Item in Grass Below Fence": (Or(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Route 222 - Hidden Item in Grass Below Fence on the Right": (Or(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Route 222 - Hidden Item in Grass Below SE Fence": (self.common_rules["surf"]),
            "Sunyshore City - Item from Jasmine": (Has("event_beacon_badge")),
            "Poketch Company - Gift from CEO (1 Badge)": (And(HasAll("Coupon 3", "Coupon 1", "Coupon 2", "Parcel"), self.common_rules["badges"](1))),
            "Poketch Company - Gift from CEO (3 Badges)": (And(HasAll("Coupon 3", "Coupon 1", "Coupon 2", "Parcel"), self.common_rules["badges"](3))),
            "Poketch Company - Gift from CEO (5 Badges)": (And(HasAll("Coupon 3", "Coupon 1", "Coupon 2", "Parcel"), self.common_rules["badges"](5))),
            "Poketch Company - Gift from CEO (7 Badges)": (And(HasAll("Coupon 3", "Coupon 1", "Coupon 2", "Parcel"), self.common_rules["badges"](7))),
            "Victory Road 2F - Item in NE": (HasAll("Bicycle", "Bag")),
            "Victory Road 2F - Item Above Ledge": (HasAll("Bicycle", "Bag")),
            "Victory Road 2F - NW Item": (HasAll("Bicycle", "Bag")),
            "Victory Road B1F - Item in Top Right": (self.common_rules["surf"]),
            "Victory Road B1F - Item in Bottom Right": (self.common_rules["surf"]),
            "Victory Road B1F - Hidden Item on Rock Below Corner of Water": (self.common_rules["surf"]),
            "Victory Road 1F - Item from Southern B1F Stairs": (self.common_rules["surf"]),
            "Victory Road 2F - Item from Northern 1F Stairs": (self.common_rules["strength"]),
            "Pokemon League - Hidden Item Below SW Poke Ball Statue": (And(self.common_rules["down_waterfall"], self.common_rules["surf"])),
            "Victory Road 1F - First Item on Left": (self.common_rules["rock_climb"]),
            "Victory Road 1F - Hidden Item Before First Staircase to 2F": (self.common_rules["rock_climb"]),
            "Great Marsh Lobby - Item from Cowgirl": (Has("Marsh Pass")) if self.opts.marsh_pass.value != 0 else True_(),
            "Pastoria City - Item from Wake (After Defeating Gym)": (Has("event_fen_badge")),
            "Route 210 South - Third Item from Cynthia": (Has("SecretPotion")),
            "Route 230 - Item on Island East Side": (And(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Route 230 - Hidden Item on Island East Side Behind Breakable Rock": (And(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Route 230 - Item on Island West Side": (And(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Route 230 - Hidden Item on Island North Side": (And(self.common_rules["surf"], self.common_rules["rock_smash"])),
            "Route 229 - Item in Center Behind Cut Tree": (self.common_rules["cut"]),
            "Route 229 - Item Northeast of Pond": (self.common_rules["cut"]),
            "Route 229 - Hidden Item Southwest of Pond": (And(self.common_rules["cut"], self.common_rules["surf"])),
            "Resort Area - Item Across Pond": (self.common_rules["surf"]),
            "Route 228 - Item in Northernmost Pit": (And(Has("Bag"), (Or(Has("Bicycle"), self.common_rules["fly"])))),
            "Route 228 - Item Behind Breakable Rocks": (self.common_rules["rock_smash"]),
            "Route 228 - Item Across Bike Rail Above Vents": (HasAll("Bicycle", "Bag")),
            "Route 228 - Hidden Item in SE Corner by Rock": (HasAll("Bicycle", "Bag")),
            "Route 228 - Hidden Item in SW Grass": (HasAll("Bicycle", "Bag")),
            "Route 226 - Hidden Item in Tree Gap North of Meister's House": (self.common_rules["surf"]),
            "Route 226 - Hidden Item on Beach Below Rock Climb Area": (self.common_rules["surf"]),
            "Survival Area - Item to Left of Move Tutor's House": (self.common_rules["rock_climb"]),
            "Route 225 - Item on SW Hill": (self.common_rules["rock_climb"]),
            "Route 225 - Item Behind Cut Trees Near Trainer Trio": (self.common_rules["cut"]),
            "Route 225 - Item Behind Cut Trees Next to House": (self.common_rules["cut"]),
            "Route 225 - Item Across Lake Above House": (self.common_rules["surf"]),
            "Route 225 - Item on Northern Rock Climb Ledge": (self.common_rules["rock_climb"]),
            "Stark Mountain Exterior - Item on Southwest Hill": (self.common_rules["rock_climb"]),
            "Stark Mountain First Room - NE Item": (self.common_rules["rock_smash"]),
            "Stark Mountain First Room - Hidden Item Behind NE Item": (self.common_rules["rock_smash"]),
            "Stark Mountain Cavern - Item on Top of Central Rock Climb Hill": (self.common_rules["rock_climb"]),
            "Stark Mountain Cavern - Hidden Item Down SW Rock Climb Slope": (self.common_rules["rock_climb"]),
            "Stark Mountain Cavern - Item in East Pit": (self.common_rules["rock_climb"]),
            "Stark Mountain Cavern - Item in NE Corner": (self.common_rules["rock_climb"]),
            "Jubilife City - Item from Schoolboy in Southwest Corner": (self.common_rules["badges"](1)),
            "Twinleaf Town - Item from Mom (After Defeating Champion)": (Has("event_beat_cynthia")),
            "Celestic Town - Item from Man in Shop (Day)": (HasAll("Poketch", "Daytime")),
            "Celestic Town - Item from Man in Shop (Night)": (HasAll("Poketch", "Nighttime")),
            "event_roamer_0": (Has("event_distortion_world")),
            "event_lake_explosion": (HasAll("HM04 Strength", "event_mine_badge")),
        }
        self.location_type_rules = {
            "hidden": (self.common_rules["dowsingmachine_if_opt"]),
            "uunown": (self.common_rules["dowsingmachine_if_opt"]),
        }
        self.encounter_type_rules = {
            "surf": (self.common_rules["surf"]),
            "good_rod": (HasAll("Good Rod", "Bag")),
            "super_rod": (HasAll("Super Rod", "Bag")),
            "old_rod": (HasAll("Old Rod", "Bag")),
            "radar": (HasAll("Poke Radar", "Bag")),
            "ruby": (HasAll("Poketch", "Ruby Cartridge")),
            "sapphire": (HasAll("Poketch", "Sapphire Cartridge")),
            "night": (HasAll("Poketch", "Nighttime")),
            "emerald": (HasAll("Poketch", "Emerald Cartridge")),
            "firered": (HasAll("Poketch", "Fire Red Cartridge")),
            "leafgreen": (HasAll("Poketch", "Leaf Green Cartridge")),
            "day": (HasAll("Poketch", "Daytime")),
            "swarms": (HasAll("Poffin Case", "Bag")) if self.opts.start_with_swarms.value != 0 else (And(HasAll("Poffin Case", "event_beat_cynthia", "Bag"), self.common_rules["national_dex"])),
            "regular_honey_tree": (Has("event_floaroma_meadow")),
            "munchlax_honey_tree": (HasAll("Poketch", "event_floaroma_meadow", "Tree Camera", "DOWSING MACHINE")),
        }
        self.trainer_rules = {
            "galactic_boss_cyrus_celestic_town_ruins": (Has("Old Charm")),
            "rival_pastoria_city": (Has("event_cobble_badge")),
            "psychic_bryce": (self.common_rules["rock_climb"]),
            "ace_trainer_mariah": (self.common_rules["rock_climb"]),
            "psychic_valencia": (self.common_rules["surf"]),
            "ace_trainer_henry": (self.common_rules["surf"]),
            "double_team_jo_and_pat": (self.common_rules["surf"]),
            "veteran_grant": (self.common_rules["surf"]),
            "camper_diego": (self.common_rules["rock_smash"]),
            "picnicker_tori": (self.common_rules["rock_smash"]),
            "lass_cassidy": (self.common_rules["rock_smash"]),
            "youngster_wayne": (self.common_rules["rock_smash"]),
            "hiker_reginald": (self.common_rules["rock_smash"]),
            "collector_terry": (self.common_rules["rock_smash"]),
            "picnicker_ana": (self.common_rules["rock_smash"]),
            "camper_parker": (self.common_rules["rock_smash"]),
            "ruin_maniac_gerald": (self.common_rules["rock_smash"]),
            "hiker_lorenzo": (self.common_rules["rock_smash"]),
            "hiker_alexander": (self.common_rules["rock_climb"]),
            "fisherman_cody": (self.common_rules["surf"]),
            "rival_route_209": (Has("event_relic_badge")),
            "twins_teri_and_tia": (HasAll("Bicycle", "Bag")),
            "breeder_kahlil": (HasAll("Bicycle", "Bag")),
            "ninja_boy_davido": (And(Has("Bicycle"), (Or(Has("Bag"), And(self.common_rules["strength"], self.common_rules["rock_smash"]))))),
            "dragon_tamer_patrick": (self.common_rules["rock_climb"]),
            "bird_keeper_alexandra": (self.common_rules["rock_smash"]),
            "policeman_alex": (HasAll("Poketch", "Nighttime")),
            "policeman_dylan": (HasAll("Poketch", "Nighttime")),
            "policeman_caleb": (HasAll("Poketch", "Nighttime")),
            "policeman_bobby": (HasAll("Poketch", "Nighttime")),
            "policeman_danny": (HasAll("Poketch", "Nighttime")),
            "scientist_shaun": (And(HasAll("Bicycle", "Bag"), self.common_rules["cut"])) if self.opts.pastoria_barriers.value != 0 else (And(Has("Bicycle"), self.common_rules["cut"], self.common_rules["veilstone_bicycle_from_solaceon"])),
            "parasol_lady_sabrina": (And(HasAll("Bicycle", "Bag"), self.common_rules["cut"])) if self.opts.pastoria_barriers.value != 0 else (And(Has("Bicycle"), self.common_rules["cut"], self.common_rules["veilstone_bicycle_from_solaceon"])),
            "swimmer_sheltin": (self.common_rules["surf"]),
            "swimmer_evan": (self.common_rules["surf"]),
            "swimmer_mary": (self.common_rules["surf"]),
            "swimmer_haley": (self.common_rules["surf"]),
            "sailor_paul": (self.common_rules["surf"]),
            "black_belt_gregory": (self.common_rules["cut"]),
            "black_belt_philip": (self.common_rules["rock_climb"]),
            "skier_bradley": (self.common_rules["rock_climb"]),
            "skier_kaitlyn": (self.common_rules["rock_climb"]),
            "skier_andrea": (self.common_rules["rock_climb"]),
            "fisherman_miguel": (self.common_rules["surf"]),
            "fisherman_luc": (self.common_rules["surf"]),
            "tuber_trenton": (self.common_rules["surf"]),
            "tuber_mariel": (self.common_rules["surf"]),
            "swimmer_dillon": (self.common_rules["surf"]),
            "swimmer_vanessa": (self.common_rules["surf"]),
            "policeman_thomas": (HasAll("Poketch", "Nighttime")),
            "dragon_tamer_geoffrey": (self.common_rules["rock_climb"]),
            "dragon_tamer_keegan": (HasAll("Bicycle", "Bag")),
            "psychic_corbin": (HasAll("Bicycle", "Bag")),
            "swimmer_lydia": (self.common_rules["surf"]),
            "swimmer_wade": (self.common_rules["surf"]),
            "swimmer_glenn": (self.common_rules["surf"]),
            "swimmer_joanna": (self.common_rules["surf"]),
            "swimmer_kurt": (self.common_rules["surf"]),
            "swimmer_sophia": (self.common_rules["surf"]),
            "swimmer_sam": (self.common_rules["surf"]),
            "swimmer_mallory": (self.common_rules["surf"]),
            "champion_cynthia_rematch": (Has("event_stark_mountain_arrest_team_galactic")),
            "elite_four_bertha_rematch": (Has("event_stark_mountain_arrest_team_galactic")),
            "elite_four_aaron_rematch": (Has("event_stark_mountain_arrest_team_galactic")),
            "elite_four_lucian_rematch": (Has("event_stark_mountain_arrest_team_galactic")),
            "elite_four_flint_rematch": (Has("event_stark_mountain_arrest_team_galactic")),
            "galactic_grunt_celestic_town": (Has("Old Charm")),
            "galactic_grunt_valor_lakefront": (Has("event_fen_badge")),
            "galactic_grunt_jubilife_city_1": (Has("event_coal_badge")),
            "galactic_grunt_jubilife_city_2": (Has("event_coal_badge")),
            "galactic_grunt_veilstone_city_1": (Has("event_cobble_badge")),
            "galactic_grunt_veilstone_city_2": (Has("event_cobble_badge")),
            "rival_survival_area_1": (Has("event_stark_mountain_arrest_team_galactic")),
        }

    def get_enc_accessibility_rule(self, accessibility: Sequence[str]) -> Rule:
        nmd = frozenset(acc for acc in accessibility if acc in self.encounter_type_rules)
        if nmd in self.cached_enc_accessibility_rules:
            return self.cached_enc_accessibility_rules[nmd]
        rule = Or(*[self.encounter_type_rules[acc] for acc in accessibility if acc in self.encounter_type_rules])
        self.cached_enc_accessibility_rules[nmd] = rule
        return rule

    def get_pevo_rule(self, pevo: species.PreEvolution, options: "PokemonPlatinumOptions") -> Rule | None:
        mthd = pevo.method
        reqd_items = [f"mon_{pevo.species}"]
        if mthd.startswith("trade"):
            reqd_items.extend([items.items["linking_cord"].label, items.items["bag"].label])
        if mthd.endswith("day"):
            reqd_items.extend([items.items["daytime"].label, items.items["poketch"].label])
        elif mthd.endswith("night"):
            reqd_items.extend([items.items["nighttime"].label, items.items["poketch"].label])
        if pevo.item is not None:
            reqd_items.append(pevo.item)
            if "held" not in mthd:
                reqd_items.append(items.items["bag"].label)
            if not ((options.reusable_tms if pevo.item.startswith("TM") else pevo.item in items.reusable_evo_items) or options.evo_items_shop_in_ap_helper):
                reqd_items.append("event_veilstone_store")
        elif pevo.other_species is not None:
            reqd_items.append(f"mon_{pevo.other_species}")
        if mthd == "level_magnetic_field":
            reqd_items.append("event_magnetic_field")
        elif mthd == "level_moss_rock":
            reqd_items.append("event_moss_rock")
        elif mthd == "level_ice_rock":
            reqd_items.append("event_ice_rock")
        if mthd in {"level_atk_gt_def", "level_atk_eq_def", "level_atk_lt_def"}:
            reqd_items.extend(["event_veilstone_store", items.items["bag"].label])
        if "beauty" in mthd:
            reqd_items.extend(["event_veilstone_city", items.items["poffin_case"].label, "event_hearthome_city", items.items["bag"].label])

        return HasAll(*reqd_items)

    def get_mon_rule(self, mon: str) -> Rule:
        return Has(f"mon_{mon}")

    def get_once_mon_rule(self, mon: str) -> Rule:
        return Has(f"once_mon_{mon}")

    def get_roamer_rule(self, roamer: int) -> Rule:
        return Has(f"event_roamer_{roamer}")
