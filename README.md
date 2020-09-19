# AutoWaifuClaimer
Just a fun mini-project that listens for rolled waifus from Mudae, then auto claims it through keyboard input. Everything runs from [`bot.py`](./bot.py).

## Difference with version 1 (in the master branch)
The original bot used pynput for keyboard control to react to emojis and type commands in chat. This came with the major limitation that there had to be a physical Discord window focused permanantly on the rolling channel. With version 2, I use arsenic (basically selenium browser automation but async) to open a headless Firefox and login to the Discord web app. Now, the browser is controlled with python and no physical window is needed. Since now the bot can "click" on emojis instead of using keyboard input, it can also now react to Kakera.

This is a brand new implementation of the bot, and therefore many of the (experimental) features from version 1 is a WIP. For example, the bot cannot currently roll automatically every hour (I don't know if I will ever implement this).

## Features
* Automatically adds the respective emoji to claim the waifu within a fraction of a second
  * Uses keyboard emoji input, rather than mouse input
* Create a likelist for what the bot would react to
* DM the user on every attempted claim
* Save everything that was rolled and at what time in `/data/rolled.txt`
* Automatically react to kakera and DM the user on attempts
* *Technically* not a third-party client for user accounts, unlike other autoclaimers (which would be against the TOS)
* Cross-platform support
* Can be run in the background (unlike v1)

## Limitations
* May potentially break if people spam the bot or the channel
* Will attempt claim regardless of having a claim ready (marry and kakera attempts)
* You need to supply the bot with plaintext Discord login (2FA disabled)
 * It will not transfer this over the internet, but rather use it locally to login within a headless browser

## How it works
The bot listens for all valid, unclaimed rolls output by the Mudae bot (or Mudamaid).
If the name of a roll matches with one in a predetermined list (`likelist.txt`),
then it will listen for the respective emoji that Mudae reacts. Lastly, it instantly reacts back with that emoji.

When an attempted claim is made (either because it matched the list or the claim would reset soon), the bot will DM the
user of what they attempted to claim. These options can be set in `constants.py`.

## Requirements
See [`requirements.txt`](./requirements.txt)
* Python 3.7+
* discord.py
* arsenic

Also setup Firefox with Geckodriver.

## Usage
Clone this repository. All manual config files are in the `/data` directory. Fill `constants.py` with the respective data. For information on copying Discord IDs, see [this article](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-). For information on making a bot, see [this article](https://www.writebots.com/discord-bot-token/).
Number of rolls and reset times can be found by entering `$settings` to Mudae bot.

Key|Description|Value
---|:---:|:---:
`MUDAE_ID`|The ID of the respective Mudamaid bot|Integer
`CHANNEL_ID`|The ID of the channel where waifus are rolled|Integer
`SERVER_ID`|The ID of the server (guild) where the channel is located
`USER_ID`|Your own Discord user ID for DMing purposes|Integer
`BOT_TOKEN`|Your Discord bot token|String
`COMMAND_PREFIX`|The prefix for Mudae commands (default: `"$"`)|String
`LOGIN_INFO`|Your Discord user login|Tuple(String, String)


The bot must have the following permissions:
* View Channels
* Send Messages
* Read Message History

Add your wishes to [`likelist.txt`](./data/likelist.txt). See that file for more information.

Create a new virtual environment (optional) and install the required modules. Information can be found [here](https://docs.python.org/3/library/venv.html).
```
pip install -r requirements.txt
```

Run `bot.py`.

## Using the pre-built binary
WIP

## License
Licensed under GNU General Public License v3.0. See [LICENCE](./LICENSE).

## Disclaimer
This project is in no way affiliated with the Mudae bot, found [here](https://top.gg/bot/432610292342587392). I am not responsible for salty friends if this steals their wishlist characters. I am also not responsible for banned Discord user accounts. Although this should be safer than outright using an unofficial client, there are still no guarantees. Use at own risk.
