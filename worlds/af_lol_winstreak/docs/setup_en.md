# AF League of Legends Winstreak – Setup

No Riot API and nothing touches the game client (Vanguard-safe).
Items are permissions: you may only queue in unlocked **roles**, pick unlocked **champions**,
take unlocked **keystones** and buy unlocked **tier-2 boots** (Boots of Speed is always allowed).
You start with 2 roles, a few champions and keystones from different rune trees.

Other items:
- **Champion Reuse**: once, play a champion a second time within the streak.
- **Chat Picks Rune**: chat picks the next keystone (only from unlocked ones).
- **Mastery Emote Spam**: show the mastery emote after every kill next match.
- **Traps** are rules for the next match (no Flash, off-role, …).

Checks per champion: win a match, and get N kills in one match (assists do not count).

Counting queues: Normal Draft, Blind Pick, Swiftplay, Ranked Solo/Duo and Ranked Flex.
Everything else (ARAM, Arena, URF, events, bots, customs) is ignored and does not break the streak.

Checks are sent automatically by the **AF LoL Winstreak Client** (Archipelago Launcher → AF LoL Winstreak Client):
connect to the room as usual, then just type your Riot ID into the input field (`Username#Tag`,
region optional: `Username#Tag EUW`). The client reads new matches from op.gg every 60 seconds.
Games played before the Riot ID was entered are ignored. Matches with a locked champion, role, keystone or
tier-2 boots give no checks and reset the streak.
Commands: `/unlocks` or `/streak` (start items, unlocks, streak), `/opgg` (check now), `/riot Username#Tag [Region]` (change account).
Moderators can still mark checks by hand.

**Goal:** win 5 counting matches in a row (length set by `streak_length`), each with a different unlocked champion.
A loss resets the streak. A remake does not count either way.
