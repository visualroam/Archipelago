from __future__ import annotations

from worlds.minecraft_fabric.region.mc_regions_consts import *
from worlds.minecraft_fabric.region.regions_helper import create_locations_and_connect, smart_add_rule
from worlds.minecraft_fabric.logic.vanilla_logic import *


if TYPE_CHECKING:
   from worlds.minecraft_fabric import FabricMinecraftWorld


def create_ironchests_itemsanity_regions(world: FabricMinecraftWorld):
    create_locations_and_connect(world, "Menu", "MenuIronChestsItemsanity", {
        "Blank Chest Upgrade (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY
    })

    # Has Smelting
    create_region(world, "Menu", "HasSmelting", {
        "Crystal Chest Upgrade (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Copper Chest Upgrade (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Iron Chest Upgrade (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Iron Dolly (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY_EXPLORATION,
    }, canGetIron())
    smart_add_rule(world, "Iron Dolly (Itemsanity) {Iron Chests: Restocked}", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)

    # Has Smelting & Storage
    create_region(world, "HasSmelting", "HasSmeltingAndStorage", {
        "Copper Chest (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Copper Barrel (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Iron Chest (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Iron Barrel (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canGetIron() & canAccessChests())

    # Has Smelting & Storage & Gold
    create_region(world, "HasSmeltingAndStorage", "HasSmeltingAndStorageAndGold", {
        "Gold Chest (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Gold Barrel (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY
    }, canSmelt() & canAccessChests() & canGetGold())

    # Has Smelting & Storage & Gold & Iron Tools
    create_region(world, "HasSmeltingAndStorageAndGold", "HasSmeltingAndStorageAndGoldAndIronTools", {
        "Diamond Chest (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Diamond Barrel (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Crystal Chest (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Crystal Barrel (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canSmelt() & canAccessChests() & canGetGold() & canUseIronTools())

    # Has Smelting & Storage & Gold & Iron Tools & Obsidian
    create_region(world, "HasSmeltingAndStorageAndGoldAndIronTools", "HasSmeltingAndStorageAndGoldAndIronToolsAndObsidian", {
        "Obsidian Chest (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Obsidian Barrel (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canSmelt() & canAccessChests() & canGetGold() & canUseIronTools() & canGetObsidian())

    # Netherite Chest Upgrade & Storage
    create_region(world, "HasSmeltingAndStorageAndGoldAndIronTools", "HasSmeltingAndStorageAndGoldAndIronToolsAndNetherite", {
        "Netherite Chest (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Netherite Barrel (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canUseDiamondTools() & canSmith() & canAccessChests())

    # Has Gold
    create_region(world, "Menu", "HasGold", {
        "Gold Chest Upgrade (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canGetGold())

    # Has Obsidian
    create_region(world, "Menu", "HasObsidian", {
        "Obsidian Chest Upgrade (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canGetObsidian())

    # Has Gold & Iron Tools
    create_region(world, "HasGold", "HasGoldAndIronTools", {
        "Diamond Chest Upgrade (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Diamond Dolly (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY_EXPLORATION,
    }, canUseIronTools() & canGetGold())
    smart_add_rule(world, "Diamond Dolly (Itemsanity) {Iron Chests: Restocked}", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)

    # Netherite Chest Upgrade
    create_region(world, "HasGoldAndIronTools", "NetheriteChest", {
        "Netherite Chest Upgrade (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canUseDiamondTools() & canSmith())

    # Can Smelt & Compact
    create_region(world, "HasSmelting", "CanSmeltItemsAndCompact", {
        "Key (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
        "Key Ring (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canCompactResources() & canSmelt())

    # Can Smelt & Compact
    create_region(world, "Menu", "GoldAndCompacting", {
        "Lock (Itemsanity) {Iron Chests: Restocked}": ITEMSANITY,
    }, canCompactResources() & canGetGold())


def create_region(world: FabricMinecraftWorld, region_name: str, new_region_name: str, locations: dict[str, int], rule=None):
    create_locations_and_connect(world, region_name + "IronChestsItemsanity", new_region_name + "IronChestsItemsanity", locations, rule)