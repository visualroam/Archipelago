from typing import TYPE_CHECKING, Any
from typing_extensions import override
import dataclasses

from Options import Option
from BaseClasses import Location
from rule_builder.options import OptionFilter, Operator
from rule_builder.rules import Rule, Has, HasAll, True_, And, Or, CanReachLocation, CanReachRegion

if TYPE_CHECKING:
    from . import LHP2World

from .Data import LocationName, ItemName, RegionName
from .Options import EndGoal, HardPurchases, ShuffleRedBricks, ShuffleCharacterTokens
from .Locations import all_location_table, level_beaten_loc_table

itm = ItemName
locn = LocationName
regn = RegionName

# Helper Rules
can_use_dark_mag = (Has(itm.alecto_play) | Has(itm.amycus_play) | Has(itm.dolohov_play) | Has(itm.bellatrix_play) |
                    Has(itm.bellatrix_azka_play) | Has(itm.death_eater_play) | Has(itm.dolohov_workman_play) |
                    Has(itm.fenrir_play) | Has(itm.grindel_old_play) | Has(itm.grindel_young_play) |
                    Has(itm.lord_voldemort_play) | Has(itm.lucius_play) | Has(itm.lucius_death_eater_play) |
                    Has(itm.black_play) | Has(itm.pius_play) | Has(itm.scabior_play) | Has(itm.snatcher_play) |
                    Has(itm.rowle_play) | Has(itm.tom_riddle_play) | Has(itm.wormtail_play) | Has(itm.yaxley_play))

can_use_dm_in_hub = Has(ItemName.poly_unlock) & can_use_dark_mag

can_use_spanner = (Has(itm.arthur_play) | Has(itm.arthur_suit_play) | Has(itm.arthur_cardigan_play) |
                   Has(itm.arthur_torn_suit_play))

can_use_key = Has(itm.bogrod_play) | Has(itm.cole_play) | Has(itm.griphook_play) | Has(itm.ministry_guard_play)

can_use_key_in_hub = can_use_key & Has(itm.poly_unlock)

char_can_dig = (Has(itm.fang_play) | Has(itm.fenrir_play) | Has(itm.neville_cardigan_play) |
                Has(itm.neville_pyjamas_play) | Has(itm.neville_tank_top_play) | Has(itm.neville_waiter_play) |
                Has(itm.neville_winter_play) | Has(itm.neville_play) | Has(itm.prof_sprout_play))

can_dig_in_level = Has(itm.pets_unlock) | char_can_dig

can_dig_in_hub = Has(itm.pets_unlock) | (char_can_dig & Has(itm.poly_unlock))

strong_chars = (Has(itm.dudley_play) | Has(itm.dudley_grey_play) | Has(itm.dudley_shirt_play) | Has(itm.fenrir_play) |
                Has(itm.fang_play) | Has(itm.hagrid_play) | Has(itm.hagrid_wed_play) | Has(itm.muggle_orphan_play) |
                Has(itm.remus_lupin_play) | Has(itm.sirius_black_play) | Has(itm.sirius_azkaban_play) |
                Has(itm.vernon_play))

char_is_strong_level = strong_chars | Has(itm.super_strength_unlock)

char_is_strong_hub = (strong_chars & Has(itm.poly_unlock)) | Has(itm.super_strength_unlock)

ravenclaw_chars = (Has(itm.cho_play) | Has(itm.cho_winter_play) | Has(itm.luna_play) | Has(itm.luna_blue_jumper_play) |
                   Has(itm.luna_overalls_play) | Has(itm.luna_pink_dress_play) | Has(itm.luna_purple_coat_play) |
                   Has(itm.luna_yellow_dress_play) | Has(itm.belby_play) | Has(itm.padma_patil_play) |
                   Has(itm.penelope_play) | Has(itm.dumble_cursed_play) | Has(itm.dumble_young_play) |
                   Has(itm.prof_dumble_play))

has_high_multi = (Has(itm.score_x6_unlock) | Has(itm.score_x8_unlock) | Has(itm.score_x10_unlock) |
                  HasAll(itm.score_x2_unlock, itm.score_x4_unlock))
has_low_multi = Has(itm.score_x2_unlock) | Has(itm.score_x4_unlock) | has_high_multi

# Dark Times Logic
can_beat_dt = Has(itm.reducto_unlock)
can_get_dt_sc = Has(itm.diffindo_unlock)
can_get_dt_hc = Has(itm.www_box_unlock) & can_dig_in_level
can_get_dt_sip = can_use_dark_mag
can_get_arthur_suit = Has(itm.reducto_unlock) & can_use_dark_mag
can_get_elphias = Has(itm.agua_unlock)

# Dumbledore's Army Logic
can_beat_da = Has(itm.expecto_unlock)
can_access_da = Has(itm.da_unlock) & can_dig_in_level
can_access_da_free = Has(itm.pets_unlock)
can_get_da_gc = HasAll(itm.reducto_unlock, itm.specs_unlock) & char_is_strong_level
can_get_da_sc = Has(itm.focus_unlock)
can_get_da_rc = Has(itm.apparition_unlock)
can_get_da_hc = HasAll(itm.reducto_unlock, itm.www_box_unlock, itm.specs_unlock) & char_is_strong_level
can_get_da_sip = Has(itm.reducto_unlock) & can_use_dark_mag
can_get_cho_winter = HasAll(itm.reducto_unlock, itm.specs_unlock) & char_is_strong_level
can_get_herm_scarf = Has(itm.www_box_unlock)
can_get_neville_winter = Has(itm.specs_unlock)

# Focus!
can_get_foc_gc = Has(itm.reducto_unlock)
can_get_foc_hc = can_use_dark_mag
can_get_foc_sip = Has(itm.agua_unlock)
can_get_molly_apron = Has(itm.reducto_unlock) & char_is_strong_level
can_get_snape_under = Has(itm.www_box_unlock)

# Kreacher Discomforts
can_beat_kd = Has(itm.invis_unlock) & can_dig_in_level
can_get_kd_tw = HasAll(itm.reducto_unlock, itm.invis_unlock) | has_low_multi
can_get_kd_gc = Has(itm.apparition_unlock) & char_is_strong_level
can_get_kd_sc = HasAll(itm.reducto_unlock, itm.delum_unlock, itm.diffindo_unlock) & can_use_dark_mag
can_get_kd_rc = Has(itm.invis_unlock)
can_get_kd_hc = HasAll(itm.reducto_unlock, itm.diffindo_unlock, itm.invis_unlock)
can_get_kd_sip = HasAll(itm.reducto_unlock, itm.invis_unlock)
can_get_kreacher = can_use_dark_mag
can_get_sirius = HasAll(itm.agua_unlock, itm.invis_unlock)

# A Giant Virtuoso
can_access_agv_free = can_dig_in_level
can_get_agv_gc = can_use_key
can_get_agv_sc = Has(itm.herm_bag_unlock)
can_get_agv_rc = Has(itm.agua_unlock)
can_get_agv_hc = Has(itm.reducto_unlock)
can_get_agv_sip = Has(itm.www_box_unlock)
can_get_emmeline = Has(itm.agua_unlock)
can_get_neville = char_is_strong_level
can_get_prof_umbridge = can_use_dark_mag

# A Veiled Threat Logic
can_beat_avt = Has(itm.diffindo_unlock) & can_dig_in_level
can_get_avt_rc = Has(itm.agua_unlock) & Has(itm.diffindo_unlock) & can_dig_in_level
can_get_avt_hc = can_use_dark_mag
can_get_avt_sip = can_dig_in_level
can_get_fudge_wizen = Has(itm.diffindo_unlock) & can_dig_in_level
can_get_herm_jumper = Has(itm.agua_unlock)
can_get_lucius_death = can_use_dark_mag

# Out of Retirement Logic
can_access_oor = HasAll(itm.apparition_unlock, itm.lumos_unlock, itm.oor_unlock)
can_access_oor_free = HasAll(itm.reducto_unlock)
can_beat_oor = Has(itm.www_box_unlock)
can_get_oor_gc = can_use_spanner
can_get_oor_sc = Has(itm.agua_unlock) & can_use_dark_mag
can_get_oor_rc = Has(itm.specs_unlock) & can_use_dark_mag
can_get_oor_hc = HasAll(itm.www_box_unlock, itm.diffindo_unlock) & can_use_dark_mag
can_get_oor_sip = HasAll(itm.www_box_unlock, itm.diffindo_unlock) & can_use_dark_mag
can_get_dumble_cursed = can_use_dark_mag
can_get_milk_man = Has(itm.herm_bag_unlock)
can_get_slug_pajamas = can_use_dark_mag & can_use_key

# Just Desserts Logic
can_get_jd_sc = char_is_strong_level
can_get_jd_rc = HasAll(itm.delum_unlock, itm.herm_bag_unlock) & can_use_dark_mag
can_get_jd_hc = can_use_dark_mag
can_get_jd_sip = can_use_dark_mag
can_get_cormac_suit = Has(itm.agua_unlock)
can_get_harry_christ = HasAll(itm.herm_bag_unlock, itm.specs_unlock) & can_use_dark_mag
can_get_madam_rosmerta = can_use_dark_mag

# A Not So Merry Christmas Logic
can_access_ansmc_free = HasAll(itm.reducto_unlock, itm.specs_unlock, itm.agua_unlock) & can_dig_in_level
can_beat_ansmc = Has(itm.lumos_unlock)
can_get_ansmc_gc = HasAll(itm.apparition_unlock, itm.lumos_unlock) & can_use_key
can_get_ansmc_sc = can_use_dark_mag
can_get_ansmc_hc = Has(itm.pets_unlock)
can_get_bill_wedding = HasAll(itm.reducto_unlock, itm.delum_unlock)

# Love Hurts Logic
can_access_lh_free = HasAll(itm.reducto_unlock, itm.agua_unlock)
can_beat_lh = HasAll(itm.diffindo_unlock, itm.www_box_unlock, itm.pets_unlock)
can_get_lh_gc = HasAll(itm.www_box_unlock, itm.pets_unlock) & can_use_spanner
can_get_lh_sc = HasAll(itm.www_box_unlock, itm.pets_unlock) & can_use_dark_mag
can_get_lh_rc = Has(itm.reducto_unlock) & can_use_key
can_get_lh_hc = char_is_strong_level
can_get_lh_sip = can_use_dark_mag
can_get_draco_suit = Has(itm.delum_unlock) & can_use_dark_mag
can_get_ginny = Has(itm.agua_unlock) & can_dig_in_level
can_get_prof_slug = char_is_strong_level

# Felix Felicis Logic
can_access_ff = HasAll(itm.lumos_unlock, itm.ff_unlock)
can_access_ff_free = HasAll(itm.reducto_unlock, itm.agua_unlock)
can_beat_ff = Has(itm.diffindo_unlock)
can_get_ff_sc = can_use_key
can_get_ff_rc = can_use_dark_mag
can_get_ff_hc = can_use_dark_mag
can_get_ff_sip = Has(itm.www_box_unlock)
can_get_hagrid = Has(itm.herm_bag_unlock) & can_use_dark_mag
can_get_prof_sprout = HasAll(itm.reducto_unlock, itm.specs_unlock)

# The Horcrux and the Hand Logic
can_access_thath_free = HasAll(itm.apparition_unlock, itm.diffindo_unlock, itm.lumos_unlock)
can_beat_thath = HasAll(itm.reducto_unlock, itm.agua_unlock)
can_get_thath_sc = char_is_strong_level
can_get_thath_rc = HasAll(itm.apparition_unlock, itm.herm_bag_unlock)
can_get_thath_hc = HasAll(itm.reducto_unlock, itm.delum_unlock)
can_get_thath_sip = HasAll(itm.reducto_unlock, itm.agua_unlock)
can_get_hagrid_wed = HasAll(itm.reducto_unlock, itm.agua_unlock) & char_is_strong_level
can_get_prof_dumble = can_use_dark_mag
can_get_tr_orphan = can_use_dark_mag

# The Seven Harry's Logic
can_access_tsh_free = HasAll(itm.reducto_unlock, itm.agua_unlock, itm.herm_bag_unlock, itm.delum_unlock)
can_get_delum = HasAll(itm.reducto_unlock, itm.agua_unlock, itm.delum_unlock)
can_get_polyjuice = Has(itm.reducto_unlock)
can_get_tsh_sc = Has(itm.reducto_unlock) & can_dig_in_level
can_get_tsh_rc = Has(itm.lumos_unlock)
can_get_tsh_sip = Has(itm.lumos_unlock)
can_get_mad_eye = HasAll(itm.reducto_unlock, itm.agua_unlock) & can_use_dark_mag
can_get_ron_wed = HasAll(itm.apparition_unlock, itm.specs_unlock)

# Magic is Might Logic
can_access_mim_free = HasAll(itm.reducto_unlock, itm.diffindo_unlock, itm.delum_unlock, itm.agua_unlock)
can_beat_mim = Has(itm.pets_unlock)
can_get_mim_gc = char_is_strong_level
can_get_mim_sc = Has(itm.pets_unlock)
can_get_mim_rc = HasAll(itm.reducto_unlock, itm.diffindo_unlock, itm.delum_unlock) & can_use_key
can_get_mim_hc = can_use_dark_mag
can_get_mim_sip = can_use_dark_mag
can_get_ron_reg = HasAll(itm.reducto_unlock, itm.diffindo_unlock)

# In Grave Danger Logic
can_access_igd_free = HasAll(itm.diffindo_unlock, itm.reducto_unlock, itm.herm_bag_unlock)
can_beat_igd = Has(itm.agua_unlock)
can_get_igd_gc = HasAll(itm.www_box_unlock, itm.specs_unlock) & can_dig_in_level
can_get_igd_sc = can_use_dark_mag
can_get_igd_rc = HasAll(itm.www_box_unlock, itm.delum_unlock, itm.herm_bag_unlock)
can_get_igd_sip = can_use_dark_mag
can_get_bathilda_snake = can_use_dark_mag
can_get_harry_god_hollow = Has(itm.agua_unlock) & can_use_dark_mag
can_get_lily = Has(itm.www_box_unlock)

# Sword and Locket Logic
can_access_sal = HasAll(itm.lumos_unlock, itm.sal_unlock)
can_beat_sal = HasAll(itm.apparition_unlock, itm.diffindo_unlock)
can_get_sal_gc = can_use_dark_mag
can_get_sal_sc = Has(itm.herm_bag_unlock)
can_get_sal_rc = Has(itm.www_box_unlock)
can_get_sal_sip = Has(itm.herm_bag_unlock) & can_use_dark_mag
can_get_herm_gray_coat = HasAll(itm.herm_bag_unlock, itm.specs_unlock)

# Lovegood's Lunacy Logic
can_access_ll_free = HasAll(itm.agua_unlock, itm.herm_bag_unlock, itm.lumos_unlock) & can_dig_in_level
can_access_second_floor = HasAll(itm.diffindo_unlock, itm.pets_unlock)
can_access_lunas_room = Or(char_is_strong_level, HasAll(itm.specs_unlock, itm.reducto_unlock)) & can_access_second_floor
can_beat_ll = can_access_lunas_room & Has(itm.reducto_unlock)
can_get_ll_rc = can_access_lunas_room & Has(itm.delum_unlock)
can_get_ll_hc = can_use_spanner
can_get_ll_sip = Has(itm.lumos_unlock)
can_get_skeleton = can_use_dark_mag
can_get_xeno_luna = HasAll(itm.www_box_unlock, itm.specs_unlock) & can_use_dark_mag & can_access_lunas_room

# Dobby! Logic
can_access_dob_free = HasAll(itm.specs_unlock, itm.pets_unlock) & Or(Has(itm.lumos_unlock), Has(itm.delum_unlock))
can_get_dob_gc = Has(itm.diffindo_unlock)
can_get_dob_rc = can_use_dark_mag
can_get_dob_sip = Has(itm.reducto_unlock)
can_get_dobby = can_use_dark_mag
can_get_wormtail = can_use_dark_mag
can_get_olivander = Has(itm.lumos_unlock) | Has(itm.delum_unlock)

# The Thief's Downfall Logic
can_access_ttd_free = Has(itm.herm_bag_unlock)
can_beat_ttd = HasAll(itm.reducto_unlock, itm.agua_unlock, itm.delum_unlock)
can_get_ttd_gc = Has(itm.reducto_unlock)
can_get_ttd_sc = can_use_dark_mag
can_get_ttd_rc = Has(itm.specs_unlock) & char_is_strong_level
can_get_ttd_hc = HasAll(itm.reducto_unlock, itm.agua_unlock, itm.delum_unlock, itm.specs_unlock) & char_is_strong_level
can_get_ttd_sip = can_use_dark_mag
can_get_bogrod = can_use_dark_mag
can_get_griphook = can_use_dark_mag & Has(itm.www_box_unlock)
can_get_herm_gringotts = can_use_dark_mag

# Back To School Logic
can_access_bts = HasAll(itm.herm_bag_unlock, itm.bts_unlock) & can_dig_in_level
can_access_bts_free = HasAll(itm.agua_unlock, itm.delum_unlock, itm.www_box_unlock, itm.diffindo_unlock)
can_get_bts_sc = Has(itm.reducto_unlock)
can_get_bts_hc = HasAll(itm.agua_unlock, itm.delum_unlock) & can_use_key
can_get_bts_sip = HasAll(itm.agua_unlock, itm.delum_unlock)
can_get_aberforth = HasAll(itm.agua_unlock, itm.delum_unlock) & char_is_strong_level
can_get_alecto = can_use_dark_mag
can_get_amycus = can_use_dark_mag

# Burning Bridges Logic
can_access_bb = HasAll(itm.bb_unlock, itm.agua_unlock)
can_access_bb_free = HasAll(itm.specs_unlock, itm.reducto_unlock)
can_beat_bb = HasAll(itm.diffindo_unlock, itm.herm_bag_unlock, itm.www_box_unlock, itm.delum_unlock, itm.lumos_unlock)
can_get_bb_gc = can_beat_bb & can_use_dark_mag & can_use_key
can_get_bb_sc = can_use_dark_mag
can_get_bb_rc = HasAll(itm.diffindo_unlock, itm.lumos_unlock)
can_get_bb_hc = Has(itm.delum_unlock)
can_get_bb_sip = can_use_dark_mag
can_get_neville_cardigan = HasAll(itm.diffindo_unlock, itm.herm_bag_unlock, itm.lumos_unlock) & can_use_dark_mag
can_get_seamus = HasAll(itm.delum_unlock, itm.www_box_unlock)

# Fiendfyre Frenzy Logic
can_access_fiend = (HasAll(itm.www_box_unlock, itm.reducto_unlock, itm.herm_bag_unlock, itm.fiend_unlock)
                    & can_dig_in_level)
can_access_fiend_free = HasAll(itm.specs_unlock, itm.delum_unlock)
can_beat_fiend = HasAll(itm.agua_unlock, itm.diffindo_unlock, itm.pets_unlock)
can_get_fiend_gc = char_is_strong_level
can_get_fiend_sc = can_use_dark_mag & Has(itm.pets_unlock)
can_get_fiend_rc = Has(itm.agua_unlock) & can_use_dark_mag
can_get_fiend_hc = char_is_strong_level
can_get_fiend_sip = Has(itm.specs_unlock)
can_get_goyle = HasAll(itm.agua_unlock, itm.pets_unlock) & can_use_key
can_get_harry_brown_jacket = HasAll(itm.agua_unlock, itm.diffindo_unlock, itm.pets_unlock) & can_use_spanner
can_get_tom_riddle = HasAll(itm.agua_unlock, itm.diffindo_unlock, itm.pets_unlock)

# Snape's Tears Logic
can_access_st = HasAll(itm.agua_unlock, itm.www_box_unlock, itm.st_unlock)
can_access_st_free = HasAll(itm.reducto_unlock, itm.herm_bag_unlock)
can_beat_st = HasAll(itm.diffindo_unlock, itm.delum_unlock, itm.focus_unlock, itm.lumos_unlock, itm.invis_unlock)
can_get_st_gc = can_use_dark_mag
can_get_st_sc = can_use_dark_mag & Has(itm.invis_unlock)
can_get_st_rc = HasAll(itm.diffindo_unlock, itm.lumos_unlock, itm.invis_unlock) & can_use_spanner
can_get_st_hc = HasAll(itm.diffindo_unlock, itm.lumos_unlock, itm.invis_unlock) & char_is_strong_level
can_get_death_eater = can_use_key
can_get_fenrir = can_use_dark_mag
can_get_prof_snape = HasAll(itm.diffindo_unlock, itm.lumos_unlock, itm.invis_unlock) & can_use_dark_mag

# The Flaw in the Plan Logic
can_access_tfitp_free = HasAll(itm.reducto_unlock, itm.agua_unlock, itm.diffindo_unlock, itm.www_box_unlock)
can_beat_tfitp = Has(itm.expecto_unlock)
can_get_tfitp_sc = can_use_dark_mag
can_get_tfitp_rc = Has(itm.specs_unlock) & char_is_strong_level
can_get_tfitp_sip = can_use_key
defeat_voldemort = Has("Voldemort Defeated")

# Hub Logic
# Access Logic
can_access_knockturn = HasAll(itm.diffindo_unlock, itm.dada_lesson_e_item)
can_access_tent = HasAll(itm.herm_bag_unlock, itm.apparition_unlock, itm.cafe_lesson_e_item)
can_access_train_grounds = HasAll(itm.agua_unlock, itm.dada_lesson_e_item)
can_access_library = Has(itm.agua_unlock) & (Has(itm.cafe_lesson_e_item) | Has(itm.y6_hogwarts_e_item))
can_access_hog_grounds = Has(itm.dada_lesson_e_item) & Has(itm.lumos_unlock)
can_access_lake = HasAll(itm.herm_bag_unlock, itm.cafe_lesson_e_item)
can_access_quid = HasAll(itm.delum_unlock, itm.cafe_lesson_e_item)
can_access_potions = Has(itm.y6_hogwarts_e_item)
can_access_div_court = HasAll(itm.diffindo_unlock, itm.dada_lesson_e_item)
can_access_astron = Has(itm.herm_bag_unlock) & (Has(itm.cafe_lesson_e_item) | Has(itm.y6_hogwarts_e_item))
can_access_great_hall = Has(itm.dada_lesson_e_item)
can_access_weasley_courtyard = HasAll(itm.focus_lesson_e_item, itm.www_box_unlock)
can_access_mid_grand_stair = HasAll(itm.y6_hogwarts_e_item, itm.diffindo_unlock)
can_access_dumb_office = Has(itm.www_box_unlock)
can_access_upper_grand_stair = HasAll(itm.dada_lesson_e_item, itm.agua_unlock)
can_access_slytherin_common = HasAll(itm.herm_bag_unlock, itm.y5_hogwarts_e_item) & can_use_dm_in_hub
can_access_hufflepuff_common = Has(itm.y5_hogwarts_e_item) & can_use_dm_in_hub
can_access_ravenclaw_tower = Has(itm.agua_unlock) & (Has(itm.cafe_lesson_e_item) | Has(itm.y6_hogwarts_e_item))
can_access_hogsmeade = Has(itm.y6_hogwarts_e_item) | Has(itm.cafe_lesson_e_item)
can_access_cafe = Has(itm.y6_story_complete_e_item) | Has(itm.y5_story_complete_e_item)
can_access_y5c = HasAll(itm.diffindo_unlock, itm.pets_unlock, itm.dueling_lesson_e_item)
can_access_y6c = HasAll(itm.agua_unlock, itm.lumos_unlock, itm.vial_lesson_e_item)

# Hub Collectibles
can_get_knock_sip = can_use_dm_in_hub
can_get_www_gb = (Has(itm.y6_hogwarts_e_item) | Has(itm.y5_story_complete_e_item)) & can_use_dm_in_hub
can_get_cafe_gb = char_is_strong_hub & Has(itm.cafe_lesson_e_item)
can_get_cafe_sip = Has(itm.cafe_lesson_e_item)
can_get_tent_gb = can_use_dm_in_hub
can_get_tent_sip = Has(itm.delum_unlock)
can_get_wild_gb = can_use_dm_in_hub
can_get_wild_sip = Has(itm.agua_unlock)
can_get_kcs_gb = HasAll(itm.dada_lesson_e_item, itm.pets_unlock)
can_get_kcs_rb = HasAll(itm.dada_lesson_e_item, itm.diffindo_unlock)
can_get_hogstat_rb = can_use_dm_in_hub
can_get_hogstat_sip = HasAll(itm.herm_bag_unlock, itm.reducto_unlock, itm.y6_story_complete_e_item)
can_get_hogspath_gb = char_is_strong_hub
can_get_hogspath_rb = Has(itm.delum_unlock)
can_get_hogspath_sip = Has(itm.reducto_unlock)
can_get_hogs_gb = can_use_key_in_hub
can_get_hogs_sip = Has(itm.delum_unlock)
can_get_hogs_rb = Has(itm.specs_unlock)
can_get_hogwpath_gb = HasAll(itm.reducto_unlock, itm.dada_lesson_e_item)
can_get_hogwpath_rb = Has(itm.herm_bag_unlock)
can_get_hogwpath_sip = HasAll(itm.dada_lesson_e_item, itm.lumos_unlock)
can_get_quad_gb = HasAll(itm.www_box_unlock, itm.dada_lesson_e_item)
can_get_quad_rb = HasAll(itm.diffindo_unlock, itm.dada_lesson_e_item)
can_get_quad_sip = Has(itm.delum_unlock)
can_get_tg_gb = can_use_dm_in_hub
can_get_herb_gb = Has(itm.diffindo_unlock)
can_get_grounds_rb = HasAll(itm.specs_unlock, itm.y6_hogwarts_e_item)
can_get_thest_gb = Has(itm.thestral_lesson_e_item)
can_get_thest_rb = Has(itm.thestral_lesson_e_item) & can_use_dm_in_hub
can_get_thest_sip = Has(itm.thestral_lesson_e_item)
can_get_lake_rb = Has(itm.reducto_unlock)
can_get_lake_sip = can_use_dm_in_hub
can_get_foyer_gb = Has(itm.y5_hogwarts_e_item)
can_get_foyer_sip = Has(itm.y5_hogwarts_e_item)
can_get_stair_gb = Has(itm.diffindo_unlock)
can_get_stair_sip = HasAll(itm.diffindo_unlock, itm.dada_lesson_e_item)
can_get_dorm_lobby_gb = Has(itm.y5_hogwarts_e_item)
can_get_dorm_lobby_sip = Has(itm.y5_hogwarts_e_item)
can_get_gryf_common_gb = HasAll(itm.dada_lesson_e_item, itm.reducto_unlock)
can_get_gryf_common_sip = HasAll(itm.dada_lesson_e_item, itm.agua_unlock)
can_get_raven_tower_sip = can_use_dm_in_hub
can_get_lib_rb = HasAll(itm.poly_unlock, itm.diffindo_unlock) & ravenclaw_chars
can_get_lib_sip = Has(itm.herm_bag_unlock)
can_get_lib_gb = Has(itm.pets_unlock)
can_get_ghl_gb = Has(itm.focus_unlock)
can_get_ghl_rb = can_use_dm_in_hub
can_get_ghl_sip = Has(itm.delum_unlock)
can_get_wc_gb = Has(itm.owls_lesson_e_item)
can_get_wc_rb = can_use_dm_in_hub & Has(itm.owls_lesson_e_item)
can_get_wc_sip = HasAll(itm.reducto_unlock, itm.owls_lesson_e_item)
can_get_wcs_sip = can_use_dm_in_hub & Has(itm.owls_lesson_e_item)
can_get_gh_rb = can_use_dm_in_hub
can_get_gh_sip = Has(itm.reducto_unlock)
can_get_ror_gb = can_use_dm_in_hub
can_get_ror_rb = Has(itm.reducto_unlock)
can_get_cl_gb = Has(itm.draught_lesson_e_item)
can_get_cl_sip = HasAll(itm.reducto_unlock, itm.dada_lesson_e_item)
can_get_y5c_gb = Has(itm.diffindo_lesson_e_item)
can_get_y5c_sip = Has(itm.diffindo_lesson_e_item)
can_get_y6c_gb = Has(itm.agua_lesson_e_item)
can_get_y6c_sip = Has(itm.agua_lesson_e_item)
can_get_dada_gb = Has(itm.dada_lesson_e_item)
can_get_dada_rb = Has(itm.dada_lesson_e_item) & can_use_dm_in_hub
can_get_dada_sip = Has(itm.dada_lesson_e_item)
can_get_pot_gb = Has(itm.draught_lesson_e_item)
can_get_pot_sip = Has(itm.draught_lesson_e_item)
can_get_divc_gb = Has(itm.specs_unlock)
can_get_divc_rb = Has(itm.agua_unlock)
can_get_divc_sip = Has(itm.agua_unlock)
can_get_div_rb = Has(itm.specs_unlock)
can_get_ast_rb = can_use_dm_in_hub & Has(itm.cafe_lesson_e_item)
can_get_ast_sip = Has(itm.cafe_lesson_e_item)

# Hub Token Logic
can_get_anthony_token = HasAll(itm.poly_unlock, itm.diffindo_unlock) & ravenclaw_chars
can_get_filch_token = Has(itm.owls_lesson_e_item)
can_get_arthur_cardigan = HasAll(itm.herm_bag_unlock, itm.diffindo_unlock)
can_get_arthur_torn_suit = Has(itm.owls_lesson_e_item)
can_get_bella_azka = HasAll(itm.herm_bag_unlock, itm.cafe_lesson_e_item)
can_get_blaise = HasAll(itm.y5_story_complete_e_item, itm.herm_bag_unlock) & can_use_dm_in_hub
can_get_charity = Has(itm.draught_lesson_e_item)
can_get_charlie = Has(itm.owls_lesson_e_item)
can_get_cho = HasAll(itm.delum_unlock, itm.poly_unlock, itm.agua_lesson_e_item)
can_get_crabbe_jumper = char_is_strong_hub
can_get_dean_winter = can_dig_in_hub
can_get_dolohov = Has(itm.cafe_lesson_e_item)
can_get_dolohov_work = Has(itm.cafe_lesson_e_item) & can_use_dm_in_hub
can_get_draco = Has(itm.dada_lesson_e_item) & can_use_dm_in_hub
can_get_dragomir = Has(itm.diffindo_unlock)
can_get_dudley = Has(itm.cafe_lesson_e_item)
can_get_dudley_shirt = HasAll(itm.dada_lesson_e_item, itm.pets_unlock)
can_get_dumble_young = Has(itm.agua_unlock)
can_get_fat_lady = HasAll(itm.reducto_unlock, itm.dada_lesson_e_item)
can_get_fleur = Has(itm.agua_unlock)
can_get_fred_owls = HasAll(itm.agua_unlock, itm.owls_lesson_e_item)
can_get_fred_pyjamas = (Has(itm.y6_hogwarts_e_item) | Has(itm.y5_story_complete_e_item))
can_get_fred = (Has(itm.y6_hogwarts_e_item) | Has(itm.y5_story_complete_e_item))
can_get_george_owls = HasAll(itm.owls_lesson_e_item, itm.lumos_unlock) & can_dig_in_hub
can_get_george_pyjamas = Has(itm.reducto_unlock) & (Has(itm.y6_hogwarts_e_item) | Has(itm.y5_story_complete_e_item))
can_get_george = (Has(itm.y6_hogwarts_e_item) | Has(itm.y5_story_complete_e_item))
can_get_ginny_pyjamas = Has(itm.y5_hogwarts_e_item)
can_get_goyle_jumper = HasAll(itm.agua_unlock, itm.dada_lesson_e_item)
can_get_gregorovitch = HasAll(itm.dada_lesson_e_item, itm.lumos_unlock)
can_get_hannah = Has(itm.specs_unlock)
can_get_harry_pyjamas = Has(itm.y5_hogwarts_e_item)
can_get_herm_ball_gown = Has(itm.y5_hogwarts_e_item)
can_get_herm_cardigan = Has(itm.y5_hogwarts_e_item)
can_get_katie_bell = can_use_dm_in_hub & Has(itm.thestral_lesson_e_item)
can_get_lavender = Has(itm.agua_lesson_e_item)
can_get_lily_casual = HasAll(itm.reducto_unlock, itm.dada_lesson_e_item)
can_get_lucius = can_use_dm_in_hub
can_get_luna_blue = Has(itm.thestral_lesson_e_item)
can_get_luna_overalls = HasAll(itm.reducto_unlock, itm.dada_lesson_e_item, itm.pets_unlock)
can_get_luna_pink = Has(itm.specs_unlock)
can_get_luna = Has(itm.dada_lesson_e_item) & can_dig_in_hub
can_get_madam_pince = can_use_dm_in_hub
can_get_mafalda = HasAll(itm.agua_unlock, itm.dada_lesson_e_item)
can_get_belby = can_use_dm_in_hub
can_get_mary = HasAll(itm.agua_unlock, itm.dada_lesson_e_item)
can_get_mcgonagall_black = Has(itm.cafe_lesson_e_item)
can_get_mcgonagall_pyjamas = HasAll(itm.delum_unlock, itm.dada_lesson_e_item)
can_get_michael = Has(itm.reducto_unlock)
can_get_ministry_guard = can_use_key_in_hub
can_get_myrtle = Has(itm.reducto_unlock)
can_get_mrs_black = can_use_dm_in_hub
can_get_mrs_cole = can_use_dm_in_hub
can_get_narcissa = Has(itm.agua_unlock)
can_get_neville_tank = HasAll(itm.reducto_unlock, itm.dada_lesson_e_item)
can_get_neville_waiter = Has(itm.specs_unlock)
can_get_padma = Has(itm.thestral_lesson_e_item) & can_dig_in_hub
can_get_petunia_green = Has(itm.cafe_lesson_e_item)
can_get_petunia = Has(itm.cafe_lesson_e_item)
can_get_pius = can_use_dm_in_hub
can_get_prof_binns = can_use_key_in_hub
can_get_prof_flitwick = HasAll(itm.agua_unlock, itm.diffindo_lesson_e_item)
can_get_prof_grub = Has(itm.agua_unlock)
can_get_prof_mcgonagall = can_use_key_in_hub & Has(itm.delum_unlock)
can_get_prof_trelawney = Has(itm.agua_unlock)
can_get_reg_catter = Has(itm.agua_unlock)
can_get_regulus = Has(itm.agua_unlock)
can_get_rita = HasAll(itm.agua_unlock, itm.dada_lesson_e_item)
can_get_ron_blue = Has(itm.y5_hogwarts_e_item)
can_get_ron_green = HasAll(itm.reducto_unlock, itm.www_box_unlock)
can_get_ron_red_sweater = HasAll(itm.dada_lesson_e_item, itm.lumos_unlock)
can_get_rufus = Has(itm.delum_unlock)
can_get_seamus_winter = can_dig_in_hub
can_get_scabior = can_use_dm_in_hub
can_get_slug_young = can_use_dm_in_hub & Has(itm.diffindo_unlock)
can_get_snatcher = can_use_dm_in_hub
can_get_susan_bones = Has(itm.y5_hogwarts_e_item)
can_get_rowle = can_use_dm_in_hub
can_get_umbridge_wizen = Has(itm.dada_lesson_e_item) & can_use_dm_in_hub
can_get_vernon = Has(itm.cafe_lesson_e_item)
can_get_waitress_luchino = Has(itm.cafe_lesson_e_item)
can_get_yaxley = can_use_dm_in_hub


# Shop Logic
def from_option(option: type[Option], value: Any, operator: Operator = "eq") -> Rule:
    return True_(options=[OptionFilter(option, value, operator)])


def can_purch_red_brick(location_name: str) -> Rule:
    red_brick = location_name.replace("sed", "sable")

    # Verify they have the Red Brick (if the options require it) and the required multiplier
    has_red_brick = Has(red_brick) | from_option(ShuffleRedBricks, 0, "ne")
    has_multi = has_needed_multi(location_name)

    # Verify they have the moves to do the Red Brick Check (if the options require it)
    from .Data import RuleMapping
    can_get_red_brick = (
            from_option(ShuffleRedBricks, 2, "ne")
            | RuleMapping.red_brick_rule_table.get(location_name, True_())
    )

    # Verify they have the moves to access the Red Brick Region (if the options require it)
    loc_data = all_location_table.get(location_name)
    if loc_data and loc_data.token_region:
        can_access_token_region = CanReachRegion(loc_data.token_region) | from_option(ShuffleRedBricks, 2, "ne")
    else:
        can_access_token_region = True_()

    return And(has_red_brick, has_multi, can_get_red_brick, can_access_token_region)


def can_purch_char(location_name: str) -> Rule:
    token = location_name.replace(" Purchased", " Token")

    # Verify they have the Token (if the options require it) and the required multiplier
    has_token = Has(token) | from_option(ShuffleCharacterTokens, 0, "ne")
    has_multi = has_needed_multi(location_name)

    # Verify they have the moves to do the Token Check (if the options require it)
    from .Data import RuleMapping
    can_get_token = (
            from_option(ShuffleCharacterTokens, 2, "ne")
            | RuleMapping.token_rule_table.get(location_name, True_())
    )

    # Verify that they have the moves to access the Token Region (if the options require it)
    token_location = token + " Collected"
    loc_data = all_location_table.get(token_location)

    if loc_data and loc_data.region:
        can_access_token_region = (
            CanReachRegion(loc_data.region)
            | from_option(ShuffleCharacterTokens, 2, "ne")
        )
    else:
        can_access_token_region = True_()

    return And(has_token, has_multi, can_get_token, can_access_token_region)


def can_purch_joke(location_name: str) -> Rule:
    return And(has_needed_multi(location_name), Has(itm.dada_lesson_e_item))


def has_needed_multi(location_name: str) -> Rule:
    return Or(from_option(HardPurchases, 1), HasMultiplier(location_name))


@dataclasses.dataclass
class HasMultiplier(Rule, game="Lego Harry Potter 5-7"):
    location_name: str

    @override
    def _instantiate(self, world: "LHP2World") -> Rule.Resolved:
        # Look up the price
        data = all_location_table[self.location_name]
        cheaper_shop_amount = world.options.CheaperShops
        price = data.price / cheaper_shop_amount

        # Get Multiplier Requirements
        low = world.options.LowMultiplierPriceMinimum
        high = world.options.HighMultiplierPriceMinimum

        # Compare and Return
        if price < low:
            return True_().resolve(world)
        elif price < high:
            return has_low_multi.resolve(world)
        else:
            return has_high_multi.resolve(world)


def set_entrance_rules(world):
    # Level Entrance Rules
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.dt), Has(itm.dt_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.da), Has(itm.da_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.foc), Has(itm.foc_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.kd), Has(itm.kd_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.agv), Has(itm.agv_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.avt), Has(itm.avt_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.oor), can_access_oor)
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.jd), Has(itm.jd_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.ansmc), Has(itm.ansmc_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.lh), Has(itm.lh_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.ff), can_access_ff)
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.thath), Has(itm.thath_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.tsh), Has(itm.tsh_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.mim), Has(itm.mim_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.igd), Has(itm.igd_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.sal), can_access_sal)
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.ll), Has(itm.ll_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.dob), Has(itm.dob_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.ttd), Has(itm.ttd_unlock))
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.bts), can_access_bts)
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.bb), can_access_bb)
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.fiend), can_access_fiend)
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.st), can_access_st)
    world.set_rule(world.get_entrance(regn.leaky + " -> " + regn.tfitp), Has(itm.tfitp_unlock))
    # Freeplay Entrance Rules
    world.set_rule(world.get_entrance(regn.da + " -> " + regn.daf), can_access_da_free)
    world.set_rule(world.get_entrance(regn.foc + " -> " + regn.focf), Has(itm.focus_unlock))
    world.set_rule(world.get_entrance(regn.agv + " -> " + regn.agvf), can_access_agv_free)
    world.set_rule(world.get_entrance(regn.oor + " -> " + regn.oorf), can_access_oor_free)
    world.set_rule(world.get_entrance(regn.ansmc + " -> " + regn.ansmcf), can_access_ansmc_free)
    world.set_rule(world.get_entrance(regn.lh + " -> " + regn.lhf), can_access_lh_free)
    world.set_rule(world.get_entrance(regn.ff + " -> " + regn.fff), can_access_ff_free)
    world.set_rule(world.get_entrance(regn.thath + " -> " + regn.thathf), can_access_thath_free)
    world.set_rule(world.get_entrance(regn.tsh + " -> " + regn.tshf), can_access_tsh_free)
    world.set_rule(world.get_entrance(regn.mim + " -> " + regn.mimf), can_access_mim_free)
    world.set_rule(world.get_entrance(regn.igd + " -> " + regn.igdf), can_access_igd_free)
    world.set_rule(world.get_entrance(regn.ll + " -> " + regn.llf), can_access_ll_free)
    world.set_rule(world.get_entrance(regn.dob + " -> " + regn.dobf), can_access_dob_free)
    world.set_rule(world.get_entrance(regn.ttd + " -> " + regn.ttdf), can_access_ttd_free)
    world.set_rule(world.get_entrance(regn.bts + " -> " + regn.btsf), can_access_bts_free)
    world.set_rule(world.get_entrance(regn.bb + " -> " + regn.bbf), can_access_bb_free)
    world.set_rule(world.get_entrance(regn.fiend + " -> " + regn.fiendf), can_access_fiend_free)
    world.set_rule(world.get_entrance(regn.st + " -> " + regn.stf), can_access_st_free)
    world.set_rule(world.get_entrance(regn.tfitp + " -> " + regn.tfitpf), can_access_tfitp_free)
    # Hub Entrance Rules
    world.set_rule(world.get_entrance(regn.diag + " -> " + regn.knock), can_access_knockturn)
    world.set_rule(world.get_entrance(regn.lond + " -> " + regn.tent), can_access_tent)
    world.set_rule(world.get_entrance(regn.lond + " -> " + regn.cafe), can_access_cafe)
    world.set_rule(world.get_entrance(regn.quad + " -> " + regn.tg), can_access_train_grounds)
    world.set_rule(world.get_entrance(regn.foyer + " -> " + regn.lib), can_access_library)
    world.set_rule(world.get_entrance(regn.foyer + " -> " + regn.ground), can_access_hog_grounds)
    world.set_rule(world.get_entrance(regn.ground + " -> " + regn.lake), can_access_lake)
    world.set_rule(world.get_entrance(regn.ground + " -> " + regn.qp), can_access_quid)
    world.set_rule(world.get_entrance(regn.cl + " -> " + regn.pot), can_access_potions)
    world.set_rule(world.get_entrance(regn.cl + " -> " + regn.divc), can_access_div_court)
    world.set_rule(world.get_entrance(regn.divc + " -> " + regn.ast), can_access_astron)
    world.set_rule(world.get_entrance(regn.foyer + " -> " + regn.ghl), can_access_great_hall)
    world.set_rule(world.get_entrance(regn.ghl + " -> " + regn.wc), can_access_weasley_courtyard)
    world.set_rule(world.get_entrance(regn.low_stair + " -> " + regn.mid_stair), can_access_mid_grand_stair)
    world.set_rule(world.get_entrance(regn.mid_stair + " -> " + regn.dumble_office), can_access_dumb_office)
    world.set_rule(world.get_entrance(regn.dumble_office + " -> " + regn.upper_stair), can_access_upper_grand_stair)
    world.set_rule(world.get_entrance(regn.upper_stair + " -> " + regn.dumble_office), can_access_upper_grand_stair)
    world.set_rule(world.get_entrance(regn.dormlob + " -> " + regn.slyth), can_access_slytherin_common)
    world.set_rule(world.get_entrance(regn.dormlob + " -> " + regn.huff), can_access_hufflepuff_common)
    world.set_rule(world.get_entrance(regn.dormlob + " -> " + regn.raven), can_access_ravenclaw_tower)
    world.set_rule(world.get_entrance(regn.hogwpath + " -> " + regn.hogspath), can_access_hogsmeade)
    world.set_rule(world.get_entrance(regn.cl + " -> " + regn.y5c), can_access_y5c)
    world.set_rule(world.get_entrance(regn.cl + " -> " + regn.y6c), can_access_y6c)


def set_lesson_logic(world):
    world.set_rule(world.get_location(locn.dada_lesson), Has(itm.y5_hogwarts_e_item))
    world.set_rule(world.get_location(locn.thestral_lesson), Has(itm.dada_lesson_e_item))
    world.set_rule(world.get_location(locn.dueling_lesson), Has(itm.thestral_lesson_e_item))
    world.set_rule(world.get_location(locn.diffindo_lesson), HasAll(itm.dueling_lesson_e_item))
    world.set_rule(world.get_location(locn.patroneous_lesson), HasAll(itm.expecto_unlock, itm.diffindo_lesson_e_item))
    world.set_rule(world.get_location(locn.grawp_lesson), Has(itm.patroneous_lesson_e_item))
    world.set_rule(world.get_location(locn.focus_lesson), Has(itm.grawp_lesson_e_item))
    world.set_rule(world.get_location(locn.owls_lesson), Has(itm.focus_lesson_e_item))
    world.set_rule(world.get_location(locn.y5_story_complete), Has(itm.owls_lesson_e_item))
    world.set_rule(world.get_location(locn.specs_lesson), Has(itm.specs_unlock))
    world.set_rule(world.get_location(locn.y6_hogwarts), Has(itm.specs_lesson_e_item))
    world.set_rule(world.get_location(locn.draught_lesson), Has(itm.y6_hogwarts_e_item))
    world.set_rule(world.get_location(locn.vial_lesson), Has(itm.draught_lesson_e_item))
    world.set_rule(world.get_location(locn.agua_lesson), HasAll(itm.vial_lesson_e_item))
    world.set_rule(world.get_location(locn.reducto_lesson), HasAll(itm.agua_lesson_e_item, itm.reducto_unlock,
                                                                   itm.diffindo_lesson_e_item))
    world.set_rule(world.get_location(locn.dumble_lesson), Has(itm.reducto_lesson_e_item))
    world.set_rule(world.get_location(locn.y6_story_complete), Has(itm.dumble_lesson_e_item))


def set_event_logic(world):
    world.set_rule(world.get_location(locn.y5_hogwarts_event), CanReachLocation(locn.y5_hogwarts))
    world.set_rule(world.get_location(locn.dada_lesson_event), CanReachLocation(locn.dada_lesson))
    world.set_rule(world.get_location(locn.thestral_lesson_event), CanReachLocation(locn.thestral_lesson))
    world.set_rule(world.get_location(locn.dueling_lesson_event), CanReachLocation(locn.dueling_lesson))
    world.set_rule(world.get_location(locn.diffindo_lesson_event), CanReachLocation(locn.diffindo_lesson))
    world.set_rule(world.get_location(locn.patroneous_lesson_event), CanReachLocation(locn.patroneous_lesson))
    world.set_rule(world.get_location(locn.grawp_lesson_event), CanReachLocation(locn.grawp_lesson))
    world.set_rule(world.get_location(locn.focus_lesson_event), CanReachLocation(locn.focus_lesson))
    world.set_rule(world.get_location(locn.owls_lesson_event), CanReachLocation(locn.owls_lesson))
    world.set_rule(world.get_location(locn.y5_story_complete_event), CanReachLocation(locn.y5_story_complete))
    world.set_rule(world.get_location(locn.specs_lesson_event), CanReachLocation(locn.specs_lesson))
    world.set_rule(world.get_location(locn.y6_hogwarts_event), CanReachLocation(locn.y6_hogwarts))
    world.set_rule(world.get_location(locn.draught_lesson_event), CanReachLocation(locn.draught_lesson))
    world.set_rule(world.get_location(locn.vial_lesson_event), CanReachLocation(locn.vial_lesson))
    world.set_rule(world.get_location(locn.agua_lesson_event), CanReachLocation(locn.agua_lesson))
    world.set_rule(world.get_location(locn.reducto_lesson_event), CanReachLocation(locn.reducto_lesson))
    world.set_rule(world.get_location(locn.dumble_lesson_event), CanReachLocation(locn.dumble_lesson))
    world.set_rule(world.get_location(locn.y6_story_complete_event), CanReachLocation(locn.y6_story_complete))
    world.set_rule(world.get_location(locn.cafe_lesson_event), CanReachLocation(locn.cafe_lesson))
    if world.options.EndGoal == EndGoal.option_defeat_voldemort:
        world.set_rule(world.get_location("Defeat Voldemort"),
                       Has("UNIQUE_HORCRUX", world.options.NumHorcruxRequired.value) & can_beat_tfitp)
    if world.options.EndGoal == EndGoal.option_levels_beaten:
        world.set_rule(world.get_location("All Required Levels Beaten"),
                       Has("Level Beaten", world.options.NumLevelsRequired.value))
        disabled = set(world.options.DisabledLevels.value)
        for (name, data) in level_beaten_loc_table.items():
            if data.region in disabled or data.region.endswith(" Freeplay") and data.region[:-9] in disabled:
                continue
            event_name = name + " Token"
            event: Location = world.get_location(event_name)
            world.set_rule(event, CanReachLocation(name))


def set_win_con(world):
    if world.options.EndGoal == EndGoal.option_defeat_voldemort:
        world.set_completion_rule(defeat_voldemort)
    # if options.EndGoal == EndGoal.option_the_collector:
    #     world.completion_condition[player] =
    if world.options.EndGoal == EndGoal.option_levels_beaten:
        world.set_completion_rule(Has("All Required Levels Beaten"))


def set_dt_logic(world):
    world.set_rule(world.get_location(locn.dt_beat), can_beat_dt)
    world.set_rule(world.get_location(locn.dt_tw), can_beat_dt)
    world.set_rule(world.get_location(locn.dt_sc), can_get_dt_sc)
    world.set_rule(world.get_location(locn.dt_hc), can_get_dt_hc)
    world.set_rule(world.get_location(locn.dt_sip), can_get_dt_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.arthur_suit_token), can_get_arthur_suit)
        world.set_rule(world.get_location(locn.elphias_token), can_get_elphias)


def set_da_logic(world):
    world.set_rule(world.get_location(locn.da_beat), can_beat_da)
    world.set_rule(world.get_location(locn.da_tw), can_beat_da)
    world.set_rule(world.get_location(locn.da_gc), can_get_da_gc)
    world.set_rule(world.get_location(locn.da_sc), can_get_da_sc)
    world.set_rule(world.get_location(locn.da_rc), can_get_da_rc)
    world.set_rule(world.get_location(locn.da_hc), can_get_da_hc)
    world.set_rule(world.get_location(locn.da_sip), can_get_da_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.cho_winter_token), can_get_cho_winter)
        world.set_rule(world.get_location(locn.herm_scarf_token), can_get_herm_scarf)
        world.set_rule(world.get_location(locn.neville_winter_token), can_get_neville_winter)


def set_foc_logic(world):
    world.set_rule(world.get_location(locn.foc_gc), can_get_foc_gc)
    world.set_rule(world.get_location(locn.foc_hc), can_get_foc_hc)
    world.set_rule(world.get_location(locn.foc_sip), can_get_foc_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.molly_apron_token), can_get_molly_apron)
        world.set_rule(world.get_location(locn.snape_underwear_token), can_get_snape_under)


def set_kd_logic(world):
    world.set_rule(world.get_location(locn.kd_beat), can_beat_kd)
    world.set_rule(world.get_location(locn.kd_tw), can_get_kd_tw)
    world.set_rule(world.get_location(locn.kd_gc), can_get_kd_gc)
    world.set_rule(world.get_location(locn.kd_sc), can_get_kd_sc)
    world.set_rule(world.get_location(locn.kd_rc), can_get_kd_rc)
    world.set_rule(world.get_location(locn.kd_hc), can_get_kd_hc)
    world.set_rule(world.get_location(locn.kd_sip), can_get_kd_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.kreacher_token), can_get_kreacher)
        world.set_rule(world.get_location(locn.sirius_black_token), can_get_sirius)


def set_agv_logic(world):
    world.set_rule(world.get_location(locn.agv_gc), can_get_agv_gc)
    world.set_rule(world.get_location(locn.agv_sc), can_get_agv_sc)
    world.set_rule(world.get_location(locn.agv_rc), can_get_agv_rc)
    world.set_rule(world.get_location(locn.agv_hc), can_get_agv_hc)
    world.set_rule(world.get_location(locn.agv_sip), can_get_agv_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.emmeline_token), can_get_emmeline)
        world.set_rule(world.get_location(locn.neville_token), can_get_neville)
        world.set_rule(world.get_location(locn.prof_umbridge_token), can_get_prof_umbridge)


def set_avt_logic(world):
    world.set_rule(world.get_location(locn.avt_beat), can_beat_avt)
    world.set_rule(world.get_location(locn.avt_tw), can_beat_avt)
    world.set_rule(world.get_location(locn.avt_rc), can_get_avt_rc)
    world.set_rule(world.get_location(locn.avt_hc), can_get_avt_hc)
    world.set_rule(world.get_location(locn.avt_sip), can_get_avt_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.fudge_wizengamot_token), can_get_fudge_wizen)
        world.set_rule(world.get_location(locn.herm_jumper_token), can_get_herm_jumper)
        world.set_rule(world.get_location(locn.lucius_death_eater_token), can_get_lucius_death)


def set_oor_logic(world):
    world.set_rule(world.get_location(locn.oor_beat), can_beat_oor)
    world.set_rule(world.get_location(locn.oor_tw), can_beat_oor)
    world.set_rule(world.get_location(locn.oor_gc), can_get_oor_gc)
    world.set_rule(world.get_location(locn.oor_sc), can_get_oor_sc)
    world.set_rule(world.get_location(locn.oor_rc), can_get_oor_rc)
    world.set_rule(world.get_location(locn.oor_hc), can_get_oor_hc)
    world.set_rule(world.get_location(locn.oor_sip), can_get_oor_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.dumble_cursed_token), can_get_dumble_cursed)
        world.set_rule(world.get_location(locn.milk_man_token), can_get_milk_man)
        world.set_rule(world.get_location(locn.slughorn_pyjamas_token), can_get_slug_pajamas)


def set_jd_logic(world):
    world.set_rule(world.get_location(locn.jd_sc), can_get_jd_sc)
    world.set_rule(world.get_location(locn.jd_rc), can_get_jd_rc)
    world.set_rule(world.get_location(locn.jd_hc), can_get_jd_hc)
    world.set_rule(world.get_location(locn.jd_sip), can_get_jd_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.cormac_suit_token), can_get_cormac_suit)
        world.set_rule(world.get_location(locn.harry_christmas_token), can_get_harry_christ)
        world.set_rule(world.get_location(locn.madam_rosmerta_token), can_get_madam_rosmerta)


def set_ansmc_logic(world):
    world.set_rule(world.get_location(locn.ansmc_beat), can_beat_ansmc)
    world.set_rule(world.get_location(locn.ansmc_gc), can_get_ansmc_gc)
    world.set_rule(world.get_location(locn.ansmc_sc), can_get_ansmc_sc)
    world.set_rule(world.get_location(locn.ansmc_hc), can_get_ansmc_hc)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.bill_wedding_token), can_get_bill_wedding)


def set_lh_logic(world):
    world.set_rule(world.get_location(locn.lh_beat), can_beat_lh)
    world.set_rule(world.get_location(locn.lh_tw), can_beat_lh)
    world.set_rule(world.get_location(locn.lh_gc), can_get_lh_gc)
    world.set_rule(world.get_location(locn.lh_sc), can_get_lh_sc)
    world.set_rule(world.get_location(locn.lh_rc), can_get_lh_rc)
    world.set_rule(world.get_location(locn.lh_hc), can_get_lh_hc)
    world.set_rule(world.get_location(locn.lh_sip), can_get_lh_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.draco_suit_token), can_get_draco_suit)
        world.set_rule(world.get_location(locn.ginny_token), can_get_ginny)
        world.set_rule(world.get_location(locn.prof_slughorn_token), can_get_prof_slug)


def set_ff_logic(world):
    world.set_rule(world.get_location(locn.ff_beat), can_beat_ff)
    world.set_rule(world.get_location(locn.ff_tw), can_beat_ff)
    world.set_rule(world.get_location(locn.ff_sc), can_get_ff_sc)
    world.set_rule(world.get_location(locn.ff_rc), can_get_ff_rc)
    world.set_rule(world.get_location(locn.ff_hc), can_get_ff_hc)
    world.set_rule(world.get_location(locn.ff_sip), can_get_ff_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.hagrid_token), can_get_hagrid)
        world.set_rule(world.get_location(locn.prof_sprout_token), can_get_prof_sprout)


def set_thath_logic(world):
    world.set_rule(world.get_location(locn.thath_beat), can_beat_thath)
    world.set_rule(world.get_location(locn.thath_tw), can_beat_thath)
    world.set_rule(world.get_location(locn.thath_sc), can_get_thath_sc)
    world.set_rule(world.get_location(locn.thath_rc), can_get_thath_rc)
    world.set_rule(world.get_location(locn.thath_hc), can_get_thath_hc)
    world.set_rule(world.get_location(locn.thath_sip), can_get_thath_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.hagrid_wed_token), can_get_hagrid_wed)
        world.set_rule(world.get_location(locn.prof_dumble_token), can_get_prof_dumble)
        world.set_rule(world.get_location(locn.tr_orphanage_token), can_get_tr_orphan)


def set_tsh_logic(world):
    world.set_rule(world.get_location(locn.delum_lesson), can_get_delum)
    world.set_rule(world.get_location(locn.poly_purch), can_get_polyjuice)
    world.set_rule(world.get_location(locn.tsh_sc), can_get_tsh_sc)
    world.set_rule(world.get_location(locn.tsh_rc), can_get_tsh_rc)
    world.set_rule(world.get_location(locn.tsh_sip), can_get_tsh_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.madeye_token), can_get_mad_eye)
        world.set_rule(world.get_location(locn.ron_wedding_token), can_get_ron_wed)


def set_mim_logic(world):
    world.set_rule(world.get_location(locn.mim_beat), can_beat_mim)
    world.set_rule(world.get_location(locn.mim_tw), can_beat_mim)
    world.set_rule(world.get_location(locn.mim_gc), can_get_mim_gc)
    world.set_rule(world.get_location(locn.mim_sc), can_get_mim_sc)
    world.set_rule(world.get_location(locn.mim_rc), can_get_mim_rc)
    world.set_rule(world.get_location(locn.mim_hc), can_get_mim_hc)
    world.set_rule(world.get_location(locn.mim_sip), can_get_mim_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.ron_reg_cattermole_token), can_get_ron_reg)


def set_igd_logic(world):
    world.set_rule(world.get_location(locn.igd_beat), can_beat_igd)
    world.set_rule(world.get_location(locn.igd_tw), can_beat_igd)
    world.set_rule(world.get_location(locn.igd_gc), can_get_igd_gc)
    world.set_rule(world.get_location(locn.igd_sc), can_get_igd_sc)
    world.set_rule(world.get_location(locn.igd_rc), can_get_igd_rc)
    world.set_rule(world.get_location(locn.igd_sip), can_get_igd_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.bathilda_snake_token), can_get_bathilda_snake)
        world.set_rule(world.get_location(locn.harry_godric_token), can_get_harry_god_hollow)
        world.set_rule(world.get_location(locn.lily_token), can_get_lily)


def set_sal_logic(world):
    world.set_rule(world.get_location(locn.sal_beat), can_beat_sal)
    world.set_rule(world.get_location(locn.sal_tw), can_beat_sal)
    world.set_rule(world.get_location(locn.sal_gc), can_get_sal_gc)
    world.set_rule(world.get_location(locn.sal_sc), can_get_sal_sc)
    world.set_rule(world.get_location(locn.sal_rc), can_get_sal_rc)
    world.set_rule(world.get_location(locn.sal_sip), can_get_sal_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.herm_grey_coat_token), can_get_herm_gray_coat)


def set_ll_logic(world):
    world.set_rule(world.get_location(locn.ll_beat), can_beat_ll)
    world.set_rule(world.get_location(locn.ll_tw), can_beat_ll)
    world.set_rule(world.get_location(locn.ll_rc), can_get_ll_rc)
    world.set_rule(world.get_location(locn.ll_hc), can_get_ll_hc)
    world.set_rule(world.get_location(locn.ll_sip), can_get_ll_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.skeleton_token), can_get_skeleton)
        world.set_rule(world.get_location(locn.xeno_luna_token), can_get_xeno_luna)


def set_dob_logic(world):
    world.set_rule(world.get_location(locn.dob_gc), can_get_dob_gc)
    world.set_rule(world.get_location(locn.dob_rc), can_get_dob_rc)
    world.set_rule(world.get_location(locn.dob_sip), can_get_dob_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.dobby_token), can_get_dobby)
        world.set_rule(world.get_location(locn.wormtail_token), can_get_wormtail)
        world.set_rule(world.get_location(locn.ollivander_token), can_get_olivander)


def set_ttd_logic(world):
    world.set_rule(world.get_location(locn.ttd_beat), can_beat_ttd)
    world.set_rule(world.get_location(locn.ttd_tw), can_beat_ttd)
    world.set_rule(world.get_location(locn.ttd_gc), can_get_ttd_gc)
    world.set_rule(world.get_location(locn.ttd_sc), can_get_ttd_sc)
    world.set_rule(world.get_location(locn.ttd_rc), can_get_ttd_rc)
    world.set_rule(world.get_location(locn.ttd_hc), can_get_ttd_hc)
    world.set_rule(world.get_location(locn.ttd_sip), can_get_ttd_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.bogrod_token), can_get_bogrod)
        world.set_rule(world.get_location(locn.griphook_token), can_get_griphook)
        world.set_rule(world.get_location(locn.herm_gringotts_token), can_get_herm_gringotts)


def set_bts_logic(world):
    world.set_rule(world.get_location(locn.bts_sc), can_get_bts_sc)
    world.set_rule(world.get_location(locn.bts_hc), can_get_bts_hc)
    world.set_rule(world.get_location(locn.bts_sip), can_get_bts_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.aberforth_token), can_get_aberforth)
        world.set_rule(world.get_location(locn.alecto_token), can_get_alecto)
        world.set_rule(world.get_location(locn.amycus_token), can_get_amycus)


def set_bb_logic(world):
    world.set_rule(world.get_location(locn.bb_beat), can_beat_bb)
    world.set_rule(world.get_location(locn.bb_tw), can_beat_bb)
    world.set_rule(world.get_location(locn.bb_gc), can_get_bb_gc)
    world.set_rule(world.get_location(locn.bb_sc), can_get_bb_sc)
    world.set_rule(world.get_location(locn.bb_rc), can_get_bb_rc)
    world.set_rule(world.get_location(locn.bb_hc), can_get_bb_hc)
    world.set_rule(world.get_location(locn.bb_sip), can_get_bb_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.neville_cardigan_token), can_get_neville_cardigan)
        world.set_rule(world.get_location(locn.seamus_token), can_get_seamus)


def set_fiend_logic(world):
    world.set_rule(world.get_location(locn.fiend_beat), can_beat_fiend)
    world.set_rule(world.get_location(locn.fiend_tw), can_beat_fiend)
    world.set_rule(world.get_location(locn.fiend_gc), can_get_fiend_gc)
    world.set_rule(world.get_location(locn.fiend_sc), can_get_fiend_sc)
    world.set_rule(world.get_location(locn.fiend_rc), can_get_fiend_rc)
    world.set_rule(world.get_location(locn.fiend_hc), can_get_fiend_hc)
    world.set_rule(world.get_location(locn.fiend_sip), can_get_fiend_sip)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.goyle_token), can_get_goyle)
        world.set_rule(world.get_location(locn.harry_brown_jacket_token), can_get_harry_brown_jacket)
        world.set_rule(world.get_location(locn.tom_riddle_token), can_get_tom_riddle)


def set_st_logic(world):
    world.set_rule(world.get_location(locn.st_beat), can_beat_st)
    world.set_rule(world.get_location(locn.st_tw), can_beat_st)
    world.set_rule(world.get_location(locn.st_gc), can_get_st_gc)
    world.set_rule(world.get_location(locn.st_sc), can_get_st_sc)
    world.set_rule(world.get_location(locn.st_rc), can_get_st_rc)
    world.set_rule(world.get_location(locn.st_hc), can_get_st_hc)
    if world.options.ShuffleCharacterTokens != 2:
        world.set_rule(world.get_location(locn.death_eater_token), can_get_death_eater)
        world.set_rule(world.get_location(locn.fenrir_token), can_get_fenrir)
        world.set_rule(world.get_location(locn.prof_snape_token), can_get_prof_snape)


def set_tfitp_logic(world):
    world.set_rule(world.get_location(locn.tfitp_beat), can_beat_tfitp)
    world.set_rule(world.get_location(locn.tfitp_tw), can_beat_tfitp)
    world.set_rule(world.get_location(locn.tfitp_sc), can_get_tfitp_sc)
    world.set_rule(world.get_location(locn.tfitp_rc), can_get_tfitp_rc)
    world.set_rule(world.get_location(locn.tfitp_sip), can_get_tfitp_sip)


def set_hub_collect_logic(world):
    world.set_rule(world.get_location(locn.knock_sip), can_get_knock_sip)
    world.set_rule(world.get_location(locn.www_gb), can_get_www_gb)
    world.set_rule(world.get_location(locn.cafe_gb), can_get_cafe_gb)
    world.set_rule(world.get_location(locn.cafe_sip), can_get_cafe_sip)
    world.set_rule(world.get_location(locn.tent_gb), can_get_tent_gb)
    world.set_rule(world.get_location(locn.tent_sip), can_get_tent_sip)
    world.set_rule(world.get_location(locn.wild_gb), can_get_wild_gb)
    world.set_rule(world.get_location(locn.wild_sip), can_get_wild_sip)
    world.set_rule(world.get_location(locn.kcs_gb), can_get_kcs_gb)
    world.set_rule(world.get_location(locn.hogstat_sip), can_get_hogstat_sip)
    world.set_rule(world.get_location(locn.hogspath_gb), can_get_hogspath_gb)
    world.set_rule(world.get_location(locn.hogspath_sip), can_get_hogspath_sip)
    world.set_rule(world.get_location(locn.hogs_gb), can_get_hogs_gb)
    world.set_rule(world.get_location(locn.hogs_sip), can_get_hogs_sip)
    world.set_rule(world.get_location(locn.hogs_rb), can_get_hogs_rb)
    world.set_rule(world.get_location(locn.hogwpath_gb), can_get_hogwpath_gb)
    world.set_rule(world.get_location(locn.hogwpath_sip), can_get_hogwpath_sip)
    world.set_rule(world.get_location(locn.quad_gb), can_get_quad_gb)
    world.set_rule(world.get_location(locn.quad_sip), can_get_quad_sip)
    world.set_rule(world.get_location(locn.tg_gb), can_get_tg_gb)
    world.set_rule(world.get_location(locn.herb_gb), can_get_herb_gb)
    world.set_rule(world.get_location(locn.thest_gb), can_get_thest_gb)
    world.set_rule(world.get_location(locn.thest_sip), can_get_thest_sip)
    world.set_rule(world.get_location(locn.lake_sip), can_get_lake_sip)
    world.set_rule(world.get_location(locn.foyer_gb), can_get_foyer_gb)
    world.set_rule(world.get_location(locn.foyer_sip), can_get_foyer_sip)
    world.set_rule(world.get_location(locn.stair_gb), can_get_stair_gb)
    world.set_rule(world.get_location(locn.stair_sip), can_get_stair_sip)
    world.set_rule(world.get_location(locn.dormlob_gb), can_get_dorm_lobby_gb)
    world.set_rule(world.get_location(locn.dormlob_sip), can_get_dorm_lobby_sip)
    world.set_rule(world.get_location(locn.gryf_gb), can_get_gryf_common_gb)
    world.set_rule(world.get_location(locn.gryf_sip), can_get_gryf_common_sip)
    world.set_rule(world.get_location(locn.raven_sip), can_get_raven_tower_sip)
    world.set_rule(world.get_location(locn.lib_sip), can_get_lib_sip)
    world.set_rule(world.get_location(locn.lib_gb), can_get_lib_gb)
    world.set_rule(world.get_location(locn.ghl_gb), can_get_ghl_gb)
    world.set_rule(world.get_location(locn.ghl_sip), can_get_ghl_sip)
    world.set_rule(world.get_location(locn.wc_gb), can_get_wc_gb)
    world.set_rule(world.get_location(locn.wc_sip), can_get_wc_sip)
    world.set_rule(world.get_location(locn.wcs_sip), can_get_wcs_sip)
    world.set_rule(world.get_location(locn.gh_sip), can_get_gh_sip)
    world.set_rule(world.get_location(locn.ror_gb), can_get_ror_gb)
    world.set_rule(world.get_location(locn.cl_gb), can_get_cl_gb)
    world.set_rule(world.get_location(locn.cl_sip), can_get_cl_sip)
    world.set_rule(world.get_location(locn.y5c_gb), can_get_y5c_gb)
    world.set_rule(world.get_location(locn.y5c_sip), can_get_y5c_sip)
    world.set_rule(world.get_location(locn.y6c_gb), can_get_y6c_gb)
    world.set_rule(world.get_location(locn.y6c_sip), can_get_y6c_sip)
    world.set_rule(world.get_location(locn.dada_gb), can_get_dada_gb)
    world.set_rule(world.get_location(locn.dada_sip), can_get_dada_sip)
    world.set_rule(world.get_location(locn.pot_gb), can_get_pot_gb)
    world.set_rule(world.get_location(locn.pot_sip), can_get_pot_sip)
    world.set_rule(world.get_location(locn.divc_gb), can_get_divc_gb)
    world.set_rule(world.get_location(locn.divc_sip), can_get_divc_sip)
    world.set_rule(world.get_location(locn.ast_sip), can_get_ast_sip)


def set_hub_rb_logic(world):
    world.set_rule(world.get_location(locn.kcs_rb), can_get_kcs_rb)
    world.set_rule(world.get_location(locn.hogstat_rb), can_get_hogstat_rb)
    world.set_rule(world.get_location(locn.hogspath_rb), can_get_hogspath_rb)
    world.set_rule(world.get_location(locn.hogwpath_rb), can_get_hogwpath_rb)
    world.set_rule(world.get_location(locn.quad_rb), can_get_quad_rb)
    world.set_rule(world.get_location(locn.ground_rb), can_get_grounds_rb)
    world.set_rule(world.get_location(locn.thest_rb), can_get_thest_rb)
    world.set_rule(world.get_location(locn.lake_rb), can_get_lake_rb)
    world.set_rule(world.get_location(locn.lib_rb), can_get_lib_rb)
    world.set_rule(world.get_location(locn.ghl_rb), can_get_ghl_rb)
    world.set_rule(world.get_location(locn.wc_rb), can_get_wc_rb)
    world.set_rule(world.get_location(locn.gh_rb), can_get_gh_rb)
    world.set_rule(world.get_location(locn.ror_rb), can_get_ror_rb)
    world.set_rule(world.get_location(locn.dada_rb), can_get_dada_rb)
    world.set_rule(world.get_location(locn.divc_rb), can_get_divc_rb)
    world.set_rule(world.get_location(locn.div_rb), can_get_div_rb)
    world.set_rule(world.get_location(locn.ast_rb), can_get_ast_rb)


def set_hub_token_logic(world):
    world.set_rule(world.get_location(locn.anthony_token), can_get_anthony_token)
    world.set_rule(world.get_location(locn.argus_token), can_get_filch_token)
    world.set_rule(world.get_location(locn.arthur_cardigan_token), can_get_arthur_cardigan)
    world.set_rule(world.get_location(locn.arthur_torn_suit_token), can_get_arthur_torn_suit)
    world.set_rule(world.get_location(locn.bellatrix_azka_token), can_get_bella_azka)
    world.set_rule(world.get_location(locn.blaise_token), can_get_blaise)
    world.set_rule(world.get_location(locn.charity_token), can_get_charity)
    world.set_rule(world.get_location(locn.charlie_token), can_get_charlie)
    world.set_rule(world.get_location(locn.cho_token), can_get_cho)
    world.set_rule(world.get_location(locn.crabbe_jumper_token), can_get_crabbe_jumper)
    world.set_rule(world.get_location(locn.dean_winter_token), can_get_dean_winter)
    world.set_rule(world.get_location(locn.dolohov_token), can_get_dolohov)
    world.set_rule(world.get_location(locn.dolohov_workman_token), can_get_dolohov_work)
    world.set_rule(world.get_location(locn.draco_token), can_get_draco)
    world.set_rule(world.get_location(locn.dragomir_token), can_get_dragomir)
    world.set_rule(world.get_location(locn.dudley_token), can_get_dudley)
    world.set_rule(world.get_location(locn.dudley_shirt_token), can_get_dudley_shirt)
    world.set_rule(world.get_location(locn.dumble_young_token), can_get_dumble_young)
    world.set_rule(world.get_location(locn.fat_lady_token), can_get_fat_lady)
    world.set_rule(world.get_location(locn.fleur_token), can_get_fleur)
    world.set_rule(world.get_location(locn.fred_owls_token), can_get_fred_owls)
    world.set_rule(world.get_location(locn.fred_pyjamas_token), can_get_fred_pyjamas)
    world.set_rule(world.get_location(locn.fred_token), can_get_fred)
    world.set_rule(world.get_location(locn.george_owls_token), can_get_george_owls)
    world.set_rule(world.get_location(locn.george_pyjamas_token), can_get_george_pyjamas)
    world.set_rule(world.get_location(locn.george_token), can_get_george)
    world.set_rule(world.get_location(locn.ginny_pyjamas_token), can_get_ginny_pyjamas)
    world.set_rule(world.get_location(locn.goyle_jumper_token), can_get_goyle_jumper)
    world.set_rule(world.get_location(locn.gregorovitch_token), can_get_gregorovitch)
    world.set_rule(world.get_location(locn.hannah_token), can_get_hannah)
    world.set_rule(world.get_location(locn.harry_pyjamas_token), can_get_harry_pyjamas)
    world.set_rule(world.get_location(locn.herm_ball_token), can_get_herm_ball_gown)
    world.set_rule(world.get_location(locn.herm_cardigan_token), can_get_herm_cardigan)
    world.set_rule(world.get_location(locn.katie_token), can_get_katie_bell)
    world.set_rule(world.get_location(locn.lavender_token), can_get_lavender)
    world.set_rule(world.get_location(locn.lily_young_casual_token), can_get_lily_casual)
    world.set_rule(world.get_location(locn.lucius_token), can_get_lucius)
    world.set_rule(world.get_location(locn.luna_blue_jumper_token), can_get_luna_blue)
    world.set_rule(world.get_location(locn.luna_overalls_token), can_get_luna_overalls)
    world.set_rule(world.get_location(locn.luna_pink_dress_token), can_get_luna_pink)
    world.set_rule(world.get_location(locn.luna_token), can_get_luna)
    world.set_rule(world.get_location(locn.madam_pince_token), can_get_madam_pince)
    world.set_rule(world.get_location(locn.mafalda_token), can_get_mafalda)
    world.set_rule(world.get_location(locn.belby_token), can_get_belby)
    world.set_rule(world.get_location(locn.mary_cattermole_token), can_get_mary)
    world.set_rule(world.get_location(locn.mcgon_black_token), can_get_mcgonagall_black)
    world.set_rule(world.get_location(locn.mcgon_pyjamas_token), can_get_mcgonagall_pyjamas)
    world.set_rule(world.get_location(locn.michael_token), can_get_michael)
    world.set_rule(world.get_location(locn.ministry_guard_token), can_get_ministry_guard)
    world.set_rule(world.get_location(locn.myrtle_token), can_get_myrtle)
    world.set_rule(world.get_location(locn.black_token), can_get_mrs_black)
    world.set_rule(world.get_location(locn.cole_token), can_get_mrs_cole)
    world.set_rule(world.get_location(locn.narcissa_token), can_get_narcissa)
    world.set_rule(world.get_location(locn.neville_tank_top_token), can_get_neville_tank)
    world.set_rule(world.get_location(locn.neville_waiter_token), can_get_neville_waiter)
    world.set_rule(world.get_location(locn.padma_patil_token), can_get_padma)
    world.set_rule(world.get_location(locn.petunia_green_coat_token), can_get_petunia_green)
    world.set_rule(world.get_location(locn.petunia_token), can_get_petunia)
    world.set_rule(world.get_location(locn.pius_token), can_get_pius)
    world.set_rule(world.get_location(locn.prof_binns_token), can_get_prof_binns)
    world.set_rule(world.get_location(locn.prof_flit_token), can_get_prof_flitwick)
    world.set_rule(world.get_location(locn.prof_grubbly_token), can_get_prof_grub)
    world.set_rule(world.get_location(locn.prof_mcgon_token), can_get_prof_mcgonagall)
    world.set_rule(world.get_location(locn.prof_trelawney_token), can_get_prof_trelawney)
    world.set_rule(world.get_location(locn.reg_token), can_get_reg_catter)
    world.set_rule(world.get_location(locn.regulus_token), can_get_regulus)
    world.set_rule(world.get_location(locn.rita_skeeter_token), can_get_rita)
    world.set_rule(world.get_location(locn.ron_blue_pyjamas_token), can_get_ron_blue)
    world.set_rule(world.get_location(locn.ron_green_shirt_token), can_get_ron_green)
    world.set_rule(world.get_location(locn.ron_red_sweater_token), can_get_ron_red_sweater)
    world.set_rule(world.get_location(locn.scrimgeour_token), can_get_rufus)
    world.set_rule(world.get_location(locn.seamus_winter_token), can_get_seamus_winter)
    world.set_rule(world.get_location(locn.scabior_token), can_get_scabior)
    world.set_rule(world.get_location(locn.slughorn_young_token), can_get_slug_young)
    world.set_rule(world.get_location(locn.snatcher_token), can_get_snatcher)
    world.set_rule(world.get_location(locn.susan_token), can_get_susan_bones)
    world.set_rule(world.get_location(locn.rowle_token), can_get_rowle)
    world.set_rule(world.get_location(locn.umbridge_wizengamot_token), can_get_umbridge_wizen)
    world.set_rule(world.get_location(locn.vernon_token), can_get_vernon)
    world.set_rule(world.get_location(locn.waitress_luchino_token), can_get_waitress_luchino)
    world.set_rule(world.get_location(locn.yaxley_token), can_get_yaxley)


def set_char_purch_logic(world):
    world.set_rule(world.get_location(locn.hagrid_purch), can_purch_char(locn.hagrid_purch))
    world.set_rule(world.get_location(locn.fang_purch), can_purch_char(locn.fang_purch))
    world.set_rule(world.get_location(locn.hagrid_wed_purch), can_purch_char(locn.hagrid_wed_purch))
    world.set_rule(world.get_location(locn.prof_flit_purch), can_purch_char(locn.prof_flit_purch))
    world.set_rule(world.get_location(locn.madam_malk_purch), can_purch_char(locn.madam_malk_purch))
    world.set_rule(world.get_location(locn.dobby_purch), can_purch_char(locn.dobby_purch))
    world.set_rule(world.get_location(locn.kreacher_purch), can_purch_char(locn.kreacher_purch))
    world.set_rule(world.get_location(locn.tr_orphanage_purch), can_purch_char(locn.tr_orphanage_purch))
    world.set_rule(world.get_location(locn.bogrod_purch), can_purch_char(locn.bogrod_purch))
    world.set_rule(world.get_location(locn.mund_fletch_purch), can_purch_char(locn.mund_fletch_purch))
    world.set_rule(world.get_location(locn.griphook_purch), can_purch_char(locn.griphook_purch))
    world.set_rule(world.get_location(locn.prof_mcgon_purch), can_purch_char(locn.prof_mcgon_purch))
    world.set_rule(world.get_location(locn.madam_pince_purch), can_purch_char(locn.madam_pince_purch))
    world.set_rule(world.get_location(locn.prof_sprout_purch), can_purch_char(locn.prof_sprout_purch))
    world.set_rule(world.get_location(locn.madam_pomfrey_purch), can_purch_char(locn.madam_pomfrey_purch))
    world.set_rule(world.get_location(locn.prof_trelawney_purch), can_purch_char(locn.prof_trelawney_purch))
    world.set_rule(world.get_location(locn.madam_rosmerta_purch), can_purch_char(locn.madam_rosmerta_purch))
    world.set_rule(world.get_location(locn.fat_friar_purch), can_purch_char(locn.fat_friar_purch))
    world.set_rule(world.get_location(locn.grey_lady_purch), can_purch_char(locn.grey_lady_purch))
    world.set_rule(world.get_location(locn.fat_lady_purch), can_purch_char(locn.fat_lady_purch))
    world.set_rule(world.get_location(locn.herm_ball_purch), can_purch_char(locn.herm_ball_purch))
    world.set_rule(world.get_location(locn.bellatrix_purch), can_purch_char(locn.bellatrix_purch))
    world.set_rule(world.get_location(locn.emmeline_purch), can_purch_char(locn.emmeline_purch))
    world.set_rule(world.get_location(locn.narcissa_purch), can_purch_char(locn.narcissa_purch))
    world.set_rule(world.get_location(locn.mcgon_pyjamas_purch), can_purch_char(locn.mcgon_pyjamas_purch))
    world.set_rule(world.get_location(locn.mary_cattermole_purch), can_purch_char(locn.mary_cattermole_purch))
    world.set_rule(world.get_location(locn.mcgon_black_purch), can_purch_char(locn.mcgon_black_purch))
    world.set_rule(world.get_location(locn.herm_gringotts_purch), can_purch_char(locn.herm_gringotts_purch))
    world.set_rule(world.get_location(locn.prof_grubbly_purch), can_purch_char(locn.prof_grubbly_purch))
    world.set_rule(world.get_location(locn.bellatrix_azka_purch), can_purch_char(locn.bellatrix_azka_purch))
    world.set_rule(world.get_location(locn.death_eater_purch), can_purch_char(locn.death_eater_purch))
    world.set_rule(world.get_location(locn.dudley_grey_purch), can_purch_char(locn.dudley_grey_purch))
    world.set_rule(world.get_location(locn.prof_dumble_purch), can_purch_char(locn.prof_dumble_purch))
    world.set_rule(world.get_location(locn.argus_purch), can_purch_char(locn.argus_purch))
    world.set_rule(world.get_location(locn.madam_hooch_purch), can_purch_char(locn.madam_hooch_purch))
    world.set_rule(world.get_location(locn.crabbe_purch), can_purch_char(locn.crabbe_purch))
    world.set_rule(world.get_location(locn.goyle_purch), can_purch_char(locn.goyle_purch))
    world.set_rule(world.get_location(locn.ginny_purch), can_purch_char(locn.ginny_purch))
    world.set_rule(world.get_location(locn.arthur_purch), can_purch_char(locn.arthur_purch))
    world.set_rule(world.get_location(locn.katie_purch), can_purch_char(locn.katie_purch))
    world.set_rule(world.get_location(locn.lily_purch), can_purch_char(locn.lily_purch))
    world.set_rule(world.get_location(locn.bloody_baron_purch), can_purch_char(locn.bloody_baron_purch))
    world.set_rule(world.get_location(locn.fudge_purch), can_purch_char(locn.fudge_purch))
    world.set_rule(world.get_location(locn.justin_purch), can_purch_char(locn.justin_purch))
    world.set_rule(world.get_location(locn.cho_purch), can_purch_char(locn.cho_purch))
    world.set_rule(world.get_location(locn.dean_purch), can_purch_char(locn.dean_purch))
    world.set_rule(world.get_location(locn.draco_purch), can_purch_char(locn.draco_purch))
    world.set_rule(world.get_location(locn.lucius_purch), can_purch_char(locn.lucius_purch))
    world.set_rule(world.get_location(locn.draco_suit_purch), can_purch_char(locn.draco_suit_purch))
    world.set_rule(world.get_location(locn.harry_pyjamas_purch), can_purch_char(locn.harry_pyjamas_purch))
    world.set_rule(world.get_location(locn.myrtle_purch), can_purch_char(locn.myrtle_purch))
    world.set_rule(world.get_location(locn.james_ghost_purch), can_purch_char(locn.james_ghost_purch))
    world.set_rule(world.get_location(locn.madeye_purch), can_purch_char(locn.madeye_purch))
    world.set_rule(world.get_location(locn.hannah_purch), can_purch_char(locn.hannah_purch))
    world.set_rule(world.get_location(locn.kingsley_purch), can_purch_char(locn.kingsley_purch))
    world.set_rule(world.get_location(locn.aberforth_purch), can_purch_char(locn.aberforth_purch))
    world.set_rule(world.get_location(locn.runcorn_purch), can_purch_char(locn.runcorn_purch))
    world.set_rule(world.get_location(locn.alecto_purch), can_purch_char(locn.alecto_purch))
    world.set_rule(world.get_location(locn.amycus_purch), can_purch_char(locn.amycus_purch))
    world.set_rule(world.get_location(locn.anthony_purch), can_purch_char(locn.anthony_purch))
    world.set_rule(world.get_location(locn.bathilda_snake_purch), can_purch_char(locn.bathilda_snake_purch))
    world.set_rule(world.get_location(locn.blaise_purch), can_purch_char(locn.blaise_purch))
    world.set_rule(world.get_location(locn.charity_purch), can_purch_char(locn.charity_purch))
    world.set_rule(world.get_location(locn.charlie_purch), can_purch_char(locn.charlie_purch))
    world.set_rule(world.get_location(locn.cormac_purch), can_purch_char(locn.cormac_purch))
    world.set_rule(world.get_location(locn.dedalus_purch), can_purch_char(locn.dedalus_purch))
    world.set_rule(world.get_location(locn.dirk_purch), can_purch_char(locn.dirk_purch))
    world.set_rule(world.get_location(locn.dolohov_purch), can_purch_char(locn.dolohov_purch))
    world.set_rule(world.get_location(locn.dragomir_purch), can_purch_char(locn.dragomir_purch))
    world.set_rule(world.get_location(locn.elphias_purch), can_purch_char(locn.elphias_purch))
    world.set_rule(world.get_location(locn.fenrir_purch), can_purch_char(locn.fenrir_purch))
    world.set_rule(world.get_location(locn.grindel_young_purch), can_purch_char(locn.grindel_young_purch))
    world.set_rule(world.get_location(locn.grindel_old_purch), can_purch_char(locn.grindel_old_purch))
    world.set_rule(world.get_location(locn.gregorovitch_purch), can_purch_char(locn.gregorovitch_purch))
    world.set_rule(world.get_location(locn.hestia_purch), can_purch_char(locn.hestia_purch))
    world.set_rule(world.get_location(locn.prof_slughorn_purch), can_purch_char(locn.prof_slughorn_purch))
    world.set_rule(world.get_location(locn.james_young_purch), can_purch_char(locn.james_young_purch))
    world.set_rule(world.get_location(locn.lavender_purch), can_purch_char(locn.lavender_purch))
    world.set_rule(world.get_location(locn.mafalda_purch), can_purch_char(locn.mafalda_purch))
    world.set_rule(world.get_location(locn.belby_purch), can_purch_char(locn.belby_purch))
    world.set_rule(world.get_location(locn.luna_purple_coat_purch), can_purch_char(locn.luna_purple_coat_purch))
    world.set_rule(world.get_location(locn.herm_grey_coat_purch), can_purch_char(locn.herm_grey_coat_purch))
    world.set_rule(world.get_location(locn.harry_godric_purch), can_purch_char(locn.harry_godric_purch))
    world.set_rule(world.get_location(locn.prof_umbridge_purch), can_purch_char(locn.prof_umbridge_purch))
    world.set_rule(world.get_location(locn.fred_purch), can_purch_char(locn.fred_purch))
    world.set_rule(world.get_location(locn.george_purch), can_purch_char(locn.george_purch))
    world.set_rule(world.get_location(locn.molly_apron_purch), can_purch_char(locn.molly_apron_purch))
    world.set_rule(world.get_location(locn.crabbe_jumper_purch), can_purch_char(locn.crabbe_jumper_purch))
    world.set_rule(world.get_location(locn.draco_sweater_purch), can_purch_char(locn.draco_sweater_purch))
    world.set_rule(world.get_location(locn.goyle_jumper_purch), can_purch_char(locn.goyle_jumper_purch))
    world.set_rule(world.get_location(locn.milk_man_purch), can_purch_char(locn.milk_man_purch))
    world.set_rule(world.get_location(locn.twin_2_purch), can_purch_char(locn.twin_2_purch))
    world.set_rule(world.get_location(locn.herm_mafalda_purch), can_purch_char(locn.herm_mafalda_purch))
    world.set_rule(world.get_location(locn.ministry_guard_purch), can_purch_char(locn.ministry_guard_purch))
    world.set_rule(world.get_location(locn.harry_winter_purch), can_purch_char(locn.harry_winter_purch))
    world.set_rule(world.get_location(locn.arthur_torn_suit_purch), can_purch_char(locn.arthur_torn_suit_purch))
    world.set_rule(world.get_location(locn.fred_winter_purch), can_purch_char(locn.fred_winter_purch))
    world.set_rule(world.get_location(locn.cho_winter_purch), can_purch_char(locn.cho_winter_purch))
    world.set_rule(world.get_location(locn.george_winter_purch), can_purch_char(locn.george_winter_purch))
    world.set_rule(world.get_location(locn.herm_scarf_purch), can_purch_char(locn.herm_scarf_purch))
    world.set_rule(world.get_location(locn.luna_blue_jumper_purch), can_purch_char(locn.luna_blue_jumper_purch))
    world.set_rule(world.get_location(locn.fred_owls_purch), can_purch_char(locn.fred_owls_purch))
    world.set_rule(world.get_location(locn.fred_pyjamas_purch), can_purch_char(locn.fred_pyjamas_purch))
    world.set_rule(world.get_location(locn.george_owls_purch), can_purch_char(locn.george_owls_purch))
    world.set_rule(world.get_location(locn.george_pyjamas_purch), can_purch_char(locn.george_pyjamas_purch))
    world.set_rule(world.get_location(locn.herm_jumper_purch), can_purch_char(locn.herm_jumper_purch))
    world.set_rule(world.get_location(locn.fudge_wizengamot_purch), can_purch_char(locn.fudge_wizengamot_purch))
    world.set_rule(world.get_location(locn.dudley_purch), can_purch_char(locn.dudley_purch))
    world.set_rule(world.get_location(locn.gang_mem_purch), can_purch_char(locn.gang_mem_purch))
    world.set_rule(world.get_location(locn.harry_albert_runcorn_purch), can_purch_char(locn.harry_albert_runcorn_purch))
    world.set_rule(world.get_location(locn.harry_brown_jacket_purch), can_purch_char(locn.harry_brown_jacket_purch))
    world.set_rule(world.get_location(locn.dumble_cursed_purch), can_purch_char(locn.dumble_cursed_purch))
    world.set_rule(world.get_location(locn.lucius_death_eater_purch), can_purch_char(locn.lucius_death_eater_purch))
    world.set_rule(world.get_location(locn.luna_purch), can_purch_char(locn.luna_purch))
    world.set_rule(world.get_location(locn.umbridge_wizengamot_purch), can_purch_char(locn.umbridge_wizengamot_purch))
    world.set_rule(world.get_location(locn.dolohov_workman_purch), can_purch_char(locn.dolohov_workman_purch))
    world.set_rule(world.get_location(locn.michael_purch), can_purch_char(locn.michael_purch))
    world.set_rule(world.get_location(locn.dean_winter_purch), can_purch_char(locn.dean_winter_purch))
    world.set_rule(world.get_location(locn.arthur_cardigan_purch), can_purch_char(locn.arthur_cardigan_purch))
    world.set_rule(world.get_location(locn.luna_pink_dress_purch), can_purch_char(locn.luna_pink_dress_purch))
    world.set_rule(world.get_location(locn.marietta_purch), can_purch_char(locn.marietta_purch))
    world.set_rule(world.get_location(locn.dumble_young_purch), can_purch_char(locn.dumble_young_purch))
    world.set_rule(world.get_location(locn.slughorn_young_purch), can_purch_char(locn.slughorn_young_purch))
    world.set_rule(world.get_location(locn.slughorn_pyjamas_purch), can_purch_char(locn.slughorn_pyjamas_purch))
    world.set_rule(world.get_location(locn.lily_young_casual_purch), can_purch_char(locn.lily_young_casual_purch))
    world.set_rule(world.get_location(locn.ginny_dress_purch), can_purch_char(locn.ginny_dress_purch))
    world.set_rule(world.get_location(locn.ginny_pyjamas_purch), can_purch_char(locn.ginny_pyjamas_purch))
    world.set_rule(world.get_location(locn.blaise_black_shirt_purch), can_purch_char(locn.blaise_black_shirt_purch))
    world.set_rule(world.get_location(locn.cormac_suit_purch), can_purch_char(locn.cormac_suit_purch))
    world.set_rule(world.get_location(locn.muggle_orphan_purch), can_purch_char(locn.muggle_orphan_purch))
    world.set_rule(world.get_location(locn.luna_overalls_purch), can_purch_char(locn.luna_overalls_purch))
    world.set_rule(world.get_location(locn.molly_purch), can_purch_char(locn.molly_purch))
    world.set_rule(world.get_location(locn.herm_cardigan_purch), can_purch_char(locn.herm_cardigan_purch))
    world.set_rule(world.get_location(locn.luna_yellow_dress_purch), can_purch_char(locn.luna_yellow_dress_purch))
    world.set_rule(world.get_location(locn.dudley_shirt_purch), can_purch_char(locn.dudley_shirt_purch))
    world.set_rule(world.get_location(locn.bill_wedding_purch), can_purch_char(locn.bill_wedding_purch))
    world.set_rule(world.get_location(locn.fleur_purch), can_purch_char(locn.fleur_purch))
    world.set_rule(world.get_location(locn.herm_red_dress_purch), can_purch_char(locn.herm_red_dress_purch))
    world.set_rule(world.get_location(locn.figg_purch), can_purch_char(locn.figg_purch))
    world.set_rule(world.get_location(locn.harry_locket_purch), can_purch_char(locn.harry_locket_purch))
    world.set_rule(world.get_location(locn.twin_1_purch), can_purch_char(locn.twin_1_purch))
    world.set_rule(world.get_location(locn.cole_purch), can_purch_char(locn.cole_purch))
    world.set_rule(world.get_location(locn.herm_ministry_purch), can_purch_char(locn.herm_ministry_purch))
    world.set_rule(world.get_location(locn.arthur_suit_purch), can_purch_char(locn.arthur_suit_purch))
    world.set_rule(world.get_location(locn.harry_christmas_purch), can_purch_char(locn.harry_christmas_purch))
    world.set_rule(world.get_location(locn.ernie_purch), can_purch_char(locn.ernie_purch))
    world.set_rule(world.get_location(locn.prof_snape_purch), can_purch_char(locn.prof_snape_purch))
    world.set_rule(world.get_location(locn.neville_purch), can_purch_char(locn.neville_purch))
    world.set_rule(world.get_location(locn.ron_quidditch_purch), can_purch_char(locn.ron_quidditch_purch))
    world.set_rule(world.get_location(locn.vernon_purch), can_purch_char(locn.vernon_purch))
    world.set_rule(world.get_location(locn.tom_riddle_purch), can_purch_char(locn.tom_riddle_purch))
    world.set_rule(world.get_location(locn.sirius_black_purch), can_purch_char(locn.sirius_black_purch))
    world.set_rule(world.get_location(locn.remus_lupin_purch), can_purch_char(locn.remus_lupin_purch))
    world.set_rule(world.get_location(locn.wormtail_purch), can_purch_char(locn.wormtail_purch))
    world.set_rule(world.get_location(locn.rita_skeeter_purch), can_purch_char(locn.rita_skeeter_purch))
    world.set_rule(world.get_location(locn.padma_patil_purch), can_purch_char(locn.padma_patil_purch))
    world.set_rule(world.get_location(locn.station_guard_purch), can_purch_char(locn.station_guard_purch))
    world.set_rule(world.get_location(locn.prof_binns_purch), can_purch_char(locn.prof_binns_purch))
    world.set_rule(world.get_location(locn.penelope_purch), can_purch_char(locn.penelope_purch))
    world.set_rule(world.get_location(locn.susan_purch), can_purch_char(locn.susan_purch))
    world.set_rule(world.get_location(locn.tonks_purch), can_purch_char(locn.tonks_purch))
    world.set_rule(world.get_location(locn.pius_purch), can_purch_char(locn.pius_purch))
    world.set_rule(world.get_location(locn.reg_purch), can_purch_char(locn.reg_purch))
    world.set_rule(world.get_location(locn.regulus_purch), can_purch_char(locn.regulus_purch))
    world.set_rule(world.get_location(locn.scrimgeour_purch), can_purch_char(locn.scrimgeour_purch))
    world.set_rule(world.get_location(locn.scabior_purch), can_purch_char(locn.scabior_purch))
    world.set_rule(world.get_location(locn.xeno_purch), can_purch_char(locn.xeno_purch))
    world.set_rule(world.get_location(locn.yaxley_purch), can_purch_char(locn.yaxley_purch))
    world.set_rule(world.get_location(locn.zacharias_purch), can_purch_char(locn.zacharias_purch))
    world.set_rule(world.get_location(locn.waitress_treats_purch), can_purch_char(locn.waitress_treats_purch))
    world.set_rule(world.get_location(locn.lord_voldemort_purch), can_purch_char(locn.lord_voldemort_purch))
    world.set_rule(world.get_location(locn.ron_blue_pyjamas_purch), can_purch_char(locn.ron_blue_pyjamas_purch))
    world.set_rule(world.get_location(locn.neville_cardigan_purch), can_purch_char(locn.neville_cardigan_purch))
    world.set_rule(world.get_location(locn.neville_pyjamas_purch), can_purch_char(locn.neville_pyjamas_purch))
    world.set_rule(world.get_location(locn.percy_purch), can_purch_char(locn.percy_purch))
    world.set_rule(world.get_location(locn.sirius_azkaban_purch), can_purch_char(locn.sirius_azkaban_purch))
    world.set_rule(world.get_location(locn.black_purch), can_purch_char(locn.black_purch))
    world.set_rule(world.get_location(locn.xeno_luna_purch), can_purch_char(locn.xeno_luna_purch))
    world.set_rule(world.get_location(locn.ron_reg_cattermole_purch), can_purch_char(locn.ron_reg_cattermole_purch))
    world.set_rule(world.get_location(locn.tonks_pink_coat_purch), can_purch_char(locn.tonks_pink_coat_purch))
    world.set_rule(world.get_location(locn.ron_winter_clothes_purch), can_purch_char(locn.ron_winter_clothes_purch))
    world.set_rule(world.get_location(locn.snape_underwear_purch), can_purch_char(locn.snape_underwear_purch))
    world.set_rule(world.get_location(locn.rowle_purch), can_purch_char(locn.rowle_purch))
    world.set_rule(world.get_location(locn.petunia_purch), can_purch_char(locn.petunia_purch))
    world.set_rule(world.get_location(locn.neville_tank_top_purch), can_purch_char(locn.neville_tank_top_purch))
    world.set_rule(world.get_location(locn.neville_winter_purch), can_purch_char(locn.neville_winter_purch))
    world.set_rule(world.get_location(locn.parvati_purch), can_purch_char(locn.parvati_purch))
    world.set_rule(world.get_location(locn.ron_red_sweater_purch), can_purch_char(locn.ron_red_sweater_purch))
    world.set_rule(world.get_location(locn.ollivander_purch), can_purch_char(locn.ollivander_purch))
    world.set_rule(world.get_location(locn.seamus_winter_purch), can_purch_char(locn.seamus_winter_purch))
    world.set_rule(world.get_location(locn.ron_underwear_purch), can_purch_char(locn.ron_underwear_purch))
    world.set_rule(world.get_location(locn.ron_wedding_purch), can_purch_char(locn.ron_wedding_purch))
    world.set_rule(world.get_location(locn.waitress_luchino_purch), can_purch_char(locn.waitress_luchino_purch))
    world.set_rule(world.get_location(locn.petunia_green_coat_purch), can_purch_char(locn.petunia_green_coat_purch))
    world.set_rule(world.get_location(locn.seamus_purch), can_purch_char(locn.seamus_purch))
    world.set_rule(world.get_location(locn.snatcher_purch), can_purch_char(locn.snatcher_purch))
    world.set_rule(world.get_location(locn.ron_green_shirt_purch), can_purch_char(locn.ron_green_shirt_purch))
    world.set_rule(world.get_location(locn.neville_waiter_purch), can_purch_char(locn.neville_waiter_purch))
    world.set_rule(world.get_location(locn.xeno_wedding_purch), can_purch_char(locn.xeno_wedding_purch))
    world.set_rule(world.get_location(locn.skeleton_purch), can_purch_char(locn.skeleton_purch))


def set_joke_purch_logic(world):
    world.set_rule(world.get_location(locn.slug_purch), can_purch_joke(locn.slug_purch))
    world.set_rule(world.get_location(locn.rictu_purch), can_purch_joke(locn.rictu_purch))
    world.set_rule(world.get_location(locn.entomo_purch), can_purch_joke(locn.entomo_purch))
    world.set_rule(world.get_location(locn.taranta_purch), can_purch_joke(locn.taranta_purch))
    world.set_rule(world.get_location(locn.loco_purch), can_purch_joke(locn.loco_purch))
    world.set_rule(world.get_location(locn.redact_purch), can_purch_joke(locn.redact_purch))
    world.set_rule(world.get_location(locn.colo_purch), can_purch_joke(locn.colo_purch))
    world.set_rule(world.get_location(locn.calvo_purch), can_purch_joke(locn.calvo_purch))
    world.set_rule(world.get_location(locn.anteo_purch), can_purch_joke(locn.anteo_purch))
    world.set_rule(world.get_location(locn.herbi_purch), can_purch_joke(locn.herbi_purch))
    world.set_rule(world.get_location(locn.glaci_purch), can_purch_joke(locn.glaci_purch))
    world.set_rule(world.get_location(locn.incarc_purch), can_purch_joke(locn.incarc_purch))
    world.set_rule(world.get_location(locn.expel_purch), can_purch_joke(locn.expel_purch))
    world.set_rule(world.get_location(locn.flip_purch), can_purch_joke(locn.flip_purch))
    world.set_rule(world.get_location(locn.trip_purch), can_purch_joke(locn.trip_purch))
    world.set_rule(world.get_location(locn.stup_purch), can_purch_joke(locn.stup_purch))
    world.set_rule(world.get_location(locn.transfig_purch), can_purch_joke(locn.transfig_purch))
    world.set_rule(world.get_location(locn.engorg_purch), can_purch_joke(locn.engorg_purch))
    world.set_rule(world.get_location(locn.immob_purch), can_purch_joke(locn.immob_purch))


def set_gold_brick_purch_logic(world):
    world.set_rule(world.get_location(locn.bb_gb2), has_needed_multi(locn.bb_gb2))
    world.set_rule(world.get_location(locn.bb_gb3), has_needed_multi(locn.bb_gb3))
    world.set_rule(world.get_location(locn.bb_gb4), has_needed_multi(locn.bb_gb4))
    world.set_rule(world.get_location(locn.bb_gb5), has_needed_multi(locn.bb_gb5))
    world.set_rule(world.get_location(locn.bb_gb6), has_needed_multi(locn.bb_gb6))
    world.set_rule(world.get_location(locn.bb_gb7), has_needed_multi(locn.bb_gb7))
    world.set_rule(world.get_location(locn.bb_gb8), has_needed_multi(locn.bb_gb8))
    world.set_rule(world.get_location(locn.bb_gb9), has_needed_multi(locn.bb_gb9))
    world.set_rule(world.get_location(locn.bb_gb10), has_needed_multi(locn.bb_gb10))
    world.set_rule(world.get_location(locn.bb_gb11), has_needed_multi(locn.bb_gb11))
    world.set_rule(world.get_location(locn.bb_gb12), has_needed_multi(locn.bb_gb12))
    world.set_rule(world.get_location(locn.bb_gb13), has_needed_multi(locn.bb_gb13))
    world.set_rule(world.get_location(locn.bb_gb14), has_needed_multi(locn.bb_gb14))
    world.set_rule(world.get_location(locn.bb_gb15), has_needed_multi(locn.bb_gb15))
    world.set_rule(world.get_location(locn.bb_gb16), has_needed_multi(locn.bb_gb16))


def set_red_brick_purch_logic(world):
    world.set_rule(world.get_location(locn.com_spec_purch), HasMultiplier(locn.com_spec_purch))
    world.set_rule(world.get_location(locn.adv_guide_purch), HasMultiplier(locn.adv_guide_purch))
    world.set_rule(world.get_location(locn.disguise_purch), HasMultiplier(locn.disguise_purch))
    world.set_rule(world.get_location(locn.carrot_wand_purch), HasMultiplier(locn.carrot_wand_purch))
    world.set_rule(world.get_location(locn.super_strength_purch), can_purch_red_brick(locn.super_strength_purch))
    world.set_rule(world.get_location(locn.char_token_detect_purch), can_purch_red_brick(locn.char_token_detect_purch))
    world.set_rule(world.get_location(locn.fall_rescue_purch), can_purch_red_brick(locn.fall_rescue_purch))
    world.set_rule(world.get_location(locn.char_studs_purch), can_purch_red_brick(locn.char_studs_purch))
    world.set_rule(world.get_location(locn.score_x2_purch), can_purch_red_brick(locn.score_x2_purch))
    world.set_rule(world.get_location(locn.score_x4_purch), can_purch_red_brick(locn.score_x4_purch))
    world.set_rule(world.get_location(locn.score_x6_purch), can_purch_red_brick(locn.score_x6_purch))
    world.set_rule(world.get_location(locn.score_x8_purch), can_purch_red_brick(locn.score_x8_purch))
    world.set_rule(world.get_location(locn.score_x10_purch), can_purch_red_brick(locn.score_x10_purch))
    world.set_rule(world.get_location(locn.stud_mag_purch), can_purch_red_brick(locn.stud_mag_purch))
    world.set_rule(world.get_location(locn.regen_hearts_purch), can_purch_red_brick(locn.regen_hearts_purch))
    world.set_rule(world.get_location(locn.extra_hears_purch), can_purch_red_brick(locn.extra_hears_purch))
    world.set_rule(world.get_location(locn.invincibility_purch), can_purch_red_brick(locn.invincibility_purch))
    world.set_rule(world.get_location(locn.red_brick_detect_purch), can_purch_red_brick(locn.red_brick_detect_purch))
    world.set_rule(world.get_location(locn.crest_detect_purch), can_purch_red_brick(locn.crest_detect_purch))
    world.set_rule(world.get_location(locn.gb_detect_purch), can_purch_red_brick(locn.gb_detect_purch))
    world.set_rule(world.get_location(locn.christmas_purch), can_purch_red_brick(locn.christmas_purch))
    world.set_rule(world.get_location(locn.ghost_studs_purch), can_purch_red_brick(locn.ghost_studs_purch))
    world.set_rule(world.get_location(locn.fast_magic_purch), can_purch_red_brick(locn.fast_magic_purch))
    world.set_rule(world.get_location(locn.fast_dig_purch), can_purch_red_brick(locn.fast_dig_purch))


def set_rules(world: "LHP2World"):
    set_entrance_rules(world)
    set_lesson_logic(world)
    set_event_logic(world)
    set_win_con(world)

    from .Data import RuleMapping

    disabled = set(world.options.DisabledLevels.value)

    for level_name, func in RuleMapping.LEVEL_LOGIC_FUNCS.items():
        if level_name not in disabled:
            func(world)

    # Hub Logic
    set_hub_collect_logic(world)
    if world.options.ShuffleCharacterTokens != 2:
        set_hub_token_logic(world)
    if world.options.ShuffleRedBricks != 2:
        set_hub_rb_logic(world)
    # Shop Logic
    if world.options.ShuffleCharacterTokens != 1:
        set_char_purch_logic(world)
    if world.options.ShuffleJokeSpells == 1:
        set_joke_purch_logic(world)
    if world.options.ShuffleGoldBrickPurchases == 1:
        set_gold_brick_purch_logic(world)
    if world.options.ShuffleRedBricks != 1:
        set_red_brick_purch_logic(world)
