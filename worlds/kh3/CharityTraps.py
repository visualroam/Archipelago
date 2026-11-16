"""KH3 AP items handled by the client during a charity run."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CharityTrap:
    key: str
    duration: int
    instructions: str | None = None
    pro_codes: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProCode:
    key: str
    item_name: str
    label: str
    mask: int


# Premium Menu order. Masks are the two-byte little-endian word measured at
# 0x94F2F1 in the Windows Steam build by the v5 in-game trace.
PRO_CODES = (
    ProCode("LEVEL_ONE", "Trap: Lvl1 Stats", "Grundstatus", 0x0001),
    ProCode("ZERO_DEFENSE", "Trap: Zero Defense", "Null Abwehr", 0x0002),
    ProCode("HP_SLIP", "Trap: HP Slip", "LP-Sturz", 0x0008),
    ProCode("MP_SLIP", "Trap: MP Slip", "MP-Sturz", 0x0010),
    ProCode("NO_SHOTLOCKS", "Trap: No Shotlocks", "Multifokus-Sperre", 0x0100),
    ProCode("NO_CURE", "Trap: No Cure", "Vita-Sperre", 0x0020),
    ProCode("NO_BATTLE_ITEMS", "Trap: No Battle Items", "Kampf-Item-Sperre", 0x0040),
    ProCode("NO_LINKS", "Trap: No Links", "Koop-Sperre", 0x0800),
    ProCode("NO_FORMCHANGE", "Trap: No Formchange", "Form-Starre und keine Hochmagie", 0x0080),
    ProCode("NO_ATTRACTIONS", "Trap: No Attraction Flow", "Attraktionen-Sperre", 0x0200),
    ProCode("NO_TEAM_ATTACKS", "Trap: No Team Attacks", "Teamangriffs-Sperre", 0x0400),
    ProCode("NO_KUPO_COINS", "Trap: No Kupo Coins", "Kupo-Münzen-Sperre", 0x1000),
    ProCode("ABILITY_LIMIT", "Trap: Ability Limit", "Fertigkeiten-Limit", 0x0004),
)
PRO_CODE_MASKS = {code.key: code.mask for code in PRO_CODES}
PRO_CODE_MASK = sum(PRO_CODE_MASKS.values())


CHARITY_TRAPS = {
    "Trap: Blackout": CharityTrap("BLACKOUT", 2),
    "Trap: Lvl1 Stats": CharityTrap(
        "LEVEL_ONE", 3600, "Den PRO-Code Grundstatus aktivieren.", ("LEVEL_ONE",)),
    "Trap: No Formchange": CharityTrap(
        "NO_FORMCHANGE", 600, "Den PRO-Code Form-Starre und keine Hochmagie aktivieren.", ("NO_FORMCHANGE",)),
    "Trap: No Attraction Flow": CharityTrap(
        "NO_ATTRACTIONS", 600, "Den PRO-Code Attraktionen-Sperre aktivieren.", ("NO_ATTRACTIONS",)),
    "Trap: No Formchange & Attraction Flow": CharityTrap(
        "NO_FORMCHANGE_OR_ATTRACTIONS", 600, "Form-Starre und Attraktionen-Sperre aktivieren.",
        ("NO_FORMCHANGE", "NO_ATTRACTIONS")),
}

for code in PRO_CODES:
    if code.item_name not in CHARITY_TRAPS:
        CHARITY_TRAPS[code.item_name] = CharityTrap(
            code.key, 600, f"Den PRO-Code {code.label} aktivieren.", (code.key,),
        )

# These tokens are used when reading seeds generated with the old catalog.
RETIRED_MANUAL_TRAP_TOKENS = {
    "Trap: Elemental Encoder": "KH3AP_CHARITY_TRAP::ELEMENTAL_ENCODER",
    "Trap: No Magic": "KH3AP_CHARITY_TRAP::NO_MAGIC",
    "Trap: No Healing": "KH3AP_CHARITY_TRAP::NO_HEALING",
}
RETIRED_MANUAL_TRAP_ALIASES = {
    f"{name.removeprefix('Trap: ')} Challenge": name for name in RETIRED_MANUAL_TRAP_TOKENS
}
RETIRED_MANUAL_TRAP_NAMES = frozenset((*RETIRED_MANUAL_TRAP_TOKENS, *RETIRED_MANUAL_TRAP_ALIASES))

# Reserve the retired items' published positions so subsequent IDs stay valid.
_ORIGINAL_CHARITY_ITEM_ORDER = (
    "Trap: Blackout",
    "Trap: Elemental Encoder",
    "Trap: Lvl1 Stats",
    "Trap: No Magic",
    "Trap: No Healing",
    "Trap: No Formchange",
    "Trap: No Attraction Flow",
    "Trap: No Formchange & Attraction Flow",
)
CHARITY_ITEM_ID_RESERVATIONS = (
    *_ORIGINAL_CHARITY_ITEM_ORDER,
    *(name for name in CHARITY_TRAPS if name not in _ORIGINAL_CHARITY_ITEM_ORDER),
)
PRO_CODE_DEFAULT_DURATIONS = {name: trap.duration for name, trap in CHARITY_TRAPS.items() if trap.pro_codes}
PRO_CODE_DURATION_OPTION = "pro_code_trap_durations"
MAX_PRO_CODE_DURATION = 0x7fffffff


def valid_pro_code_duration(seconds: object) -> bool:
    return type(seconds) is int and 1 <= seconds <= MAX_PRO_CODE_DURATION


NATIVE_TRAP_NAMES = {"Trap: Sneeze": "Sneeze Trap", "Trap: Burn": "Burn Trap"}
TRAP_ITEM_ALIASES = {
    **{original: name for name, original in NATIVE_TRAP_NAMES.items()},
    "Blackout Trap": "Trap: Blackout",
    **{f"{name.removeprefix('Trap: ')} Challenge": name for name in CHARITY_TRAPS if name != "Trap: Blackout"},
}

CHARITY_RUNTIME_TOKENS = {
    name: f"KH3AP_CHARITY_TRAP::{trap.key}" for name, trap in CHARITY_TRAPS.items()
}
