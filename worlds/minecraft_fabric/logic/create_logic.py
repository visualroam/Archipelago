from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.minecraft_fabric import FabricMinecraftWorld

from rule_builder.rules import Rule, Has

from .vanilla_logic import *
from BaseClasses import CollectionState


########################################################################################################################
########################################################################################################################
# CREATE MOD LOGIC #####################################################################################################
########################################################################################################################
########################################################################################################################


# BASIC COMPONENTS #####################################################################################################

def canCraftAndesiteAlloy():
    return canCompactResources() & canGetIron()

def canGetZinc():
    return canGetIron() & canUseIronTools()

def canCraftBrass():
    return hasMixer() & hasBlazeBurner() & canUseIronTools()

def canCraftCardboard():
    return hasMixer() & canFillFluidWater() & hasPress()

def canCraftRoseQuartz():
    return canAccessNether() & canUseIronTools()

def canUseSandpaper():
    return Has("Sand Paper")

def canCraftElectronTube():
    return canCraftRoseQuartz() & hasPress() & canUseSandpaper()

def canCraftPercisionMechanism():
    return hasDeployer() & hasPress() & hasCogs() & canUseSandpaper()

def canCraftSturdySheet():
    return (hasCrusher() & hasPress() & canUseSpout()
            & canUseBucket() & canGetObsidian())

def canCraftTrainTracks():
    return hasPress() & hasDeployer()

def hasCogs():
    return canCraftAndesiteAlloy() & Has("Cogwheels")

def hasBlazeBurner():
    return canAccessNether() & hasPress() & Has("Blaze Burners")

def canUseBlazeCake():
    return hasBlazeBurner() & hasCrusher() & canCraftDriedKelp() & canUseSpout()

def canFillFluidWater():
    return hasPump() & canUseBucket()

def canMakeHeat():
    return (canUseFlintAndSteel() | canUseStoneTools() | canGetIron() |
            canUseBucket())

def canUsePackager():
    return (canCompactResources() & canGetIron() & canUseIronTools() &
            canAccessChests() & canCraftCardboard())

# POWER GENERATION #####################################################################################################

def hasWaterWheel():
    return canCraftAndesiteAlloy() & Has("Water Wheels")

def hasWindmill():
    return canCraftAndesiteAlloy() & Has("Windmills")

def hasSteamEngine():
    return ((canCraftAndesiteAlloy() & Has("Steam Engines")
            & canCompactResources() & canFillFluidTankWater() & canMakeHeat())
            & canUseIronTools())

def hasMorePower():
    return hasWaterWheel() | hasWindmill() | hasSteamEngine()

# CRAFTING #############################################################################################################

def hasPress():
    return (Has("Mechanical Press Recipes") & canCompactResources() &
            canCraftAndesiteAlloy())

def hasMixer():
    return (Has("Mechanical Mixer Recipes") & canCraftAndesiteAlloy()
            & hasCogs() & hasPress())

def hasSaw():
    return hasPress()

def hasDeployer():
    return canCraftElectronTube() & canCraftBrass()

def canUseSpout():
    return canCraftDriedKelp() & canUseStoneTools() & hasPump() & canUseBucket()

def hasMechanicalCrafter():
    return hasMorePower() & canCraftElectronTube() & canCraftBrass()

def hasCrusher():
    return hasMechanicalCrafter()

# FAN CRAFTING #########################################################################################################

def canWash():
    return hasPress()

def canHaunt():
    return hasPress() & canAccessNether()

# FLUID TANKS ##########################################################################################################

def hasFluidTank():
    return hasPress() & canAccessChests() & canGetIron()

def canFillFluidTankWater():
    return hasFluidTank() & canFillFluidWater()

def hasPump():
    return hasCogs() & hasPress()

# OTHER CHECKS #########################################################################################################

def canCraftSPDecorativeStone():
    return hasSaw() | canAccessMiscJobsites()