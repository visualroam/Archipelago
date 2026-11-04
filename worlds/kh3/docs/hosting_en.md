# Kingdom Hearts III hosting

The website offers two downloads for the same Kingdom Hearts III world version:

- **Player APWorld**: the standard package, including the KH3 client, pak generator,
  game assets, and runtime mod needed to play.
- **Host APWorld**: generation rules, options, item/location data, and player seed
  output. It contains no game DLLs, client, pak generator, or cooked game assets.

Install the host download as `kh3.apworld` in Archipelago's `custom_worlds` folder.
Install only one KH3 APWorld at a time. The host package and player package share
the same world identity, so the host package replaces the full package there.
Hosts who also play KH3 should use the player package, which supports both roles.

Generate and host rooms normally using the `Kingdom Hearts III` game name. The
host package generates each player's `.apkh3` seed file and the room's server
data without needing KH3 installed. Give each player their `.apkh3` download;
players use the player APWorld of the same version to build their game pak and
connect to the room. The host package cannot patch or launch the game.

## Race Generation

Enable Archipelago's race setting when generating the room. For local CLI
generation, use `--race --spoiler 0`; the spoiler setting is separate from the
race flag. This is a generation setting, not a KH3 player YAML option.

KH3 race player files contain check locations and gameplay settings without
the hidden item assignments or remote hint placements. The client can still
build its pak locally. Every race reward uses a generic AP placeholder until
the server sends the actual item, so players should keep the client connected.
Secret Report hints are disabled in race seeds. Standard AP hints remain
subject to the room's hint settings, and logic tracking remains available.

Local race builds do not export spoiler logs or full generation metadata.
Organizers must keep the full generated archive and `.archipelago` server data
private; distribute individual player `.apkh3` or `.pak` files instead. This
protects the distributed player data, not against modified clients or access to
the organizer's server files.
