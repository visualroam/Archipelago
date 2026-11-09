from __future__ import annotations


from worlds.minecraft_fabric.region.regions_helper import create_locations_and_connect, smart_add_rule
from worlds.minecraft_fabric.logic.create_logic import *
from worlds.minecraft_fabric.region.mc_regions_consts import *

if TYPE_CHECKING:
   from worlds.minecraft_fabric import FabricMinecraftWorld


def create_create_advancement_regions(world: FabricMinecraftWorld):
    create_locations_and_connect(world, "Menu", "MenuCreateAdvancements", {})

    # Has Andesite Alloy
    create_region(world, "Menu", "AndesiteAlloy", {
        "Sturdier Rocks {Create}": ADVANCEMENT,
        "The Andesite Age {Create}": ADVANCEMENT,
        "Workout Session {Create}": ADVANCEMENT
    }, canCraftAndesiteAlloyCreate())

    # REQUIRES ROSE QUARTZ
    create_region(world, "Menu", "RoseQuartz", {
        "Supercharged {Create}": ADVANCEMENT
    }, canCraftRoseQuartz() & canUseSandpaper())

    # REQUIRES SMELTING
    create_region(world, "Menu", "Smelting", {
        "Cuprum Bokum {Create}": ADVANCEMENT,
        "The Copper Age {Create}": ADVANCEMENT,
        "Tumble Draining {Create}": ADVANCEMENT,
        "On a Roll {Create}": ADVANCEMENT
    }, canGetIron())

    # Has Diving Suit
    create_region(world, "AndesiteAlloy", "HasDivingSuit", {
        "Pressure to Go {Create}": ADVANCEMENT,
        "Ready for the Depths {Create}": ADVANCEMENT
    }, canWearGoldArmor() & canCompactResources())

    # Has Spout
    create_region(world, "AndesiteAlloy", "HasSpout", {
        "Sploosh {Create}": ADVANCEMENT
    }, canUseSpout())

    # Has Steam Engine
    create_region(world, "AndesiteAlloy", "SteamEngine", {
        "The Powerhouse {Create}": ADVANCEMENT
    }, hasSteamEngine())

    # Has Cogs
    create_region(world, "AndesiteAlloy", "Cogs", {
        "Shifting Gears {Create}": ADVANCEMENT,
        "Embrace the Grind {Create}": ADVANCEMENT
    }, hasCogs())

    # Has Water Wheel
    create_region(world, "AndesiteAlloy", "WaterWheel", {
        "Harnessed Hydraulics {Create}": ADVANCEMENT
    }, hasWaterWheel())

    # Has Windmill
    create_region(world, "AndesiteAlloy", "Windmill", {
        "A mild Breeze {Create}": ADVANCEMENT,
        "A strong Breeze {Create}": ADVANCEMENT
    }, hasWindmill())

    # Has Press
    create_region(world, "AndesiteAlloy", "Press", {
        "Area of Connect {Create}": ADVANCEMENT,
        "Moving with Purpose {Create}": ADVANCEMENT,
        "Drive-by Exchange {Create}": ADVANCEMENT,
        "Rope to Nowhere {Create}": ADVANCEMENT,
        "Bonk! {Create}": ADVANCEMENT,
        "Wind Maker {Create}": ADVANCEMENT,
        "Processing by Particle {Create}": ADVANCEMENT,
        "Workshop's Most Feared {Create}": ADVANCEMENT,
        "Compactification {Create}": ADVANCEMENT,
        "Vertical Logistics {Create}": ADVANCEMENT,
        "Remote Activation {Create}": ADVANCEMENT
    }, hasPress())

    # Has Pump
    create_region(world, "Press", "HasPump", {
        "Under Pressure {Create}": ADVANCEMENT,
        "Don't Cross the Streams! {Create}": ADVANCEMENT,
        "Flow Discovery {Create}": ADVANCEMENT,
        "Puddle Collector {Create}": ADVANCEMENT,
        "Industrial Spillage {Create}": ADVANCEMENT,
        "Autonomous Bee-Keeping {Create}": ADVANCEMENT
    }, hasPump())

    # Has Mixer
    create_region(world, "AndesiteAlloy", "Mixer", {
        "Mixing It Up {Create}": ADVANCEMENT
    }, hasMixer())

    # Has Kelp
    create_region(world, "AndesiteAlloy", "Kelp", {
        "Kelp Drive {Create}": ADVANCEMENT
    }, canCraftAndesiteAlloy() & canCraftDriedKelp())

    # Has Cardboard
    create_region(world, "AndesiteAlloy", "Cardboard", {
        "Part and Parcel {Create}": ADVANCEMENT,
        "Full Stealth {Create}": ADVANCEMENT
    }, canCraftCardboard())

    # Has Packager
    create_region(world, "Cardboard", "Packager", {
        "Post Production {Create}": ADVANCEMENT,
        "Order Up! {Create}": ADVANCEMENT,
        "Open for business {Create}": ADVANCEMENT,
        "Nothing but net {Create}": ADVANCEMENT
    }, canUsePackager())

    # Has Brass
    create_region(world, "AndesiteAlloy", "Brass", {
        "Real Alloys {Create}": ADVANCEMENT,
        "The Brass Age {Create}": ADVANCEMENT,
        "Shadow Sense {Create}": ADVANCEMENT,
        "Contraption o'Clock {Create}": ADVANCEMENT,
        "Big Data {Create}": ADVANCEMENT,
    }, canCraftBrass())

    # Has Brass & Sandpaper
    create_region(world, "AndesiteAlloy", "BrassAndSandpaper", {
        "Artificial Intelligence {Create}": ADVANCEMENT,
        "Pound It, Bro! {Create}": ADVANCEMENT
    }, canCraftBrass() & canUseSandpaper())

    # Has Brass & Minecarts
    create_region(world, "Brass", "BrassAndMinecarts", {
        "Self-Driving Cart {Create}": ADVANCEMENT
    }, canCraftBrass() & canUseMinecart())

    # Has Percision Mechanism
    create_region(world, "Brass", "PercisionMechanism", {
        "Complex Curiosities {Create}": ADVANCEMENT,
        "Engineers hate this simple trick! {Create}": ADVANCEMENT,
        "Busy Hands {Create}": ADVANCEMENT,
        "Organize-o-Tron {Create}": ADVANCEMENT,
        "DJ Mechanico {Create}": ADVANCEMENT
    }, canCraftPercisionMechanism())

    # Has Mechanical Crafters
    create_region(world, "Brass", "MechanicalCrafter", {
        "Automated Assembly {Create}": ADVANCEMENT,
        "Crushing It {Create}": ADVANCEMENT,
        "Wheels of Destruction {Create}": ADVANCEMENT
    }, hasMechanicalCrafter())

    # Has Sturdy Sheet
    create_region(world, "Brass", "SturdySheet", {
        "The Sturdiest Rocks {Create}": ADVANCEMENT,
        "The Locomotive Age {Create}": ADVANCEMENT,
        "All Aboard! {Create}": ADVANCEMENT,
        "Choo Choo! {Create}": ADVANCEMENT,
        "Dimensional Commuter {Create}": ADVANCEMENT_HARD,
        "Ambitious Endeavours {Create}": ADVANCEMENT_HARD,
        "Field Trip {Create}": ADVANCEMENT_UNREASONABLE,
        "Conductor Instructor {Create}": ADVANCEMENT,
        "Traffic Control {Create}": ADVANCEMENT,
        "Blind Spot {Create}": ADVANCEMENT_HARD,
        "Road Kill {Create}": ADVANCEMENT,
        "Dynamic Timetables {Create}": ADVANCEMENT,
        "Expert Driver {Create}": ADVANCEMENT,
        "Terrible Service {Create}": ADVANCEMENT_HARD
    }, canCraftSturdySheet())

    # Has Train Tracks
    create_region(world, "AndesiteAlloy", "TrainTracks", {
        "A New Gauge {Create}": ADVANCEMENT,
        "Track Factory {Create}": ADVANCEMENT_UNREASONABLE
    }, canCraftTrainTracks())

    # Has Percision Mechanism & Mechanical Crafter
    create_region(world, "PercisionMechanism", "PercisionMechanismAndMechanicalCrafter", {
        "Fwoomp! {Create}": ADVANCEMENT,
        "Boioioing! {Create}": ADVANCEMENT,
        "Veggie Fireworks {Create}": ADVANCEMENT_HARD,
        "To Full Extent {Create}": ADVANCEMENT_HARD,
        "Desperate Measures {Create}": ADVANCEMENT
    }, canCraftPercisionMechanism() & hasMechanicalCrafter())

    # Has Percision Mechanism & Blaze Burner
    create_region(world, "PercisionMechanism", "PercisionMechanismAndBlazeBurner", {
        "Combust-o-Tron {Create}": ADVANCEMENT
    }, canCraftPercisionMechanism() & hasBlazeBurner())

    # Has Cardboard & Smithing
    create_region(world, "Cardboard", "CardboardAndSmithing", {
        "Arts and Crafts {Create}": ADVANCEMENT
    }, canCraftCardboard() & canGetAndUseArmorTrims())

    # Has Packager & Precision Mechanism
    create_region(world, "Packager", "PackagerAndPrecisionMechanism", {
        "High Logistics {Create}": ADVANCEMENT
    }, canUsePackager() & canCraftPercisionMechanism())

    # Has Packager & Bucket
    create_region(world, "Packager", "PackagerAndBucket", {
        "Hungry hoppers {Create}": ADVANCEMENT_EXPLORATION
    }, canUsePackager() & canUseBucket())
    smart_add_rule(world, "Hungry hoppers {Create}", wetlandBiomesExploration(), ADVANCEMENT_EXPLORATION)

    # Has Water Wheel & Bucket
    create_region(world, "WaterWheel", "WaterWheelAndBucket", {
        "Magma Wheel {Create}": ADVANCEMENT
    }, hasWaterWheel() & canUseBucket())

    # Has Kelp & Press
    create_region(world, "Kelp", "KelpAndPress", {
        "The Parrots and the Flaps {Create}": ADVANCEMENT
    }, canCraftAndesiteAlloy() & canCraftDriedKelp() & hasPress())


    # Has Steam Engine & Press
    create_region(world, "Press", "SteamEngineAndPress", {
        "Voice of an Angel {Create}": ADVANCEMENT,
        "The Pipe Organ {Create}": ADVANCEMENT
    }, hasSteamEngine() & hasPress())

    # Has Press & Nether
    create_region(world, "Press", "PressAndNether", {
        "Sentient Fireplace {Create}": ADVANCEMENT
    }, hasPress() & canAccessNether())

    # Has Kelp & Chests
    create_region(world, "Kelp", "KelpAndChests", {
        "Airport Aesthetic {Create}": ADVANCEMENT
    }, canCraftAndesiteAlloy() & canCraftDriedKelp() & canAccessChests())

    # Has Press & Minecarts
    create_region(world, "Press", "PressAndMinecart", {
        "Strong Arms {Create}": ADVANCEMENT_HARD
    }, hasPress() & canUseMinecart())

    # Has Press & Cogs
    create_region(world, "Press", "PressAndCogs", {
        "Springboard Champion {Create}": ADVANCEMENT
    }, hasPress() & hasCogs())

    # Has Press & Cogs & Nether & Buckets
    create_region(world, "PressAndCogs", "PressAndCogsAndNetherAndBuckets", {
        "Tapping the Mantle {Create}": ADVANCEMENT_UNREASONABLE
    }, hasPress() & hasCogs() & canAccessNether() & canUseBucket()
                     & canAccessChests())

    # Can Max Out Boiler
    create_region(world, "Menu", "CanMaxOutBoiler", {
        "Full Steam {Create}": ADVANCEMENT_UNREASONABLE
    }, hasSteamEngine() & canUseBlazeCake() & canUseBucket()
                     & hasCogs() & canAccessChests())

    # Can Use Netherite Diving Gear
    create_region(world, "AndesiteAlloy", "NetheriteDivingGear", {
        "Swimming with the Striders {Create}": ADVANCEMENT_HARD
    }, canCompactResources() & canWearNetheriteArmor() & canGetIron())

    # Can Make Fluid Foods
    create_region(world, "Menu", "CanMakeFluidFoods", {
        "Balanced Diet {Create}": ADVANCEMENT_UNREASONABLE
    }, canUseSpout() & canUseBottles() & canUseBucket() & hasBlazeBurner())

    # Has Iron Tools
    create_region(world, "AndesiteAlloy", "AlloyAndIronTools", {
        "Is it Time? {Create}": ADVANCEMENT
    }, canUseIronTools())

    # Has Press & Armor
    create_region(world, "Press", "PressAndArmor", {
        "Kitted Out {Create}": ADVANCEMENT,
        "Stress for Nerds {Create}": ADVANCEMENT,
        "Perfectly Stressed {Create}": ADVANCEMENT
    }, hasPress() & canWearLeatherArmor() & canUseIronTools())

    # Has Mechanical Press & Enchanting
    create_region(world, "AndesiteAlloy", "MechanicalPressAndEnchant", {
        "Blacksmith Artillery {Create}": ADVANCEMENT
    }, canCraftAndesiteAlloyCreate() & canEnchant())

    # Can Make Chocolate
    create_region(world, "Mixer", "CanMakeChocolate", {
        "A World of Imagination {Create}": ADVANCEMENT
    }, hasMixer() & hasPump() & canUseBucket() & hasBlazeBurner())


def create_region(world: FabricMinecraftWorld, region_name: str, new_region_name: str, locations: dict[str, int], rule=None):
    create_locations_and_connect(world, region_name + "CreateAdvancements", new_region_name + "CreateAdvancements", locations, rule)