from ..Rules import *

itm = ItemName
locn = LocationName
regn = RegionName

red_brick_rule_table = {
    locn.score_x4_purch: can_get_kcs_rb,
    locn.red_brick_detect_purch: can_get_hogstat_rb,
    locn.score_x8_purch: can_get_hogwpath_rb,
    locn.score_x6_purch: can_get_hogspath_rb,
    locn.ghost_studs_purch: can_get_quad_rb,
    locn.fast_dig_purch: can_get_grounds_rb,
    locn.regen_hearts_purch: can_get_thest_rb,
    locn.score_x10_purch: can_get_lake_rb,
    locn.fall_rescue_purch: can_get_lib_rb,
    locn.crest_detect_purch: can_get_ghl_rb,
    locn.super_strength_purch: can_get_wc_rb,
    locn.char_studs_purch: can_get_gh_rb,
    locn.stud_mag_purch: can_get_ror_rb,
    locn.extra_hears_purch: can_get_dada_rb,
    locn.invincibility_purch: can_get_divc_rb,
    locn.char_token_detect_purch: can_get_div_rb,
    locn.fast_magic_purch: can_get_ast_rb,
}

LEVEL_LOGIC_FUNCS = {
    # Y5
    regn.dt: set_dt_logic,
    regn.da: set_da_logic,
    regn.foc: set_foc_logic,
    regn.kd: set_kd_logic,
    regn.agv: set_agv_logic,
    regn.avt: set_avt_logic,

    # Y6
    regn.oor: set_oor_logic,
    regn.jd: set_jd_logic,
    regn.ansmc: set_ansmc_logic,
    regn.lh: set_lh_logic,
    regn.ff: set_ff_logic,
    regn.thath: set_thath_logic,

    # Y7
    regn.tsh: set_tsh_logic,
    regn.mim: set_mim_logic,
    regn.igd: set_igd_logic,
    regn.sal: set_sal_logic,
    regn.ll: set_ll_logic,
    regn.dob: set_dob_logic,

    # Y8
    regn.ttd: set_ttd_logic,
    regn.bts: set_bts_logic,
    regn.bb: set_bb_logic,
    regn.fiend: set_fiend_logic,
    regn.st: set_st_logic,
    regn.tfitp: set_tfitp_logic,
}

token_rule_table = {
    # Hub Tokens
    locn.anthony_purch:            can_get_anthony_token,
    locn.argus_purch:              can_get_filch_token,
    locn.arthur_cardigan_purch:    can_get_arthur_cardigan,
    locn.arthur_torn_suit_purch:   can_get_arthur_torn_suit,
    locn.bellatrix_azka_purch:     can_get_bella_azka,
    locn.blaise_purch:             can_get_blaise,
    locn.charity_purch:            can_get_charity,
    locn.charlie_purch:            can_get_charlie,
    locn.cho_purch:                can_get_cho,
    locn.crabbe_jumper_purch:      can_get_crabbe_jumper,
    locn.dolohov_purch:            can_get_dolohov,
    locn.dolohov_workman_purch:    can_get_dolohov_work,
    locn.draco_purch:              can_get_draco,
    locn.dudley_purch:             can_get_dudley,
    locn.dumble_young_purch:       can_get_dumble_young,
    locn.fat_lady_purch:           can_get_fat_lady,
    locn.fred_owls_purch:          can_get_fred_owls,
    locn.fred_pyjamas_purch:       can_get_fred_pyjamas,
    locn.fred_purch:               can_get_fred,
    locn.george_owls_purch:        can_get_george_owls,
    locn.george_pyjamas_purch:     can_get_george_pyjamas,
    locn.george_purch:             can_get_george,
    locn.ginny_pyjamas_purch:      can_get_ginny_pyjamas,
    locn.goyle_jumper_purch:       can_get_goyle_jumper,
    locn.gregorovitch_purch:       can_get_gregorovitch,
    locn.hannah_purch:             can_get_hannah,
    locn.harry_pyjamas_purch:      can_get_harry_pyjamas,
    locn.herm_ball_purch:          can_get_herm_ball_gown,
    locn.herm_cardigan_purch:      can_get_herm_cardigan,
    locn.katie_purch:              can_get_katie_bell,
    locn.lavender_purch:           can_get_lavender,
    locn.lily_young_casual_purch:               can_get_lily_casual,
    locn.lucius_purch:             can_get_lucius,
    locn.luna_blue_jumper_purch:   can_get_luna_blue,
    locn.luna_overalls_purch:      can_get_luna_overalls,
    locn.luna_pink_dress_purch:    can_get_luna_pink,
    locn.luna_purch:               can_get_luna,
    locn.madam_pince_purch:        can_get_madam_pince,
    locn.mafalda_purch:            can_get_mafalda,
    locn.belby_purch:              can_get_belby,
    locn.mary_cattermole_purch:    can_get_mary,
    locn.mcgon_black_purch:        can_get_mcgonagall_black,
    locn.mcgon_pyjamas_purch:      can_get_mcgonagall_pyjamas,
    locn.michael_purch:            can_get_michael,
    locn.ministry_guard_purch:     can_get_ministry_guard,
    locn.myrtle_purch:             can_get_myrtle,
    locn.black_purch:              can_get_mrs_black,
    locn.cole_purch:               can_get_mrs_cole,
    locn.narcissa_purch:           can_get_narcissa,
    locn.neville_tank_top_purch:   can_get_neville_tank,
    locn.neville_waiter_purch:     can_get_neville_waiter,
    locn.padma_patil_purch:        can_get_padma,
    locn.petunia_green_coat_purch: can_get_petunia_green,
    locn.petunia_purch:            can_get_petunia,
    locn.pius_purch:               can_get_pius,
    locn.prof_binns_purch:         can_get_prof_binns,
    locn.prof_flit_purch:          can_get_prof_flitwick,
    locn.prof_grubbly_purch:       can_get_prof_grub,
    locn.prof_mcgon_purch:         can_get_prof_mcgonagall,
    locn.prof_trelawney_purch:     can_get_prof_trelawney,
    locn.reg_purch:                can_get_reg_catter,
    locn.regulus_purch:            can_get_regulus,
    locn.rita_skeeter_purch:       can_get_rita,
    locn.ron_blue_pyjamas_purch:   can_get_ron_blue,
    locn.ron_green_shirt_purch:    can_get_ron_green,
    locn.scrimgeour_purch:         can_get_rufus,
    locn.scabior_purch:            can_get_scabior,
    locn.slughorn_young_purch:     can_get_slug_young,
    locn.snatcher_purch:           can_get_snatcher,
    locn.susan_purch:              can_get_susan_bones,
    locn.rowle_purch:              can_get_rowle,
    locn.umbridge_wizengamot_purch: can_get_umbridge_wizen,
    locn.vernon_purch:             can_get_vernon,
    locn.waitress_luchino_purch:   can_get_waitress_luchino,
    locn.yaxley_purch:             can_get_yaxley,

    # Dark Times Logic
    locn.arthur_suit_purch: can_get_arthur_suit,
    locn.elphias_purch: can_get_elphias,

    # Dumbledore's Army Logic
    locn.cho_winter_purch: can_get_cho_winter,
    locn.herm_scarf_purch: can_get_herm_scarf,
    locn.neville_winter_purch: can_get_neville_winter,

    # Focus!
    locn.molly_apron_purch: can_get_molly_apron,
    locn.snape_underwear_purch: can_get_snape_under,

    # Kreacher Discomforts
    locn.kreacher_purch: can_get_kreacher,
    locn.sirius_black_purch: can_get_sirius,

    # A Giant Virtuoso
    locn.emmeline_purch: can_get_emmeline,
    locn.neville_purch: can_get_neville,
    locn.prof_umbridge_purch: can_get_prof_umbridge,

    # A Veiled Threat
    locn.fudge_wizengamot_purch: can_get_fudge_wizen,
    locn.herm_jumper_purch: can_get_herm_jumper,
    locn.lucius_death_eater_purch: can_get_lucius_death,

    # Out of Retirement
    locn.dumble_cursed_purch: can_get_dumble_cursed,
    locn.milk_man_purch: can_get_milk_man,
    locn.slughorn_pyjamas_purch: can_get_slug_pajamas,

    # Just Desserts
    locn.cormac_suit_purch: can_get_cormac_suit,
    locn.harry_christmas_purch: can_get_harry_christ,
    locn.madam_rosmerta_purch: can_get_madam_rosmerta,

    # A Not So Merry Christmas
    locn.bill_wedding_purch: can_get_bill_wedding,

    # Love Hurts
    locn.draco_suit_purch: can_get_draco_suit,
    locn.ginny_purch: can_get_ginny,
    locn.prof_slughorn_purch: can_get_prof_slug,

    # Felix Felicis
    locn.hagrid_purch: can_get_hagrid,
    locn.prof_sprout_purch: can_get_prof_sprout,

    # Horcrux and the Hand
    locn.hagrid_wed_purch: can_get_hagrid_wed,
    locn.prof_dumble_purch: can_get_prof_dumble,
    locn.tr_orphanage_purch: can_get_tr_orphan,

    # Seven Harrys
    locn.madeye_purch: can_get_mad_eye,
    locn.ron_wedding_purch: can_get_ron_wed,

    # Magic is Might
    locn.ron_reg_cattermole_purch: can_get_ron_reg,

    # In Grave Danger
    locn.bathilda_snake_purch: can_get_bathilda_snake,
    locn.harry_godric_purch: can_get_harry_god_hollow,
    locn.lily_purch: can_get_lily,

    # Sword and Locket
    locn.herm_grey_coat_purch: can_get_herm_gray_coat,

    # Lovegood’s Lunacy
    locn.skeleton_purch: can_get_skeleton,
    locn.xeno_luna_purch: can_get_xeno_luna,

    # Dobby!
    locn.dobby_purch: can_get_dobby,
    locn.wormtail_purch: can_get_wormtail,

    # Thief’s Downfall
    locn.bogrod_purch: can_get_bogrod,
    locn.griphook_purch: can_get_griphook,
    locn.herm_gringotts_purch: can_get_herm_gringotts,

    # Back to School
    locn.aberforth_purch: can_get_aberforth,
    locn.alecto_purch: can_get_alecto,
    locn.amycus_purch: can_get_amycus,

    # Burning Bridges
    locn.neville_cardigan_purch: can_get_neville_cardigan,
    locn.seamus_purch: can_get_seamus,

    # Fiendfyre Frenzy
    locn.goyle_purch: can_get_goyle,
    locn.harry_brown_jacket_purch: can_get_harry_brown_jacket,
    locn.tom_riddle_purch: can_get_tom_riddle,

    # Snape’s Tears
    locn.death_eater_purch: can_get_death_eater,
    locn.fenrir_purch: can_get_fenrir,
    locn.prof_snape_purch: can_get_prof_snape,
}

