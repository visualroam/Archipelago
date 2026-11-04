# Kingdom Hearts III

> Use a fresh KH3 save for each seed and install/update the bundled runtime
> before playing.

Kingdom Hearts III for Archipelago uses the [Garden of Assemblage mod](https://github.com/Water-and-Critic/KH3-Rando-GoA) as a hub
and a KH3-specific runtime bridge to report checks and deliver items while the
game is running.

The randomizer is heavily based on the original randomizer from the [Garden of Assemblage mod](https://github.com/Water-and-Critic/KH3-Rando-GoA)

Use `Patch Game` in the Archipelago Kingdom Hearts III client to install or
update the required runtime and Garden of Assemblage mod. For Steam installs on
Windows, Patch Game also disables Steam Cloud for KINGDOM HEARTS III only; it
does not change Steam's global Cloud setting. Then connect the client directly
to your room. After authenticating your slot, the client automatically
downloads a hosted player `.pak` or builds one from the room's generation data,
stores it in `Save Manager`, and installs it as the only active seed pak. You
normally do not need to download, generate, or copy a player pak manually.

Manual `.pak`, `.apkh3`, and generated `.zip` imports remain available as an
optional fallback for older rooms or for preparing a run before connecting.

## Current Features

- [Garden of Assemblage mod](https://github.com/ashandarei/AP-GOA-KH3)  routing with world portals.
- Goal is either 3 proofs or 7 heart pieces.
- Generated KH3 `.pak` files whose local KH3 placements match the AP seed.
- Chests.
- Story event and victory bonuses.
- Moogle Shop items.
- Optional music shuffle, keyblade form themes and your own music files.

## Checks And Rewards

Depending on
your options, checks can include treasures, event rewards, victory
bonuses, lucky emblem rewards, battlegates, data battle rewards, minigames,
Moogle Workshop rewards, and other KH3 reward pools.

## Important Notes

- Use a fresh KH3 save when starting a new KH3 AP seed.
- The KH3 client should be connected before launching or loading into KH3.
- The generated player `.pak` must match the AP room you are connected to.
- If you regenerate or restart a room, reconnect with KH3 closed so the client
  can resolve, build if necessary, and install the new player pak.
- Do not keep old KH3 AP seed paks in `~mods`; stale paks can make the game
  reward different items than the Archipelago server expects.
