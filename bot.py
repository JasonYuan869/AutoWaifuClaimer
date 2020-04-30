import datetime
import json

import discord
import keyboard
from discord.embeds import _EmptyEmbed

client = discord.Client()
dm = None

with open('./data/likelist.txt', 'r') as file_handle:
    likeArray = [x for x in file_handle.readlines() if not x.startswith('\n')]
    likeArray = [x for x in likeArray if not x.startswith('#')]
    likeArray = [x.strip() for x in likeArray]

with open('./data/config.json') as file_handle:
    config = json.load(file_handle)
    bot_id = config["bot_id"]
    channel_id = config["channel_id"]
    user_id = config["user_id"]
    token = config["token"]


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
    print("Ready and listening! Check if the bot's online in the members panel!")
    global dm
    try:
        dm = await client.get_user(user_id).create_dm()
    except AttributeError:
        print("Invalid User ID! Check the entry in config.json.")
        print("Bot will not DM the user of marry attempts!")


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
        payload = await client.wait_for('raw_reaction_add')
        emoji = str(payload.emoji)
        try:
            give_emoji(emoji)
        except NameError:
            return
        else:
            await dm.send(content='Marry Attempt', embed=embed)
            return


client.run(token)
