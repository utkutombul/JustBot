"""
    /events.py

    Author(s):
        Utku Tombul (Calabresi)

    Changelog:
        28/02/2018: 
            - Initial file commit.
        09/12/2018: 
            - String formatting has been fixed and properly adapted to Python 3.
            - Added localization support.
            - Translated everything to English to make it the default language.
"""

import asyncio
import commands

from config import Config
from datetime import datetime, timedelta
from extensions import client, logger, session
from functions import get_user, create_user, give_role_to_user, add_currency_to_user, get_current_date, create_system_variable, get_system_variable, update_currencies


@client.event
async def on_ready():
    await client.wait_until_ready()
    print("Ready to serve as %s (%s)." % (client.user.name, client.user.id))


@client.event
async def on_message(message):
    # Parsing and forwarding the command, if message starts with bot prefix.
    if message.content.startswith(Config.COMMAND_PREFIX):
        command = message.content.split()[0][1:]
        arguments = []

        try:
            arguments = message.content.split()[1:]
        except IndexError:
            pass

        try:
            await getattr(commands, command)(message, arguments)
        except Exception as e:
            logger.error(e)
            print(e)

    # Checking user, and adding to database if not exists.
    user = get_user(discord_id=message.author.id).first()

    if not user:
        user = create_user(discord_id=message.author.id)

    # Properly rewarding user for contribution.
    if not message.content.startswith(Config.COMMAND_PREFIX):
        message_length = len(message.content)
        add_currency_to_user(user.id, Config.CURRENCY_CODE, int(message_length / 5))

    # Checking currency conversion data request time.
    last_update = get_system_variable("currency_last_update")

    if not last_update:
        last_update = create_system_variable("currency_last_update", get_current_date())

    if (get_current_date() - datetime.strptime(last_update.value, "%Y-%m-%d %H:%M:%S.%f")) >= timedelta(hours=1):
        update_currencies()
        last_update.value = get_current_date()
        session.commit()


@client.event
async def on_message_delete(message):
    await client.send_message(
        client.get_channel(Config.RECORD_CHANNEL_ID),
        _("Message deleted for **{user}** in *{channel}*: `{message}`").format_map({"channel": message.channel.name, "user": message.author, "message": message.content}))


@client.event
async def on_member_remove(member):
    await client.send_message(client.get_channel(Config.RECORD_CHANNEL_ID), _("`{user}` has left the server.").format_map({"user": member.name}))


@client.event
async def on_member_ban(member):
    await client.send_message(client.get_channel(Config.RECORD_CHANNEL_ID), _("`{user}` has been banned from the server.").format_map({"user": member.name}))


@client.event
async def on_member_unban(server, user):
    await client.send_message(client.get_channel(Config.RECORD_CHANNEL_ID), _("`{user}` has been unbanned from the server.").format_map({"user": member.name}))
