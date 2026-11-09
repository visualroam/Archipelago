from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING, Any

from typing_extensions import override

if TYPE_CHECKING:
    from worlds.minecraft_fabric import FabricMinecraftWorld, World

from rule_builder.field_resolvers import FieldResolver
from rule_builder.rules import Rule, Has, True_, HasAll, Filtered
from rule_builder.options import OptionFilter

from ..options import *

from dataclasses import dataclass

from BaseClasses import CollectionState

########################################################################################################################
########################################################################################################################
# VANILLA ##############################################################################################################
########################################################################################################################
########################################################################################################################

# DIFFICULTY CHECK #####################################################################################################

def getDifficultyRequirements(required_options):
    required = True_()
    required = required & Filtered(canUseIronWeapons(), options=[OptionFilter(required_options, "Iron Weapons", operator="contains")], filtered_resolution=True)
    required = required & Filtered(canWearIronArmor(), options=[OptionFilter(required_options, "Iron Armor", operator="contains")], filtered_resolution=True)
    required = required & Filtered(canUseBow(), options=[OptionFilter(required_options, "Bow", operator="contains")], filtered_resolution=True)
    required = required & Filtered(optionalRequireSprint(), options=[OptionFilter(required_options, "Sprint", operator="contains")], filtered_resolution=True)
    required = required & Filtered(optionalRequireJump(), options=[OptionFilter(required_options, "Jump", operator="contains")], filtered_resolution=True)
    required = required & Filtered(canSleep(), options=[OptionFilter(required_options, "Beds", operator="contains")], filtered_resolution=True)
    return required

# OPTIONAL ABILITY CHECKS ##############################################################################################

def optionalRequireSprint():
    return checkRandomizedAbility("Sprint", "Sprint")

def optionalRequireJump():
    return checkRandomizedAbility("Jump", "Jump")

def canAccessChests():
    return checkRandomizedAbility("Chests", "Chests & Barrels")

def canSwim():
    return checkRandomizedAbility("Swim", "Swim")

def checkRandomizedAbility(value: str, item: str):
    return Has(item, options=[OptionFilter(RandomizedAbilities, value, operator="contains")], filtered_resolution=True)

def hasOptionalGoalAbilities():
    return optionalRequireJump() & optionalRequireSprint()

def hasTNT():
    return Has("TNT Recipes")

# ABILITY CHECKS #######################################################################################################

def canTrade():
    return Has("Villager Trading") & villageExploration()

def canBarter():
    return Has("Piglin Bartering") & canAccessNether() & canGetGold()

def canSleep():
    return Has("Sleeping")

# CRAFTING STATION CHECKS ##############################################################################################

def canSmelt():
    return Has("Progressive Smelting")

def canSmeltBetter():
    return Has("Progressive Smelting", count=2)

def canSmith():
    return canGetIron() & Has("Smithing")

def canBrew():
    return canAccessNether() & canUseBottles() & Has("Brewing") & (fortressExploration() | villageExploration())

def canEnchant():
    return canGetObsidian() & Has("Enchanting") & canUseIronTools()

def canAccessMiscJobsites():
    return Has("Other Crafting Stations")

# MINING TOOL CHECKS ###################################################################################################

def canUseStoneTools():
    return Has("Progressive Tools")

def canUseIronTools():
    return canGetIron() & Has("Progressive Tools", count=2)

def canUseDiamondTools():
    return canUseIronTools() & Has("Progressive Tools", count=3)

def canUseNetheriteTools():
    return (Has("Progressive Tools", count=4) & canSmith() & canGetUpgradeTemplate() & canGetNetherite())

# WEAPON CHECKS ###################################################################################################

def canUseStoneWeapons():
    return Has("Progressive Weapons")

def canUseIronWeapons():
    return canUseStoneTools() & canGetIron() & Has("Progressive Weapons", count=2)

def canUseDiamondWeapons():
    return canUseIronTools() & Has("Progressive Weapons", count=3)

def canUseNetheriteWeapons():
    return (Has("Progressive Weapons", count=4) & canSmith() & canGetUpgradeTemplate() & canGetNetherite())

# ARMOR CHECKS #########################################################################################################

def canWearLeatherArmor():
    return Has("Progressive Armor")

def canWearGoldArmor():
    return canGetGold() & Has("Progressive Armor", count=2)

def canWearIronArmor():
    return canGetIron() & Has("Progressive Armor", count=3)

def canWearDiamondArmor():
    return Has("Progressive Armor", count=4) & canUseIronTools()

def canWearNetheriteArmor():
    return (Has("Progressive Armor", count=5) & canSmith() & canGetNetherite() & canGetUpgradeTemplate())

# OTHER TOOL CHECKS ####################################################################################################

def canUseBucket():
    return canGetIron() & Has("Bucket Recipes")

def canUseFlintAndSteel():
    return canGetIron() & Has("Flint and Steel Recipes")

def canUseMinecart():
    return canGetIron() & Has("Minecart Recipes")

def canUseBrush():
    return canGetIron() & Has("Brush Recipes")

def canUseSpyglass():
    return canGetIron() & Has("Spyglass Recipes")

def canUseShears():
    return canGetIron() & Has("Shear Recipes")

def canUseFishingRod():
    return Has("Fishing Rod Recipes")

def canUseBottles():
    return canSmelt() & Has("Glass Bottle Recipes")

def canUseBow():
    return Has("Progressive Archery")

def canUseCrossBow():
    return Has("Progressive Archery", count=2) & canGetIron()

def canUseShield():
    return Has("Shield Recipes") & canGetIron()

# OTHER RECIPE CHECKS ##################################################################################################

def canCompactResources():
    return Has("Resource Compacting Recipes")

def canGetEyesOfEnder():
    return canAccessNether() & fortressExploration() & Has("Eye of Ender Recipes")

def canGetAndUseArmorTrims():
    return canSmith() & canAccessChests() & canWearLeatherArmor()

# DIMENSION CHECKS #####################################################################################################

def canAccessNether():
    createMethod = Has("Water Wheels") | Has("Windmills")

    return (((canGetObsidian() | canUseBucket()) & canUseFlintAndSteel()) & getDifficultyRequirements(ShouldHaveBeforeNetherAccess) & Filtered(createMethod, options=[OptionFilter(EnabledModSupport, "create", operator="contains")], filtered_resolution=True))

def canAccessEnd():
    return canGetEyesOfEnder() & getDifficultyRequirements(ShouldHaveBeforeWitherOrDragon)

# MISC VANILLA #########################################################################################################

def canGetNetherite():
    return (hasTNT() | canSleep()) & canUseDiamondTools() & canAccessNether() & canAccessChests()

def canPlaceBeacon():
    return canGoalWither() & canGetIron() & canGetObsidian() & canCompactResources()

def canGetPrismarine():
    createMethod = canUseStoneTools() & canHauntCreate()

    return (canSwim() & monumentExploration()) | Filtered(createMethod, options=[OptionFilter(EnabledModSupport, "create", operator="contains")], filtered_resolution=False)

def canGetObsidian():
    createMethod = hasFanCreate() & canSwim()

    return (canUseDiamondTools() & (ruinedPortalExploration() | canUseBucket())) | Filtered(createMethod, options=[OptionFilter(EnabledModSupport, "create", operator="contains")], filtered_resolution=False)

def canGetMud():
    createMethod = hasMixerCreate() & canFillFluidWaterCreate()

    return canUseBottles() | Filtered(createMethod, options=[OptionFilter(EnabledModSupport, "create", operator="contains")], filtered_resolution=False)

def canGetIron():
    return canUseStoneTools() & canSmelt()

def canGetGold():
    return ((canUseIronTools() & canSmelt()) |
            (canAccessNether() & canCompactResources()))

def canGetGoldNugget():
    return ((canUseIronTools() & canGetIron() & canCompactResources()) |
            canAccessNether())

def canCraftDriedKelp():
    return canSwim() & canSmelt()

def canGetCryingObsidian():
    return canBarter() | (canUseDiamondTools() & ruinedPortalExploration())

def canDyeBasic():
    return Has("Progressive Dye Recipes")

def canDyeFull():
    return Has("Progressive Dye Recipes", count=2)

def canDyeBlack():
    createMethod = Has("Cogwheels") & canCraftAndesiteAlloyCreate() & canGetIron()

    return (canDyeBasic() & (canGoalWither() | canSwim())) | Filtered(createMethod, options=[OptionFilter(EnabledModSupport, "create", operator="contains")], filtered_resolution=False)

def canDyeGreen():
    createMethod = Has("Cogwheels") & canCraftAndesiteAlloyCreate() & canGetIron()

    return (canSmelt() & aridBiomesExploration()) | Filtered(createMethod, options=[OptionFilter(EnabledModSupport, "create", operator="contains")], filtered_resolution=False)

def canGetUpgradeTemplate():
    return canAccessNether() & canAccessChests() & bastionRemnantExploration()

def canCureZombieVillager():
    return canBrew() & canUseIronTools() & villageExploration() & (canAccessNether() | wetlandBiomesExploration() | forestBiomesExploration())

def canGetSmoothStone():
    return canSmelt() | canEnchant()

def canFightRaid():
    return getDifficultyRequirements(ShouldHaveBeforeRaids)

# GOAL CHECKS ##########################################################################################################

def canAccessVanillaEndGame():
    createMethod = Has("Water Wheels") & Has("Windmills") & Has("Steam Engines")

    return ((canEnchant() & canBrew() & canPlaceBeacon()
            & canBeatDragonAndWither() & canUseDiamondTools())
            & canAccessChests() & canSmith() & Filtered(createMethod, options=[OptionFilter(EnabledModSupport, "create", operator="contains")], filtered_resolution=True)
            & endCityExploration() & fortressExploration() & bastionRemnantExploration()
            & ancientCityExploration() & mansionExploration() & monumentExploration()
            & ruinsExploration() & plainsBiomesExploration() & forestBiomesExploration()
            & undergroundBiomesExploration() & wetlandBiomesExploration() & villageExploration()
            & desertPyramidExploration() & oceanBiomesExploration() & highlandBiomesExploration()
            & jungleBiomesExploration() & pillagerOutpostExploration())

def canGoalEnderDragon():
    return canAccessEnd()

def canGoalWither():
    return (canAccessNether() & fortressExploration() & Has("Wither Summoning")
            & getDifficultyRequirements(ShouldHaveBeforeWitherOrDragon))

def canBeatDragonAndWither():
    return canGoalEnderDragon() & canGoalWither()

@dataclass(frozen=True)
class RubyCount(FieldResolver, game="Minecraft Fabric"):
    @override
    def resolve(self, world: "World") -> Any:
        return floor(world.max_ruby_count * (world.options.percentage_of_rubies_needed.value * 0.01))

def canCompleteRubyHunt():
    createMethod = Has("Water Wheels") | Has("Windmills")

    return Has("Ruby", count=RubyCount()) & Filtered(createMethod, options=[OptionFilter(EnabledModSupport, "create", operator="contains")], filtered_resolution=True)

# EXPLORATION

def canExplore():
    return Filtered(optionalRequireJump() & optionalRequireSprint() & canSwim(), options=[OptionFilter(LogicDifficultyOptions, "Movement Before Exploration", operator="contains")], filtered_resolution=True) & Filtered(canSleep(), options=[OptionFilter(LogicDifficultyOptions, "Sleeping Before Exploration", operator="contains")], filtered_resolution=True)

# BIOME CHECKS
def oceanBiomesExploration():
    return Has("Ocean Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def plainsBiomesExploration():
    return Has("Plains Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def savannaBiomesExploration():
    return Has("Savanna Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def forestBiomesExploration():
    return Has("Forest Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def jungleBiomesExploration():
    return Has("Jungle Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def wetlandBiomesExploration():
    return Has("Wetland Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def mountainBiomesExploration():
    return Has("Mountain Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def highlandBiomesExploration():
    return Has("Highland Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def aridBiomesExploration():
    return Has("Arid Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def undergroundBiomesExploration():
    return Has("Underground Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def netherBiomesExploration():
    return Has("Nether Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def endBiomesExploration():
    return Has("End Biomes (Nature's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Natures Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

# STRUCTURE CHECKS

def villageExploration():
    return Has("Village (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def ruinsExploration():
    return Has("Ruins (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def ruinedPortalExploration():
    return Has("Ruined Portal (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def shipwreckExploration():
    return Has("Shipwreck (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def buriedTreasureExploration():
    return Has("Buried Treasure (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def mineshaftExploration():
    return Has("Mineshaft (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def monumentExploration():
    return Has("Monument (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def endCityExploration():
    return Has("End City (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def desertPyramidExploration():
    return Has("Desert Pyramid (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def junglePyramidExploration():
    return Has("Jungle Pyramid (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def pillagerOutpostExploration():
    return Has("Pillager Outpost (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def fortressExploration():
    return Has("Fortress (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def bastionRemnantExploration():
    return Has("Bastion Remnant (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def mansionExploration():
    return Has("Mansion (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

def ancientCityExploration():
    return Has("Ancient City (Explorer's Compass)", options=[OptionFilter(LogicDifficultyOptions, "Explorers Compass Logic", operator="contains")], filtered_resolution=True) & canExplore()

# WEATHER

def weatherControl():
    return Has("Totem of Meteorology", options=[OptionFilter(LogicDifficultyOptions, "Meteorology", operator="contains")], filtered_resolution=True)


########################################################################################################################
########################################################################################################################
# MODDED CHECKS TO PREVENT CYCLICAL DEPENDENCY ISSUES ##################################################################
########################################################################################################################
########################################################################################################################

def canCraftAndesiteAlloyCreate():
    return canCompactResources() & canGetIron()

def hasCogsCreate():
    return canCraftAndesiteAlloyCreate() & Has("Cogwheels")

def hasPressCreate():
    return (Has("Mechanical Press Recipes") & canCompactResources() &
            canCraftAndesiteAlloyCreate())

def hasFanCreate():
    return canCraftAndesiteAlloyCreate() & hasPressCreate()

def canHauntCreate():
    return hasFanCreate() & canAccessNether()

def hasMixerCreate():
    return (Has("Mechanical Mixer Recipes") & canCraftAndesiteAlloyCreate()
            & hasCogsCreate() & hasPressCreate())

def canFillFluidWaterCreate():
    return canUseBucket() | hasPumpCreate() | canUseBottles()

def hasPumpCreate():
    return hasCogsCreate() & hasPressCreate()

########################################################################################################################
########################################################################################################################
# MOD CHECKING #########################################################################################################
########################################################################################################################
########################################################################################################################

def hasCreate():
    return OptionFilter(EnabledModSupport, "create", operator="contains")

