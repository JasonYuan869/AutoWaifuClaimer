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

import asyncio
import datetime
import sys

import arsenic
import discord
from aiohttp import ClientConnectorError
from arsenic import keys, browsers, services, start_session, stop_session
from arsenic.actions import Keyboard, chain
from arsenic.errors import ArsenicTimeout, NoSuchElement
from discord import LoginFailure
from discord.embeds import _EmptyEmbed

import constants

f = open('./log.txt', 'w')

K = Keyboard()
service = services.Geckodriver(log_file=f)
browser = browsers.Firefox(**{'moz:firefoxOptions': {'args': ['-headless']}})
session: arsenic.session.Session
done = False


async def stop():
    print('Quitting...')
    await stop_session(session)
    await client.close()
    f.close()
    sys.exit()


async def browser_init():
    global done

    # Open the WebDriver session to the stored channel
    await session.get(f'https://discord.com/channels/{constants.SERVER_ID}/{constants.CHANNEL_ID}')

    try:
        # Wait for login screen
        await session.wait_for_element(10, '[name="email"]')
    except ArsenicTimeout:  # No login screen
        # No login screen, but not the correct channel (some weird error)
        if f'{constants.SERVER_ID}/{constants.CHANNEL_ID}' not in await session.get_url():
            print('The channel did not load, but no login was asked!')
            print('Double check the SERVER_ID and CHANNEL_ID entries in constants.py')
            await stop()
    else:
        # Login attempt
        print('Logging in with provided credentials...')
        print('This can take up to 30 seconds.')
        await (await session.get_element('[name="email"]')).send_keys(constants.LOGIN_INFO[0])
        await (await session.get_element('[name="password"]')).send_keys(constants.LOGIN_INFO[1])
        await (await session.get_element('button[type="submit"]')).click()
        try:
            # Wait for regular Discord to load
            await session.wait_for_element(30, '.slateTextArea-1Mkdgw')

            if f'{constants.SERVER_ID}/{constants.CHANNEL_ID}' not in await session.get_url():
                raise ValueError
        except ArsenicTimeout:
            # Regular Discord did not load, login unsuccessful
            print('Login was unsuccessful. Please check LOGIN_INFO entry in constants.py')
            await stop()
        except ValueError:
            # Discord loaded, but no the correct channel (some weird error)
            print('Login was successful, but the redirect was to the wrong channel.')
            print('Try running the bot again.')
            await stop()
        else:
            print("Login successful!")
            done = True


async def send_command(text):
    # Activate the window and type command prefix (because the keyboard can't do it)
    await (await session.get_element('#chat-messages')).click()
    await (await session.get_element('.slateTextArea-1Mkdgw')).send_keys(constants.COMMAND_PREFIX)

    # For some reason, typing directly into the input box using Element.send_keys() doesn't work
    # Arsenic actions must be used instead to send keyboard press by press (and they're confusing)
    ticklist = []
    for char in text:
        ticklist.append(K.down(char))
        ticklist.append(K.up(char))
    ticklist.append(K.down(keys.ENTER))
    ticklist.append(K.up(keys.ENTER))
    await session.perform_actions(chain(*ticklist))


async def react_emoji(emoji, message_id):
    try:
        # Wait for message identified by ID to appear
        # The Discord bot is faster than the web browser
        await asyncio.sleep(1)
        reaction_divs = await (await session.wait_for_element(2, f'[id="chat-messages-{message_id}"]'))\
            .get_elements('div')
        for element in reaction_divs:
            # Find the emoji and click it
            try:
                if await element.get_attribute('class') != 'reactionInner-15NvIl focusable-1YV_-H': continue
            except arsenic.errors.StaleElementReference:  # Weird error that idk why shows up
                continue
            if emoji in await element.get_attribute('aria-label'):
                await element.click()
                break
    except ArsenicTimeout:
        raise ValueError
    except NoSuchElement:
        raise ValueError


# DISCORD STUFF BELOW

client = discord.Client()
initiated = False
dm: discord.DMChannel
daily_timer = datetime.datetime.now()

# Open and parse likelist into like_array
with open('./data/likelist.txt', 'r') as file_handle:
    like_array = [x for x in file_handle.readlines() if not x.startswith('\n')]
    like_array = [x for x in like_array if not x.startswith('#')]
    like_array = [x.strip() for x in like_array]


@client.event
async def on_ready():
    global initiated
    global dm
    global session

    # First time initialization, only to be run once
    if not initiated:
        dm = await client.get_user(constants.USER_ID).create_dm()
        session = await start_session(service, browser)
        await browser_init()
        initiated = True


@client.event
async def on_message(message):
    global dm
    global done
    global daily_timer

    if not done: return
    
    # Daily routines
    if (datetime.datetime.now() - daily_timer) >= datetime.timedelta(hours=20):
        daily_timer = datetime.datetime.now()
        await send_command('daily')
        await asyncio.sleep(2)
        await send_command('dk')
    
    # Check if we care about the message
    if message.author.id != constants.MUDAE_ID or message.channel.id != constants.CHANNEL_ID:
        return

    # Check if the message has an embed
    try:
        embed = message.embeds[0]
    except IndexError:
        return

    # Check if the embed is a valid roll
    if type(embed.description) is _EmptyEmbed or type(embed.author.name) is _EmptyEmbed:
        return
    if '\n' in embed.description:
        return

    # Check footer text for "belongs to"
    # If so, react with appropriate kakera emoji
    if type(embed.footer.text) is not _EmptyEmbed:
        if 'Belongs to' in embed.footer.text:
            try:
                payload = await client.wait_for('raw_reaction_add', timeout=3)
            except asyncio.TimeoutError:
                return
            emoji = str(payload.emoji)
            try:
                await react_emoji(emoji, message.id)
            except ValueError:
                return
            else:
                await dm.send(content='Kakera loot attempted.', embed=embed)
            return  # End

    with open('./data/rolled.txt', 'a', encoding='utf-8') as rolled:
        rolled.write(str(datetime.datetime.now()) + '\t' + embed.author.name + '\n')
        print(str(datetime.datetime.now()) + '\t' + embed.author.name)

    if embed.author.name in like_array:
        try:
            payload = await client.wait_for('raw_reaction_add', timeout=3)
        except asyncio.TimeoutError:
            return
        emoji = str(payload.emoji)
        print(emoji)
        try:
            await react_emoji(emoji, message.id)
        except ValueError:
            return
        else:
            await dm.send(content='Claim attempted.', embed=embed)


try:
    client.run(constants.BOT_TOKEN)
except LoginFailure:
    print("Invalid bot token! Please double check your config.json file.")
    print("Quitting...")
    sys.exit()
except ClientConnectorError:
    print("Unable to connect to Discord! Please check your internet connection.")
    print("Quitting...")
    sys.exit()
