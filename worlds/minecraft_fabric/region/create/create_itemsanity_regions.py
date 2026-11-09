from __future__ import annotations


from worlds.minecraft_fabric.region.regions_helper import create_locations_and_connect, smart_add_rule
from worlds.minecraft_fabric.logic.create_logic import *
from worlds.minecraft_fabric.logic.vanilla_logic import *
from worlds.minecraft_fabric.region.mc_regions_consts import *

if TYPE_CHECKING:
   from worlds.minecraft_fabric import FabricMinecraftWorld


def create_create_itemsanity_regions(world: FabricMinecraftWorld):
    create_locations_and_connect(world, "Menu", "MenuCreateItemsanity", {
        "Crafting Blueprint (Itemsanity) {Create}": ITEMSANITY,
        "Asurine (Itemsanity) {Create}": ITEMSANITY,
        "Crimsite (Itemsanity) {Create}": ITEMSANITY,
        "Limestone (Itemsanity) {Create}": ITEMSANITY,
        "Ochrum (Itemsanity) {Create}": ITEMSANITY,
        "Veridium (Itemsanity) {Create}": ITEMSANITY,
        "Scoria (Itemsanity) {Create}": ITEMSANITY,
    })

    # Nether Access | Black Dye
    create_region(world, "Menu", "NetherAccess", {
        "Scorchia (Itemsanity) {Create}": ITEMSANITY,
    }, canAccessNether() | canDyeBlack())

    # Can Use Sandpaper
    create_region(world, "Menu", "Sandpaper", {
        "Sand Paper (Itemsanity) {Create}": ITEMSANITY
    }, canUseSandpaper())

    # Can Use Red Sandpaper
    create_region(world, "Sandpaper", "RedSandpaper", {
        "Red Sand Paper (Itemsanity) {Create}": ITEMSANITY
    }, canUseSandpaper() & hasCogs() & canCraftAndesiteAlloy())

    # Can Get Iron
    create_region(world, "Menu", "CanGetIron", {
        "Item Drain (Itemsanity) {Create}": ITEMSANITY,
        "Copper Casing (Itemsanity) {Create}": ITEMSANITY,
        "Copper Door (Itemsanity) {Create}": ITEMSANITY
    }, canGetIron())

    # Can Smelt & Nether Access
    create_region(world, "Menu", "CanSmeltAndNether", {
        "Crimson Window (Itemsanity) {Create}": ITEMSANITY,
        "Warped Window (Itemsanity) {Create}": ITEMSANITY,
        "Crimson Window Pane (Itemsanity) {Create}": ITEMSANITY,
        "Warped Window Pane (Itemsanity) {Create}": ITEMSANITY
    }, canSmelt() & canAccessNether())

    # Can Smelt & Compact
    create_region(world, "Menu", "CanSmeltAndCompact", {
        "Copper Nugget (Itemsanity) {Create}": ITEMSANITY,
        "List Filter (Itemsanity) {Create}": ITEMSANITY,
        "Ornate Iron Window (Itemsanity) {Create}": ITEMSANITY,
        "Ornate Iron Window Pane (Itemsanity) {Create}": ITEMSANITY,
    }, canGetIron() & canCompactResources())

    # Has Iron Tools
    create_region(world, "Menu", "IronTools", {
        "Powered Latch (Itemsanity) {Create}": ITEMSANITY,
        "Powered Toggle Latch (Itemsanity) {Create}": ITEMSANITY,
        "Raw Zinc (Itemsanity) {Create}": ITEMSANITY
    }, canUseIronTools())

    # Has Iron Tools & Compact
    create_region(world, "IronTools", "IronToolsAndCompact", {
        "Block of Raw Zinc (Itemsanity) {Create}": ITEMSANITY
    }, canUseIronTools() & canCompactResources())

    # Has Zinc
    create_region(world, "Menu", "Zinc", {
        "Zinc Ingot (Itemsanity) {Create}": ITEMSANITY
    }, canGetZinc())

    # Has Zinc & Compact
    create_region(world, "Menu", "ZincAndCompact", {
        "Zinc Nugget (Itemsanity) {Create}": ITEMSANITY,
        "Package Filter (Itemsanity) {Create}": ITEMSANITY,
        "Block of Zinc (Itemsanity) {Create}": ITEMSANITY
    }, canGetZinc() & canCompactResources())

    # Has Rose Quartz
    create_region(world, "Menu", "RoseQuartz", {
        "Rose Quartz (Itemsanity) {Create}": ITEMSANITY
    }, canCraftRoseQuartz())

    # Has Rose Quartz & Sand Paper
    create_region(world, "RoseQuartz", "RoseQuartzAndSandpaper", {
        "Polished Rose Quartz (Itemsanity) {Create}": ITEMSANITY
    }, canCraftRoseQuartz() & canUseSandpaper())

    # Has Kelp
    create_region(world, "Menu", "Kelp", {
        "Mechanical Belt (Itemsanity) {Create}": ITEMSANITY
    }, canCraftDriedKelp())

    # Has Andesite Alloy
    create_region(world, "Menu", "AndesiteAlloy", {
        "Shaft (Itemsanity) {Create}": ITEMSANITY,
        "Clutch (Itemsanity) {Create}": ITEMSANITY,
        "Encased Chain Drive (Itemsanity) {Create}": ITEMSANITY,
        "Nozzle (Itemsanity) {Create}": ITEMSANITY,
        "Turntable (Itemsanity) {Create}": ITEMSANITY,
        "Hand Crank (Itemsanity) {Create}": ITEMSANITY,
        "Basin (Itemsanity) {Create}": ITEMSANITY,
        "Depot (Itemsanity) {Create}": ITEMSANITY,
        "Wooden Bracket (Itemsanity) {Create}": ITEMSANITY,
        "Metal Bracket (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Piston (Itemsanity) {Create}": ITEMSANITY,
        "Piston Extension Pole (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Bearing (Itemsanity) {Create}": ITEMSANITY,
        "Linear Chassis (Itemsanity) {Create}": ITEMSANITY,
        "Secondary Linear Chassis (Itemsanity) {Create}": ITEMSANITY,
        "Radial Chassis (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Drill (Itemsanity) {Create}": ITEMSANITY,
        "Andesite Casing (Itemsanity) {Create}": ITEMSANITY,
        "Item Hatch (Itemsanity) {Create}": ITEMSANITY,
        "Analog Lever (Itemsanity) {Create}": ITEMSANITY,
        "Andesite Alloy (Itemsanity) {Create}": ITEMSANITY,
        "Clipboard (Itemsanity) {Create}": ITEMSANITY,
        "Andesite Door (Itemsanity) {Create}": ITEMSANITY
    }, canCraftAndesiteAlloy())

    # Has Andesite Alloy & Compact
    create_region(world, "AndesiteAlloy", "AndesiteAlloyAndCompact", {
        "Block of Andesite Alloy (Itemsanity) {Create}": ITEMSANITY
    }, canCraftAndesiteAlloy() & canCompactResources())

    # Has Andesite Alloy & Iron Tools
    create_region(world, "AndesiteAlloy", "AndesiteAlloyAndIronTools", {
        "Cuckoo Clock (Itemsanity) {Create}": ITEMSANITY,
        "Speedometer (Itemsanity) {Create}": ITEMSANITY,
        "Stressometer (Itemsanity) {Create}": ITEMSANITY,
        "Gantry Shaft (Itemsanity) {Create}": ITEMSANITY,
        "Sticky Mechanical Piston (Itemsanity) {Create}": ITEMSANITY_EXPLORATION,
        "Sticker (Itemsanity) {Create}": ITEMSANITY_EXPLORATION
    }, canCraftAndesiteAlloy() & canUseIronTools())
    smart_add_rule(world, "Sticky Mechanical Piston (Itemsanity) {Create}", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    smart_add_rule(world, "Sticker (Itemsanity) {Create}", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)

    # Has Cogs
    create_region(world, "AndesiteAlloy", "Cogs", {
        "Cogwheel (Itemsanity) {Create}": ITEMSANITY,
        "Large Cogwheel (Itemsanity) {Create}": ITEMSANITY,
        "Gearbox (Itemsanity) {Create}": ITEMSANITY,
        "Vertical Gearbox (Itemsanity) {Create}": ITEMSANITY,
        "Gearshift (Itemsanity) {Create}": ITEMSANITY,
        "Chain Conveyor (Itemsanity) {Create}": ITEMSANITY,
        "Millstone (Itemsanity) {Create}": ITEMSANITY,
        "Gantry Carriage (Itemsanity) {Create}": ITEMSANITY,
        "Wheat Flour (Itemsanity) {Create}": ITEMSANITY
    }, hasCogs())

    # Has Waterwheel
    create_region(world, "AndesiteAlloy", "Waterwheel", {
        "Water Wheel (Itemsanity) {Create}": ITEMSANITY,
        "Large Water Wheel (Itemsanity) {Create}": ITEMSANITY
    }, hasWaterWheel())

    # Has Windmill
    create_region(world, "AndesiteAlloy", "Windmill", {
        "Windmill Bearing (Itemsanity) {Create}": ITEMSANITY,
        "Windmill Sail Frame (Itemsanity) {Create}": ITEMSANITY,
        "Windmill Sail (Itemsanity) {Create}": ITEMSANITY
    }, hasWindmill())

    # Has Press
    create_region(world, "AndesiteAlloy", "Press", {
        "Encased Fan (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Press (Itemsanity) {Create}": ITEMSANITY,
        "Chute (Itemsanity) {Create}": ITEMSANITY,
        "Fluid Pipe (Itemsanity) {Create}": ITEMSANITY,
        "Fluid Valve (Itemsanity) {Create}": ITEMSANITY,
        "Copper Valve Handle (Itemsanity) {Create}": ITEMSANITY,
        "Hose Pulley (Itemsanity) {Create}": ITEMSANITY,
        "Portable Fluid Interface (Itemsanity) {Create}": ITEMSANITY,
        "Rope Pulley (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Saw (Itemsanity) {Create}": ITEMSANITY,
        "Portable Storage Interface (Itemsanity) {Create}": ITEMSANITY,
        "Redstone Contact (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Harvester (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Plough (Itemsanity) {Create}": ITEMSANITY,
        "Propeller (Itemsanity) {Create}": ITEMSANITY,
        "Whisk (Itemsanity) {Create}": ITEMSANITY,
        "Copper Sheet (Itemsanity) {Create}": ITEMSANITY,
        "Iron Sheet (Itemsanity) {Create}": ITEMSANITY,
        "Super Glue (Itemsanity) {Create}": ITEMSANITY_EXPLORATION,
        "Metal Girder (Itemsanity) {Create}": ITEMSANITY
    }, hasPress())
    smart_add_rule(world, "Super Glue (Itemsanity) {Create}", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)

    # Has Press & Iron Tools
    create_region(world, "Press", "PressAndIronTools", {
        "Redstone Link (Itemsanity) {Create}": ITEMSANITY,
        "Transmitter (Itemsanity) {Create}": ITEMSANITY,
        "Linked Controller (Itemsanity) {Create}": ITEMSANITY
    }, hasPress() & canUseIronTools())

    # Has Steam Engine
    create_region(world, "Press", "SteamEngine", {
        "Steam Engine (Itemsanity) {Create}": ITEMSANITY
    }, hasSteamEngine())

    # Has Mixer
    create_region(world, "Press", "Mixer", {
        "Mechanical Mixer (Itemsanity) {Create}": ITEMSANITY
    }, hasMixer())

    # Has Mixer & Fluid
    create_region(world, "Mixer", "MixerAndFluid", {
        "Sweet Roll (Itemsanity) {Create}": ITEMSANITY
    }, hasMixer() & canUseBucket())

    # Has Chocolate
    create_region(world, "MixerAndFluid", "Chocolate", {
        "Bar of Chocolate (Itemsanity) {Create}": ITEMSANITY,
        "Chocolate Glazed Berries (Itemsanity) {Create}": ITEMSANITY,
        "Chocolate Bucket (Itemsanity) {Create}": ITEMSANITY
    }, hasBlazeBurner() & hasMixer() & canUseBucket())

    # Has Blaze Burner
    create_region(world, "Press", "BlazeBurner", {
        "Blaze Burner (Itemsanity) {Create}": ITEMSANITY,
        "Empty Blaze Burner (Itemsanity) {Create}": ITEMSANITY
    }, hasBlazeBurner())

    # Has Electron Tube
    create_region(world, "AndesiteAlloy", "ElectronTube", {
        "Adjustable Chain Gearshift (Itemsanity) {Create}": ITEMSANITY,
        "Contraption Controls (Itemsanity) {Create}": ITEMSANITY,
        "Display Board (Itemsanity) {Create}": ITEMSANITY,
        "Nixie Tube (Itemsanity) {Create}": ITEMSANITY,
        "Electron Tube (Itemsanity) {Create}": ITEMSANITY
    }, canCraftElectronTube())

    # Has Crushing Wheel
    create_region(world, "AndesiteAlloy", "CrushingWheel", {
        "Crushing Wheel (Itemsanity) {Create}": ITEMSANITY,
        "Cinder Flour (Itemsanity) {Create}": ITEMSANITY,
        "Blaze Cake Base (Itemsanity) {Create}": ITEMSANITY,
        "Blaze Cake (Itemsanity) {Create}": ITEMSANITY,
        "Nugget of Experience (Itemsanity) {Create}": ITEMSANITY,
        "Crushed Raw Iron (Itemsanity) {Create}": ITEMSANITY,
        "Crushed Raw Gold (Itemsanity) {Create}": ITEMSANITY,
        "Crushed Raw Copper (Itemsanity) {Create}": ITEMSANITY,
        "Crushed Raw Zinc (Itemsanity) {Create}": ITEMSANITY,
        "Block of Experience (Itemsanity) {Create}": ITEMSANITY,
    }, hasCrusher())

    # Has Fluid Tank
    create_region(world, "AndesiteAlloy", "FluidTank", {
        "Fluid Tank (Itemsanity) {Create}": ITEMSANITY
    }, hasFluidTank())

    # Has Spout
    create_region(world, "AndesiteAlloy", "Spout", {
        "Spout (Itemsanity) {Create}": ITEMSANITY
    }, canUseSpout())

    # Has Cardboard
    create_region(world, "AndesiteAlloy", "Cardboard", {
        "Packager (Itemsanity) {Create}": ITEMSANITY,
        "Re-Packager (Itemsanity) {Create}": ITEMSANITY,
        "Pulp (Itemsanity) {Create}": ITEMSANITY,
        "Cardboard (Itemsanity) {Create}": ITEMSANITY,
        "Cardboard Sword (Itemsanity) {Create}": ITEMSANITY,
        "Cardboard Helmet (Itemsanity) {Create}": ITEMSANITY,
        "Cardboard Chestplate (Itemsanity) {Create}": ITEMSANITY,
        "Cardboard Leggings (Itemsanity) {Create}": ITEMSANITY,
        "Cardboard Boots (Itemsanity) {Create}": ITEMSANITY,
        "Block of Cardboard (Itemsanity) {Create}": ITEMSANITY,
        "Bound Block of Cardboard (Itemsanity) {Create}": ITEMSANITY,
    }, canCraftCardboard())

    # Has Brass
    create_region(world, "AndesiteAlloy", "Brass", {
        "Elevator Pulley (Itemsanity) {Create}": ITEMSANITY,
        "Brass Casing (Itemsanity) {Create}": ITEMSANITY,
        "Flywheel (Itemsanity) {Create}": ITEMSANITY,
        "Display Link (Itemsanity) {Create}": ITEMSANITY,
        "Placard (Itemsanity) {Create}": ITEMSANITY,
        "Pulse Repeater (Itemsanity) {Create}": ITEMSANITY,
        "Pulse Extender (Itemsanity) {Create}": ITEMSANITY,
        "Pulse Timer (Itemsanity) {Create}": ITEMSANITY,
        "Brass Hand (Itemsanity) {Create}": ITEMSANITY,
        "Crafter Slot Cover (Itemsanity) {Create}": ITEMSANITY,
        "Brass Ingot (Itemsanity) {Create}": ITEMSANITY,
        "Brass Nugget (Itemsanity) {Create}": ITEMSANITY,
        "Brass Sheet (Itemsanity) {Create}": ITEMSANITY,
        "Attribute Filter (Itemsanity) {Create}": ITEMSANITY,
        "Peculiar Bell (Itemsanity) {Create}": ITEMSANITY,
        "Haunted Bell (Itemsanity) {Create}": ITEMSANITY,
        "Brass Door (Itemsanity) {Create}": ITEMSANITY,
        "Block of Brass (Itemsanity) {Create}": ITEMSANITY,
    }, canCraftBrass())

    # Has Brass & ElectronTube
    create_region(world, "Brass", "BrassAndElectronTube", {
        "Smart Observer (Itemsanity) {Create}": ITEMSANITY,
        "Deployer (Itemsanity) {Create}": ITEMSANITY,
        "Sequenced Gearshift (Itemsanity) {Create}": ITEMSANITY,
        "Threshold Switch (Itemsanity) {Create}": ITEMSANITY,
        "Clockwork Bearing (Itemsanity) {Create}": ITEMSANITY,
        "Smart Fluid Pipe (Itemsanity) {Create}": ITEMSANITY,
        "Smart Chute (Itemsanity) {Create}": ITEMSANITY,
    }, canCraftBrass() & canUseSandpaper())

    # Has Mechanical Crafter
    create_region(world, "Brass", "MechanicalCrafter", {
        "Mechanical Crafter (Itemsanity) {Create}": ITEMSANITY
    }, hasMechanicalCrafter())

    # Has Percision Mechanism
    create_region(world, "Brass", "PercisionMechanism", {
        "Rotation Speed Controller (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Arm (Itemsanity) {Create}": ITEMSANITY,
        "Incomplete Precision Mechanism (Itemsanity) {Create}": ITEMSANITY,
        "Precision Mechanism (Itemsanity) {Create}": ITEMSANITY
    }, canCraftPercisionMechanism())

    # Has Train Tracks
    create_region(world, "Brass", "TrainTracks", {
        "Train Track (Itemsanity) {Create}": ITEMSANITY,
        "Incomplete Track (Itemsanity) {Create}": ITEMSANITY
    }, canCraftTrainTracks())

    # Has Sturdy Sheet
    create_region(world, "Brass", "SturdySheet", {
        "Train Casing (Itemsanity) {Create}": ITEMSANITY,
        "Train Station (Itemsanity) {Create}": ITEMSANITY,
        "Train Signal (Itemsanity) {Create}": ITEMSANITY,
        "Train Observer (Itemsanity) {Create}": ITEMSANITY,
        "Sturdy Sheet (Itemsanity) {Create}": ITEMSANITY,
        "Unprocessed Obsidian Sheet (Itemsanity) {Create}": ITEMSANITY,
        "Train Schedule (Itemsanity) {Create}": ITEMSANITY,
        "Train Door (Itemsanity) {Create}": ITEMSANITY,
        "Train Trapdoor (Itemsanity) {Create}": ITEMSANITY,
    }, canCraftSturdySheet())

    # Has Sturdy Sheet & Percision Mechanism
    create_region(world, "SturdySheet", "SturdySheetAndPercisionMechanism", {
        "Train Controls (Itemsanity) {Create}": ITEMSANITY
    }, canCraftSturdySheet() & canCraftPercisionMechanism())

    # Has Mechanical Crafter & Percision Mechanism
    create_region(world, "Brass", "MechanicalCrafterAndPercisionMechanism", {
        "Potato Cannon (Itemsanity) {Create}": ITEMSANITY,
        "Extendo Grip (Itemsanity) {Create}": ITEMSANITY,
    }, hasMechanicalCrafter() & canCraftPercisionMechanism())

    # Has Mechanical Crafter & Percision Mechanism
    create_region(world, "MechanicalCrafterAndPercisionMechanism", "MechanicalCrafterAndPercisionMechanismAndObsidian", {
        "Wand Of Symmetry (Itemsanity) {Create}": ITEMSANITY
    }, hasMechanicalCrafter() & canCraftPercisionMechanism() & canGetObsidian())

    # Has Andesite & Kelp
    create_region(world, "AndesiteAlloy", "AndesiteAlloyAndKelp", {
        "Andesite Funnel (Itemsanity) {Create}": ITEMSANITY,
        "Andesite Tunnel (Itemsanity) {Create}": ITEMSANITY
    }, canCraftAndesiteAlloy() & canCraftDriedKelp())

    # Has Brass & Kelp
    create_region(world, "Brass", "BrassAndKelp", {
        "Brass Funnel (Itemsanity) {Create}": ITEMSANITY,
        "Brass Tunnel (Itemsanity) {Create}": ITEMSANITY
    }, canCraftBrass() & canCraftDriedKelp() & canUseSandpaper())

    # Has Press & Cogs
    create_region(world, "Press", "PressAndCogs", {
        "Weighted Ejector (Itemsanity) {Create}": ITEMSANITY,
        "Mechanical Pump (Itemsanity) {Create}": ITEMSANITY
    }, hasPress() & hasCogs())

    # Has Press & Storage
    create_region(world, "Press", "PressAndStorage", {
        "Item Vault (Itemsanity) {Create}": ITEMSANITY,
        "Package Frogport (Itemsanity) {Create}": ITEMSANITY_EXPLORATION,
        "Stock Link (Itemsanity) {Create}": ITEMSANITY_EXPLORATION
    }, hasPress() & canAccessChests())
    smart_add_rule(world, "Package Frogport (Itemsanity) {Create}", wetlandBiomesExploration(), ITEMSANITY_EXPLORATION)
    # Why is Stock Link exploration?

    # Has Percision Mechanism & Storage
    create_region(world, "Brass", "PercisionMechanismAndStorage", {
        "Factory Gauge (Itemsanity) {Create}": ITEMSANITY
    }, canCraftPercisionMechanism() & canAccessChests())

    # Has Press & Storage & Iron Tools
    create_region(world, "PressAndStorage", "PressAndStorageAndIronTools", {
        "Stock Ticker (Itemsanity) {Create}": ITEMSANITY,
        "Redstone Requester (Itemsanity) {Create}": ITEMSANITY
    }, hasPress() & canAccessChests() & canUseIronTools())

    # Has Press & Gold
    create_region(world, "Press", "PressAndGold", {
        "Steam Whistle (Itemsanity) {Create}": ITEMSANITY,
        "Golden Sheet (Itemsanity) {Create}": ITEMSANITY,
        "Desk Bell (Itemsanity) {Create}": ITEMSANITY
    }, hasPress() & canGetGold())

    # Has Press & Gold & Armor
    create_region(world, "PressAndGold", "PressAndGoldAndArmor", {
        "Engineer's Goggles (Itemsanity) {Create}": ITEMSANITY
    }, hasPress() & canGetGold() & canWearLeatherArmor())

    # Has Press & Gold & Cogs
    create_region(world, "PressAndGold", "PressAndGoldAndCogs", {
        "Wrench (Itemsanity) {Create}": ITEMSANITY
    }, hasPress() & canGetGold() & hasCogs())

    # Has Crushing Wheel & Electron Tube
    create_region(world, "CrushingWheel", "CrushingWheelAndElectronTube", {
        "Mechanical Roller (Itemsanity) {Create}": ITEMSANITY
    }, hasCrusher() & canCraftElectronTube())

    # Has Crushing Wheel & Obsidian
    create_region(world, "CrushingWheel", "CrushingWheelAndObsidian", {
        "Powdered Obsidian (Itemsanity) {Create}": ITEMSANITY
    }, hasCrusher() & canGetObsidian())

    # Has Press & Minecarts
    create_region(world, "Press", "PressAndMinecarts", {
        "Minecart Coupling (Itemsanity) {Create}": ITEMSANITY
    }, hasPress() & canUseMinecart())

    # Can Smelt & Can Compact & Has Archery
    create_region(world, "Menu", "CanSmeltAndCompactAndArchery", {
        "Schematicannon (Itemsanity) {Create}": ITEMSANITY
    }, canGetIron() & canCompactResources() & canUseBow())

    # Has Gold & Electron Tubes & Minecarts
    create_region(world, "AndesiteAlloy", "GoldAndElectronTubesAndMinecarts", {
        "Controller Rail (Itemsanity) {Create}": ITEMSANITY
    }, canGetGold() & canCraftElectronTube() & canUseMinecart())

    # Has Zinc & Rose Quartz & Sandpaper
    create_region(world, "Menu", "ZincAndRoseQuartz", {
        "Rose Quartz Lamp (Itemsanity) {Create}": ITEMSANITY
    }, canGetZinc() & canCraftRoseQuartz() & canUseSandpaper())

    # Dough
    create_region(world, "AndesiteAlloy", "Dough", {
        "Dough (Itemsanity) {Create}": ITEMSANITY
    }, hasCogs() & (canUseBucket() | hasPress()))

    # Has Mixer & Bottles
    create_region(world, "Mixer", "MixerAndBottles", {
        "Honeyed Apple (Itemsanity) {Create}": ITEMSANITY
    }, hasMixer() & canUseBottles())

    # Has Mixer & Bottles & Bucket
    create_region(world, "MixerAndBottles", "MixerAndBottlesAndBucket", {
        "Honey Bucket (Itemsanity) {Create}": ITEMSANITY
    }, hasMixer() & canUseBottles() & canUseBucket())

    # Builders Tea
    create_region(world, "MixerAndBottles", "BuildersTea", {
        "Builder's Tea (Itemsanity) {Create}": ITEMSANITY
    }, hasMixer() & canUseBottles() & canUseBucket() & hasBlazeBurner() & (
        canUseShears() | canEnchant()
    ))

    # Copper Diving Gear
    create_region(world, "AndesiteAlloy", "CopperDivingGear", {
        "Copper Backtank (Itemsanity) {Create}": ITEMSANITY,
        "Copper Diving Helmet (Itemsanity) {Create}": ITEMSANITY,
        "Copper Diving Boots (Itemsanity) {Create}": ITEMSANITY
    }, canCraftAndesiteAlloy() & canWearGoldArmor())

    # Netherite Diving Gear
    create_region(world, "CopperDivingGear", "NetheriteDivingGear", {
        "Netherite Backtank (Itemsanity) {Create}": ITEMSANITY,
        "Netherite Diving Boots (Itemsanity) {Create}": ITEMSANITY
    }, canCraftAndesiteAlloy() & canWearNetheriteArmor())

    # Netherite Diving Gear
    create_region(world, "Menu", "NetheriteDivingHelmet", {
        "Netherite Diving Helmet (Itemsanity) {Create}": ITEMSANITY
    }, canGetIron() & canWearNetheriteArmor())

    # Has Enchanting
    create_region(world, "Menu", "HasEnchanting", {
        "Zinc Ore (Itemsanity) {Create}": ITEMSANITY,
        "Deepslate Zinc Ore (Itemsanity) {Create}": ITEMSANITY
    }, canEnchant())

    # Has Swimming & Enchanting
    create_region(world, "HasEnchanting", "HasSwimAndEnchanting", {
        "Tree Fertilizer (Itemsanity) {Create}": ITEMSANITY
    }, canSwim() & canEnchant())

    # Schematic
    create_region(world, "Menu", "Schematic", {
        "Empty Schematic (Itemsanity) {Create}": ITEMSANITY,
        "Schematic And Quill (Itemsanity) {Create}": ITEMSANITY
    }, canDyeFull())

    ####################################################################################################################
    # STONE CUTTING & SAW EXCLUSIVES #################################################################################
    ####################################################################################################################


    create_region(world, "Menu", "Cutting", {
        "Cut Granite (Itemsanity) {Create}": ITEMSANITY,
        "Cut Granite Stairs (Itemsanity) {Create}": STAIR,
        "Cut Granite Slab (Itemsanity) {Create}": SLAB,
        "Cut Granite Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Granite (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Granite Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Granite Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Granite Wall (Itemsanity) {Create}": WALL,
        "Cut Granite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Granite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Granite Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Granite Brick Wall (Itemsanity) {Create}": WALL,
        "Small Granite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Granite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Granite Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Granite Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Granite (Itemsanity) {Create}": ITEMSANITY,
        "Granite Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Diorite (Itemsanity) {Create}": ITEMSANITY,
        "Cut Diorite Stairs (Itemsanity) {Create}": STAIR,
        "Cut Diorite Slab (Itemsanity) {Create}": SLAB,
        "Cut Diorite Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Diorite (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Diorite Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Diorite Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Diorite Wall (Itemsanity) {Create}": WALL,
        "Cut Diorite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Diorite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Diorite Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Diorite Brick Wall (Itemsanity) {Create}": WALL,
        "Small Diorite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Diorite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Diorite Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Diorite Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Diorite (Itemsanity) {Create}": ITEMSANITY,
        "Diorite Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Andesite (Itemsanity) {Create}": ITEMSANITY,
        "Cut Andesite Stairs (Itemsanity) {Create}": STAIR,
        "Cut Andesite Slab (Itemsanity) {Create}": SLAB,
        "Cut Andesite Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Andesite (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Andesite Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Andesite Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Andesite Wall (Itemsanity) {Create}": WALL,
        "Cut Andesite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Andesite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Andesite Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Andesite Brick Wall (Itemsanity) {Create}": WALL,
        "Small Andesite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Andesite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Andesite Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Andesite Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Andesite (Itemsanity) {Create}": ITEMSANITY,
        "Andesite Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Calcite (Itemsanity) {Create}": ITEMSANITY,
        "Cut Calcite Stairs (Itemsanity) {Create}": STAIR,
        "Cut Calcite Slab (Itemsanity) {Create}": SLAB,
        "Cut Calcite Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Calcite (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Calcite Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Calcite Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Calcite Wall (Itemsanity) {Create}": WALL,
        "Cut Calcite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Calcite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Calcite Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Calcite Brick Wall (Itemsanity) {Create}": WALL,
        "Small Calcite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Calcite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Calcite Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Calcite Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Calcite (Itemsanity) {Create}": ITEMSANITY,
        "Calcite Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Dripstone (Itemsanity) {Create}": ITEMSANITY,
        "Cut Dripstone Stairs (Itemsanity) {Create}": STAIR,
        "Cut Dripstone Slab (Itemsanity) {Create}": SLAB,
        "Cut Dripstone Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Dripstone (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Dripstone Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Dripstone Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Dripstone Wall (Itemsanity) {Create}": WALL,
        "Cut Dripstone Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Dripstone Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Dripstone Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Dripstone Brick Wall (Itemsanity) {Create}": WALL,
        "Small Dripstone Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Dripstone Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Dripstone Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Dripstone Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Dripstone (Itemsanity) {Create}": ITEMSANITY,
        "Dripstone Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Tuff (Itemsanity) {Create}": ITEMSANITY,
        "Cut Tuff Stairs (Itemsanity) {Create}": STAIR,
        "Cut Tuff Slab (Itemsanity) {Create}": SLAB,
        "Cut Tuff Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Tuff (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Tuff Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Tuff Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Tuff Wall (Itemsanity) {Create}": WALL,
        "Cut Tuff Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Tuff Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Tuff Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Tuff Brick Wall (Itemsanity) {Create}": WALL,
        "Small Tuff Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Tuff Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Tuff Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Tuff Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Tuff (Itemsanity) {Create}": ITEMSANITY,
        "Tuff Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Asurine (Itemsanity) {Create}": ITEMSANITY,
        "Cut Asurine Stairs (Itemsanity) {Create}": STAIR,
        "Cut Asurine Slab (Itemsanity) {Create}": SLAB,
        "Cut Asurine Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Asurine (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Asurine Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Asurine Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Asurine Wall (Itemsanity) {Create}": WALL,
        "Cut Asurine Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Asurine Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Asurine Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Asurine Brick Wall (Itemsanity) {Create}": WALL,
        "Small Asurine Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Asurine Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Asurine Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Asurine Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Asurine (Itemsanity) {Create}": ITEMSANITY,
        "Asurine Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Crimsite (Itemsanity) {Create}": ITEMSANITY,
        "Cut Crimsite Stairs (Itemsanity) {Create}": STAIR,
        "Cut Crimsite Slab (Itemsanity) {Create}": SLAB,
        "Cut Crimsite Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Crimsite (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Crimsite Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Crimsite Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Crimsite Wall (Itemsanity) {Create}": WALL,
        "Cut Crimsite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Crimsite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Crimsite Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Crimsite Brick Wall (Itemsanity) {Create}": WALL,
        "Small Crimsite Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Crimsite Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Crimsite Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Crimsite Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Crimsite (Itemsanity) {Create}": ITEMSANITY,
        "Crimsite Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Limestone (Itemsanity) {Create}": ITEMSANITY,
        "Cut Limestone Stairs (Itemsanity) {Create}": STAIR,
        "Cut Limestone Slab (Itemsanity) {Create}": SLAB,
        "Cut Limestone Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Limestone (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Limestone Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Limestone Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Limestone Wall (Itemsanity) {Create}": WALL,
        "Cut Limestone Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Limestone Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Limestone Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Limestone Brick Wall (Itemsanity) {Create}": WALL,
        "Small Limestone Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Limestone Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Limestone Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Limestone Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Limestone (Itemsanity) {Create}": ITEMSANITY,
        "Limestone Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Ochrum (Itemsanity) {Create}": ITEMSANITY,
        "Cut Ochrum Stairs (Itemsanity) {Create}": STAIR,
        "Cut Ochrum Slab (Itemsanity) {Create}": SLAB,
        "Cut Ochrum Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Ochrum (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Ochrum Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Ochrum Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Ochrum Wall (Itemsanity) {Create}": WALL,
        "Cut Ochrum Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Ochrum Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Ochrum Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Ochrum Brick Wall (Itemsanity) {Create}": WALL,
        "Small Ochrum Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Ochrum Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Ochrum Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Ochrum Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Ochrum (Itemsanity) {Create}": ITEMSANITY,
        "Ochrum Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Veridium (Itemsanity) {Create}": ITEMSANITY,
        "Cut Veridium Stairs (Itemsanity) {Create}": STAIR,
        "Cut Veridium Slab (Itemsanity) {Create}": SLAB,
        "Cut Veridium Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Veridium (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Veridium Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Veridium Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Veridium Wall (Itemsanity) {Create}": WALL,
        "Cut Veridium Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Veridium Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Veridium Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Veridium Brick Wall (Itemsanity) {Create}": WALL,
        "Small Veridium Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Veridium Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Veridium Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Veridium Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Veridium (Itemsanity) {Create}": ITEMSANITY,
        "Veridium Pillar (Itemsanity) {Create}": ITEMSANITY,
        "Cut Scoria (Itemsanity) {Create}": ITEMSANITY,
        "Cut Scoria Stairs (Itemsanity) {Create}": STAIR,
        "Cut Scoria Slab (Itemsanity) {Create}": SLAB,
        "Cut Scoria Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Scoria (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Scoria Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Scoria Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Scoria Wall (Itemsanity) {Create}": WALL,
        "Cut Scoria Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Scoria Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Scoria Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Scoria Brick Wall (Itemsanity) {Create}": WALL,
        "Small Scoria Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Scoria Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Scoria Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Scoria Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Scoria (Itemsanity) {Create}": ITEMSANITY,
        "Scoria Pillar (Itemsanity) {Create}": ITEMSANITY,
    }, canCraftSPDecorativeStone())

    # Has Iron
    create_region(world, "Menu", "IronAndCutting", {
        "Copper Table Cover (Itemsanity) {Create}": ITEMSANITY,
        "Copper Ladder (Itemsanity) {Create}": ITEMSANITY,
        "Copper Bars (Itemsanity) {Create}": ITEMSANITY,
        "Copper Scaffolding (Itemsanity) {Create}": ITEMSANITY,
        "Framed Glass Door (Itemsanity) {Create}": ITEMSANITY,
        "Framed Glass Trapdoor (Itemsanity) {Create}": ITEMSANITY,
        "Block of Industrial Iron (Itemsanity) {Create}": ITEMSANITY,
        "Block of Weathered Iron (Itemsanity) {Create}": ITEMSANITY,
        "Copper Shingles (Itemsanity) {Create}": ITEMSANITY,
        "Exposed Copper Shingles (Itemsanity) {Create}": ITEMSANITY,
        "Weathered Copper Shingles (Itemsanity) {Create}": ITEMSANITY,
        "Oxidized Copper Shingles (Itemsanity) {Create}": ITEMSANITY,
        "Copper Shingle Slab (Itemsanity) {Create}": SLAB,
        "Exposed Copper Shingle Slab (Itemsanity) {Create}": SLAB,
        "Weathered Copper Shingle Slab (Itemsanity) {Create}": SLAB,
        "Oxidized Copper Shingle Slab (Itemsanity) {Create}": SLAB,
        "Copper Shingle Stairs (Itemsanity) {Create}": STAIR,
        "Exposed Copper Shingle Stairs (Itemsanity) {Create}": STAIR,
        "Weathered Copper Shingle Stairs (Itemsanity) {Create}": STAIR,
        "Oxidized Copper Shingle Stairs (Itemsanity) {Create}": STAIR,
        "Waxed Copper Shingles (Itemsanity) {Create}": ITEMSANITY,
        "Waxed Exposed Copper Shingles (Itemsanity) {Create}": ITEMSANITY,
        "Waxed Weathered Copper Shingles (Itemsanity) {Create}": ITEMSANITY,
        "Waxed Oxidized Copper Shingles (Itemsanity) {Create}": ITEMSANITY,
        "Waxed Copper Shingle Slab (Itemsanity) {Create}": SLAB,
        "Waxed Exposed Copper Shingle Slab (Itemsanity) {Create}": SLAB,
        "Waxed Weathered Copper Shingle Slab (Itemsanity) {Create}": SLAB,
        "Waxed Oxidized Copper Shingle Slab (Itemsanity) {Create}": SLAB,
        "Waxed Copper Shingle Stairs (Itemsanity) {Create}": STAIR,
        "Waxed Exposed Copper Shingle Stairs (Itemsanity) {Create}": STAIR,
        "Waxed Weathered Copper Shingle Stairs (Itemsanity) {Create}": STAIR,
        "Waxed Oxidized Copper Shingle Stairs (Itemsanity) {Create}": STAIR,
        "Copper Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Exposed Copper Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Weathered Copper Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Oxidized Copper Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Copper Tile Slab (Itemsanity) {Create}": SLAB,
        "Exposed Copper Tile Slab (Itemsanity) {Create}": SLAB,
        "Weathered Copper Tile Slab (Itemsanity) {Create}": SLAB,
        "Oxidized Copper Tile Slab (Itemsanity) {Create}": SLAB,
        "Copper Tile Stairs (Itemsanity) {Create}": STAIR,
        "Exposed Copper Tile Stairs (Itemsanity) {Create}": STAIR,
        "Weathered Copper Tile Stairs (Itemsanity) {Create}": STAIR,
        "Oxidized Copper Tile Stairs (Itemsanity) {Create}": STAIR,
        "Waxed Copper Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Waxed Exposed Copper Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Waxed Weathered Copper Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Waxed Oxidized Copper Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Waxed Copper Tile Slab (Itemsanity) {Create}": SLAB,
        "Waxed Exposed Copper Tile Slab (Itemsanity) {Create}": SLAB,
        "Waxed Weathered Copper Tile Slab (Itemsanity) {Create}": SLAB,
        "Waxed Oxidized Copper Tile Slab (Itemsanity) {Create}": SLAB,
        "Waxed Copper Tile Stairs (Itemsanity) {Create}": STAIR,
        "Waxed Exposed Copper Tile Stairs (Itemsanity) {Create}": STAIR,
        "Waxed Weathered Copper Tile Stairs (Itemsanity) {Create}": STAIR,
        "Waxed Oxidized Copper Tile Stairs (Itemsanity) {Create}": STAIR,
        "Tiled Glass (Itemsanity) {Create}": ITEMSANITY,
        "Framed Glass (Itemsanity) {Create}": ITEMSANITY,
        "Horizontal Framed Glass (Itemsanity) {Create}": ITEMSANITY,
        "Vertical Framed Glass (Itemsanity) {Create}": ITEMSANITY,
        "Tiled Glass Pane (Itemsanity) {Create}": ITEMSANITY,
        "Framed Glass Pane (Itemsanity) {Create}": ITEMSANITY,
        "Horizontal Framed Glass Pane (Itemsanity) {Create}": ITEMSANITY,
        "Vertical Framed Glass Pane (Itemsanity) {Create}": ITEMSANITY,
        "Industrial Iron Window (Itemsanity) {Create}": ITEMSANITY,
        "Weathered Iron Window (Itemsanity) {Create}": ITEMSANITY,
        "Industrial Iron Window Pane (Itemsanity) {Create}": ITEMSANITY,
        "Weathered Iron Window Pane (Itemsanity) {Create}": ITEMSANITY
    }, canGetIron() & canCraftSPDecorativeStone())


    # Has Smelting
    create_region(world, "Menu", "SmeltAndCutting", {
        "Cut Deepslate (Itemsanity) {Create}": ITEMSANITY,
        "Cut Deepslate Stairs (Itemsanity) {Create}": STAIR,
        "Cut Deepslate Slab (Itemsanity) {Create}": SLAB,
        "Cut Deepslate Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Deepslate (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Deepslate Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Deepslate Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Deepslate Wall (Itemsanity) {Create}": WALL,
        "Cut Deepslate Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Deepslate Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Deepslate Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Deepslate Brick Wall (Itemsanity) {Create}": WALL,
        "Small Deepslate Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Deepslate Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Deepslate Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Deepslate Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Deepslate (Itemsanity) {Create}": ITEMSANITY,
        "Deepslate Pillar (Itemsanity) {Create}": ITEMSANITY,
    }, canSmelt() & canCraftSPDecorativeStone())

    # Has Nether Access | Black Dye
    create_region(world, "NetherAccess", "NetherAccessAndCutting", {
        "Cut Scorchia (Itemsanity) {Create}": ITEMSANITY,
        "Cut Scorchia Stairs (Itemsanity) {Create}": STAIR,
        "Cut Scorchia Slab (Itemsanity) {Create}": SLAB,
        "Cut Scorchia Wall (Itemsanity) {Create}": WALL,
        "Polished Cut Scorchia (Itemsanity) {Create}": ITEMSANITY,
        "Polished Cut Scorchia Stairs (Itemsanity) {Create}": STAIR,
        "Polished Cut Scorchia Slab (Itemsanity) {Create}": SLAB,
        "Polished Cut Scorchia Wall (Itemsanity) {Create}": WALL,
        "Cut Scorchia Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Cut Scorchia Brick Stairs (Itemsanity) {Create}": STAIR,
        "Cut Scorchia Brick Slab (Itemsanity) {Create}": SLAB,
        "Cut Scorchia Brick Wall (Itemsanity) {Create}": WALL,
        "Small Scorchia Bricks (Itemsanity) {Create}": ITEMSANITY,
        "Small Scorchia Brick Stairs (Itemsanity) {Create}": STAIR,
        "Small Scorchia Brick Slab (Itemsanity) {Create}": SLAB,
        "Small Scorchia Brick Wall (Itemsanity) {Create}": WALL,
        "Layered Scorchia (Itemsanity) {Create}": ITEMSANITY,
        "Scorchia Pillar (Itemsanity) {Create}": ITEMSANITY,
    }, (canAccessNether() | canDyeBlack()) & canCraftSPDecorativeStone())

    # Has Rose Quartz
    create_region(world, "RoseQuartz", "RoseQuartzAndCutting", {
        "Block of Rose Quartz (Itemsanity) {Create}": ITEMSANITY
    }, canCraftRoseQuartz() & canCraftSPDecorativeStone())

    # Has Rose Quartz & Sandpaper
    create_region(world, "RoseQuartz", "RoseQuartzAndCuttingAndSandpaper", {
        "Rose Quartz Tiles (Itemsanity) {Create}": ITEMSANITY,
        "Small Rose Quartz Tiles (Itemsanity) {Create}": ITEMSANITY,
    }, canCraftRoseQuartz() & canCraftSPDecorativeStone() & canUseSandpaper())

    # Has Zinc
    create_region(world, "Zinc", "ZincCutting", {
        "Copycat Step (Itemsanity) {Create}": ITEMSANITY,
        "Copycat Panel (Itemsanity) {Create}": ITEMSANITY,
    }, canGetZinc() & canCraftSPDecorativeStone())

    # Has Andesite Alloy
    create_region(world, "AndesiteAlloy", "AndesiteAlloyCutting", {
        "Andesite Table Cover (Itemsanity) {Create}": ITEMSANITY,
        "Andesite Ladder (Itemsanity) {Create}": ITEMSANITY,
        "Andesite Bars (Itemsanity) {Create}": ITEMSANITY,
        "Andesite Scaffolding (Itemsanity) {Create}": ITEMSANITY,
    }, canCraftAndesiteAlloy() & canCraftSPDecorativeStone())

    # Has Brass
    create_region(world, "Brass", "BrassCutting", {
        "Brass Table Cover (Itemsanity) {Create}": ITEMSANITY,
        "Brass Ladder (Itemsanity) {Create}": ITEMSANITY,
        "Brass Bars (Itemsanity) {Create}": ITEMSANITY,
        "Brass Scaffolding (Itemsanity) {Create}": ITEMSANITY,
    }, canCraftBrass() & canCraftSPDecorativeStone())

    ####################################################################################################################
    # DYED ITEMS #######################################################################################################
    ####################################################################################################################

    # Regular Dye & Press
    create_region(world, "AndesiteAlloy", "RegularDyeAndPress", {
        "Red Valve Handle (Itemsanity) {Create}": DYE,
        "Yellow Valve Handle (Itemsanity) {Create}": DYE,
        "Blue Valve Handle (Itemsanity) {Create}": DYE,
        "White Valve Handle (Itemsanity) {Create}": DYE
    }, canDyeBasic() & hasPress())

    # Black Dye & Press
    create_region(world, "AndesiteAlloy", "BlackDyeAndPress", {
        "Black Valve Handle (Itemsanity) {Create}": DYE,
        "Gray Valve Handle (Itemsanity) {Create}": DYE
    }, canDyeBlack() & hasPress())

    # Green Dye & Press
    create_region(world, "AndesiteAlloy", "GreenDyeAndPress", {
        "Green Valve Handle (Itemsanity) {Create}": DYE_AND_EXPLORATION
    }, hasPress() & canDyeGreen())

    # Full Dye & Press
    create_region(world, "AndesiteAlloy", "FullDyeAndPress", {
        "Orange Valve Handle (Itemsanity) {Create}": DYE,
        "Light Blue Valve Handle (Itemsanity) {Create}": DYE,
        "Purple Valve Handle (Itemsanity) {Create}": DYE,
        "Light Gray Valve Handle (Itemsanity) {Create}": DYE,
        "Brown Valve Handle (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Pink Valve Handle (Itemsanity) {Create}": DYE,
        "Magenta Valve Handle (Itemsanity) {Create}": DYE
    }, canDyeFull() & hasPress())
    smart_add_rule(world, "Brown Valve Handle (Itemsanity) {Create}", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Lime & Cyan Dye & Press
    create_region(world, "AndesiteAlloy", "LimeAndCyanDyeAndPress", {
        "Lime Valve Handle (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Cyan Valve Handle (Itemsanity) {Create}": DYE_AND_EXPLORATION
    }, canDyeFull() & hasPress() & canDyeGreen())




    # Regular Dye & Storage
    create_region(world, "AndesiteAlloy", "RegularDyeAndStorageAndAlloy", {
        "Red Postbox (Itemsanity) {Create}": DYE,
        "Yellow Postbox (Itemsanity) {Create}": DYE,
        "Blue Postbox (Itemsanity) {Create}": DYE,
        "White Postbox (Itemsanity) {Create}": DYE
    }, canDyeBasic() & canAccessChests())

    # Black Dye & Storage
    create_region(world, "AndesiteAlloy", "BlackDyeAndStorageAndAlloy", {
        "Black Postbox (Itemsanity) {Create}": DYE,
        "Gray Postbox (Itemsanity) {Create}": DYE
    }, canDyeBlack() & canAccessChests())

    # Green Dye & Storage
    create_region(world, "AndesiteAlloy", "GreenDyeAndStorageAndAlloy", {
        "Green Postbox (Itemsanity) {Create}": DYE_AND_EXPLORATION
    }, canAccessChests() & canDyeGreen())

    # Full Dye & Storage
    create_region(world, "AndesiteAlloy", "FullDyeAndStorageAndAlloy", {
        "Orange Postbox (Itemsanity) {Create}": DYE,
        "Light Blue Postbox (Itemsanity) {Create}": DYE,
        "Purple Postbox (Itemsanity) {Create}": DYE,
        "Light Gray Postbox (Itemsanity) {Create}": DYE,
        "Brown Postbox (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Pink Postbox (Itemsanity) {Create}": DYE,
        "Magenta Postbox (Itemsanity) {Create}": DYE
    }, canDyeFull() & canAccessChests())
    smart_add_rule(world, "Brown Postbox (Itemsanity) {Create}", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Lime & Cyan Dye & Storage
    create_region(world, "AndesiteAlloy", "LimeAndCyanDyeAndStorageAndAlloy", {
        "Lime Postbox (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Cyan Postbox (Itemsanity) {Create}": DYE_AND_EXPLORATION
    }, canDyeFull() & canAccessChests() & canDyeGreen())


    # Regular Dye
    create_region(world, "AndesiteAlloy", "RegularDye", {
        "Red Table Cloth (Itemsanity) {Create}": DYE,
        "Yellow Table Cloth (Itemsanity) {Create}": DYE,
        "Blue Table Cloth (Itemsanity) {Create}": DYE,
        "White Table Cloth (Itemsanity) {Create}": DYE,

        "Red Seat (Itemsanity) {Create}": DYE,
        "Yellow Seat (Itemsanity) {Create}": DYE,
        "Blue Seat (Itemsanity) {Create}": DYE,
        "White Seat (Itemsanity) {Create}": DYE
    }, canDyeBasic())

    # Black Dye
    create_region(world, "AndesiteAlloy", "BlackDye", {
        "Black Table Cloth (Itemsanity) {Create}": DYE,
        "Gray Table Cloth (Itemsanity) {Create}": DYE,

        "Black Seat (Itemsanity) {Create}": DYE,
        "Gray Seat (Itemsanity) {Create}": DYE
    }, canDyeBlack())

    # Green Dye
    create_region(world, "AndesiteAlloy", "GreenDye", {
        "Green Table Cloth (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Green Seat (Itemsanity) {Create}": DYE_AND_EXPLORATION,
    }, canDyeGreen())

    # Full Dye
    create_region(world, "AndesiteAlloy", "FullDye", {
        "Orange Table Cloth (Itemsanity) {Create}": DYE,
        "Light Blue Table Cloth (Itemsanity) {Create}": DYE,
        "Purple Table Cloth (Itemsanity) {Create}": DYE,
        "Light Gray Table Cloth (Itemsanity) {Create}": DYE,
        "Brown Table Cloth (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Pink Table Cloth (Itemsanity) {Create}": DYE,
        "Magenta Table Cloth (Itemsanity) {Create}": DYE,

        "Orange Seat (Itemsanity) {Create}": DYE,
        "Light Blue Seat (Itemsanity) {Create}": DYE,
        "Purple Seat (Itemsanity) {Create}": DYE,
        "Light Gray Seat (Itemsanity) {Create}": DYE,
        "Brown Seat (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Pink Seat (Itemsanity) {Create}": DYE,
        "Magenta Seat (Itemsanity) {Create}": DYE
    }, canDyeFull())
    smart_add_rule(world, "Brown Table Cloth (Itemsanity) {Create}", jungleBiomesExploration(), DYE_AND_EXPLORATION)
    smart_add_rule(world, "Brown Seat (Itemsanity) {Create}", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Lime & Cyan Dye
    create_region(world, "AndesiteAlloy", "LimeAndCyanDye", {
        "Lime Table Cloth (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Cyan Table Cloth (Itemsanity) {Create}": DYE_AND_EXPLORATION,

        "Lime Seat (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Cyan Seat (Itemsanity) {Create}": DYE_AND_EXPLORATION
    }, canDyeFull() & canDyeGreen())


    # Regular Dye & Press & Storage & Gold
    create_region(world, "AndesiteAlloy", "RegularDyeAndPressAndStorageAndGold", {
        "Red Toolbox (Itemsanity) {Create}": DYE,
        "Yellow Toolbox (Itemsanity) {Create}": DYE,
        "Blue Toolbox (Itemsanity) {Create}": DYE,
        "White Toolbox (Itemsanity) {Create}": DYE
    }, canDyeBasic() & hasPress() & canAccessChests() & canGetGold())

    # Black Dye & Press & Storage & Gold
    create_region(world, "AndesiteAlloy", "BlackDyeAndPressAndStorageAndGold", {
        "Black Toolbox (Itemsanity) {Create}": DYE,
        "Gray Toolbox (Itemsanity) {Create}": DYE
    }, canDyeBlack() & hasPress() & canAccessChests() & canGetGold())

    # Green Dye & Press & Storage & Gold
    create_region(world, "AndesiteAlloy", "GreenDyeAndPressAndStorageAndGold", {
        "Green Toolbox (Itemsanity) {Create}": DYE_AND_EXPLORATION
    }, hasPress() & canDyeGreen() & canAccessChests() & canGetGold())

    # Full Dye & Press & Storage & Gold
    create_region(world, "AndesiteAlloy", "FullDyeAndPressAndStorageAndGold", {
        "Orange Toolbox (Itemsanity) {Create}": DYE,
        "Light Blue Toolbox (Itemsanity) {Create}": DYE,
        "Purple Toolbox (Itemsanity) {Create}": DYE,
        "Light Gray Toolbox (Itemsanity) {Create}": DYE,
        "Brown Toolbox (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Pink Toolbox (Itemsanity) {Create}": DYE,
        "Magenta Toolbox (Itemsanity) {Create}": DYE
    }, canDyeFull() & hasPress() & canAccessChests() & canGetGold())
    smart_add_rule(world, "Brown Toolbox (Itemsanity) {Create}", jungleBiomesExploration(), DYE_AND_EXPLORATION)

    # Lime & Cyan Dye & Press & Storage & Gold
    create_region(world, "AndesiteAlloy", "LimeAndCyanDyeAndPressAndStorageAndGold", {
        "Lime Toolbox (Itemsanity) {Create}": DYE_AND_EXPLORATION,
        "Cyan Toolbox (Itemsanity) {Create}": DYE_AND_EXPLORATION
    }, canDyeFull() & hasPress() & canDyeGreen() & canAccessChests() & canGetGold())



def create_region(world: FabricMinecraftWorld, region_name: str, new_region_name: str, locations: dict[str, int], rule=None):
    create_locations_and_connect(world, region_name + "CreateItemsanity", new_region_name + "CreateItemsanity", locations, rule)