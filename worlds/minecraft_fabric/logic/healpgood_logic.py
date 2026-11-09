from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.minecraft_fabric import FabricMinecraftWorld

from rule_builder.rules import Rule, Has

from .vanilla_logic import *
from BaseClasses import CollectionState


########################################################################################################################
########################################################################################################################
# HEALING PRETTY GOOD MOD LOGIC ########################################################################################
########################################################################################################################
########################################################################################################################

def heartCrystalExploration():
    return Has("Heart Crystal (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()