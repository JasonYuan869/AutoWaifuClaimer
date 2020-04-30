# AutoWaifuClaimer
Just a fun mini-project that listens for rolled waifus from Mudae, then auto claims it through keyboard input. Everything runs from [`bot.py`](./bot.py).

## Features
* Automatically adds the respective emoji to claim the waifu within a fraction of a second
  * Uses keyboard emoji input, rather than mouse input
* Create a likelist for what the bot would react to
* DM the user on every attempted claim
* Save everything that was rolled and at what time in `/data/rolled.txt`
* Automatically send roll commands
* *Technically* not a third-party client for user accounts, unlike other autoclaimers (which would be against the TOS)
* Cross-platform support (requires sudo on Linux)

## Limitations
* Must be focused on the Discord window, so it's not a background process
* Cannot react to kakera
  * This is because Mudae uses a custom kakera emoji that cannot be entered from the keyboard
* May potentially break if people spam the bot or the channel
* Will attempt claim regardless of having a claim ready

## How it works
The bot listens for all valid, unclaimed rolls output by the Mudae bot (or Mudamaid).
If the name of a roll matches with one in a predetermined list (`likelist.txt`),
then it will listen for the respective emoji that Mudae reacts. Lastly, it instantly reacts back with that emoji.

The bot can also autoroll at specified time intervals automatically, using a claim just before the reset to not waste it.

When an attempted claim is made (either because it matched the list or the claim would reset soon), the bot can DM the
user of what they attempted to claim. These options can be set in `config.json`.

## Requirements
See [`requirements.txt`](./requirements.txt)
* Python 3.7+
* discord.py
* keyboard

## Usage
Clone this repository. All manual config files are in the `/data` directory. Fill `config.json` with the respective data. For information on copying Discord IDs, see [this article](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-). For information on making a bot, see [this article](https://www.writebots.com/discord-bot-token/).
Number of rolls and reset times can be found by entering `$settings` to Mudae bot.

Key|Description|Value
---|:---:|:---:
`bot_id`|The ID of the respective Mudamaid bot|Integer
`channel_id`|The ID of the channel where waifus are rolled|Integer
`user_id`|Your own Discord user ID for DMing purposes|Integer
`token`|Your Discord bot token|String
`command_prefix`|The prefix for Mudae commands (default: `"$"`)|String
`w/m/h`|Whether to roll `$w`, `$m`, or `$h` commands (default: `"w"`)|String
`enable_dm`|Set false to disable DMs|Boolean
`auto_roll_enable`|Set false to disable autorolling|Boolean
`pokemon_enable`|Set false to disable Pokemon rolls|Boolean
`roll_count`|The number of rolls to send per reset (default: `10`)|Integer
`reset_min`|The exact minute that the rolls reset|Integer[0-59]
`reset_hour`|Any hour that claims reset. The bot assumes 3 hours between resets.|Integer[0-23]
`daily_hour`|The hour to run `$daily` and `$dailykakera` commands|Integer[0-23]


The bot must have the following permissions:
* View Channels
* Send Messages
* Read Message History

Add your wishes to [`likelist.txt`](./data/likelist.txt). See that file for more information.

Create a new virtual environment (optional) and install the required modules. Information can be found [here](https://docs.python.org/3/library/venv.html).
```
pip install -r requirements.txt
```

Run `bot.py`. You must be focused on the Discord window in the specific waifu-rolling channel.

## Using the pre-built binary (Windows only)
Download the zipped release from the releases tab. Edit the files in the `/data` folder as explained in the above heading. Run `bot.exe`. You must be focused on the Discord window in the specific waifu-rolling channel.

## License
Licensed under GNU General Public License v3.0. See [LICENCE](./LICENSE).

## Disclaimer
This project is in no way affiliated with the Mudae bot, found [here](https://top.gg/bot/432610292342587392). I am not responsible for salty friends if this steals their wishlist characters. I am also not responsible for banned Discord user accounts. Although this should be safer than outright using an unofficial client, there are still no guarantees. Use at own risk.
