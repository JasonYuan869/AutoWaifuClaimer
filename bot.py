#    AutoWaifuClaimer
#    Copyright (C) 2020 RandomBananazz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import sys
import time
import asyncio

import ujson
import discord
import keyboard
from discord.embeds import _EmptyEmbed

client = discord.Client()
dm = None
run_once = True

with open('./data/likelist.txt', 'r') as file_handle:
    likeArray = [x for x in file_handle.readlines() if not x.startswith('\n')]
    likeArray = [x for x in likeArray if not x.startswith('#')]
    likeArray = [x.strip() for x in likeArray]

with open('./data/config.json') as file_handle:
    config = ujson.load(file_handle)

try:
    bot_id = int(config["bot_id"])
    channel_id = int(config["channel_id"])
    user_id = int(config["user_id"])
    token = str(config["token"])
    command_prefix = str(config["command_prefix"])
    rollcommand = str(config["w/m/h"])

    auto_roll_enable = config["auto_roll_enable"]
    pokemon_enable = config["pokemon_enable"]
    roll_count = int(config["roll_count"])
    reset_minute = int(config["reset_min"])
    reset_hour = int(config["reset_hour"])
    daily_hour = int(config["daily_hour"])
    dm_messages = config["enable_dm"]
except ValueError:
    print("Invalid entry in config.json! Double check the presence (or lack of) quotes. See README.md for more.")
    sys.exit()

if not 0 <= reset_minute <= 59:
    print("reset_min is outside of range! Check config.json.")
    sys.exit()

if not 0 <= daily_hour <= 23:
    print("daily_hour is outside of range! Check config.json.")
    sys.exit()

if not 0 <= reset_hour <= 23:
    print("reset_hour is outside of range! Check config.json.")
    sys.exit()


def give_emoji(emoji):
    if emoji == '❤':
        keyboard.write('+:heart:\n')
    elif emoji == '💖':
        keyboard.write('+:sparkling_heart:\n')
    elif emoji == '💘':
        keyboard.write('+:cupid:\n')
    elif emoji == '💕':
        keyboard.write('+:two_hearts:\n')
    elif emoji == '💓':
        keyboard.write('+:heartbeat:\n')
    elif emoji == '💗':
        keyboard.write('+:heartpulse:\n')
    elif emoji == '❣':
        keyboard.write('+:heart_exclamation:\n')
    elif emoji == '♥':
        keyboard.write('+:hearts:\n')
    else:
        raise NameError


@client.event
async def on_ready():
    global run_once
    global dm
    global dm_messages

    print("Ready and listening! Check if the bot's online in the members panel!")

    if dm_messages:
        try:
            dm = await client.get_user(user_id).create_dm()
        except AttributeError:
            print("Invalid User ID! Check the entry in config.json.")
            print("Bot will not DM the user of marry attempts!")
            dm_messages = False
        else:
            print("DMs are ENABLED! The bot will message you of marry attempts.")
    else:
        print("DMs are DISABLED! You will not receive any messages from the bot.")

    if run_once:  # Because on_ready() may execute more than once, breaking the bot
        run_once = False
        if auto_roll_enable:
            print("Auto rolling is ENABLED! AFK with the Discord window focused and in your appropriate waifu channel.")
            await loop()  # Must be the last thing, otherwise nothing else in this function will run
        else:
            print("Auto rolling is DISABLED! Edit config.json to enable.")


@client.event
async def on_message(message):
    global dm
    if message.author.id != bot_id or message.channel.id != channel_id:
        return

    try:
        embed = message.embeds[0]
    except IndexError:
        return

    if embed.footer.text is _EmptyEmbed or embed.description is _EmptyEmbed:
        return

    if "\n" in embed.description:
        return

    with open('./data/rolled.txt', 'a', encoding='utf-8') as rolled:
        rolled.write(str(datetime.datetime.now()) + '\t' + embed.author.name + '\n')
        print(str(datetime.datetime.now()) + '\t' + embed.author.name)

    if embed.author.name in likeArray:
        try:
            payload = await client.wait_for('raw_reaction_add', timeout=3)
        except asyncio.TimeoutError:
            return
        emoji = str(payload.emoji)
        try:
            give_emoji(emoji)
        except NameError:
            return
        else:
            if dm_messages:
                await dm.send(content='Claim attempted.', embed=embed)
            return


async def loop():
    while True:
        await wait()
        await roller()
        await asyincio.sleep(3)


async def wait():
    now = datetime.datetime.now()
    if now.minute >= (reset_minute - 1):
        dt = (now + datetime.timedelta(hours=1)).replace(minute=reset_minute - 1, second=0, microsecond=0)
    else:
        dt = now.replace(minute=reset_minute - 1, second=0, microsecond=0)
    remaining_time = (dt - now).total_seconds()
    print("Waiting for {0}.".format(dt))
    print("Next rolling interval in {0} seconds.".format(remaining_time))
    await asyncio.sleep(remaining_time)


async def roller():
    payload = None
    current_hour = time.localtime()[3]
    i = 0
    emoji = None
    while i < (roll_count - 1):
        i += 1
        keyboard.write('{0}{1}\n'.format(command_prefix, rollcommand))
        await asyncio.sleep(3)

    keyboard.write('{0}{1}\n'.format(command_prefix, rollcommand))
    if (current_hour - reset_hour) % 3 == 0:
        while True:
            try:
                payload = await client.wait_for('raw_reaction_add', timeout=3)
            except asyncio.TimeoutError:
                break
            if payload.channel_id != channel_id or payload.user_id != bot_id:
                continue
            else:
                emoji = str(payload.emoji)
                break
        try:
            give_emoji(emoji)
        except NameError:
            pass
        else:
            await asyncio.sleep(3)
            if dm_messages:
                message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
                try:
                    embed = message.embeds[0]
                except IndexError:
                    pass
                else:
                    await dm.send(content='Autoclaim attempted.', embed=embed)

        if current_hour == daily_hour:
            keyboard.write('{0}daily\n'.format(command_prefix))
            await asyncio.sleep(3)
            keyboard.write('{0}dk\n'.format(command_prefix))
            await asyncio.sleep(3)
            if dm_messages:
                await dm.send(content="Daily commands sent.")

        if current_hour % 2 == 0 and pokemon_enable:
            keyboard.write('{0}p\n'.format(command_prefix))
            if dm_messages:
                await dm.send(content="Pokemon command sent.")

try:
    client.run(token)
except discord.errors.LoginFailure:
    print("Invalid bot token! Please double check your config.json file.")
    sys.exit()
