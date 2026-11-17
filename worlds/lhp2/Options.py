from dataclasses import dataclass
from Options import DefaultOnToggle, Toggle, Range, Choice, PerGameCommonOptions, OptionList


class EndGoal(Choice):
    """
    Determine the goal for the seed

    Defeat Voldemort: Collect the 7 Horcruxes and defeat Voldemort in The Flaw in the Plan

    Levels Beaten: Beat X number of levels to win
    """
    display_name = "Goal"
    option_defeat_voldemort = 0
    # option_the_collector = 1
    option_levels_beaten = 2
    default = 0


# class CollectibleQuantity(OptionDict):
#     """
#     The number of each collectible you need to beat the seed. Does nothing if the collector is your not win con.
#
#     Valid Keys:
#     - Character Token
#     - Gold Brick
#     - House Crest Completed
#     - Student in Peril
#     - True Wizard
#     """
#     display_name = "Collectibles Required"
#     min = 0
#     max_values_dict: dict[str, int] = {
#         ItemName.gb: 200,
#         ItemName.sip: 60,
#         ItemName.tw: 24,
#         ItemName.ct: 200,
#         ItemName.hcgb: 24,
#     }
#     default = {ItemName.gb: 100, ItemName.sip: 30, ItemName.tw: 12, ItemName.ct: 100, ItemName.hcgb: 12}


# class FlawInThePlanCondition(Choice):
#     """
#     Determine the Level Unlock Condition for The Flaw in The Plan. Does nothing if Voldemort is not the goal.
#     """
#     display_name = "Flaw In The Plan Unlock Condition"
#     option_horcruxes = 0
#     option_level_shuffled = 1
#     default = 0


class NumHorcruxesRequired(Range):
    """
    Determine the required number of Horcruxes to beat the game.
    """
    display_name = "Number of Horcruxes"
    range_start = 1
    range_end = 7
    default = 4


class NumLevelsRequired(Range):
    """
    Determine the required number of Levels Required to beat the game.
    """
    display_name = "Number of Levels Required"
    range_start = 1
    range_end = 24
    default = 12


class NumStartSpells(Range):
    """
    Determine the number of starting spells (excludes joke spells).
    """
    display_name = "Number of Starting Spells"
    range_start = 0
    range_end = 14
    default = 0


class NumStartLevels(Range):
    """
    Determine the number of starting levels.
    """
    display_name = "Number of Starting Levels"
    range_start = 0
    range_end = 24
    default = 0


class StartingLevelOptions(OptionList):
    """
    Determines which levels you start with.

    Valid Keys:
    "Dark Times"
    "Dumbledore's Army"
    "Focus!"
    "Kreacher Discomforts"
    "A Giant Virtuoso"
    "A Veiled Threat"
    "Out of Retirement"
    "Just Desserts"
    "A Not So Merry Christmas"
    "Love Hurts"
    "Felix Felicis"
    "The Horcrux and the Hand"
    "The Seven Harry's"
    "Magic is Might"
    "In Grave Danger"
    "Sword and Locket"
    "Lovegood's Lunacy"
    "DOBBY!"
    "The Thief's Downfall"
    "Back to School"
    "Burning Bridges"
    "Fiendfyre Frenzy"
    "Snape's Tears"
    "The Flaw in the Plan"
    """

    display_name = "Starting Level Options"

    valid_keys = {
        "Dark Times",
        "Dumbledore's Army",
        "Focus!",
        "Kreacher Discomforts",
        "A Giant Virtuoso",
        "A Veiled Threat",
        "Out of Retirement",
        "Just Desserts",
        "A Not So Merry Christmas",
        "Love Hurts",
        "Felix Felicis",
        "The Horcrux and the Hand",
        "The Seven Harrys",
        "Magic is Might",
        "In Grave Danger",
        "Sword and Locket",
        "Lovegood's Lunacy",
        "DOBBY!",
        "The Thief's Downfall",
        "Back to School",
        "Burning Bridges",
        "Fiendfyre Frenzy",
        "Snape's Tears",
        "The Flaw in the Plan",
    }

    default = [
        "Dark Times",
        "Dumbledore's Army",
        "Focus!",
        "Kreacher Discomforts",
        "A Giant Virtuoso",
        "A Veiled Threat",
        "Out of Retirement",
        "Just Desserts",
        "A Not So Merry Christmas",
        "Love Hurts",
        "Felix Felicis",
        "The Horcrux and the Hand",
        "The Seven Harrys",
        "Magic is Might",
        "In Grave Danger",
        "Sword and Locket",
        "Lovegood's Lunacy",
        "DOBBY!",
        "The Thief's Downfall",
        "Back to School",
        "Burning Bridges",
        "Fiendfyre Frenzy",
        "Snape's Tears",
        "The Flaw in the Plan",
    ]


class DisabledLevels(OptionList):
    """
    Determines which levels won't have any checks.
    Each level disabled removes 3 purple studs from the pool (6 in the case of The Seven Harrys).
    If there are no purple studs remaining, Gold bricks will then be removed.

    Valid Keys:
    "Dark Times"
    "Dumbledore's Army"
    "Focus!"
    "Kreacher Discomforts"
    "A Giant Virtuoso"
    "A Veiled Threat"
    "Out of Retirement"
    "Just Desserts"
    "A Not So Merry Christmas"
    "Love Hurts"
    "Felix Felicis"
    "The Horcrux and the Hand"
    "The Seven Harry's"
    "Magic is Might"
    "In Grave Danger"
    "Sword and Locket"
    "Lovegood's Lunacy"
    "DOBBY!"
    "The Thief's Downfall"
    "Back to School"
    "Burning Bridges"
    "Fiendfyre Frenzy"
    "Snape's Tears"
    "The Flaw in the Plan"
    """

    display_name = "Disabled Levels"

    valid_keys = {
        "Dark Times",
        "Dumbledore's Army",
        "Focus!",
        "Kreacher Discomforts",
        "A Giant Virtuoso",
        "A Veiled Threat",
        "Out of Retirement",
        "Just Desserts",
        "A Not So Merry Christmas",
        "Love Hurts",
        "Felix Felicis",
        "The Horcrux and the Hand",
        "The Seven Harrys",
        "Magic is Might",
        "In Grave Danger",
        "Sword and Locket",
        "Lovegood's Lunacy",
        "DOBBY!",
        "The Thief's Downfall",
        "Back to School",
        "Burning Bridges",
        "Fiendfyre Frenzy",
        "Snape's Tears",
        "The Flaw in the Plan",
    }

    default = []


class ShuffleCharacterTokens(Choice):
    """
    Determines how Character Tokens are shuffled in the Multiworld.

    Tokens & Purchases means the tokens collected and purchases and unlocks are items and location (2 separate items & 2 separate locations).
    Tokens only means that tokens collected are locations and extras unlocks are items (1 item & 1 location).
    Purchases only means that purchases are locations and extras unlocks are items (1 item & 1 location). In this setting you, you have to collect the token before you can purchase it.

    Please note that Purchases only and Disabled Levels are incompatible settings
    """
    display_name = "Character Token Shuffle"
    option_tokens_and_purchases = 0
    option_tokens_only = 1
    option_purchases_only = 2
    default = 0


class ShuffleRedBricks(Choice):
    """
    Determines how Red Bricks are shuffled in the Multiworld.

    Bricks & Purchases means the red bricks collected in the hub and purchases and unlocks are items and location (2 separate items & 2 separate locations).
    Bricks only means that red bricks collected in the hub are locations and extras unlocks are items (1 item & 1 location).
    Purchases only means that purchases are locations and extras unlocks are items (1 item & 1 location). In this setting you, you have to collect the red brick in the hub before you can purchase it.
    """
    display_name = "Red Brick Shuffle"
    option_bricks_and_purchases = 0
    option_bricks_only = 1
    option_purchases_only = 2
    default = 0


class ShuffleJokeSpells(DefaultOnToggle):
    """
    Turning this on makes it so Joke Shop purchases are shuffled
    """
    display_name = "Shuffle Joke Shop Purchases"


class ShuffleGoldBrickPurchases(DefaultOnToggle):
    """
    Turning this on makes it so Gold Brick purchases are shuffled
    Removes Purples studs from the pool first and then removes Gold Bricks
    """
    display_name = "Shuffle Gold Brick Purchases"


class CheaperShops(Range):
    """
    Determines how many times cheaper purchases are from vanilla game.
    1 is no change and 10 is 10x cheaper.
    This is taken into account for stud multiplier logic
    """
    display_name = "Cheaper Shop Purchases"
    range_start = 1
    range_end = 10
    default = 5


class HardPurchases(Toggle):
    """
    Turning this on makes it so purchases no longer require a stud multiplier.
    """
    display_name = "Hard Purchases"


class LowMultiplierPriceMinimum(Range):
    """
    Determines the starting price for a low multiplier.
    A low multiplier is defined as any multiplier.
    """
    display_name = "Low Multiplier Price Minimum"
    range_start = 10
    range_end = 10000000
    default = 50000


class HighMultiplierPriceMinimum(Range):
    """
    Determines the starting price for a high multiplier.
    Must be larger than Low Multiplier Price.
    A high multiplier is defined as Score x6, Score x8, Score x10 or both Score x2 and Score x4.
    """
    display_name = "High Multiplier Price Minimum"
    range_start = 10
    range_end = 10000000
    default = 100000


class StartingDetectors(DefaultOnToggle):
    """
    Determines if the player starts with Character Token, Red Brick, Hogwarts Crest, & Gold Brick Detectors.
    """
    display_name = "Start With Detectors"


class StartingFastMagic(DefaultOnToggle):
    """
    Determines if the player starts with Fast Magic & Dig.
    """
    display_name = "Start With Fast Magic & Dig"


class FasterDuels(DefaultOnToggle):
    """
    Turning this on means that all enemies and players only have 1 HP in duels
    """
    display_name = "Faster Duels"


@dataclass
class LHP2Options(PerGameCommonOptions):
    EndGoal: EndGoal
    # CollectibleQuantity: CollectibleQuantity
    # FlawInThePlanCondition: FlawInThePlanCondition
    NumHorcruxRequired: NumHorcruxesRequired
    NumLevelsRequired: NumLevelsRequired
    NumStartSpells: NumStartSpells
    NumStartLevels: NumStartLevels
    StartingLevelOptions: StartingLevelOptions
    DisabledLevels: DisabledLevels
    ShuffleCharacterTokens: ShuffleCharacterTokens
    ShuffleRedBricks: ShuffleRedBricks
    ShuffleJokeSpells: ShuffleJokeSpells
    ShuffleGoldBrickPurchases: ShuffleGoldBrickPurchases
    CheaperShops: CheaperShops
    HardPurchases: HardPurchases
    LowMultiplierPriceMinimum: LowMultiplierPriceMinimum
    HighMultiplierPriceMinimum: HighMultiplierPriceMinimum
    StartingDetectors: StartingDetectors
    StartingFastMagic: StartingFastMagic
    FasterDuels: FasterDuels
