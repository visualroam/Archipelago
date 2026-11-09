from __future__ import annotations


from typing import TYPE_CHECKING, Optional

from worlds.minecraft_fabric.region.mc_regions_consts import *
from worlds.minecraft_fabric.region.regions_helper import create_locations_and_connect, smart_add_rule
from worlds.minecraft_fabric.logic.vanilla_logic import *


if TYPE_CHECKING:
   from worlds.minecraft_fabric import FabricMinecraftWorld


def create_vanilla_advancement_regions(world: FabricMinecraftWorld):
    # BASE (REQUIRES NOTHING TO GET)
    create_locations_and_connect(world, "Menu", "MenuVanillaAdvancements", {
        "Stone Age": ADVANCEMENT,
        "Voluntary Exile": ADVANCEMENT,
        "Monster Hunter": ADVANCEMENT,
        "The Parrots and the Bats": ADVANCEMENT,
        "You've Got a Friend in Me": ADVANCEMENT_EXPLORATION,
        "Best Friends Forever": ADVANCEMENT,
        "A Seedy Place": ADVANCEMENT,
        "Getting Wood": ADVANCEMENT,
        "Benchmarking": ADVANCEMENT,
        "Time to Mine!": ADVANCEMENT,
        "Time to Farm!": ADVANCEMENT,
        "Bake Bread": ADVANCEMENT,
        "Time to Strike!": ADVANCEMENT,
        "Cow Tipper": ADVANCEMENT,
        "When the Squad Hops into Town": ADVANCEMENT_HARD,
        "Whatever Floats Your Goat!": ADVANCEMENT_EXPLORATION,
        "Sneak 100": ADVANCEMENT_EXPLORATION,
        "It Spreads": ADVANCEMENT_EXPLORATION
    })
    smart_add_rule(world, "Voluntary Exile", pillagerOutpostExploration(), ADVANCEMENT)
    smart_add_rule(world, "You've Got a Friend in Me", pillagerOutpostExploration(), ADVANCEMENT_EXPLORATION)
    smart_add_rule(world, "When the Squad Hops into Town", wetlandBiomesExploration() & canUseBucket(), ADVANCEMENT_HARD)
    smart_add_rule(world, "Whatever Floats Your Goat!", mountainBiomesExploration() | highlandBiomesExploration(), ADVANCEMENT_EXPLORATION)
    smart_add_rule(world, "Sneak 100", undergroundBiomesExploration(), ADVANCEMENT_EXPLORATION)
    smart_add_rule(world, "It Spreads", undergroundBiomesExploration(), ADVANCEMENT_EXPLORATION)

    # REQUIRES NETHER ACCESS
    create_region(world, "Menu", "NetherAccess", {
        "We Need to Go Deeper": ADVANCEMENT,
        "Return to Sender": ADVANCEMENT,
        "Those Were the Days": ADVANCEMENT,
        "Subspace Bubble": ADVANCEMENT,
        "A Terrible Fortress": ADVANCEMENT,
        "Uneasy Alliance": ADVANCEMENT_HARD,
        "Spooky Scary Skeleton": ADVANCEMENT,
        "Into Fire": ADVANCEMENT,
        "The Power of Books": ADVANCEMENT,
        "With Our Powers Combined!": ADVANCEMENT_HARD,
        "Hot Tourist Destinations": ADVANCEMENT_EXPLORATION
    }, canAccessNether())
    smart_add_rule(world, "Those Were the Days", bastionRemnantExploration(), ADVANCEMENT)
    smart_add_rule(world, "Spooky Scary Skeleton", fortressExploration(), ADVANCEMENT)
    smart_add_rule(world, "Into Fire", fortressExploration(), ADVANCEMENT)
    smart_add_rule(world, "A Terrible Fortress", fortressExploration(), ADVANCEMENT)
    smart_add_rule(world, "With Our Powers Combined!", wetlandBiomesExploration() & canUseBucket(), ADVANCEMENT_HARD)
    smart_add_rule(world, "Hot Tourist Destinations", netherBiomesExploration(), ADVANCEMENT_EXPLORATION)

    # REQUIRES END ACCESS
    create_region(world, "NetherAccess", "EndAccess", {
       "Free the End": ADVANCEMENT,
       "The Next Generation": ADVANCEMENT,
       "Remote Getaway": ADVANCEMENT,
       "The City at the End of the Game": ADVANCEMENT,
       "Sky's the Limit": ADVANCEMENT,
       "Great View From Up Here": ADVANCEMENT,
       "Eye Spy": ADVANCEMENT,
       "The End?": ADVANCEMENT
    }, canAccessEnd())
    smart_add_rule(world, "The City at the End of the Game", endCityExploration(), ADVANCEMENT)
    smart_add_rule(world, "Sky's the Limit", endCityExploration(), ADVANCEMENT)
    smart_add_rule(world, "Great View From Up Here", endCityExploration(), ADVANCEMENT)

    # REQUIRES STONE TOOLS
    create_region(world, "Menu", "HasStoneTools", {
        "Getting an Upgrade": ADVANCEMENT
    }, canUseStoneTools())

    # REQUIRES LEATHER ARMOR
    create_region(world, "Menu", "HasLeatherArmor", {
        "Light as a Rabbit": ADVANCEMENT_EXPLORATION
    }, canWearLeatherArmor())
    smart_add_rule(world, "Light as a Rabbit", highlandBiomesExploration(), ADVANCEMENT_EXPLORATION)

    # REQUIRES SMELTING
    create_region(world, "Menu", "CanSmeltItems", {
        "Hot Topic": ADVANCEMENT
    }, canSmelt())

    # REQUIRES SMELTING
    create_region(world, "HasStoneTools", "CanGetIron", {
        "Acquire Hardware": ADVANCEMENT
    }, canGetIron())

    # REQUIRES SHIELD
    create_region(world, "CanSmeltItems", "HasShield", {
        "Not Today, Thank You": ADVANCEMENT
    }, canUseShield())

    # REQUIRES IRON TOOLS
    create_region(world, "CanSmeltItems", "HasIronTools", {
        "Isn't It Iron Pick": ADVANCEMENT,
        "Diamonds!": ADVANCEMENT,
        "Sound of Music": ADVANCEMENT_EXPLORATION
    }, canUseIronTools())
    smart_add_rule(world, "Sound of Music", highlandBiomesExploration(), ADVANCEMENT_EXPLORATION)

    # REQUIRES IRON ARMOR
    create_region(world, "CanSmeltItems", "HasIronArmor", {
        "Suit Up": ADVANCEMENT
    }, canWearIronArmor())

    # REQUIRES DIAMOND TOOLS
    create_region(world, "HasIronTools", "HasDiamondTools", {
        "Ice Bucket Challenge": ADVANCEMENT
    }, canUseDiamondTools())

    # REQUIRES DIAMOND ARMOR
    create_region(world, "HasIronTools", "HasDiamondArmor", {
        "Cover Me with Diamonds": ADVANCEMENT
    }, canWearDiamondArmor())

    # REQUIRES ARMOR TRIMS
    create_region(world, "CanSmeltItems", "CanSmithItems", {
        "Crafting a New Look": ADVANCEMENT
    }, canGetAndUseArmorTrims())

    # REQUIRES NETHERITE TOOLS
    create_region(world, "CanSmithItems", "HasNetheriteTools", {
        "Serious Dedication": ADVANCEMENT_HARD
    }, canUseNetheriteTools())

    # REQUIRES NETHERITE Armor
    create_region(world, "CanSmithItems", "HasNetheriteArmor", {
        "Cover Me in Debris": ADVANCEMENT_HARD
    }, canWearNetheriteArmor())

    # REQUIRES BOW
    create_region(world, "Menu", "HasBow", {
        "Take Aim": ADVANCEMENT,
        "Bullseye": ADVANCEMENT,
        "Sniper Duel": ADVANCEMENT
    }, canUseBow())

    # REQUIRES CROSSBOW
    create_region(world, "CanSmeltItems", "HasCrossbow", {
        "Ol' Betsy": ADVANCEMENT,
        "Who's the Pillager Now?": ADVANCEMENT
    }, canUseCrossBow())
    smart_add_rule(world, "Who's the Pillager Now?", pillagerOutpostExploration(), ADVANCEMENT)

    # REQUIRES MINECART
    create_region(world, "CanSmeltItems", "HasMinecart", {
        "On A Rail": ADVANCEMENT
    }, canUseMinecart())

    # REQUIRES FISHING
    create_region(world, "Menu", "HasFishing", {
        "Fishy Business": ADVANCEMENT,
        "A Complete Catalogue": ADVANCEMENT_HARD
    }, canUseFishingRod())
    smart_add_rule(world, "A Complete Catalogue", villageExploration(), ADVANCEMENT_HARD)

    # REQUIRES BRUSH
    create_region(world, "CanSmeltItems", "HasBrush", {
        "Respecting the Remnants": ADVANCEMENT,
        "Careful Restoration": ADVANCEMENT
    }, canUseBrush() & ruinsExploration())

    # REQUIRES CHESTS
    create_region(world, "Menu", "HasChests", {
        "When Pigs Fly": ADVANCEMENT,
        "Overpowered": ADVANCEMENT_EXPLORATION
    }, canAccessChests())
    smart_add_rule(world, "Overpowered", ancientCityExploration() & bastionRemnantExploration() & desertPyramidExploration() & ruinedPortalExploration() & mansionExploration(), ADVANCEMENT_EXPLORATION)

    # REQUIRES TRADING
    create_region(world, "Menu", "HasTrading", {
        "What a Deal!": ADVANCEMENT
    }, canTrade())

    # REQUIRES ENCHANTING
    create_region(world, "HasDiamondTools", "HasEnchanting", {
        "Enchanter": ADVANCEMENT,
        "Librarian": ADVANCEMENT,
        "Total Beelocation": ADVANCEMENT,
        "Surge Protector": ADVANCEMENT_HARD
    }, canEnchant())
    smart_add_rule(world, "Surge Protector", weatherControl(), ADVANCEMENT_HARD)

    # REQUIRES BUCKET
    create_region(world, "CanSmeltItems", "HasBucket", {
        "Hot Stuff": ADVANCEMENT,
        "The Lie": ADVANCEMENT,
        "Bukkit Bukkit": ADVANCEMENT_EXPLORATION
    }, canUseBucket())
    smart_add_rule(world, "Bukkit Bukkit", wetlandBiomesExploration(), ADVANCEMENT_EXPLORATION)

    # REQUIRES BUCKET & IRON TOOLS
    create_region(world, "HasBucket", "HasBucketAndIronTools", {
        "Birthday Song": ADVANCEMENT_EXPLORATION
    }, canUseBucket() & canUseIronTools())
    smart_add_rule(world, "Birthday Song", pillagerOutpostExploration(), ADVANCEMENT_EXPLORATION)

    # REQUIRES BREWING
    create_region(world, "NetherAccess", "HasBrewing", {
        "Local Brewery": ADVANCEMENT,
        "A Furious Cocktail": ADVANCEMENT_HARD
    }, canBrew())

    # ZOMBIE DOCTOR
    create_region(world, "HasBrewing", "CanCureZombieVillager", {
        "Zombie Doctor": ADVANCEMENT
    }, canCureZombieVillager())

    # REQUIRES BARTERING
    create_region(world, "NetherAccess", "HasBartering", {
        "Oh Shiny": ADVANCEMENT
    }, canBarter())

    # REQUIRES SLEEP
    create_region(world, "Menu", "HasSleep", {
        "Sweet Dreams": ADVANCEMENT
    }, canSleep())

    # REQUIRES SPYGLASS
    create_region(world, "CanSmeltItems", "HasSpyglass", {
        "Is It a Bird?": ADVANCEMENT_EXPLORATION
    }, canUseSpyglass())
    smart_add_rule(world, "Is It a Bird?", jungleBiomesExploration(), ADVANCEMENT_EXPLORATION)

    # REQUIRES GLASS BOTTLES
    create_region(world, "CanSmeltItems", "HasBottles", {
        "Sticky Situation": ADVANCEMENT,
        "Bee Our Guest": ADVANCEMENT
    }, canUseBottles())

    # REQUIRES SWIMMING
    create_region(world, "Menu", "HasSwim", {
        "A Throwaway Joke": ADVANCEMENT,
        "Glow and Behold!": ADVANCEMENT,
        "The Healing Power of Friendship!": ADVANCEMENT
    }, canSwim())
    smart_add_rule(world, "The Healing Power of Friendship!", undergroundBiomesExploration() & canUseBucket(), ADVANCEMENT)

    # REQUIRES WITHER SUMMONING
    create_region(world, "NetherAccess", "CanSummonWither", {
        "Withering Heights": ADVANCEMENT
    }, canGoalWither())

    # REQUIRES BEACON
    create_region(world, "CanSummonWither", "CanUseBeacon", {
        "Bring Home the Beacon": ADVANCEMENT,
        "Beaconator": ADVANCEMENT_HARD
    }, canPlaceBeacon())

    # REQUIRES CRYING OBSIDIAN
    create_region(world, "Menu", "CanGetCryingObsidian", {
        "Who is Cutting Onions?": ADVANCEMENT,
        "Not Quite \"Nine\" Lives": ADVANCEMENT
    }, canGetCryingObsidian())

    # REQUIRES RAIDS
    create_locations_and_connect(world, "MenuVanillaAdvancements", "CanFightRaid", {
        "Hero of the Village": ADVANCEMENT,
        "Postmortal": ADVANCEMENT_EXPLORATION
    }, canFightRaid())
    smart_add_rule(world, "Hero of the Village", pillagerOutpostExploration() & villageExploration(), ADVANCEMENT)
    smart_add_rule(world, "Postmortal", pillagerOutpostExploration() & villageExploration(), ADVANCEMENT_EXPLORATION)

    ####################################################################################################################
    # MULTIPLE CHECKS ##################################################################################################
    ####################################################################################################################

    # REQUIRES CROSSBOW & ENCHANTING
    create_region(world, "HasCrossbow", "HasCrossbowAndEnchanting", {
        "Arbalistic": ADVANCEMENT_HARD,
        "Two Birds, One Arrow": ADVANCEMENT_HARD
    }, canUseCrossBow() & canEnchant())

    # REQUIRES TRADING & BUCKETS
    create_region(world, "HasTrading", "HasTradingAndBuckets", {
        "Star Trader": ADVANCEMENT
    }, canTrade() & canUseBucket())
    smart_add_rule(world, "Star Trader", villageExploration(), ADVANCEMENT)

    # REQUIRES SWIMMING & ENCHANTING
    create_region(world, "HasEnchanting", "HasSwimAndEnchanting", {
        "Very Very Frightening": ADVANCEMENT_HARD
    }, canSwim() & canEnchant())
    smart_add_rule(world, "Very Very Frightening", weatherControl(), ADVANCEMENT_HARD)

    # REQUIRES SWIMMING & BRUSH
    create_region(world, "HasBrush", "HasSwimAndBrush", {
        "Smells Interesting": ADVANCEMENT,
        "Little Sniffs": ADVANCEMENT_HARD,
        "Planting the Past": ADVANCEMENT_HARD
    }, canSwim() & canUseBrush() & ruinsExploration())

    # REQUIRES FISHING & SMELTING
    create_region(world, "CanSmeltItems", "CanSmeltItemsAndHasFishing", {
        "Delicious Fish": ADVANCEMENT
    }, canSmelt() & canUseFishingRod())

    # REQUIRES NETHERITE NO SMITHING
    create_region(world, "HasDiamondTools", "NetheriteNoSmithing", {
        "Country Lode, Take Me Home": ADVANCEMENT
    }, canSmelt() & canAccessNether() & canUseDiamondTools())

    # REQUIRES SHEARS & COMPACTING
    create_region(world, "CanSmeltItems", "HasShearsAndCompacting", {
        "Wax On": ADVANCEMENT,
        "Wax Off": ADVANCEMENT
    }, canUseShears() & canCompactResources())

    # REQUIRES BUCKET & SWIM
    create_region(world, "HasBucket", "HasBucketAndSwim", {
        "Caves & Cliffs": ADVANCEMENT,
        "Tactical Fishing": ADVANCEMENT,
        "The Cutest Predator": ADVANCEMENT
    }, canUseBucket() & canSwim())
    smart_add_rule(world, "The Cutest Predator", undergroundBiomesExploration(), ADVANCEMENT)

    # REQUIRES SPYGLASS & NETHER
    create_region(world, "HasSpyglass", "HasSpyglassNether", {
        "Is It a Balloon?": ADVANCEMENT
    }, canUseSpyglass() & canAccessNether())

    # REQUIRES SPYGLASS & END
    create_region(world, "HasSpyglass", "HasSpyglassEnd", {
        "Is It a Plane?": ADVANCEMENT
    }, canUseSpyglass() & canAccessEnd())

    # REQUIRES COMPACTING & SMELTING
    create_region(world, "CanSmeltItems", "CanSmeltAndCanCompact", {
        "Hired Help": ADVANCEMENT
    }, canGetIron() & canCompactResources() & canUseShears())

    # REQUIRES NETHER & FISHING ROD & CHESTS
    create_region(world, "NetherAccess", "NetherAccessAndFishingRodAndChests", {
        "This Boat Has Legs": ADVANCEMENT,
        "Feels Like Home": ADVANCEMENT_HARD
    }, canAccessNether() & canUseFishingRod() & canAccessChests())

    # REQUIRES END & SMELTING
    create_region(world, "EndAccess", "EndAccessAndSmelting", {
        "The End... Again...": ADVANCEMENT
    }, canAccessEnd() & canSmelt())

    # REQUIRES END & GLASS BOTTLES & SMELTING
    create_region(world, "EndAccessAndSmelting", "EndAccessAndGlassBottles", {
        "You Need a Mint": ADVANCEMENT
    }, canAccessEnd() & canSmelt() & canUseBottles())

    # REQUIRES VANILLA END GAME
    create_region(world, "EndAccess", "VanillaEndGame", {
        "Overkill": ADVANCEMENT,
        "Monsters Hunted": ADVANCEMENT_HARD,
        "Smithing with Style": ADVANCEMENT_UNREASONABLE,
        "Two by Two": ADVANCEMENT_HARD,
        "A Balanced Diet": ADVANCEMENT_HARD,
        "Adventuring Time": ADVANCEMENT_UNREASONABLE,
        "How Did We Get Here?": ADVANCEMENT_UNREASONABLE
    }, canAccessVanillaEndGame())

    # REQUIRES NETHER & CHESTS
    create_region(world, "NetherAccess", "NetherAccessAndChests", {
        "War Pigs": ADVANCEMENT
    }, canAccessNether() & canAccessChests())
    smart_add_rule(world, "War Pigs", bastionRemnantExploration(), ADVANCEMENT)

    # REQUIRES NETHER + DIAMOND TOOLS | CHESTS
    create_region(world, "NetherAccess", "NetherAccessGetDebree", {
        "Hidden in the Depths": ADVANCEMENT
    }, canAccessNether() & (canAccessChests() | canUseDiamondTools()))



def create_region(world: FabricMinecraftWorld, region_name: str, new_region_name: str, locations: dict[str, int], rule=None):
    create_locations_and_connect(world, region_name + "VanillaAdvancements", new_region_name + "VanillaAdvancements", locations, rule)