# AutoWaifuClaimer
Just a for fun project that listens and reads rolled waifus from Mudae, then auto claims it through keyboard input.

## Features
* Automatically adds the respective emoji to claim the waifu within a fraction of a second
  * Uses keyboard emoji input, rather than mouse input
* Create a likelist for what the bot would react to
* Save what was rolled at what time in rolled.txt
* *Technically* not a third-party client for user accounts, unlike other autoclaimers (which would be against the TOS)

## Requirements
See requirements.txt
* Python 3.7+
* discord.py
* keyboard

## Usage
Clone this repository. Fill `config.json` with the respected data. For information on copying Discord IDs, see [this article](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-). For information on making a bot, see [this article](https://www.writebots.com/discord-bot-token/).
```
{
  "bot_id": <MUDAMAID_ID_HERE>,
  "channel_id": <WAIFU_CHANNEL_HERE>,
  "user_id": <YOUR_USER_ID_HERE>,
  "token": "<DISCORD_BOT_TOKEN_HERE>"
}
```
The bot must have the following permissions:
* View Channels
* Send Messages
* Read Message History

Also add your wishes to `likelist.txt`. See [likelist.txt](./likelist.txt) for more information.

Create a new virtual environment (optional) and install the required modules. Information can be found [here](https://docs.python.org/3/library/venv.html).
```
pip install -r requirements.txt
```

Run `bot.py`. You must be focused on the Discord window in the specific waifu-rolling channel.

## Limitations
* Must be focused on the Discord window, so it's not a background process
* Cannot react to kakera
  * This is because Mudae uses a custom kakera emoji that cannot be entered from the keyboard

## License
Licensed under GNU General Public License v3.0. See [LICENCE](./LICENSE).
