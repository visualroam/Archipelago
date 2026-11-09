from __future__ import annotations


from typing import TYPE_CHECKING, Optional

from worlds.minecraft_fabric.region.mc_regions_consts import *
from worlds.minecraft_fabric.region.regions_helper import create_locations_and_connect, smart_add_rule
from worlds.minecraft_fabric.logic.vanilla_logic import *



if TYPE_CHECKING:
   from worlds.minecraft_fabric import FabricMinecraftWorld

def create_vanilla_itemsanity_regions(world: FabricMinecraftWorld):
    create_locations_and_connect(world, "Menu", "MenuVanillaItemsanity", {
        "Dirt (Itemsanity)": ITEMSANITY,
        "Coarse Dirt (Itemsanity)": ITEMSANITY,
        "Rooted Dirt (Itemsanity)": ITEMSANITY,
        "Oak Planks (Itemsanity)": ITEMSANITY,
        "Spruce Planks (Itemsanity)": ITEMSANITY,
        "Birch Planks (Itemsanity)": ITEMSANITY,
        "Oak Sapling (Itemsanity)": ITEMSANITY,
        "Spruce Sapling (Itemsanity)": ITEMSANITY,
        "Birch Sapling (Itemsanity)": ITEMSANITY,
        "Sand (Itemsanity)": ITEMSANITY,
        "Gravel (Itemsanity)": ITEMSANITY,
        "Oak Log (Itemsanity)": ITEMSANITY,
        "Spruce Log (Itemsanity)": ITEMSANITY,
        "Birch Log (Itemsanity)": ITEMSANITY,
        "Stripped Oak Log (Itemsanity)": ITEMSANITY,
        "Stripped Spruce Log (Itemsanity)": ITEMSANITY,
        "Stripped Birch Log (Itemsanity)": ITEMSANITY,
        "Stripped Oak Wood (Itemsanity)": ITEMSANITY,
        "Stripped Spruce Wood (Itemsanity)": ITEMSANITY,
        "Stripped Birch Wood (Itemsanity)": ITEMSANITY,
        "Oak Wood (Itemsanity)": ITEMSANITY,
        "Spruce Wood (Itemsanity)": ITEMSANITY,
        "Birch Wood (Itemsanity)": ITEMSANITY,
        "Sandstone (Itemsanity)": ITEMSANITY,
        "Chiseled Sandstone (Itemsanity)": ITEMSANITY,
        "Cut Sandstone (Itemsanity)": ITEMSANITY,
        "Dandelion (Itemsanity)": FLOWER,
        "Poppy (Itemsanity)": FLOWER,
        "Allium (Itemsanity)": FLOWER,
        "Azure Bluet (Itemsanity)": FLOWER,
        "Red Tulip (Itemsanity)": FLOWER,
        "Orange Tulip (Itemsanity)": FLOWER,
        "White Tulip (Itemsanity)": FLOWER,
        "Pink Tulip (Itemsanity)": FLOWER,
        "Oxeye Daisy (Itemsanity)": FLOWER,
        "Cornflower (Itemsanity)": FLOWER,
        "Lily of the Valley (Itemsanity)": FLOWER,
        "Brown Mushroom (Itemsanity)": ITEMSANITY,
        "Red Mushroom (Itemsanity)": ITEMSANITY,
        "Sugar Cane (Itemsanity)": ITEMSANITY,
        "Oak Slab (Itemsanity)": SLAB,
        "Spruce Slab (Itemsanity)": SLAB,
        "Birch Slab (Itemsanity)": SLAB,
        "Chiseled Bookshelf (Itemsanity)": ITEMSANITY,
        "Torch (Itemsanity)": ITEMSANITY,
        "Crafting Table (Itemsanity)": ITEMSANITY,
        "Ladder (Itemsanity)": ITEMSANITY,
        "Granite (Itemsanity)": ITEMSANITY,
        "Polished Granite (Itemsanity)": ITEMSANITY,
        "Diorite (Itemsanity)": ITEMSANITY,
        "Polished Diorite (Itemsanity)": ITEMSANITY,
        "Andesite (Itemsanity)": ITEMSANITY,
        "Polished Andesite (Itemsanity)": ITEMSANITY,
        "Cobbled Deepslate (Itemsanity)": ITEMSANITY,
        "Polished Deepslate (Itemsanity)": ITEMSANITY,
        "Calcite (Itemsanity)": ITEMSANITY,
        "Tuff (Itemsanity)": ITEMSANITY,
        "Dripstone Block (Itemsanity)": ITEMSANITY,
        "Cobblestone (Itemsanity)": ITEMSANITY,
        "Block of Amethyst (Itemsanity)": ITEMSANITY,
        "Moss Carpet (Itemsanity)": ITEMSANITY,
        "Moss Block (Itemsanity)": ITEMSANITY,
        "Big Dripleaf (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Spore Blossom (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Azalea (Itemsanity)": ITEMSANITY,
        "Flowering Azalea (Itemsanity)": ITEMSANITY,
        "Sandstone Slab (Itemsanity)": SLAB,
        "Cut Sandstone Slab (Itemsanity)": SLAB,
        "Cobblestone Slab (Itemsanity)": SLAB,
        "Cobblestone Stairs (Itemsanity)": STAIR,
        "Snow (Itemsanity)": ITEMSANITY,
        "Snow Block (Itemsanity)": ITEMSANITY,
        "Clay (Itemsanity)": ITEMSANITY,
        "Clay Ball (Itemsanity)": ITEMSANITY,
        "Oak Fence (Itemsanity)": WALL,
        "Spruce Fence (Itemsanity)": WALL,
        "Birch Fence (Itemsanity)": WALL,
        "Pumpkin (Itemsanity)": ITEMSANITY,
        "Deepslate Bricks (Itemsanity)": ITEMSANITY,
        "Deepslate Tiles (Itemsanity)": ITEMSANITY,
        "Chiseled Deepslate (Itemsanity)": ITEMSANITY,
        "Melon (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Sandstone Stairs (Itemsanity)": STAIR,
        "Oak Stairs (Itemsanity)": STAIR,
        "Spruce Stairs (Itemsanity)": STAIR,
        "Birch Stairs (Itemsanity)": STAIR,
        "Cobblestone Wall (Itemsanity)": WALL,
        "Granite Wall (Itemsanity)": WALL,
        "Andesite Wall (Itemsanity)": WALL,
        "Sandstone Wall (Itemsanity)": WALL,
        "Diorite Wall (Itemsanity)": WALL,
        "Cobbled Deepslate Wall (Itemsanity)": WALL,
        "Polished Deepslate Wall (Itemsanity)": WALL,
        "Deepslate Brick Wall (Itemsanity)": WALL,
        "Deepslate Tile Wall (Itemsanity)": WALL,
        "Hay Bale (Itemsanity)": ITEMSANITY,
        "Lilac (Itemsanity)": FLOWER,
        "Rose Bush (Itemsanity)": FLOWER,
        "Peony (Itemsanity)": FLOWER,
        "Bone Block (Itemsanity)": ITEMSANITY,
        "Polished Granite Stairs (Itemsanity)": STAIR,
        "Polished Diorite Stairs (Itemsanity)": STAIR,
        "Granite Stairs (Itemsanity)": STAIR,
        "Andesite Stairs (Itemsanity)": STAIR,
        "Polished Andesite Stairs (Itemsanity)": STAIR,
        "Diorite Stairs (Itemsanity)": STAIR,
        "Cobbled Deepslate Stairs (Itemsanity)": STAIR,
        "Polished Deepslate Stairs (Itemsanity)": STAIR,
        "Deepslate Brick Stairs (Itemsanity)": STAIR,
        "Deepslate Tile Stairs (Itemsanity)": STAIR,
        "Polished Granite Slab (Itemsanity)": SLAB,
        "Polished Diorite Slab (Itemsanity)": SLAB,
        "Granite Slab (Itemsanity)": SLAB,
        "Andesite Slab (Itemsanity)": SLAB,
        "Polished Andesite Slab (Itemsanity)": SLAB,
        "Diorite Slab (Itemsanity)": SLAB,
        "Cobbled Deepslate Slab (Itemsanity)": SLAB,
        "Polished Deepslate Slab (Itemsanity)": SLAB,
        "Deepslate Brick Slab (Itemsanity)": SLAB,
        "Deepslate Tile Slab (Itemsanity)": SLAB,
        "Lever (Itemsanity)": ITEMSANITY,
        "Oak Button (Itemsanity)": ITEMSANITY,
        "Spruce Button (Itemsanity)": ITEMSANITY,
        "Birch Button (Itemsanity)": ITEMSANITY,
        "Oak Pressure Plate (Itemsanity)": ITEMSANITY,
        "Spruce Pressure Plate (Itemsanity)": ITEMSANITY,
        "Birch Pressure Plate (Itemsanity)": ITEMSANITY,
        "Oak Door (Itemsanity)": ITEMSANITY,
        "Spruce Door (Itemsanity)": ITEMSANITY,
        "Birch Door (Itemsanity)": ITEMSANITY,
        "Oak Trapdoor (Itemsanity)": ITEMSANITY,
        "Spruce Trapdoor (Itemsanity)": ITEMSANITY,
        "Birch Trapdoor (Itemsanity)": ITEMSANITY,
        "Oak Fence Gate (Itemsanity)": WALL,
        "Spruce Fence Gate (Itemsanity)": WALL,
        "Birch Fence Gate (Itemsanity)": WALL,
        "Oak Boat (Itemsanity)": ITEMSANITY,
        "Spruce Boat (Itemsanity)": ITEMSANITY,
        "Birch Boat (Itemsanity)": ITEMSANITY,
        "Apple (Itemsanity)": ITEMSANITY,
        "Arrow (Itemsanity)": ITEMSANITY,
        "Coal (Itemsanity)": ITEMSANITY,
        "Amethyst Shard (Itemsanity)": ITEMSANITY,
        "Wooden Sword (Itemsanity)": ITEMSANITY,
        "Wooden Shovel (Itemsanity)": ITEMSANITY,
        "Wooden Pickaxe (Itemsanity)": ITEMSANITY,
        "Wooden Axe (Itemsanity)": ITEMSANITY,
        "Wooden Hoe (Itemsanity)": ITEMSANITY,
        "Stick (Itemsanity)": ITEMSANITY,
        "Bowl (Itemsanity)": ITEMSANITY,
        "Mushroom Stew (Itemsanity)": ITEMSANITY,
        "String (Itemsanity)": ITEMSANITY,
        "Feather (Itemsanity)": ITEMSANITY,
        "Gunpowder (Itemsanity)": ITEMSANITY,
        "Wheat Seeds (Itemsanity)": ITEMSANITY,
        "Wheat (Itemsanity)": ITEMSANITY,
        "Bread (Itemsanity)": ITEMSANITY,
        "Flint (Itemsanity)": ITEMSANITY,
        "Raw Porkchop (Itemsanity)": ITEMSANITY,
        "Painting (Itemsanity)": ITEMSANITY,
        "Oak Sign (Itemsanity)": ITEMSANITY,
        "Spruce Sign (Itemsanity)": ITEMSANITY,
        "Birch Sign (Itemsanity)": ITEMSANITY,
        "Snowball (Itemsanity)": ITEMSANITY,
        "Leather (Itemsanity)": ITEMSANITY,
        "Paper (Itemsanity)": ITEMSANITY,
        "Book (Itemsanity)": ITEMSANITY,
        "Egg (Itemsanity)": ITEMSANITY,
        "Bone Meal (Itemsanity)": ITEMSANITY,
        "Bone (Itemsanity)": ITEMSANITY,
        "Sugar (Itemsanity)": ITEMSANITY,
        "Cookie (Itemsanity)": ITEMSANITY,
        "Pumpkin Seeds (Itemsanity)": ITEMSANITY,
        "Raw Beef (Itemsanity)": ITEMSANITY,
        "Raw Chicken (Itemsanity)": ITEMSANITY,
        "Rotten Flesh (Itemsanity)": ITEMSANITY,
        "Ender Pearl (Itemsanity)": ITEMSANITY,
        "Spider Eye (Itemsanity)": ITEMSANITY,
        "Fermented Spider Eye (Itemsanity)": ITEMSANITY,
        "Item Frame (Itemsanity)": ITEMSANITY,
        "Carrot (Itemsanity)": ITEMSANITY,
        "Potato (Itemsanity)": ITEMSANITY,
        "Poisonous Potato (Itemsanity)": ITEMSANITY,
        "Pumpkin Pie (Itemsanity)": ITEMSANITY,
        "Raw Rabbit (Itemsanity)": ITEMSANITY,
        "Rabbit's Foot (Itemsanity)": ITEMSANITY,
        "Rabbit Hide (Itemsanity)": ITEMSANITY,
        "Leather Horse Armor (Itemsanity)": ITEMSANITY,
        "Raw Mutton (Itemsanity)": ITEMSANITY,
        "Beetroot (Itemsanity)": ITEMSANITY,
        "Beetroot Seeds (Itemsanity)": ITEMSANITY,
        "Beetroot Soup (Itemsanity)": ITEMSANITY,
        "Phantom Membrane (Itemsanity)": ITEMSANITY,
        "Composter (Itemsanity)": ITEMSANITY,
        "Glow Berries (Itemsanity)": ITEMSANITY,
        "Pointed Dripstone (Itemsanity)": ITEMSANITY,
        "Firework Rocket (Itemsanity)": ITEMSANITY,
        "Suspicious Stew (Itemsanity)": ITEMSANITY,
        "Flower Charge Banner Pattern (Itemsanity)": ITEMSANITY,
        "Music Disc Blocks (Itemsanity)": DISCS,
        "Music Disc Chirp (Itemsanity)": DISCS,
        "Music Disc Far (Itemsanity)": DISCS,
        "Music Disc Mall (Itemsanity)": DISCS,
        "Music Disc Mellohi (Itemsanity)": DISCS,
        "Music Disc Stal (Itemsanity)": DISCS,
        "Music Disc Strad (Itemsanity)": DISCS,
        "Music Disc Ward (Itemsanity)": DISCS,
        "Music Disc 11 (Itemsanity)": DISCS,
        "Music Disc Wait (Itemsanity)": DISCS,

        "Bell (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cactus (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Sunflower (Itemsanity)": FLOWER_AND_EXPLORATION,
        "Sweet Berries (Itemsanity)": ITEMSANITY_EXPLORATION
    })
    smart_add_rule(world, "Rooted Dirt (Itemsanity)", undergroundBiomesExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Allium (Itemsanity)", forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Red Tulip (Itemsanity)", plainsBiomesExploration() | forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Orange Tulip (Itemsanity)", plainsBiomesExploration() | forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "White Tulip (Itemsanity)", plainsBiomesExploration() | forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Pink Tulip (Itemsanity)", plainsBiomesExploration() | forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Oxeye Daisy (Itemsanity)", plainsBiomesExploration() | forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Cornflower (Itemsanity)", plainsBiomesExploration() | forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Lily of the Valley (Itemsanity)", forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Brown Mushroom (Itemsanity)", forestBiomesExploration() | wetlandBiomesExploration() | canAccessNether(), ITEMSANITY)
    smart_add_rule(world, "Red Mushroom (Itemsanity)", forestBiomesExploration() | wetlandBiomesExploration() | canAccessNether(), ITEMSANITY)
    smart_add_rule(world, "Dripstone Block (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Moss Carpet (Itemsanity)", undergroundBiomesExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Moss Block (Itemsanity)", undergroundBiomesExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Big Dripleaf (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Spore Blossom (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Azalea (Itemsanity)", undergroundBiomesExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Flowering Azalea (Itemsanity)", undergroundBiomesExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Melon (Itemsanity)", jungleBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Lilac (Itemsanity)", forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Rose Bush (Itemsanity)", forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Peony (Itemsanity)", forestBiomesExploration(), FLOWER)
    smart_add_rule(world, "Mushroom Stew (Itemsanity)", forestBiomesExploration() | wetlandBiomesExploration() | canAccessNether(), ITEMSANITY)
    smart_add_rule(world, "Cookie (Itemsanity)", jungleBiomesExploration() | villageExploration(), ITEMSANITY)
    smart_add_rule(world, "Fermented Spider Eye (Itemsanity)", forestBiomesExploration() | wetlandBiomesExploration() | canAccessNether(), ITEMSANITY)
    smart_add_rule(world, "Carrot (Itemsanity)", villageExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Potato (Itemsanity)", villageExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Poisonous Potato (Itemsanity)", villageExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Raw Rabbit (Itemsanity)", highlandBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Rabbit's Foot (Itemsanity)", highlandBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Rabbit Hide (Itemsanity)", highlandBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Beetroot (Itemsanity)", villageExploration(), ITEMSANITY)
    smart_add_rule(world, "Beetroot Seeds (Itemsanity)", villageExploration(), ITEMSANITY)
    smart_add_rule(world, "Beetroot Soup (Itemsanity)", villageExploration(), ITEMSANITY)
    smart_add_rule(world, "Glow Berries (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Pointed Dripstone (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Suspicious Stew (Itemsanity)", forestBiomesExploration() | wetlandBiomesExploration() | canAccessNether(), ITEMSANITY)
    smart_add_rule(world, "Bell (Itemsanity)", villageExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Cactus (Itemsanity)", aridBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Sunflower (Itemsanity)", plainsBiomesExploration(), FLOWER_AND_EXPLORATION)
    smart_add_rule(world, "Sweet Berries (Itemsanity)", forestBiomesExploration(), ITEMSANITY_EXPLORATION)

    # SAVANNA BIOME NATURE COMPASS LOGIC
    create_region(world, "Menu", "Savanna Exploration", {
        "Acacia Planks (Itemsanity)": ITEMSANITY,
        "Acacia Sapling (Itemsanity)": ITEMSANITY,
        "Acacia Log (Itemsanity)": ITEMSANITY,
        "Stripped Acacia Log (Itemsanity)": ITEMSANITY,
        "Stripped Acacia Wood (Itemsanity)": ITEMSANITY,
        "Acacia Wood (Itemsanity)": ITEMSANITY,
        "Acacia Slab (Itemsanity)": SLAB,
        "Acacia Fence (Itemsanity)": WALL,
        "Acacia Stairs (Itemsanity)": STAIR,
        "Acacia Button (Itemsanity)": ITEMSANITY,
        "Acacia Pressure Plate (Itemsanity)": ITEMSANITY,
        "Acacia Door (Itemsanity)": ITEMSANITY,
        "Acacia Trapdoor (Itemsanity)": ITEMSANITY,
        "Acacia Fence Gate (Itemsanity)": WALL,
        "Acacia Boat (Itemsanity)": ITEMSANITY,
        "Acacia Sign (Itemsanity)": ITEMSANITY
    }, savannaBiomesExploration())

    # HIGHLANDS BIOME NATURE COMPASS LOGIC
    create_region(world, "Menu", "HighlandsExploration", {
        "Pink Petals (Itemsanity)": FLOWER_AND_EXPLORATION,

        "Cherry Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Boat (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Fence Gate (Itemsanity)": WALL_AND_EXPLORATION,
        "Cherry Trapdoor (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Door (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Pressure Plate (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Button (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
        "Cherry Fence (Itemsanity)": WALL_AND_EXPLORATION,
        "Cherry Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Cherry Wood (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Stripped Cherry Wood (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Stripped Cherry Log (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Log (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Planks (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cherry Sapling (Itemsanity)": ITEMSANITY_EXPLORATION
    }, highlandBiomesExploration())

    # FOREST BIOME NATURE COMPASS LOGIC
    create_region(world, "Menu", "ForestExploration", {
        "Dark Oak Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Boat (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Fence Gate (Itemsanity)": WALL_AND_EXPLORATION,
        "Dark Oak Trapdoor (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Door (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Pressure Plate (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Button (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
        "Dark Oak Fence (Itemsanity)": WALL_AND_EXPLORATION,
        "Dark Oak Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Dark Oak Wood (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Stripped Dark Oak Wood (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Stripped Dark Oak Log (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Log (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Planks (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Sapling (Itemsanity)": ITEMSANITY_EXPLORATION
    }, forestBiomesExploration())

    # WETLAND BIOME NATURE COMPASS LOGIC
    create_region(world, "Menu", "WetlandExploration", {
        "Slimeball (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Slime Block (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Blue Orchid (Itemsanity)": FLOWER_AND_EXPLORATION,
        "Lead (Itemsanity)": ITEMSANITY_EXPLORATION,

        "Mangrove Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Boat (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Fence Gate (Itemsanity)": WALL_AND_EXPLORATION,
        "Mangrove Trapdoor (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Door (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Pressure Plate (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Button (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
        "Mangrove Fence (Itemsanity)": WALL_AND_EXPLORATION,
        "Mangrove Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Mangrove Wood (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Stripped Mangrove Wood (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Stripped Mangrove Log (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Log (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Planks (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Propagule (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Roots (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Muddy Mangrove Roots (Itemsanity)": ITEMSANITY_EXPLORATION
    }, wetlandBiomesExploration())

    # JUNGLE BIOME NATURE COMPASS LOGIC
    create_region(world, "Menu", "JungleExploration", {
        "Cocoa Beans (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Melon Slice (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Melon Seeds (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Scaffolding (Itemsanity)": ITEMSANITY_EXPLORATION,

        "Bamboo Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Raft (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Fence Gate (Itemsanity)": WALL_AND_EXPLORATION,
        "Bamboo Trapdoor (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Door (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Pressure Plate (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Button (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
        "Bamboo Mosaic Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
        "Bamboo Fence (Itemsanity)": WALL_AND_EXPLORATION,
        "Bamboo Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Bamboo Mosaic Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Bamboo (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Block of Stripped Bamboo (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Block of Bamboo (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Planks (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Mosaic (Itemsanity)": ITEMSANITY_EXPLORATION,

        "Jungle Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Boat (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Fence Gate (Itemsanity)": WALL_AND_EXPLORATION,
        "Jungle Trapdoor (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Door (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Pressure Plate (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Button (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
        "Jungle Fence (Itemsanity)": WALL_AND_EXPLORATION,
        "Jungle Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Jungle Wood (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Stripped Jungle Wood (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Stripped Jungle Log (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Log (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Planks (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Jungle Sapling (Itemsanity)": ITEMSANITY_EXPLORATION
    }, jungleBiomesExploration())

    # REQUIRES NETHER ACCESS
    create_region(world, "Menu", "NetherAccess", {
        "Crimson Planks (Itemsanity)": ITEMSANITY,
        "Warped Planks (Itemsanity)": ITEMSANITY,
        "Crimson Stem (Itemsanity)": ITEMSANITY,
        "Warped Stem (Itemsanity)": ITEMSANITY,
        "Stripped Crimson Stem (Itemsanity)": ITEMSANITY,
        "Stripped Warped Stem (Itemsanity)": ITEMSANITY,
        "Stripped Crimson Hyphae (Itemsanity)": ITEMSANITY,
        "Stripped Warped Hyphae (Itemsanity)": ITEMSANITY,
        "Crimson Hyphae (Itemsanity)": ITEMSANITY,
        "Warped Hyphae (Itemsanity)": ITEMSANITY,
        "Crimson Fungus (Itemsanity)": ITEMSANITY,
        "Warped Fungus (Itemsanity)": ITEMSANITY,
        "Crimson Roots (Itemsanity)": ITEMSANITY,
        "Warped Roots (Itemsanity)": ITEMSANITY,
        "Weeping Vines (Itemsanity)": ITEMSANITY,
        "Twisting Vines (Itemsanity)": ITEMSANITY,
        "Crimson Slab (Itemsanity)": SLAB,
        "Warped Slab (Itemsanity)": SLAB,
        "Quartz Slab (Itemsanity)": SLAB,
        "Crimson Fence (Itemsanity)": WALL,
        "Warped Fence (Itemsanity)": WALL,
        "Netherrack (Itemsanity)": ITEMSANITY,
        "Soul Sand (Itemsanity)": ITEMSANITY,
        "Soul Soil (Itemsanity)": ITEMSANITY,
        "Basalt (Itemsanity)": ITEMSANITY,
        "Polished Basalt (Itemsanity)": ITEMSANITY,
        "Soul Torch (Itemsanity)": ITEMSANITY,
        "Glowstone (Itemsanity)": ITEMSANITY,
        "Crimson Stairs (Itemsanity)": STAIR,
        "Warped Stairs (Itemsanity)": STAIR,
        "Blackstone Wall (Itemsanity)": WALL,
        "Polished Blackstone Wall (Itemsanity)": WALL,
        "Polished Blackstone Brick Wall (Itemsanity)": WALL,
        "Chiseled Quartz Block (Itemsanity)": ITEMSANITY,
        "Block of Quartz (Itemsanity)": ITEMSANITY,
        "Quartz Bricks (Itemsanity)": ITEMSANITY,
        "Quartz Pillar (Itemsanity)": ITEMSANITY,
        "Quartz Stairs (Itemsanity)": STAIR,
        "Nether Wart Block (Itemsanity)": ITEMSANITY,
        "Warped Wart Block (Itemsanity)": ITEMSANITY,
        "Polished Blackstone Button (Itemsanity)": ITEMSANITY,
        "Crimson Button (Itemsanity)": ITEMSANITY,
        "Warped Button (Itemsanity)": ITEMSANITY,
        "Polished Blackstone Pressure Plate (Itemsanity)": ITEMSANITY,
        "Crimson Pressure Plate (Itemsanity)": ITEMSANITY,
        "Warped Pressure Plate (Itemsanity)": ITEMSANITY,
        "Crimson Door (Itemsanity)": ITEMSANITY,
        "Warped Door (Itemsanity)": ITEMSANITY,
        "Crimson Trapdoor (Itemsanity)": ITEMSANITY,
        "Warped Trapdoor (Itemsanity)": ITEMSANITY,
        "Crimson Fence Gate (Itemsanity)": WALL,
        "Warped Fence Gate (Itemsanity)": WALL,
        "Nether Quartz (Itemsanity)": ITEMSANITY,
        "Crimson Sign (Itemsanity)": ITEMSANITY,
        "Warped Sign (Itemsanity)": ITEMSANITY,
        "Glowstone Dust (Itemsanity)": ITEMSANITY,
        "Blaze Rod (Itemsanity)": ITEMSANITY,
        "Ghast Tear (Itemsanity)": ITEMSANITY,
        "Nether Wart (Itemsanity)": ITEMSANITY,
        "Blaze Powder (Itemsanity)": ITEMSANITY,
        "Magma Cream (Itemsanity)": ITEMSANITY,
        "Fire Charge (Itemsanity)": ITEMSANITY,
        "Spectral Arrow (Itemsanity)": ITEMSANITY,
        "Soul Campfire (Itemsanity)": ITEMSANITY,
        "Shroomlight (Itemsanity)": ITEMSANITY,
        "Blackstone (Itemsanity)": ITEMSANITY,
        "Blackstone Slab (Itemsanity)": SLAB,
        "Blackstone Stairs (Itemsanity)": STAIR,
        "Gilded Blackstone (Itemsanity)": ITEMSANITY,
        "Polished Blackstone (Itemsanity)": ITEMSANITY,
        "Polished Blackstone Slab (Itemsanity)": SLAB,
        "Polished Blackstone Stairs (Itemsanity)": STAIR,
        "Chiseled Polished Blackstone (Itemsanity)": ITEMSANITY,
        "Polished Blackstone Bricks (Itemsanity)": ITEMSANITY,
        "Polished Blackstone Brick Slab (Itemsanity)": SLAB,
        "Polished Blackstone Brick Stairs (Itemsanity)": STAIR,
        "Wither Skeleton Skull (Itemsanity)": ITEMSANITY,
        "Skull Charge Banner Pattern (Itemsanity)": ITEMSANITY,

        "Ochre Froglight (Itemsanity)": ITEMSANITY_HARD,
        "Verdant Froglight (Itemsanity)": ITEMSANITY_HARD,
        "Pearlescent Froglight (Itemsanity)": ITEMSANITY_HARD
    },  canAccessNether())
    smart_add_rule(world, "Blaze Rod (Itemsanity)", fortressExploration(), ITEMSANITY)
    smart_add_rule(world, "Nether Wart (Itemsanity)", fortressExploration() | bastionRemnantExploration(), ITEMSANITY)
    smart_add_rule(world, "Blaze Powder (Itemsanity)", fortressExploration(), ITEMSANITY)
    smart_add_rule(world, "Wither Skeleton Skull (Itemsanity)", fortressExploration(), ITEMSANITY)
    smart_add_rule(world, "Skull Charge Banner Pattern (Itemsanity)", fortressExploration(), ITEMSANITY)
    smart_add_rule(world, "Ochre Froglight (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_HARD)
    smart_add_rule(world, "Verdant Froglight (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_HARD)
    smart_add_rule(world, "Pearlescent Froglight (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_HARD)

    # REQUIRES END ACCESS
    create_region(world, "NetherAccess", "EndAccess", {
        "Dragon Egg (Itemsanity)": ITEMSANITY,
        "End Stone (Itemsanity)": ITEMSANITY,
        "End Stone Bricks (Itemsanity)": ITEMSANITY,
        "End Stone Brick Wall (Itemsanity)": WALL,
        "End Stone Brick Stairs (Itemsanity)": STAIR,
        "End Stone Brick Slab (Itemsanity)": SLAB,
        "Elytra (Itemsanity)": ITEMSANITY,
        "Dragon Head (Itemsanity)": ITEMSANITY,
        "Eye of Ender (Itemsanity)": ITEMSANITY,
        "End Crystal (Itemsanity)": ITEMSANITY,
        "Chorus Fruit (Itemsanity)": ITEMSANITY,
        "Shulker Shell (Itemsanity)": ITEMSANITY
    },  canAccessEnd())
    smart_add_rule(world, "Elytra (Itemsanity)", endCityExploration(), ITEMSANITY)
    smart_add_rule(world, "Dragon Head (Itemsanity)", endCityExploration(), ITEMSANITY)
    smart_add_rule(world, "Shulker Shell (Itemsanity)", endCityExploration(), ITEMSANITY)

    # REQUIRES STONE TOOLS
    create_region(world, "Menu", "HasStoneTools", {
        "Lapis Lazuli (Itemsanity)": ITEMSANITY,
        "Raw Iron (Itemsanity)": ITEMSANITY,
        "Raw Copper (Itemsanity)": ITEMSANITY,
        "Stone Shovel (Itemsanity)": ITEMSANITY,
        "Stone Pickaxe (Itemsanity)": ITEMSANITY,
        "Stone Hoe (Itemsanity)": ITEMSANITY
    },  canUseStoneTools())

    # REQUIRES STONE TOOLS
    create_region(world, "Menu", "HasStoneWeapons", {
        "Stone Sword (Itemsanity)": ITEMSANITY,
        "Stone Axe (Itemsanity)": ITEMSANITY
    },  canUseStoneWeapons())

    # REQUIRES LEATHER ARMOR
    create_region(world, "Menu", "HasLeatherArmor", {
        "Leather Cap (Itemsanity)": ITEMSANITY,
        "Leather Tunic (Itemsanity)": ITEMSANITY,
        "Leather Pants (Itemsanity)": ITEMSANITY,
        "Leather Boots (Itemsanity)": ITEMSANITY
    },  canWearLeatherArmor())

    # REQUIRES SMELTING
    create_region(world, "Menu", "CanSmeltItems", {
        "Glass (Itemsanity)": ITEMSANITY,
        "Tinted Glass (Itemsanity)": ITEMSANITY,
        "Smooth Stone Slab (Itemsanity)": SLAB,
        "Brick Slab (Itemsanity)": SLAB,
        "Bricks (Itemsanity)": ITEMSANITY,
        "Smooth Sandstone (Itemsanity)": ITEMSANITY,
        "Smooth Stone (Itemsanity)": ITEMSANITY,
        "Decorated Pot (Itemsanity)": ITEMSANITY,
        "Furnace (Itemsanity)": ITEMSANITY,
        "Cracked Stone Bricks (Itemsanity)": ITEMSANITY,
        "Glass Pane (Itemsanity)": ITEMSANITY,
        "Brick Stairs (Itemsanity)": STAIR,
        "Smooth Basalt (Itemsanity)": ITEMSANITY,
        "Brick Wall (Itemsanity)": WALL,
        "Terracotta (Itemsanity)": ITEMSANITY,
        "Smooth Sandstone Stairs (Itemsanity)": STAIR,
        "Smooth Sandstone Slab (Itemsanity)": SLAB,
        "Charcoal (Itemsanity)": ITEMSANITY,
        "Cooked Porkchop (Itemsanity)": ITEMSANITY,
        "Brick (Itemsanity)": ITEMSANITY,
        "Steak (Itemsanity)": ITEMSANITY,
        "Cooked Chicken (Itemsanity)": ITEMSANITY,
        "Flower Pot (Itemsanity)": ITEMSANITY,
        "Baked Potato (Itemsanity)": ITEMSANITY,
        "Cooked Rabbit (Itemsanity)": ITEMSANITY,
        "Rabbit Stew (Itemsanity)": ITEMSANITY,
        "Armor Stand (Itemsanity)": ITEMSANITY,
        "Cooked Mutton (Itemsanity)": ITEMSANITY,
        "Campfire (Itemsanity)": ITEMSANITY,
        "Cracked Deepslate Bricks (Itemsanity)": ITEMSANITY,
        "Cracked Deepslate Tiles (Itemsanity)": ITEMSANITY
    },  canSmelt())
    smart_add_rule(world, "Baked Potato (Itemsanity)", villageExploration() | shipwreckExploration(), ITEMSANITY)
    smart_add_rule(world, "Cooked Rabbit (Itemsanity)", highlandBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Rabbit Stew (Itemsanity)", highlandBiomesExploration() & (forestBiomesExploration() | wetlandBiomesExploration() | canAccessNether()) & (villageExploration() | shipwreckExploration()), ITEMSANITY)

    # CAN GET IRON
    create_region(world, "HasStoneTools", "CanSmeltItemsIron", {
        "Iron Bars (Itemsanity)": ITEMSANITY,
        "Tripwire Hook (Itemsanity)": ITEMSANITY,
        "Heavy Weighted Pressure Plate (Itemsanity)": ITEMSANITY,
        "Iron Door (Itemsanity)": ITEMSANITY,
        "Iron Trapdoor (Itemsanity)": ITEMSANITY,
        "Iron Ingot (Itemsanity)": ITEMSANITY,
        "Copper Ingot (Itemsanity)": ITEMSANITY,
        "Cauldron (Itemsanity)": ITEMSANITY,
    },  canGetIron())

    # REQUIRES SMELTING (x2)
    create_region(world, "CanSmeltItems", "CanSmeltItemsBetter", {
        "Smoker (Itemsanity)": ITEMSANITY
    },  canSmeltBetter())

    # REQUIRES SMELTING (x2) & IRON
    create_region(world, "CanSmeltItemsBetter", "CanSmeltItemsBetterAndMineIron", {
        "Blast Furnace (Itemsanity)": ITEMSANITY
    },  canSmeltBetter() & canUseStoneTools())

    # REQUIRES SHIELD
    create_region(world, "CanSmeltItems", "HasShield", {
        "Shield (Itemsanity)": ITEMSANITY
    },  canUseShield())

    # REQUIRES IRON TOOLS
    create_region(world, "CanSmeltItems", "HasIronTools", {
        "Jukebox (Itemsanity)": ITEMSANITY,
        "Redstone Dust (Itemsanity)": ITEMSANITY,
        "Redstone Torch (Itemsanity)": ITEMSANITY,
        "Redstone Repeater (Itemsanity)": ITEMSANITY,
        "Piston (Itemsanity)": ITEMSANITY,
        "Dropper (Itemsanity)": ITEMSANITY,
        "Target (Itemsanity)": ITEMSANITY,
        "Lightning Rod (Itemsanity)": ITEMSANITY,
        "Note Block (Itemsanity)": ITEMSANITY,
        "Diamond (Itemsanity)": ITEMSANITY,
        "Emerald (Itemsanity)": ITEMSANITY,
        "Raw Gold (Itemsanity)": ITEMSANITY,
        "Golden Shovel (Itemsanity)": ITEMSANITY,
        "Golden Pickaxe (Itemsanity)": ITEMSANITY,
        "Golden Hoe (Itemsanity)": ITEMSANITY,
        "Iron Shovel (Itemsanity)": ITEMSANITY,
        "Iron Pickaxe (Itemsanity)": ITEMSANITY,
        "Iron Hoe (Itemsanity)": ITEMSANITY,
        "Compass (Itemsanity)": ITEMSANITY,
        "Clock (Itemsanity)": ITEMSANITY,
        "Map (Itemsanity)": ITEMSANITY,

        "Sticky Piston (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canUseIronTools())
    smart_add_rule(world, "Sticky Piston (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)

    # CAN GET GOLD
    create_region(world, "Menu", "CanGetGold", {
        "Gold Ingot (Itemsanity)": ITEMSANITY,
        "Golden Apple (Itemsanity)": ITEMSANITY,
        "Light Weighted Pressure Plate (Itemsanity)": ITEMSANITY
    },  canGetGold())

    # CAN GET GOLD Nugget
    create_region(world, "Menu", "CanGetGoldNugget", {
        "Gold Nugget (Itemsanity)": ITEMSANITY,
        "Glistering Melon Slice (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Golden Carrot (Itemsanity)": ITEMSANITY
    },  canGetGoldNugget())
    smart_add_rule(world, "Glistering Melon Slice (Itemsanity)", jungleBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Golden Carrot (Itemsanity)", villageExploration() | shipwreckExploration(), ITEMSANITY)

    # REQUIRES IRON WEAPONS
    create_region(world, "CanSmeltItems", "HasIronWeapons", {
        "Iron Axe (Itemsanity)": ITEMSANITY,
        "Iron Sword (Itemsanity)": ITEMSANITY
    },  canUseIronWeapons())

    # REQUIRES IRON WEAPONS & GOLD
    create_region(world, "HasIronWeapons", "HasIronWeaponsAndGold", {
        "Golden Sword (Itemsanity)": ITEMSANITY,
        "Golden Axe (Itemsanity)": ITEMSANITY
    },  canUseIronWeapons() & canGetGold())

    # REQUIRES IRON ARMOR
    create_region(world, "CanSmeltItems", "HasIronArmor", {
        "Iron Helmet (Itemsanity)": ITEMSANITY,
        "Iron Chestplate (Itemsanity)": ITEMSANITY,
        "Iron Leggings (Itemsanity)": ITEMSANITY,
        "Iron Boots (Itemsanity)": ITEMSANITY
    },  canWearIronArmor())

    # REQUIRES GOLD ARMOR
    create_region(world, "CanSmeltItems", "HasGoldArmor", {
        "Golden Helmet (Itemsanity)": ITEMSANITY,
        "Golden Chestplate (Itemsanity)": ITEMSANITY,
        "Golden Leggings (Itemsanity)": ITEMSANITY,
        "Golden Boots (Itemsanity)": ITEMSANITY
    },  canWearGoldArmor())

    # REQUIRES DIAMOND TOOLS
    create_region(world, "HasIronTools", "HasDiamondTools", {
        "Obsidian (Itemsanity)": ITEMSANITY,
        "Diamond Shovel (Itemsanity)": ITEMSANITY,
        "Diamond Pickaxe (Itemsanity)": ITEMSANITY,
        "Diamond Hoe (Itemsanity)": ITEMSANITY
    },  canUseDiamondTools())

    # REQUIRES DIAMOND WEAPONS
    create_region(world, "HasIronTools", "HasDiamondWeapons", {
        "Diamond Sword (Itemsanity)": ITEMSANITY,
        "Diamond Axe (Itemsanity)": ITEMSANITY
    },  canUseDiamondWeapons())

    # REQUIRES DIAMOND ARMOR
    create_region(world, "HasIronTools", "HasDiamondArmor", {
        "Diamond Helmet (Itemsanity)": ITEMSANITY,
        "Diamond Chestplate (Itemsanity)": ITEMSANITY,
        "Diamond Leggings (Itemsanity)": ITEMSANITY,
        "Diamond Boots (Itemsanity)": ITEMSANITY
    },  canWearDiamondArmor())

    # REQUIRES ARMOR TRIMS
    create_region(world, "CanSmeltItems", "CanSmithItems", {
        "Smithing Table (Itemsanity)": ITEMSANITY
    },  canGetAndUseArmorTrims())

    # REQUIRES NETHERITE TOOLS
    create_region(world, "CanSmithItems", "HasNetheriteTools", {
        "Netherite Shovel (Itemsanity)": NETHERITE,
        "Netherite Pickaxe (Itemsanity)": NETHERITE,
        "Netherite Hoe (Itemsanity)": NETHERITE
    },  canUseNetheriteTools())

    # REQUIRES NETHERITE WEAPONS
    create_region(world, "CanSmithItems", "HasNetheriteWeapons", {
        "Netherite Sword (Itemsanity)": NETHERITE,
        "Netherite Axe (Itemsanity)": NETHERITE
    },  canUseNetheriteWeapons())

    # REQUIRES NETHERITE Armor
    create_region(world, "CanSmithItems", "HasNetheriteArmor", {
        "Netherite Helmet (Itemsanity)": NETHERITE,
        "Netherite Chestplate (Itemsanity)": NETHERITE,
        "Netherite Leggings (Itemsanity)": NETHERITE,
        "Netherite Boots (Itemsanity)": NETHERITE
    },  canWearNetheriteArmor())

    # REQUIRES BOW
    create_region(world, "Menu", "HasBow", {
        "Bow (Itemsanity)": ITEMSANITY
    },  canUseBow())

    # REQUIRES CROSSBOW
    create_region(world, "CanSmeltItems", "HasCrossbow", {
        "Crossbow (Itemsanity)": ITEMSANITY
    },  canUseCrossBow())

    # REQUIRES MINECART
    create_region(world, "CanSmeltItems", "HasMinecart", {
        "Rail (Itemsanity)": ITEMSANITY,
        "Minecart (Itemsanity)": ITEMSANITY,
        "Minecart with TNT (Itemsanity)": ITEMSANITY,
        "Minecart with Furnace (Itemsanity)": ITEMSANITY
    },  canUseMinecart())

    # REQUIRES FISHING
    create_region(world, "Menu", "HasFishing", {
        "Carrot on a Stick (Itemsanity)": ITEMSANITY,
        "Fishing Rod (Itemsanity)": ITEMSANITY
    },  canUseFishingRod())
    smart_add_rule(world, "Carrot on a Stick (Itemsanity)", villageExploration() | shipwreckExploration(), ITEMSANITY)

    # REQUIRES BRUSH
    create_region(world, "CanSmeltItems", "HasBrush", {
        "Brush (Itemsanity)": ITEMSANITY,

        "Music Disc Relic (Itemsanity)": DISCS,
        "Archer Pottery Sherd (Itemsanity)": SHERD,
        "Miner Pottery Sherd (Itemsanity)": SHERD,
        "Prize Pottery Sherd (Itemsanity)": SHERD,
        "Skull Pottery Sherd (Itemsanity)": SHERD,

        "Wayfinder Armor Trim (Itemsanity)": TRIM,
        "Shaper Armor Trim (Itemsanity)": TRIM,
        "Raiser Armor Trim (Itemsanity)": TRIM,
        "Host Armor Trim (Itemsanity)": TRIM,
        "Arms Up Pottery Sherd (Itemsanity)": SHERD,
        "Brewer Pottery Sherd (Itemsanity)": SHERD,
        "Burn Pottery Sherd (Itemsanity)": SHERD,
        "Danger Pottery Sherd (Itemsanity)": SHERD,
        "Friend Pottery Sherd (Itemsanity)": SHERD,
        "Heart Pottery Sherd (Itemsanity)": SHERD,
        "Heartbreak Pottery Sherd (Itemsanity)": SHERD,
        "Howl Pottery Sherd (Itemsanity)": SHERD,
        "Sheaf Pottery Sherd (Itemsanity)": SHERD
    },  canUseBrush() & ruinsExploration())

    # REQUIRES FLINT & STEEL
    create_region(world, "CanSmeltItems", "HasFlintAndSteel", {
        "Flint and Steel (Itemsanity)": ITEMSANITY
    },  canUseFlintAndSteel())

    # REQUIRES CHESTS
    create_region(world, "Menu", "HasChests", {
        "Chest (Itemsanity)": ITEMSANITY,
        "Saddle (Itemsanity)": ITEMSANITY,
        "Oak Boat with Chest (Itemsanity)": ITEMSANITY,
        "Spruce Boat with Chest (Itemsanity)": ITEMSANITY,
        "Birch Boat with Chest (Itemsanity)": ITEMSANITY,
        "Jungle Boat with Chest (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Acacia Boat with Chest (Itemsanity)": ITEMSANITY,
        "Cherry Boat with Chest (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Boat with Chest (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Boat with Chest (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Raft with Chest (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Iron Horse Armor (Itemsanity)": ITEMSANITY,
        "Golden Horse Armor (Itemsanity)": ITEMSANITY,
        "Diamond Horse Armor (Itemsanity)": ITEMSANITY,
        "Name Tag (Itemsanity)": ITEMSANITY,
        "Barrel (Itemsanity)": ITEMSANITY,
        "Music Disc 13 (Itemsanity)": DISCS,
        "Music Disc Cat (Itemsanity)": DISCS,

        "Enchanted Golden Apple (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Thing Banner Pattern (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Tall Grass (Itemsanity)": ITEMSANITY_UNREASONABLE,
        "Large Fern (Itemsanity)": ITEMSANITY_UNREASONABLE,
        "Echo Shard (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Goat Horn (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Music Disc 5 (Itemsanity)": DISCS,
        "Disc 5 Fragment (Itemsanity)": DISCS,
        "Music Disc Otherside (Itemsanity)": DISCS,
        "Sentry Armor Trim (Itemsanity)": TRIM,
        "Dune Armor Trim (Itemsanity)": TRIM,
        "Vex Armor Trim (Itemsanity)": TRIM,

        "Wild Armor Trim (Itemsanity)": TRIM,
        "Ward Armor Trim (Itemsanity)": TRIM,
        "Silence Armor Trim (Itemsanity)": TRIM,
    },  canAccessChests())
    smart_add_rule(world, "Jungle Boat with Chest (Itemsanity)", jungleBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Acacia Boat with Chest (Itemsanity)", savannaBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Cherry Boat with Chest (Itemsanity)", highlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Dark Oak Boat with Chest (Itemsanity)", forestBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Mangrove Boat with Chest (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Bamboo Raft with Chest (Itemsanity)", jungleBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Iron Horse Armor (Itemsanity)", fortressExploration() & desertPyramidExploration(), ITEMSANITY)
    smart_add_rule(world, "Golden Horse Armor (Itemsanity)", fortressExploration() & desertPyramidExploration(), ITEMSANITY)
    smart_add_rule(world, "Diamond Horse Armor (Itemsanity)", fortressExploration() & desertPyramidExploration(), ITEMSANITY)
    smart_add_rule(world, "Enchanted Golden Apple (Itemsanity)", ancientCityExploration() & bastionRemnantExploration() & desertPyramidExploration() & ruinedPortalExploration() & mansionExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Thing Banner Pattern (Itemsanity)", ancientCityExploration() & bastionRemnantExploration() & desertPyramidExploration() & ruinedPortalExploration() & mansionExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Tall Grass (Itemsanity)", villageExploration(), ITEMSANITY_UNREASONABLE)
    smart_add_rule(world, "Large Fern (Itemsanity)", villageExploration(), ITEMSANITY_UNREASONABLE)
    smart_add_rule(world, "Goat Horn (Itemsanity)", pillagerOutpostExploration() | highlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Echo Shard (Itemsanity)", ancientCityExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Music Disc 5 (Itemsanity)", ancientCityExploration(), DISCS)
    smart_add_rule(world, "Disc 5 Fragment (Itemsanity)", ancientCityExploration(), DISCS)
    smart_add_rule(world, "Music Disc Otherside (Itemsanity)", ancientCityExploration(), DISCS)
    smart_add_rule(world, "Sentry Armor Trim (Itemsanity)", pillagerOutpostExploration(), TRIM)
    smart_add_rule(world, "Dune Armor Trim (Itemsanity)", desertPyramidExploration(), TRIM)
    smart_add_rule(world, "Vex Armor Trim (Itemsanity)", mansionExploration(), TRIM)
    smart_add_rule(world, "Wild Armor Trim (Itemsanity)", junglePyramidExploration(), TRIM)
    smart_add_rule(world, "Ward Armor Trim (Itemsanity)", ancientCityExploration(), TRIM)
    smart_add_rule(world, "Silence Armor Trim (Itemsanity)", ancientCityExploration(), TRIM)

    # REQUIRES ENCHANTING
    create_region(world, "HasDiamondTools", "HasEnchanting", {
        "Grass Block (Itemsanity)": ITEMSANITY,
        "Podzol (Itemsanity)": ITEMSANITY,
        "Coal Ore (Itemsanity)": ITEMSANITY,
        "Iron Ore (Itemsanity)": ITEMSANITY,
        "Deepslate Iron Ore (Itemsanity)": ITEMSANITY,
        "Copper Ore (Itemsanity)": ITEMSANITY,
        "Deepslate Copper Ore (Itemsanity)": ITEMSANITY,
        "Gold Ore (Itemsanity)": ITEMSANITY,
        "Deepslate Gold Ore (Itemsanity)": ITEMSANITY,
        "Redstone Ore (Itemsanity)": ITEMSANITY,
        "Deepslate Redstone Ore (Itemsanity)": ITEMSANITY,
        "Emerald Ore (Itemsanity)": ITEMSANITY,
        "Lapis Lazuli Ore (Itemsanity)": ITEMSANITY,
        "Deepslate Lapis Lazuli Ore (Itemsanity)": ITEMSANITY,
        "Deepslate Diamond Ore (Itemsanity)": ITEMSANITY,
        "Bookshelf (Itemsanity)": ITEMSANITY,
        "Ice (Itemsanity)": ITEMSANITY,
        "Brown Mushroom Block (Itemsanity)": ITEMSANITY,
        "Red Mushroom Block (Itemsanity)": ITEMSANITY,
        "Mushroom Stem (Itemsanity)": ITEMSANITY,
        "Sculk (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Sculk Vein (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Sculk Catalyst (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Sculk Shrieker (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Enchanting Table (Itemsanity)": ITEMSANITY,
        "Anvil (Itemsanity)": ITEMSANITY,
        "Chipped Anvil (Itemsanity)": ITEMSANITY,
        "Damaged Anvil (Itemsanity)": ITEMSANITY,
        "Packed Ice (Itemsanity)": ITEMSANITY,
        "Blue Ice (Itemsanity)": ITEMSANITY,
        "Lectern (Itemsanity)": ITEMSANITY,
        "Sculk Sensor (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Calibrated Sculk Sensor (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bee Nest (Itemsanity)": ITEMSANITY,
        "Small Amethyst Bud (Itemsanity)": ITEMSANITY,
        "Medium Amethyst Bud (Itemsanity)": ITEMSANITY,
        "Large Amethyst Bud (Itemsanity)": ITEMSANITY,
        "Amethyst Cluster (Itemsanity)": ITEMSANITY,

        "Deepslate Coal Ore (Itemsanity)": RARE_ORE,
        "Deepslate Emerald Ore (Itemsanity)": RARE_ORE,
        "Diamond Ore (Itemsanity)": RARE_ORE
    },  canEnchant())
    smart_add_rule(world, "Podzol (Itemsanity)", forestBiomesExploration() | jungleBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Brown Mushroom Block (Itemsanity)", forestBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Red Mushroom Block (Itemsanity)", forestBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Sculk (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Sculk Vein (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Sculk Catalyst (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Sculk Shrieker (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Sculk Sensor (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Calibrated Sculk Sensor (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)

    # REQUIRES BUCKET
    create_region(world, "CanSmeltItems", "HasBucket", {
        "Bucket (Itemsanity)": ITEMSANITY,
        "Water Bucket (Itemsanity)": ITEMSANITY,
        "Lava Bucket (Itemsanity)": ITEMSANITY,
        "Milk Bucket (Itemsanity)": ITEMSANITY,
        "Cake (Itemsanity)": ITEMSANITY,

        "Powder Snow Bucket (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canUseBucket())
    smart_add_rule(world, "Powder Snow Bucket (Itemsanity)", highlandBiomesExploration(), ITEMSANITY_EXPLORATION)

    # REQUIRES TNT
    create_region(world, "Menu", "HasTNT", {
        "TNT (Itemsanity)": ITEMSANITY,
    },  hasTNT())

    # REQUIRES SMOOTH STONE OBTAINING
    create_region(world, "Menu", "CanGetSmoothStone", {
        "Stone (Itemsanity)": ITEMSANITY,
        "Stone Slab (Itemsanity)": SLAB,
        "Stone Brick Slab (Itemsanity)": SLAB,
        "Chiseled Stone Bricks (Itemsanity)": ITEMSANITY,
        "Stone Bricks (Itemsanity)": ITEMSANITY,
        "Stone Brick Stairs (Itemsanity)": STAIR,
        "Stone Brick Wall (Itemsanity)": WALL,
        "Stone Stairs (Itemsanity)": STAIR,
        "Stone Button (Itemsanity)": ITEMSANITY,
        "Stone Pressure Plate (Itemsanity)": ITEMSANITY,
        "Deepslate (Itemsanity)": ITEMSANITY
    },  canEnchant() | canSmelt())

    # REQUIRES BREWING
    create_region(world, "NetherAccess", "HasBrewing", {
        "Brewing Stand (Itemsanity)": ITEMSANITY
    },  canBrew())

    # REQUIRES SPYGLASS
    create_region(world, "CanSmeltItems", "HasSpyglass", {
        "Spyglass (Itemsanity)": ITEMSANITY
    },  canUseSpyglass())

    # REQUIRES GLASS BOTTLES
    create_region(world, "CanSmeltItems", "HasBottles", {
        "Honey Block (Itemsanity)": ITEMSANITY,
        "Glass Bottle (Itemsanity)": ITEMSANITY,
        "Honey Bottle (Itemsanity)": ITEMSANITY,

        "Mud Brick Wall (Itemsanity)": WALL,
        "Mud Brick Stairs (Itemsanity)": STAIR,
        "Packed Mud (Itemsanity)": ITEMSANITY,
        "Mud Bricks (Itemsanity)": ITEMSANITY,
        "Mud (Itemsanity)": ITEMSANITY,
        "Mud Brick Slab (Itemsanity)": SLAB,
    },  canUseBottles())

    # REQUIRES SWIMMING
    create_region(world, "Menu", "HasSwim", {
        "Sea Pickle (Itemsanity)": ITEMSANITY,
        "Kelp (Itemsanity)": ITEMSANITY,
        "Ink Sac (Itemsanity)": ITEMSANITY,
        "Glow Ink Sac (Itemsanity)": ITEMSANITY,
        "Book and Quill (Itemsanity)": ITEMSANITY,
        "Glow Item Frame (Itemsanity)": ITEMSANITY,
        "Trident (Itemsanity)": ITEMSANITY,
        "Nautilus Shell (Itemsanity)": ITEMSANITY,

        "Lily Pad (Itemsanity)": ITEMSANITY_EXPLORATION,

        "Dark Prismarine Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Dark Prismarine (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Prismarine Stairs (Itemsanity)": STAIR_AND_EXPLORATION,

        "Sea Lantern (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Wet Sponge (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Tide Armor Trim (Itemsanity)": TRIM
    },  canSwim())
    smart_add_rule(world, "Sea Pickle (Itemsanity)", oceanBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Lily Pad (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Dark Prismarine Slab (Itemsanity)", monumentExploration(), SLAB_AND_EXPLORATION)
    smart_add_rule(world, "Dark Prismarine (Itemsanity)", monumentExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Dark Prismarine Stairs (Itemsanity)", monumentExploration(), STAIR_AND_EXPLORATION)
    smart_add_rule(world, "Sea Lantern (Itemsanity)", monumentExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Wet Sponge (Itemsanity)", monumentExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Tide Armor Trim (Itemsanity)", monumentExploration(), TRIM)

    # REQUIRES PRISMARINE
    create_region(world, "Menu", "CanGetPrismarine", {
        "Prismarine Shard (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Prismarine Crystals (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Prismarine Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Prismarine Brick Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        "Prismarine Wall (Itemsanity)": WALL_AND_EXPLORATION,
        "Prismarine (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Prismarine Bricks (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Prismarine Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
        "Prismarine Brick Stairs (Itemsanity)": STAIR_AND_EXPLORATION
    }, canGetPrismarine())

    # REQUIRES WITHER SUMMONING
    create_region(world, "NetherAccess", "CanSummonWither", {
        "Wither Rose (Itemsanity)": ITEMSANITY,
        "Nether Star (Itemsanity)": ITEMSANITY
    },  canGoalWither())

    # REQUIRES BEACON
    create_region(world, "CanSummonWither", "CanUseBeacon", {
        "Beacon (Itemsanity)": ITEMSANITY
    },  canPlaceBeacon())

    # REQUIRES CRYING OBSIDIAN
    create_region(world, "Menu", "CanGetCryingObsidian", {
        "Crying Obsidian (Itemsanity)": ITEMSANITY,
        "Respawn Anchor (Itemsanity)": ITEMSANITY
    },  canGetCryingObsidian())

    # REQUIRES SHEARS
    create_region(world, "CanSmeltItemsIron", "HasShears", {
        "Grass (Itemsanity)": ITEMSANITY,
        "Fern (Itemsanity)": ITEMSANITY,
        "Dead Bush (Itemsanity)": ITEMSANITY,
        "Small Dripleaf (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mossy Cobblestone (Itemsanity)": ITEMSANITY,
        "Mossy Stone Bricks (Itemsanity)": ITEMSANITY,
        "Vines (Itemsanity)": ITEMSANITY,
        "Glow Lichen (Itemsanity)": ITEMSANITY,
        "Mossy Cobblestone Wall (Itemsanity)": WALL,
        "Mossy Stone Brick Wall (Itemsanity)": WALL,
        "Mossy Stone Brick Stairs (Itemsanity)": STAIR,
        "Mossy Cobblestone Stairs (Itemsanity)": STAIR,
        "Mossy Stone Brick Slab (Itemsanity)": SLAB,
        "Mossy Cobblestone Slab (Itemsanity)": SLAB,
        "Shears (Itemsanity)": ITEMSANITY,
        "Honeycomb (Itemsanity)": ITEMSANITY,
        "Beehive (Itemsanity)": ITEMSANITY,
        "Honeycomb Block (Itemsanity)": ITEMSANITY,
        "Hanging Roots (Itemsanity)": ITEMSANITY,
        "Candle (Itemsanity)": ITEMSANITY,
        "Carved Pumpkin (Itemsanity)": ITEMSANITY,
        "Jack o'Lantern (Itemsanity)": ITEMSANITY,
    },  canUseShears())
    smart_add_rule(world, "Dead Bush (Itemsanity)", aridBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Small Dripleaf (Itemsanity)", undergroundBiomesExploration(), ITEMSANITY_EXPLORATION)

    # REQUIRES MISC CRAFTING
    create_region(world, "Menu", "CanCraftMiscStations", {
        "Loom (Itemsanity)": ITEMSANITY,
        "Cartography Table (Itemsanity)": ITEMSANITY,
        "Fletching Table (Itemsanity)": ITEMSANITY,
    },  canAccessMiscJobsites())

    # REQUIRES MISC CRAFTING & SMELT
    create_region(world, "Menu", "CanCraftMiscStationsAndSmelt", {
        "Grindstone (Itemsanity)": ITEMSANITY
    },  canAccessMiscJobsites() & canSmelt())

    # REQUIRES MISC CRAFTING & SMELT & STONE TOOLS
    create_region(world, "CanCraftMiscStationsAndSmelt", "CanCraftMiscStationsAndSmeltAndStoneTools", {
        "Stonecutter (Itemsanity)": ITEMSANITY
    },  canAccessMiscJobsites() & canGetIron())

    # REQUIRES TRADING
    create_region(world, "Menu", "HasTrading", {
        "Chainmail Helmet (Itemsanity)": ITEMSANITY_HARD,
        "Chainmail Chestplate (Itemsanity)": ITEMSANITY_HARD,
        "Chainmail Leggings (Itemsanity)": ITEMSANITY_HARD,
        "Chainmail Boots (Itemsanity)": ITEMSANITY_HARD,
        "Globe Banner Pattern (Itemsanity)": ITEMSANITY_HARD,

        "Bottle o' Enchanting (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canTrade())
    smart_add_rule(world, "Bottle o' Enchanting (Itemsanity)", ancientCityExploration() | pillagerOutpostExploration() | villageExploration(), ITEMSANITY_EXPLORATION)

    # REQUIRES RAIDS
    create_region(world, "Menu", "CanFightRaids", {
        "Totem of Undying (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canFightRaid())
    smart_add_rule(world, "Totem of Undying (Itemsanity)", pillagerOutpostExploration(), ITEMSANITY_EXPLORATION)

    ####################################################################################################################
    # MULTIPLE CHECKS ##################################################################################################
    ####################################################################################################################

    # REQUIRES BUCKET & NETHER ACCESS | SHEARS
    create_region(world, "Menu", "HasBucketAndNetherOrShears", {
        "Suspicious Sand (Itemsanity)": ITEMSANITY_HARD,
        "Suspicious Gravel (Itemsanity)": ITEMSANITY_HARD,
    },  canUseShears() | canEnchant() | (canUseBucket() & canAccessNether()))

    # REQUIRES SWIMMING & ENCHANTING
    create_region(world, "HasEnchanting", "HasSwimAndEnchanting", {
        "Zombie Head (Itemsanity)": MOB_HEADS,
        "Skeleton Skull (Itemsanity)": MOB_HEADS,
        "Creeper Head (Itemsanity)": MOB_HEADS,
        "Creeper Charge Banner Pattern (Itemsanity)": MOB_HEADS,

        "Mycelium (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canSwim() & canEnchant())
    smart_add_rule(world, "Zombie Head (Itemsanity)", weatherControl(), MOB_HEADS)
    smart_add_rule(world, "Skeleton Skull (Itemsanity)", weatherControl(), MOB_HEADS)
    smart_add_rule(world, "Creeper Head (Itemsanity)", weatherControl(), MOB_HEADS)
    smart_add_rule(world, "Creeper Charge Banner Pattern (Itemsanity)", weatherControl(), MOB_HEADS)
    smart_add_rule(world, "Mycelium (Itemsanity)", plainsBiomesExploration(), ITEMSANITY_EXPLORATION)

    create_region(world, "HasSwimAndEnchanting", "HasSwimAndEnchantingandOceans", {
            "Tube Coral Block (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Brain Coral Block (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Bubble Coral Block (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Fire Coral Block (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Horn Coral Block (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Tube Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Brain Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Bubble Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Fire Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Horn Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Brain Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Bubble Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Fire Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Horn Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Tube Coral (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Tube Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Brain Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Bubble Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Fire Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Horn Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Tube Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Brain Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Bubble Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Fire Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Dead Horn Coral Fan (Itemsanity)": ITEMSANITY_EXPLORATION
        },  canSwim() & canEnchant() & oceanBiomesExploration())

    # REQUIRES SWIMMING & ENCHANTING & NETHER
    create_region(world, "HasSwimAndEnchanting", "HasSwimAndEnchantingAndNether", {
        "Piglin Head (Itemsanity)": MOB_HEADS,
    },  canSwim() & canEnchant() & canAccessNether())

    # REQUIRES SWIMMING & BRUSH
    create_region(world, "HasBrush", "HasSwimAndBrush", {
        "Sniffer Egg (Itemsanity)": ITEMSANITY_HARD,
        "Torchflower Seeds (Itemsanity)": FLOWER_AND_HARD,
        "Pitcher Pod (Itemsanity)": FLOWER_AND_HARD,
        "Torchflower (Itemsanity)": FLOWER_AND_HARD,
        "Pitcher Plant (Itemsanity)": FLOWER_AND_HARD,

        "Angler Pottery Sherd (Itemsanity)": SHERD,
        "Shelter Pottery Sherd (Itemsanity)": SHERD,
        "Snort Pottery Sherd (Itemsanity)": SHERD,
        "Blade Pottery Sherd (Itemsanity)": SHERD,
        "Explorer Pottery Sherd (Itemsanity)": SHERD,
        "Mourner Pottery Sherd (Itemsanity)": SHERD,
        "Plenty Pottery Sherd (Itemsanity)": SHERD
    },  canSwim() & canUseBrush() & ruinsExploration())

    # REQUIRES SWIMMING & SHEARS
    create_region(world, "HasShears", "HasSwimAndShears", {
        "Seagrass (Itemsanity)": ITEMSANITY,
        "Scute (Itemsanity)": ITEMSANITY_HARD,
        "Turtle Shell (Itemsanity)": ITEMSANITY_UNREASONABLE
    },  canUseShears() & canSwim())
    smart_add_rule(world, "Scute (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_HARD)
    smart_add_rule(world, "Turtle Shell (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_UNREASONABLE)

    # REQUIRES SWIMMING & CHESTS
    create_region(world, "HasSwim", "HasSwimAndChests", {
        "Heart of the Sea (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Conduit (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Coast Armor Trim (Itemsanity)": TRIM
    },  canAccessChests() & canSwim())
    smart_add_rule(world, "Heart of the Sea (Itemsanity)", buriedTreasureExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Conduit (Itemsanity)", buriedTreasureExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Coast Armor Trim (Itemsanity)", shipwreckExploration(), TRIM)

    # REQUIRES EYES OF ENDER & CHESTS
    create_region(world, "HasChests", "HasChestsAndEyesOfEnder", {
        "Eye Armor Trim (Itemsanity)": TRIM
    },  canAccessChests() & canGetEyesOfEnder())

    # REQUIRES SWIMMING & SMELTING
    create_region(world, "CanSmeltItems", "HasSwimAndSmelting", {
        "Dried Kelp Block (Itemsanity)": ITEMSANITY,
        "Dried Kelp (Itemsanity)": ITEMSANITY
    },  canSmelt() & canSwim())

    # REQUIRES SWIMMING & STONE TOOLS
    create_region(world, "HasStoneTools", "HasSwimAndStoneTools", {
        "Dead Tube Coral Block (Itemsanity)": ITEMSANITY,
        "Dead Brain Coral Block (Itemsanity)": ITEMSANITY,
        "Dead Bubble Coral Block (Itemsanity)": ITEMSANITY,
        "Dead Fire Coral Block (Itemsanity)": ITEMSANITY,
        "Dead Horn Coral Block (Itemsanity)": ITEMSANITY
    },  canSmelt() & canSwim() & oceanBiomesExploration())

    # REQUIRES SHEARS & COMPACTING
    create_region(world, "CanSmeltItems", "HasShearsAndCompacting", {
        "Waxed Block of Copper (Itemsanity)": ITEMSANITY,
        "Waxed Exposed Copper (Itemsanity)": ITEMSANITY,
        "Waxed Weathered Copper (Itemsanity)": ITEMSANITY,
        "Waxed Oxidized Copper (Itemsanity)": ITEMSANITY,
        "Waxed Cut Copper (Itemsanity)": ITEMSANITY,
        "Waxed Exposed Cut Copper (Itemsanity)": ITEMSANITY,
        "Waxed Weathered Cut Copper (Itemsanity)": ITEMSANITY,
        "Waxed Oxidized Cut Copper (Itemsanity)": ITEMSANITY,
        "Waxed Cut Copper Stairs (Itemsanity)": STAIR,
        "Waxed Exposed Cut Copper Stairs (Itemsanity)": STAIR,
        "Waxed Weathered Cut Copper Stairs (Itemsanity)": STAIR,
        "Waxed Oxidized Cut Copper Stairs (Itemsanity)": STAIR,
        "Waxed Cut Copper Slab (Itemsanity)": SLAB,
        "Waxed Exposed Cut Copper Slab (Itemsanity)": SLAB,
        "Waxed Weathered Cut Copper Slab (Itemsanity)": SLAB,
        "Waxed Oxidized Cut Copper Slab (Itemsanity)": SLAB
    },  canUseShears() & canCompactResources())

    # REQUIRES BUCKET & SWIM
    create_region(world, "HasBucket", "HasBucketAndSwim", {
        "Bucket of Pufferfish (Itemsanity)": ITEMSANITY,
        "Bucket of Salmon (Itemsanity)": ITEMSANITY,
        "Bucket of Cod (Itemsanity)": ITEMSANITY,
        "Bucket of Tropical Fish (Itemsanity)": ITEMSANITY,
        "Bucket of Axolotl (Itemsanity)": ITEMSANITY,

        "Bucket of Tadpole (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canUseBucket() & canSwim())
    smart_add_rule(world, "Bucket of Pufferfish (Itemsanity)", oceanBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Bucket of Tropical Fish (Itemsanity)", oceanBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Bucket of Tadpole (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)

    # REQUIRES SMELT & SWIM
    create_region(world, "HasSwim", "HasSmeltAndSwim", {
        "Sponge (Itemsanity)": ITEMSANITY_EXPLORATION,
    },  canSmelt() & canSwim() & monumentExploration())

    # REQUIRES COMPACTING & SMELTING
    create_region(world, "CanSmeltItems", "CanSmeltAndCanCompact", {
        "Block of Iron (Itemsanity)": ITEMSANITY,
        "Block of Copper (Itemsanity)": ITEMSANITY,
        "Exposed Copper (Itemsanity)": ITEMSANITY,
        "Weathered Copper (Itemsanity)": ITEMSANITY,
        "Oxidized Copper (Itemsanity)": ITEMSANITY,
        "Cut Copper (Itemsanity)": ITEMSANITY,
        "Exposed Cut Copper (Itemsanity)": ITEMSANITY,
        "Weathered Cut Copper (Itemsanity)": ITEMSANITY,
        "Oxidized Cut Copper (Itemsanity)": ITEMSANITY,
        "Cut Copper Stairs (Itemsanity)": STAIR,
        "Exposed Cut Copper Stairs (Itemsanity)": STAIR,
        "Weathered Cut Copper Stairs (Itemsanity)": STAIR,
        "Oxidized Cut Copper Stairs (Itemsanity)": STAIR,
        "Cut Copper Slab (Itemsanity)": SLAB,
        "Exposed Cut Copper Slab (Itemsanity)": SLAB,
        "Weathered Cut Copper Slab (Itemsanity)": SLAB,
        "Oxidized Cut Copper Slab (Itemsanity)": SLAB,
        "Iron Nugget (Itemsanity)": ITEMSANITY,
    },  canGetIron() & canCompactResources())

    # REQUIRES COMPACTING
    create_region(world, "Menu", "CanCompact", {
        "Block of Coal (Itemsanity)": ITEMSANITY
    },  canCompactResources())

    # REQUIRES COMPACTING & STONE TOOLS
    create_region(world, "HasStoneTools", "CanCompactAndStoneTools", {
        "Block of Raw Iron (Itemsanity)": ITEMSANITY,
        "Block of Raw Copper (Itemsanity)": ITEMSANITY,
        "Block of Lapis Lazuli (Itemsanity)": ITEMSANITY
    },  canCompactResources())

    # REQUIRES COMPACTING & IRON TOOLS
    create_region(world, "HasIronTools", "CanCompactAndIronTools", {
        "Block of Raw Gold (Itemsanity)": ITEMSANITY,
        "Block of Diamond (Itemsanity)": ITEMSANITY,
        "Block of Emerald (Itemsanity)": ITEMSANITY,
        "Block of Redstone (Itemsanity)": ITEMSANITY
    },  canCompactResources())

    # REQUIRES COMPACTING & DIAMOND TOOLS
    create_region(world, "CanCompactAndIronTools", "CanCompactAndDiamondTools", {
        "Block of Netherite (Itemsanity)": ITEMSANITY
    },  canCompactResources() & canGetNetherite())

    # REQUIRES COMPACTING & IRON TOOLS & SMELTING
    create_region(world, "HasIronTools", "CanCompactAndIronToolsAndSmelting", {
        "Block of Gold (Itemsanity)": ITEMSANITY
    },  canCompactResources() & canGetIron() & canUseIronTools())

    # REQUIRES NETHER & FISHING ROD
    create_region(world, "NetherAccess", "NetherAccessAndFishing", {
        "Warped Fungus on a Stick (Itemsanity)": ITEMSANITY
    },  canAccessNether() & canUseFishingRod())

    # REQUIRES END & SMELTING
    create_region(world, "EndAccess", "EndAccessAndSmelting", {
        "Purpur Slab (Itemsanity)": SLAB,
        "Purpur Block (Itemsanity)": ITEMSANITY,
        "Purpur Pillar (Itemsanity)": ITEMSANITY,
        "Purpur Stairs (Itemsanity)": STAIR,
        "Popped Chorus Fruit (Itemsanity)": ITEMSANITY
    },  canAccessEnd() & canSmelt())

    # REQUIRES END & GLASS BOTTLES & SMELTING
    create_region(world, "EndAccessAndSmelting", "EndAccessAndGlassBottles", {
        "Dragon's Breath (Itemsanity)": ITEMSANITY
    },  canAccessEnd() & canSmelt() & canUseBottles())

    # REQUIRES VANILLA END GAME
    create_region(world, "EndAccess", "VanillaEndGame", {
        "End Rod (Itemsanity)": ITEMSANITY
    },  canAccessVanillaEndGame())

    # REQUIRES NETHER + DIAMOND TOOLS | CHESTS
    create_region(world, "NetherAccess", "NetherAccessGetDebree", {
        "Ancient Debris (Itemsanity)": ITEMSANITY
    },  canGetNetherite())

    # REQUIRES NETHER + DIAMOND TOOLS | CHESTS + Smelting
    create_region(world, "NetherAccessGetDebree", "NetherAccessGetDebreeScrap", {
        "Netherite Scrap (Itemsanity)": ITEMSANITY,
        "Netherite Ingot (Itemsanity)": ITEMSANITY,
        "Lodestone (Itemsanity)": ITEMSANITY
    },  canGetNetherite() & canGetIron())

    # REQUIRES NETHER & ENCHANTING
    create_region(world, "NetherAccess", "NetherAccessAndEnchanting", {
        "Crimson Nylium (Itemsanity)": ITEMSANITY,
        "Warped Nylium (Itemsanity)": ITEMSANITY,
        "Nether Gold Ore (Itemsanity)": ITEMSANITY,
        "Nether Quartz Ore (Itemsanity)": ITEMSANITY
    },  canAccessNether() & canEnchant())

    # REQUIRES NETHER & SMELTING
    create_region(world, "NetherAccess", "NetherAccessAndSmelting", {
        "Nether Brick Slab (Itemsanity)": SLAB,
        "Smooth Quartz Block (Itemsanity)": ITEMSANITY,
        "Nether Bricks (Itemsanity)": ITEMSANITY,
        "Cracked Nether Bricks (Itemsanity)": ITEMSANITY,
        "Chiseled Nether Bricks (Itemsanity)": ITEMSANITY,
        "Nether Brick Fence (Itemsanity)": WALL,
        "Nether Brick Stairs (Itemsanity)": STAIR,
        "Nether Brick Wall (Itemsanity)": WALL,
        "Red Nether Brick Wall (Itemsanity)": WALL,
        "Smooth Quartz Stairs (Itemsanity)": STAIR,
        "Red Nether Brick Stairs (Itemsanity)": STAIR,
        "Smooth Quartz Slab (Itemsanity)": SLAB,
        "Red Nether Brick Slab (Itemsanity)": SLAB,
        "Daylight Detector (Itemsanity)": ITEMSANITY,
        "Red Nether Bricks (Itemsanity)": ITEMSANITY,
        "Nether Brick (Itemsanity)": ITEMSANITY,
        "Cracked Polished Blackstone Bricks (Itemsanity)": ITEMSANITY
    },  canAccessNether() & canSmelt())
    smart_add_rule(world, "Red Nether Brick Wall (Itemsanity)", fortressExploration() | bastionRemnantExploration(), WALL)
    smart_add_rule(world, "Red Nether Brick Stairs (Itemsanity)", fortressExploration() | bastionRemnantExploration(), STAIR)
    smart_add_rule(world, "Red Nether Brick Slab (Itemsanity)", fortressExploration() | bastionRemnantExploration(), SLAB)
    smart_add_rule(world, "Red Nether Bricks (Itemsanity)", fortressExploration() | bastionRemnantExploration(), ITEMSANITY)

    # REQUIRES NETHER & SMELTING & IRON TOOLS
    create_region(world, "NetherAccessAndSmelting", "NetherAccessAndSmeltingAndIronTools", {
        "Redstone Comparator (Itemsanity)": ITEMSANITY,
        "Observer (Itemsanity)": ITEMSANITY,
        "Redstone Lamp (Itemsanity)": ITEMSANITY
    },  canAccessNether() & canGetIron() & canUseIronTools())

    # REQUIRES SHEARS | ENCHANTING
    create_region(world, "Menu", "ShearsOrEnchanting", {
        "Oak Leaves (Itemsanity)": ITEMSANITY,
        "Spruce Leaves (Itemsanity)": ITEMSANITY,
        "Birch Leaves (Itemsanity)": ITEMSANITY,
        "Jungle Leaves (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Acacia Leaves (Itemsanity)": ITEMSANITY,
        "Cherry Leaves (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Leaves (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Leaves (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Azalea Leaves (Itemsanity)": ITEMSANITY,
        "Flowering Azalea Leaves (Itemsanity)": ITEMSANITY,
        "Cobweb (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canUseShears() | canEnchant())
    smart_add_rule(world, "Jungle Leaves (Itemsanity)", jungleBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Acacia Leaves (Itemsanity)", savannaBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Cherry Leaves (Itemsanity)", highlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Dark Oak Leaves (Itemsanity)", forestBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Mangrove Leaves (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Cobweb (Itemsanity)", mineshaftExploration(), ITEMSANITY_EXPLORATION)

    # REQUIRES END & BOW
    create_region(world, "EndAccess", "EndAccessAndBow", {
        "Chorus Flower (Itemsanity)": ITEMSANITY
    },  canAccessEnd() & canUseBow())

    # REQUIRES DIAMOND TOOLS & EYES OF ENDER
    create_region(world, "HasDiamondTools", "HasDiamondToolsAndEyesOfEnder", {
        "Ender Chest (Itemsanity)": ITEMSANITY
    },  canGetObsidian() & canGetEyesOfEnder())

    # REQUIRES SWIM | NETHER ACCESS
    create_region(world, "Menu", "NetherAccessOrSwim", {
        "Magma Block (Itemsanity)": ITEMSANITY
    },  canSwim() | canAccessNether())

    # REQUIRES CHESTS & END ACCESS
    create_region(world, "EndAccess", "EndAccessAndChests", {
        "Shulker Box (Itemsanity)": ITEMSANITY,
        "Spire Armor Trim (Itemsanity)": TRIM
    },  canAccessChests() & canAccessEnd() & endCityExploration())

    # REQUIRES CHESTS & SMELTING
    create_region(world, "CanSmeltItems", "CanSmeltItemsAndUseChests", {
        "Hopper (Itemsanity)": ITEMSANITY,
        "Trapped Chest (Itemsanity)": ITEMSANITY
    },  canAccessChests() & canGetIron())

    # REQUIRES BOW & IRON TOOLS
    create_region(world, "HasIronTools", "HasIronToolsAndBow", {
        "Dispenser (Itemsanity)": ITEMSANITY
    },  canUseIronTools() & canUseBow())

    # REQUIRES MINECART & IRON TOOLS
    create_region(world, "HasMinecart", "HasMinecartAndIronTools", {
        "Powered Rail (Itemsanity)": ITEMSANITY,
        "Detector Rail (Itemsanity)": ITEMSANITY,
        "Activator Rail (Itemsanity)": ITEMSANITY
    },  canUseMinecart() & canUseIronTools())


    # REQUIRES CHESTS & IRON TOOLS
    create_region(world, "HasIronTools", "HasIronToolsAndChests", {
        "Recovery Compass (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canAccessChests() & canUseIronTools())
    smart_add_rule(world, "Recovery Compass (Itemsanity)", ancientCityExploration(), ITEMSANITY_EXPLORATION)

    # REQUIRES MINECART & CHESTS
    create_region(world, "HasMinecart", "HasMinecartAndChests", {
        "Minecart with Chest (Itemsanity)": ITEMSANITY,
        "Minecart with Hopper (Itemsanity)": ITEMSANITY
    },  canUseMinecart() & canAccessChests())

    # REQUIRES FISHING | SWIM
    create_region(world, "Menu", "HasSwimOrFishing", {
        "Raw Cod (Itemsanity)": ITEMSANITY,
        "Raw Salmon (Itemsanity)": ITEMSANITY,
        "Tropical Fish (Itemsanity)": ITEMSANITY,
        "Pufferfish (Itemsanity)": ITEMSANITY
    },  canSwim() | canUseFishingRod())

    # REQUIRES FISHING | SWIM + SMELTING
    create_region(world, "Menu", "HasSwimOrFishingAndSmelting", {
        "Cooked Cod (Itemsanity)": ITEMSANITY,
        "Cooked Salmon (Itemsanity)": ITEMSANITY
    },  canSmelt() & (canSwim() | canUseFishingRod()))

    # REQUIRES SHEARS & NETHER
    create_region(world, "NetherAccess", "NetherAccessAndShears", {
        "Nether Sprouts (Itemsanity)": ITEMSANITY
    },  canAccessNether() & canUseShears())

    # Regular Dye
    create_region(world, "Menu", "RegularDye", {
        "Red Wool (Itemsanity)": DYE,
        "Red Carpet (Itemsanity)": DYE,
        "Red Concrete (Itemsanity)": DYE,
        "Red Concrete Powder (Itemsanity)": DYE,
        "Red Dye (Itemsanity)": ITEMSANITY,
        "Red Banner (Itemsanity)": DYE,

        "Yellow Wool (Itemsanity)": DYE,
        "Yellow Carpet (Itemsanity)": DYE,
        "Yellow Concrete (Itemsanity)": DYE,
        "Yellow Concrete Powder (Itemsanity)": DYE,
        "Yellow Dye (Itemsanity)": ITEMSANITY,
        "Yellow Banner (Itemsanity)": DYE,

        "Blue Wool (Itemsanity)": DYE,
        "Blue Carpet (Itemsanity)": DYE,
        "Blue Concrete (Itemsanity)": DYE,
        "Blue Concrete Powder (Itemsanity)": DYE,
        "Blue Dye (Itemsanity)": ITEMSANITY,
        "Blue Banner (Itemsanity)": DYE,

        "White Wool (Itemsanity)": DYE,
        "White Carpet (Itemsanity)": DYE,
        "White Concrete (Itemsanity)": DYE,
        "White Concrete Powder (Itemsanity)": DYE,
        "White Dye (Itemsanity)": ITEMSANITY,
        "White Banner (Itemsanity)": DYE,

        "Firework Star (Itemsanity)": ITEMSANITY
    },  canDyeBasic())

    # Regular Dye & Smelt
    create_region(world, "RegularDye", "RegularDyeAndSmelt", {
        "Red Terracotta (Itemsanity)": DYE,
        "Red Stained Glass (Itemsanity)": DYE,
        "Red Stained Glass Pane (Itemsanity)": DYE,
        "Red Glazed Terracotta (Itemsanity)": DYE,

        "Yellow Terracotta (Itemsanity)": DYE,
        "Yellow Stained Glass (Itemsanity)": DYE,
        "Yellow Stained Glass Pane (Itemsanity)": DYE,
        "Yellow Glazed Terracotta (Itemsanity)": DYE,

        "Blue Terracotta (Itemsanity)": DYE,
        "Blue Stained Glass (Itemsanity)": DYE,
        "Blue Stained Glass Pane (Itemsanity)": DYE,
        "Blue Glazed Terracotta (Itemsanity)": DYE,

        "White Terracotta (Itemsanity)": DYE,
        "White Stained Glass (Itemsanity)": DYE,
        "White Stained Glass Pane (Itemsanity)": DYE,
        "White Glazed Terracotta (Itemsanity)": DYE
    },  canDyeBasic() & canSmelt())

    # Regular Dye & Shears
    create_region(world, "RegularDye", "RegularDyeAndShears", {
        "Red Candle (Itemsanity)": DYE,
        "Yellow Candle (Itemsanity)": DYE,
        "Blue Candle (Itemsanity)": DYE,
        "White Candle (Itemsanity)": DYE
    },  canDyeBasic() & canUseShears())

    # Regular Dye & Sleep
    create_region(world, "RegularDye", "RegularDyeAndSleep", {
        "Red Bed (Itemsanity)": DYE,
        "Yellow Bed (Itemsanity)": DYE,
        "Blue Bed (Itemsanity)": DYE,
        "White Bed (Itemsanity)": DYE
    },  canDyeBasic() & canSleep())

    # Regular Dye & End & Chests
    create_region(world, "RegularDye", "RegularDyeAndShulker", {
        "Red Shulker Box (Itemsanity)": DYE,
        "Yellow Shulker Box (Itemsanity)": DYE,
        "Blue Shulker Box (Itemsanity)": DYE,
        "White Shulker Box (Itemsanity)": DYE
    },  canDyeBasic() & canAccessChests() & canAccessEnd() & endCityExploration())

    # Black Dye
    create_region(world, "RegularDye", "BlackDye", {
        "Black Wool (Itemsanity)": DYE,
        "Black Carpet (Itemsanity)": DYE,
        "Black Concrete (Itemsanity)": DYE,
        "Black Concrete Powder (Itemsanity)": DYE,
        "Black Dye (Itemsanity)": ITEMSANITY,
        "Black Banner (Itemsanity)": DYE,

        "Gray Wool (Itemsanity)": DYE,
        "Gray Carpet (Itemsanity)": DYE,
        "Gray Concrete (Itemsanity)": DYE,
        "Gray Concrete Powder (Itemsanity)": DYE,
        "Gray Dye (Itemsanity)": ITEMSANITY,
        "Gray Banner (Itemsanity)": DYE
    },  canDyeBlack())

    # Black Dye & Smelt
    create_region(world, "RegularDye", "BlackDyeAndSmelt", {
        "Black Terracotta (Itemsanity)": DYE,
        "Black Stained Glass (Itemsanity)": DYE,
        "Black Stained Glass Pane (Itemsanity)": DYE,
        "Black Glazed Terracotta (Itemsanity)": DYE,

        "Gray Terracotta (Itemsanity)": DYE,
        "Gray Stained Glass (Itemsanity)": DYE,
        "Gray Stained Glass Pane (Itemsanity)": DYE,
        "Gray Glazed Terracotta (Itemsanity)": DYE
    },  canDyeBlack() & canSmelt())

    # Black Dye & Shears
    create_region(world, "RegularDye", "BlackDyeAndShears", {
        "Black Candle (Itemsanity)": DYE,
        "Gray Candle (Itemsanity)": DYE
    },  canDyeBlack() & canUseShears())

    # Black Dye & Sleep
    create_region(world, "RegularDye", "BlackDyeAndSleep", {
        "Black Bed (Itemsanity)": DYE,
        "Gray Bed (Itemsanity)": DYE
    },  canDyeBlack() & canSleep())

    # Black Dye & End & Chests
    create_region(world, "RegularDye", "BlackDyeAndShulker", {
        "Black Shulker Box (Itemsanity)": DYE,
        "Gray Shulker Box (Itemsanity)": DYE
    },  canDyeBlack() & canAccessChests() & canAccessEnd() & endCityExploration())

    # Green Dye & Smelt
    create_region(world, "RegularDye", "GreenDyeAndSmelt", {
        "Green Terracotta (Itemsanity)": DYE_AND_EXPLORATION,
        "Green Stained Glass (Itemsanity)": DYE_AND_EXPLORATION,
        "Green Stained Glass Pane (Itemsanity)": DYE_AND_EXPLORATION,
        "Green Glazed Terracotta (Itemsanity)": DYE_AND_EXPLORATION,
        "Green Wool (Itemsanity)": DYE_AND_EXPLORATION,
        "Green Carpet (Itemsanity)": DYE_AND_EXPLORATION,
        "Green Concrete (Itemsanity)": DYE_AND_EXPLORATION,
        "Green Concrete Powder (Itemsanity)": DYE_AND_EXPLORATION,
        "Green Dye (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Green Banner (Itemsanity)": DYE_AND_EXPLORATION
    },  canDyeGreen())

    # Green Dye & Shears
    create_region(world, "RegularDye", "GreenDyeAndShears", {
        "Green Candle (Itemsanity)": DYE_AND_EXPLORATION
    },  canUseShears() & canDyeGreen())

    # Green Dye & Sleep
    create_region(world, "RegularDye", "GreenDyeAndSleep", {
        "Green Bed (Itemsanity)": DYE_AND_EXPLORATION
    },  canSleep() & canDyeGreen())

    # Green Dye & End & Chests
    create_region(world, "RegularDye", "GreenDyeAndShulker", {
        "Green Shulker Box (Itemsanity)": DYE_AND_EXPLORATION
    },  canAccessChests() & canAccessEnd() & canDyeGreen() & endCityExploration())

    # Full Dye
    create_region(world, "RegularDye", "FullDye", {
        "Orange Wool (Itemsanity)": DYE,
        "Orange Carpet (Itemsanity)": DYE,
        "Orange Concrete (Itemsanity)": DYE,
        "Orange Concrete Powder (Itemsanity)": DYE,
        "Orange Dye (Itemsanity)": ITEMSANITY,
        "Orange Banner (Itemsanity)": DYE,

        "Light Blue Wool (Itemsanity)": DYE,
        "Light Blue Carpet (Itemsanity)": DYE,
        "Light Blue Concrete (Itemsanity)": DYE,
        "Light Blue Concrete Powder (Itemsanity)": DYE,
        "Light Blue Dye (Itemsanity)": ITEMSANITY,
        "Light Blue Banner (Itemsanity)": DYE,

        "Purple Wool (Itemsanity)": DYE,
        "Purple Carpet (Itemsanity)": DYE,
        "Purple Concrete (Itemsanity)": DYE,
        "Purple Concrete Powder (Itemsanity)": DYE,
        "Purple Dye (Itemsanity)": ITEMSANITY,
        "Purple Banner (Itemsanity)": DYE,

        "Pink Wool (Itemsanity)": DYE,
        "Pink Carpet (Itemsanity)": DYE,
        "Pink Concrete (Itemsanity)": DYE,
        "Pink Concrete Powder (Itemsanity)": DYE,
        "Pink Dye (Itemsanity)": ITEMSANITY,
        "Pink Banner (Itemsanity)": DYE,

        "Magenta Wool (Itemsanity)": DYE,
        "Magenta Carpet (Itemsanity)": DYE,
        "Magenta Concrete (Itemsanity)": DYE,
        "Magenta Concrete Powder (Itemsanity)": DYE,
        "Magenta Dye (Itemsanity)": ITEMSANITY,
        "Magenta Banner (Itemsanity)": DYE,

        "Light Gray Wool (Itemsanity)": DYE,
        "Light Gray Carpet (Itemsanity)": DYE,
        "Light Gray Concrete (Itemsanity)": DYE,
        "Light Gray Concrete Powder (Itemsanity)": DYE,
        "Light Gray Dye (Itemsanity)": ITEMSANITY,
        "Light Gray Banner (Itemsanity)": DYE,

        "Brown Wool (Itemsanity)": DYE_AND_EXPLORATION,
        "Brown Carpet (Itemsanity)": DYE_AND_EXPLORATION,
        "Brown Concrete (Itemsanity)": DYE_AND_EXPLORATION,
        "Brown Concrete Powder (Itemsanity)": DYE_AND_EXPLORATION,
        "Brown Dye (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Brown Banner (Itemsanity)": DYE_AND_EXPLORATION
    },  canDyeFull())
    smart_add_rule(world, "Brown Wool (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Carpet (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Concrete (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Concrete Powder (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Dye (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Banner (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Full Dye & Smelt
    create_region(world, "RegularDye", "FullDyeAndSmelt", {
        "Orange Terracotta (Itemsanity)": DYE,
        "Orange Stained Glass (Itemsanity)": DYE,
        "Orange Stained Glass Pane (Itemsanity)": DYE,
        "Orange Glazed Terracotta (Itemsanity)": DYE,

        "Light Blue Terracotta (Itemsanity)": DYE,
        "Light Blue Stained Glass (Itemsanity)": DYE,
        "Light Blue Stained Glass Pane (Itemsanity)": DYE,
        "Light Blue Glazed Terracotta (Itemsanity)": DYE,

        "Purple Terracotta (Itemsanity)": DYE,
        "Purple Stained Glass (Itemsanity)": DYE,
        "Purple Stained Glass Pane (Itemsanity)": DYE,
        "Purple Glazed Terracotta (Itemsanity)": DYE,

        "Light Gray Terracotta (Itemsanity)": DYE,
        "Light Gray Stained Glass (Itemsanity)": DYE,
        "Light Gray Stained Glass Pane (Itemsanity)": DYE,
        "Light Gray Glazed Terracotta (Itemsanity)": DYE,

        "Brown Terracotta (Itemsanity)": DYE_AND_EXPLORATION,
        "Brown Stained Glass (Itemsanity)": DYE_AND_EXPLORATION,
        "Brown Stained Glass Pane (Itemsanity)": DYE_AND_EXPLORATION,
        "Brown Glazed Terracotta (Itemsanity)": DYE_AND_EXPLORATION,

        "Pink Terracotta (Itemsanity)": DYE,
        "Pink Stained Glass (Itemsanity)": DYE,
        "Pink Stained Glass Pane (Itemsanity)": DYE,
        "Pink Glazed Terracotta (Itemsanity)": DYE,

        "Magenta Terracotta (Itemsanity)": DYE,
        "Magenta Stained Glass (Itemsanity)": DYE,
        "Magenta Stained Glass Pane (Itemsanity)": DYE,
        "Magenta Glazed Terracotta (Itemsanity)": DYE
    },  canDyeFull() & canSmelt())
    smart_add_rule(world, "Brown Terracotta (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Stained Glass (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Stained Glass Pane (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Glazed Terracotta (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Full Dye & Shears
    create_region(world, "RegularDye", "FullDyeAndShears", {
        "Orange Candle (Itemsanity)": DYE,
        "Light Blue Candle (Itemsanity)": DYE,
        "Purple Candle (Itemsanity)": DYE,
        "Light Gray Candle (Itemsanity)": DYE,
        "Brown Candle (Itemsanity)": DYE_AND_EXPLORATION,
        "Pink Candle (Itemsanity)": DYE,
        "Magenta Candle (Itemsanity)": DYE
    },  canDyeFull() & canUseShears())
    smart_add_rule(world, "Brown Candle (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Full Dye & Sleep
    create_region(world, "RegularDye", "FullDyeAndSleep", {
        "Orange Bed (Itemsanity)": DYE,
        "Light Blue Bed (Itemsanity)": DYE,
        "Purple Bed (Itemsanity)": DYE,
        "Light Gray Bed (Itemsanity)": DYE,
        "Brown Bed (Itemsanity)": DYE_AND_EXPLORATION,
        "Pink Bed (Itemsanity)": DYE,
        "Magenta Bed (Itemsanity)": DYE
    },  canDyeFull() & canSleep())
    smart_add_rule(world, "Brown Bed (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Full Dye & End & Chests
    create_region(world, "RegularDye", "FullDyeAndShulker", {
        "Orange Shulker Box (Itemsanity)": DYE,
        "Light Blue Shulker Box (Itemsanity)": DYE,
        "Purple Shulker Box (Itemsanity)": DYE,
        "Light Gray Shulker Box (Itemsanity)": DYE,
        "Brown Shulker Box (Itemsanity)": DYE_AND_EXPLORATION,
        "Pink Shulker Box (Itemsanity)": DYE,
        "Magenta Shulker Box (Itemsanity)": DYE
    },  canDyeFull() & canAccessChests() & canAccessEnd() & endCityExploration())
    smart_add_rule(world, "Brown Shulker Box (Itemsanity)", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Lime & Cyan Dye & Smelt
    create_region(world, "RegularDye", "LimeAndCyanDyeAndSmelt", {
        "Lime Terracotta (Itemsanity)": DYE_AND_EXPLORATION,
        "Lime Stained Glass (Itemsanity)": DYE_AND_EXPLORATION,
        "Lime Stained Glass Pane (Itemsanity)": DYE_AND_EXPLORATION,
        "Lime Glazed Terracotta (Itemsanity)": DYE_AND_EXPLORATION,
        "Lime Wool (Itemsanity)": DYE_AND_EXPLORATION,
        "Lime Carpet (Itemsanity)": DYE_AND_EXPLORATION,
        "Lime Concrete (Itemsanity)": DYE_AND_EXPLORATION,
        "Lime Concrete Powder (Itemsanity)": DYE_AND_EXPLORATION,
        "Lime Dye (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Lime Banner (Itemsanity)": DYE_AND_EXPLORATION,

        "Cyan Terracotta (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Stained Glass (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Stained Glass Pane (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Glazed Terracotta (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Wool (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Carpet (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Concrete (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Concrete Powder (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Dye (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Cyan Banner (Itemsanity)": DYE_AND_EXPLORATION
    },  canDyeFull() & canDyeGreen())

    # Lime & Cyan Dye & Shears
    create_region(world, "RegularDye", "LimeAndCyanDyeAndShears", {
        "Lime Candle (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Candle (Itemsanity)": DYE_AND_EXPLORATION
    },  canDyeFull() & canUseShears() & canDyeGreen())

    # Lime & Cyan Dye & Sleep
    create_region(world, "RegularDye", "LimeAndCyanDyeAndSleep", {
        "Lime Bed (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Bed (Itemsanity)": DYE_AND_EXPLORATION
    },  canDyeFull() & canSleep() & canDyeGreen())

    # Lime & Cyan Dye & End & Chests
    create_region(world, "RegularDye", "LimeAndCyanDyeAndShulker", {
        "Lime Shulker Box (Itemsanity)": DYE_AND_EXPLORATION,
        "Cyan Shulker Box (Itemsanity)": DYE_AND_EXPLORATION
    },  canDyeFull() & canAccessChests() & canAccessEnd() & canDyeGreen() & endCityExploration())

    # Can Smelt & Compact
    create_region(world, "CanSmeltItems", "CanSmeltItemsAndCompact", {
        "Lantern (Itemsanity)": ITEMSANITY,
        "Chain (Itemsanity)": ITEMSANITY,
        "Oak Hanging Sign (Itemsanity)": ITEMSANITY,
        "Spruce Hanging Sign (Itemsanity)": ITEMSANITY,
        "Birch Hanging Sign (Itemsanity)": ITEMSANITY,
        "Jungle Hanging Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Acacia Hanging Sign (Itemsanity)": ITEMSANITY,
        "Cherry Hanging Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Dark Oak Hanging Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Mangrove Hanging Sign (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Bamboo Hanging Sign (Itemsanity)": ITEMSANITY_EXPLORATION
    },  canCompactResources() & canGetIron())
    smart_add_rule(world, "Jungle Hanging Sign (Itemsanity)", jungleBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Acacia Hanging Sign (Itemsanity)", savannaBiomesExploration(), ITEMSANITY)
    smart_add_rule(world, "Cherry Hanging Sign (Itemsanity)", highlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Dark Oak Hanging Sign (Itemsanity)", forestBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Mangrove Hanging Sign (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Bamboo Hanging Sign (Itemsanity)", jungleBiomesExploration(), ITEMSANITY_EXPLORATION)

    # Can Smelt & Compact & Has Nether
    create_region(world, "CanSmeltItemsAndCompact", "CanSmeltItemsAndCompactAndNether", {
        "Crimson Hanging Sign (Itemsanity)": ITEMSANITY,
        "Warped Hanging Sign (Itemsanity)": ITEMSANITY,
        "Soul Lantern (Itemsanity)": ITEMSANITY
    },  canCompactResources() & canGetIron() & canAccessNether())

    # Can Shear & Enchant
    create_region(world, "HasEnchanting", "HasEnchantingAndShears", {
        "Turtle Egg (Itemsanity)": ITEMSANITY
    },  canEnchant() & canUseShears())
    smart_add_rule(world, "Turtle Egg (Itemsanity)", wetlandBiomesExploration(), ITEMSANITY)

    # Can Use Chests & Access Nether
    create_region(world, "NetherAccess", "NetherAccessAndChests", {
        "Netherite Smithing Template (Itemsanity)": NETHERITE,
        "Snout Banner Pattern (Itemsanity)": ITEMSANITY_EXPLORATION,
        "Music Disc Pigstep (Itemsanity)": DISCS,
        "Snout Armor Trim (Itemsanity)": TRIM,
        "Rib Armor Trim (Itemsanity)": TRIM
    },  canAccessChests() & canAccessNether())
    smart_add_rule(world, "Netherite Smithing Template (Itemsanity)", bastionRemnantExploration(), NETHERITE)
    smart_add_rule(world, "Snout Banner Pattern (Itemsanity)", bastionRemnantExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Music Disc Pigstep (Itemsanity)", bastionRemnantExploration(), DISCS)
    smart_add_rule(world, "Snout Armor Trim (Itemsanity)", bastionRemnantExploration(), TRIM)
    smart_add_rule(world, "Rib Armor Trim (Itemsanity)", fortressExploration(), TRIM)

    if "create" in world.options.enabled_mods.value:
        create_region(world, "Menu", "RedSand", {
            "Red Sandstone (Itemsanity)": ITEMSANITY,
            "Chiseled Red Sandstone (Itemsanity)": ITEMSANITY,
            "Cut Red Sandstone (Itemsanity)": ITEMSANITY,
            "Red Sandstone Stairs (Itemsanity)": STAIR,
            "Red Sandstone Wall (Itemsanity)": WALL,
            "Red Sand (Itemsanity)": ITEMSANITY,
            "Red Sandstone Slab (Itemsanity)": SLAB,
            "Cut Red Sandstone Slab (Itemsanity)": SLAB,
        },  canCraftAndesiteAlloyCreate() & hasCogsCreate())

        # REQUIRES SMELTING
        create_region(world, "RedSand", "CanSmeltItemsRedSand", {
            "Smooth Red Sandstone (Itemsanity)": ITEMSANITY,
            "Smooth Red Sandstone Stairs (Itemsanity)": STAIR,
            "Smooth Red Sandstone Slab (Itemsanity)": SLAB,
        },  canCraftAndesiteAlloyCreate() & hasCogsCreate() & canSmelt())
    else:
        create_region(world, "Menu", "RedSand", {
            "Red Sandstone (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Chiseled Red Sandstone (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Cut Red Sandstone (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Red Sandstone Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
            "Red Sandstone Wall (Itemsanity)": WALL_AND_EXPLORATION,
            "Red Sand (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Red Sandstone Slab (Itemsanity)": SLAB_AND_EXPLORATION,
            "Cut Red Sandstone Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        }, aridBiomesExploration())

        # REQUIRES SMELTING
        create_region(world, "RedSand", "CanSmeltItemsRedSand", {
            "Smooth Red Sandstone (Itemsanity)": ITEMSANITY_EXPLORATION,
            "Smooth Red Sandstone Stairs (Itemsanity)": STAIR_AND_EXPLORATION,
            "Smooth Red Sandstone Slab (Itemsanity)": SLAB_AND_EXPLORATION,
        },  canSmelt() & aridBiomesExploration())




def create_region(world: FabricMinecraftWorld, region_name: str, new_region_name: str, locations: dict[str, int], rule=None):
    create_locations_and_connect(world, region_name + "VanillaItemsanity", new_region_name + "VanillaItemsanity", locations, rule)