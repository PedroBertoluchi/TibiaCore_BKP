# Colored Loot and Message Events Guide

This document explains the technical implementation of dynamic Rarity-based loot coloring and new message events in TibiaCore.

## 1. Rarity-Based Colored Loot

### The Server
The server sends loot strings to the client via `MESSAGE_LOOT`. Instead of sending plain text like `"a crystal coin"`, we now embed tags that contain the item ID, the description, and the rolled rarity of the item.

When generating the loot string for the corpse, `corpse:getContentDescription(true)` is called. The `true` parameter signifies `inLootMessage` which outputs items in the following format:
`{id|description|rarity}`

For example:
`Loot of a rat: {2148|10 gold coins|0}`
`Loot of a demon: {2472|a magic plate armor|1}` (1 = Magic/Green rarity)

### The Client (OTClient)
When the client receives a `MESSAGE_LOOT` via `Server Log`, the `textmessage` module hooks into `ItemsDatabase.setColorLootMessage(text)` (in `gamelib/items.lua`).
This function uses regex to find `{id|description|rarity}`. 
1. If the item has a rarity `> 0`, it overrides the color according to the Rarity Tier (1=Green, 2=Blue, 3=Purple, 4=Yellow, 5=Red).
2. If the item has `rarity = 0` (or no dynamic rarity assigned like Gold Coins), it falls back to parsing `ThingType:getMeanPrice()` and uses the standard OTClient price-based colors.
3. The parsed string is formatted natively as `{name, #HEXCOLOR}` which OTClient's `setColoredText` uses to display multiple colors in the same string!

## 2. New Message Events (Purple, LightBlue, Pink)

We've expanded the standard Tibia `MessageClasses` to support new colored server messages.

### Server Implementation (`src/const.h` & `luascript.cpp`)
Added to `MessageClasses`:
- `MESSAGE_EVENT_PURPLE = 38`
- `MESSAGE_EVENT_LIGHTBLUE = 39`
- `MESSAGE_EVENT_PINK = 40`

You can use these directly in your Lua scripts like this:
```lua
player:sendTextMessage(MESSAGE_EVENT_PINK, "This is a beautiful pink message!")
```

### Client Implementation
These server IDs are mapped back to `Otc::MessageMode` in `protocolcodes.cpp` and `const.h`.
In the Lua interface (`gamelib/const.lua` & `game_textmessage/textmessage.lua`):
- Added `TextColors.purple` and `TextColors.pink` hex codes.
- Added `consolePurple`, `consoleLightBlue`, and `consolePink` properties to `MessageSettings`.
- Enabled `colored = true` for these channels which allows you to send `{text, #HEX}` formatted strings directly into `player:sendTextMessage(MESSAGE_EVENT_PURPLE, "Normal and {colored, #ff0000} text")` for native multi-colored messages on the screen or local chat!

### How to Add More Colors
1. **Server:** Add `MESSAGE_EVENT_NEWCOLOR = X` in `const.h` and register it in `luascript.cpp`.
2. **Client C++:** Add `MessageEventNewColor = X` in `client/const.h` and map it in `client/protocolcodes.cpp` using the exact Server ID number.
3. **Client Lua:** Add `EventNewColor = X` inside `MessageModes` (in `gamelib/const.lua`).
4. **Client Lua:** Add your hex string to `TextColors` (`gamelib/const.lua`), and map `MessageModes.EventNewColor` to a new setting in `MessageSettings` (`game_textmessage/textmessage.lua`).

### Lua Script Usage Example
We have added simple helper methods to the `Player` class in `data/lib/core/player.lua` to make sending multi-colored messages extremely easy.

#### 1. Center Screen & Local Chat (Orange Channel)
To send a message that appears in both the center of the screen and the Local Chat window with inline color parsing, use:
```lua
local itemName = "magic sword"
local colorHex = "#a335ee" -- Epic (Purple)
local msg = string.format("You opened the box and received a {%s, %s}!", itemName, colorHex)

-- Sends the parsed message to the player
player:sendColoredMessage(msg)
```
This is fully implemented in `data/scripts/actions/others/random_weapon_box.lua`.

#### 2. Server Log Custom Channels
To send a custom colored message directly to the `Server Log` (without appearing in the center of the screen), you can use:
```lua
-- Defaults to MESSAGE_EVENT_PURPLE
player:sendColoredLogMessage("This is a beautifully {colored, #ffc0cb} test string!")

-- Or specify a specific channel
player:sendColoredLogMessage("Special blue event!", MESSAGE_EVENT_LIGHTBLUE)
```

### Rarity Tiers & Colors
The system currently supports the following rarity mapping:
- **0 - Common:** Grey (`#bebebe`)
- **1 - Uncommon:** Lime Green (`#00FF00`)
- **2 - Rare:** Dodger Blue (`#1E90FF`)
- **3 - Epic:** Magenta/Purple (`#FF00FF`)
- **4 - Legendary:** Yellow (`#FFFF00`)

### Client-Side Settings for Screen Output
The `MESSAGE_EVENT_ORANGE` (ID 36) has been updated in `textmessage.lua` to use `screenTarget = 'centerTextMessageLabel'`. This ensures that important event messages (like opening a weapon box) appear in the middle of the screen as well as the console.

## 3. Testing
A talkaction `!colortest` has been added for quick validation.
- In-game, use `!colortest`
- This will broadcast the new custom colored messages to your client and trigger a simulated Rarity Loot Message.

### Client-Side Terminal Testing
You can also test the client-side parsing without server interaction by opening the OTClient Terminal (usually `CTRL+T`) and typing:
```lua
modules.game_textmessage.displayMessage(MessageModes.Loot, "Loot of test: {2472|a magic plate armor|1}, {2148|10 gold coins|0}")
modules.game_textmessage.displayMessage(MessageModes.EventPink, "This is a {native, #ffc0cb} test string!")
```
