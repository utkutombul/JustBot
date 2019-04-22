"""
    /commands.py

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
import datetime
import discord

from config import Config
from extensions import client, Base, engine, logger, session
from functions import (get_current_date, get_user, get_user_currency,
                       get_angry_message, get_currency, add_currency_to_user,
                       remove_currency_from_user, update_currencies,
                       convert_currency, get_bet, create_bet, get_user_bet,
                       create_user_bet, send_usage_message)
from pendulum import now, timezone
from random import randint, shuffle


async def para(message, arguments):
    user_currencies = get_user_currency(user_id=get_user(
        discord_id=message.author.id).first().id).all()
    counter = 0

    embed = discord.Embed(
        title=_("*{user} has the following currencies:*").format_map({
            "user": message.author.name}),
        color=0x008000)
    embed.set_author(name=_("Bank of {server}").format_map(
        {"server": message.channel.server.name}))

    for currency in user_currencies:
        embed.add_field(name=currency.short_code,
                        value=str(currency.amount), inline=True)
        counter += 1

    if not counter:
        embed.description = _("This person doesn't have any currencies.")

    await message.channel.send(embed=embed)


async def dövizkurları(message, arguments):
    currency_code = ""

    try:
        currency_code = str(arguments[0]).upper()
    except Exception:
        currency_code = Config.CURRENCY_CODE

    counter = 0
    embed = discord.Embed(
        title=_("*Latest exchange rates for the selected currency ({currency}):*").format_map({
            "currency": currency_code}),
        color=0x008000)
    embed.set_author(name=_("Bank of {server}").format_map({"server": message.channel.server.name}))

    currencies = get_currency().all()

    for currency in currencies:
        if counter < 25:
            counter += 1
        else:
            await message.author.send(embed=embed)
            embed = discord.Embed(title=_("*Latest exchange rates for the selected currency ({currency}):*").format_map({"currency": currency_code}), color=0x008000)
            embed.set_author(name=_("Bank of {server}").format_map({"server": message.channel.server.name}))
            counter = 1

        embed.add_field(name=currency.short_code, value=str(
            convert_currency(currency_code, currency.short_code)), inline=True)

    embed.add_field(name=Config.CURRENCY_CODE, value=str(
        convert_currency(currency_code, Config.CURRENCY_CODE)), inline=True)

    await message.author.send(embed=embed)


async def forex(message, arguments):
    if arguments:
        base_currency = str(arguments[0]).upper()
        amount = float(arguments[1])
        currency = str(arguments[2]).upper()

        base_currency = get_user_currency(user_id=get_user(
            discord_id=message.author.id).first().id, short_code=base_currency).first()
        currency = get_currency(short_code=currency).first()
        required_fee = (convert_currency(currency.short_code,
                                         base_currency.short_code) * amount)

        if base_currency and base_currency.amount >= required_fee:
            if currency:
                add_currency_to_user(
                    get_user(discord_id=message.author.id).first().id, currency.short_code, amount)
                remove_currency_from_user(get_user(discord_id=message.author.id).first(
                ).id, base_currency.short_code, required_fee)

                await message.channel.send(_("{user} paid {amount} {currency} and bought {converted_amount} {converted_currency}.").format_map({"user": message.author.name, "amount": required_fee, "currency": base_currency.short_code, "converted_amount": amount, "converted_currency": currency.short_code}))
            else:
                await message.author.send(_("Invalid currency."))
        else:
            await message.author.send(_("You don't have enough {currency} to exchange.").format_map({"currency": base_currency.short_code}))
    else:
        await send_usage_message(
            message.channel,
            _("{prefix}forex (Currency (SELL)) (Purchase amount) (Currency (BUY))").format_map({
                "prefix": Config.COMMAND_PREFIX})
        )


async def blackjack(message, arguments):
    game_over=False

    def deal(deck):
        hand=[]
        for i in range(2):
            shuffle(deck)
            card=deck.pop()
            if card == 11:
                card="J"
            if card == 12:
                card="Q"
            if card == 13:
                card="K"
            if card == 14:
                card="A"
            hand.append(card)
        return hand

    def total(hand):
        total=0
        for card in hand:
            if card == "J" or card == "Q" or card == "K":
                total += 10
            elif card == "A":
                if total >= 11:
                    total += 1
                else:
                    total += 11
            else:
                total += card
        return total

    def hit(hand):
        card=deck.pop()
        if card == 11:
            card="J"
        if card == 12:
            card="Q"
        if card == 13:
            card="K"
        if card == 14:
            card="A"
        hand.append(card)
        return hand

    def win():
        add_currency_to_user(get_user(
            discord_id=message.author.id).first().id, Config.CURRENCY_CODE, (bet * 2))

    async def print_results(dealer_hand, player_hand, dealer_turn = False):
        if dealer_turn:
            await message.channel.send(_("Dealer has {dealer_hand} in total of {total}.").format_map({"dealer_hand": str(dealer_hand), "total": str(total(dealer_hand))}))
        else:
            await message.channel.send(_("Dealer shows a {dealer_hand}.").format_map({"dealer_hand": str(dealer_hand[0])}))
        await message.channel.send(_("You have {player_hand} in total of {total_player_hand}.").format_map({"player_hand": str(player_hand), "total_player_hand": str(total(player_hand))}))

    async def bjack(dealer_hand, player_hand):
        if total(player_hand) == 21:
            await print_results(dealer_hand, player_hand)
            await message.channel.send(_("BLACKJACK!") + "\n")
            win()
        elif total(dealer_hand) == 21:
            await print_results(dealer_hand, player_hand)
            await message.channel.send(_("Sorry, you lost. Dealer hit a blackjack.") + "\n")

    def winner_control(dealer_hand, player_hand):
        if total(player_hand) == 21:
            return True
        elif total(dealer_hand) == 21:
            return False
        elif total(player_hand) > 21:
            return False
        elif total(dealer_hand) > 21:
            return True
        elif total(player_hand) < total(dealer_hand):
            return False
        elif total(player_hand) > total(dealer_hand):
            return True

    def blackjack_control(dealer_hand, player_hand):
        if total(player_hand) == 21:
            return True
        elif total(dealer_hand) == 21:
            return True

    async def score(dealer_hand, player_hand, dealer_turn = False):
        if total(player_hand) == 21:
            await print_results(dealer_hand, player_hand, dealer_turn)
            await message.channel.send(_("BLACKJACK!") + "\n")
            win()
        elif total(dealer_hand) == 21:
            await print_results(dealer_hand, player_hand, dealer_turn)
            await message.channel.send(_("Sorry, you lost. Dealer hit a blackjack.") + "\n")
        elif total(player_hand) > 21:
            await print_results(dealer_hand, player_hand, dealer_turn)
            await message.channel.send(_("You busted. You lost.") + "\n")
        elif total(dealer_hand) > 21:
            await print_results(dealer_hand, player_hand, dealer_turn)
            await message.channel.send(_("Dealer busted. You won!") + "\n")
        elif total(player_hand) < total(dealer_hand):
            await print_results(dealer_hand, player_hand, dealer_turn)
            if dealer_turn:
                await message.channel.send(_("Dealer has a higher hand. You lost.") + "\n")
        elif total(player_hand) > total(dealer_hand):
            await print_results(dealer_hand, player_hand, dealer_turn)
            if dealer_turn:
                await message.channel.send(_("You have a higher hand. You won!") + "\n")
                win()

    def check_message(message):
        if message.content.lower().find(_("hit")) != -1 or message.content.lower().find(_("stop")) != -1:
            return True
        else:
            return False

    if arguments:
        bet=0

        try:
            bet=float(arguments[0])
        except Exception:
            bet=0

        user_currency=get_user_currency(user_id = get_user(
            discord_id=message.author.id).first().id, short_code = Config.CURRENCY_CODE).first()

        if user_currency.amount >= bet:
            remove_currency_from_user(
                get_user(discord_id=message.author.id).first().id, Config.CURRENCY_CODE, bet)
            deck=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4

            choice=""
            dealer_hand=deal(deck)
            player_hand=deal(deck)

            message_text=_("You put {amount} {currency}.").format_map({
                "amount": bet, "currency": Config.CURRENCY_CODE})
            dealer_message=await message.channel.send(message_text)
            message_text += "\n" + _("Dealing cards...")
            await client.edit_message(dealer_message, message_text)
            message_text += "\n" + _("Dealer shows a {dealer_hand}.").format_map({
                "dealer_hand": str(dealer_hand[0])})
            await client.edit_message(dealer_message, message_text)
            message_text += "\n" + _("You have {player_hand} in total of {total_player_hand}.").format_map({
                "player_hand": str(player_hand), "total_player_hand": str(total(player_hand))})
            await client.edit_message(dealer_message, message_text)

            while choice.find(_("stop")) == -1 and total(player_hand) < 21 and not blackjack_control(dealer_hand, player_hand):
                await message.channel.send(_("Would you like to [hit], or [stop]?"))
                message=await client.wait_for_message(author = message.author, check = check_message)
                choice=message.content.lower()

                if choice.find(_("hit")) != -1:
                    hit(player_hand)
                    await score(dealer_hand, player_hand, False)

                    if not winner_control(dealer_hand, player_hand):
                        choice=_("stop")
                elif choice.find(_("stop")) != -1:
                    while total(dealer_hand) < total(player_hand):
                        hit(dealer_hand)
                        await bjack(dealer_hand, player_hand)
                    await score(dealer_hand, player_hand, True)

            if blackjack_control(dealer_hand, player_hand):
                await score(dealer_hand, player_hand, False)
        else:
            await message.channel.send(_("You don't have have enough {currency}.").format_map({"currency": Config.CURRENCY_NAME}) + "\n")
    else:
        await send_usage_message(message.channel, _("{prefix}blackjack (Bet ({amount}))").format_map({"prefix": Config.COMMAND_PREFIX, "amount": Config.CURRENCY_CODE}))


async def rulet(message, arguments):
    bet_types=[{
        "id": 0,
        "name": _("red"),
        "multiplier": 2
    }, {
        "id": 1,
        "name": _("black"),
        "multiplier": 2
    }, {
        "id": 2,
        "name": _("green"),
        "multiplier": 36
    }, {
        "id": 3,
        "name": _("odd"),
        "multiplier": 2
    }, {
        "id": 4,
        "name": _("even"),
        "multiplier": 2
    }, {
        "id": 5,
        "name": _("number (0-36)"),
        "multiplier": 36
    }, {
        "id": 6,
        "name": _("first column"),
        "multiplier": 3
    }, {
        "id": 7,
        "name": _("second column"),
        "multiplier": 3
    }, {
        "id": 8,
        "name": _("third column"),
        "multiplier": 3
    }, {
        "id": 9,
        "name": _("first dozen"),
        "multiplier": 3
    }, {
        "id": 10,
        "name": _("second dozen"),
        "multiplier": 3
    }, {
        "id": 11,
        "name": _("third dozen"),
        "multiplier": 3
    }]
    if arguments:
        bet_amount=0
        bet_type=None

        if len(arguments) > 2:
            arguments[1]="%s %s" % (arguments[1], arguments[2])

        try:
            bet_amount=float(arguments[0])
        except Exception as e:
            await message.author.send(_("Invalid bet amount."))

        try:
            for type in bet_types:
                if type["name"].lower() == arguments[1].lower():
                    bet_type=type

            if not bet_type:
                for i in range(36):
                    if str(i) == arguments[1]:
                        bet_type=bet_types[5]

            if not bet_type:
                await message.author.send(_("Invalid bet type."))
        except Exception as e:
            await message.author.send(_("Invalid bet type."))

        user_currency=get_user_currency(user_id = get_user(
            discord_id=message.author.id).first().id, short_code = Config.CURRENCY_CODE).first()

        if bet_type:
            if user_currency.amount >= bet_amount:
                remove_currency_from_user(get_user(
                    discord_id=message.author.id).first().id, Config.CURRENCY_CODE, bet_amount)

                random_generator=randint(0, 36)
                won=False
                red_values=[1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 28, 30, 32, 34, 36]
                black_values = [2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 29, 31, 33, 35]
                first_column = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
                second_column = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
                third_column = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

                if bet_type["id"] == 0:
                    for value in red_values:
                        if random_generator == value:
                            won = True
                elif bet_type["id"] == 1:
                    for value in black_values:
                        if random_generator == value:
                            won = True
                elif bet_type["id"] == 2:
                    if random_generator == 0:
                        won = True
                elif bet_type["id"] == 3:
                    if (random_generator % 2) == 1:
                        won = True
                elif bet_type["id"] == 4:
                    if (random_generator % 2) == 0:
                        won = True
                elif bet_type["id"] == 5:
                    if random_generator == int(arguments[1]):
                        won = True
                elif bet_type["id"] == 6:
                    for value in first_column:
                        if random_generator == value:
                            won = True
                elif bet_type["id"] == 7:
                    for value in second_column:
                        if random_generator == value:
                            won = True
                elif bet_type["id"] == 8:
                    for value in third_column:
                        if random_generator == value:
                            won = True
                elif bet_type["id"] == 9:
                    for value in range(1, 12):
                        if random_generator == value:
                            won = True
                elif bet_type["id"] == 10:
                    for value in range(13, 24):
                        if random_generator == value:
                            won = True
                elif bet_type["id"] == 11:
                    for value in range(25, 36):
                        if random_generator == value:
                            won = True

                color = None

                for value in red_values:
                    if random_generator == value:
                        color = 0xff0000

                for value in black_values:
                    if random_generator == value:
                        color = 0x000000

                if random_generator == 0:
                    color == 0x00ff00

                embed = discord.Embed(title=_("**Roulette**"), description=str(random_generator), color=color)
                embed.set_author(name=Config.BOT_NAME)
                await message.channel.send(embed=embed)

                if won:
                    won_amount = bet_type["multiplier"] * bet_amount
                    add_currency_to_user(get_user(discord_id=message.author.id).first(
                    ).id, Config.CURRENCY_CODE, won_amount)
                    await message.channel.send(_("You won! {amount} {currency} added to your bank account.").format_map({"amount": won_amount, "currency": Config.CURRENCY_CODE}))
                else:
                    await message.channel.send(_("Sorry, you lost."))
            else:
                await message.author.send(_("You don't have have enough {currency}.").format_map({"currency": Config.CURRENCY_NAME}))
    else:
        bet_type_list = ""
        count = 0

        for type in bet_types:
            if count == 0:
                bet_type_list += type["name"]
            else:
                bet_type_list += ", %s" % (type["name"])

            count += 1

        await send_usage_message(message.channel, _("{prefix}roulette (Bet ({currency})) (Bet Type ({bet_type_list}))").format_map({"prefix": Config.COMMAND_PREFIX, "currency": Config.CURRENCY_CODE, "bet_type_list": bet_type_list}))


async def bahisler(message, arguments):
    bet_list = get_bet().all()
    output = _("_**Current open bets:**_") + "\n\n"

    for bet in bet_list:
        total_bets = get_user_bet(bet_id=bet.id).all()
        total_deposit = 0

        for user_bet in total_bets:
            total_deposit += int(user_bet.deposit)

        if total_bets:
            output += "`#{bet_id} ({bet_rate}) {bet}` - ({stats})\n".format(**{"bet_id": bet.id, "bet_rate": bet.rate, "bet": bet.bet, "stats": _("_{total_people}_ people bet _{total_deposit} {main_currency}_ on this.").format_map({"total_people": len(total_bets), "total_deposit": total_deposit, "main_currency": Config.CURRENCY_CODE})})
        else:
            output += "`#{bet_id} ({bet_rate}) {bet}`\n".format(**{"bet_id": bet.id, "bet_rate": bet.rate, "bet": bet.bet})

    await message.channel.send(output)


async def bahisoyna(message, arguments):
    if arguments:
        if int(arguments[0]) < 1:
            await message.channel.send(_("Invalid bet number."))
        elif int(arguments[1]) < 1:
            await message.channel.send(_("Invalid bet amount."))
        else:
            bet_id = int(arguments[0])
            bet_amount = float(arguments[1])

            bet = get_bet(id=arguments[0]).first()

            if bet is None:
                await message.channel.send(_("Invalid bet number."))
            else:
                current_user = get_user(discord_id=message.author.id).first()
                user_currency = get_user_currency(
                    currency_id=Config.CURRENCY_CODE, user_id=current_user.id).first()

                if user_currency is None or user_currency.amount < bet_amount:
                    await message.channel.send(_("You don't have have enough {currency}.").format_map({"currency": Config.CURRENCY_NAME}))
                else:
                    remove_currency_from_user(get_user(
                        discord_id=message.author.id).first().id, Config.CURRENCY_CODE, bet_amount)

                    user_bet = get_user_bet(
                        user_id=current_user.id, bet_id=bet.id).first()

                    if user_bet:
                        user_bet.deposit += bet_amount
                        session.commit()

                        await message.channel.send(_("You have added {bet_amount} {bet_currency} to your previous bet on #{bet_id}, making a total of {total_bet_amount} {bet_currency} on that bet.").format_map({"bet_id": bet.id, "bet_amount": bet_amount, "bet_currency": Config.CURRENCY_CODE, "total_bet_amount": user_bet.deposit}))
                    else:
                        user_bet = create_user_bet(
                            current_user.id, bet.id, bet_amount)

                        await message.channel.send(_("You betted {bet_amount} {bet_currency} for #{bet_id}.").format_map({"bet_id": bet.id, "bet_amount": bet_amount, "bet_currency": Config.CURRENCY_CODE}))

    else:
        await send_usage_message(message.channel,
                                 _("{prefix}bahisoyna (Bet Number) (Bet Amount)*").format_map({"prefix": Config.COMMAND_PREFIX}))


"""
    This part of the file is dedicated to the administrator commands.
"""


async def removetables(message, arguments):
    if message.author.permissions_in(message.channel).administrator:
        Base.metadata.bind = engine
        Base.metadata.drop_all()

        await message.channel.send(_("Command has successfully been executed."))


async def createtables(message, arguments):
    if message.author.permissions_in(message.channel).administrator:
        Base.metadata.bind = engine
        Base.metadata.create_all()
        update_currencies()

        await message.channel.send( _("Command has successfully been executed."))


async def kendinitemizle(message, arguments):
    def is_me(m):
        return m.author == client.user

    limit = 10000

    if arguments:
        limit = int(arguments[0])

    today = datetime.datetime.now()
    limited_days = datetime.timedelta(days=14)
    date_difference = today - limited_days

    deleted = await message.channel.purge(limit=10000, check=is_me, after=date_difference)
    await message.author.send(_("Deleted {deleted} messages.").format_map({"deleted": len(deleted)}))


async def kanalısüpür(message, arguments):
    def is_command(cmd):
        return cmd.content.startswith(Config.COMMAND_PREFIX)

    limit = 10000

    if arguments:
        limit = int(arguments[0])

    today = datetime.datetime.now()
    limited_days = datetime.timedelta(days=14)
    date_difference = today - limited_days
    
    deleted = await message.channel.purge(limit=limit, check=is_command, after=date_difference)
    await message.author.send(_("Deleted {deleted} messages.").format_map({"deleted": len(deleted)}))


async def bahisbelirle(message, arguments):
    if message.author.permissions_in(message.channel).administrator:
        bet_rate = float(arguments[0])
        bet_bet = message.content[message.content.find(
            " ", message.content.find(" ") + 1):]
        bet = create_bet(get_user(discord_id=message.author.id).first().id, bet_bet, bet_rate)

        await message.channel.send(_("{user} has opened a new bet: `{bet} ({bet_rate})`").format_map({"user": message.author, "bet": bet_bet, "bet_rate": bet_rate}))
    else:
        await message.channel.send(_("You don't have access to this command."))


async def bahissonucu(message, arguments):
    if message.author.permissions_in(message.channel).administrator:
        bet_id = int(arguments[0])
        bet_result = int(arguments[1])

        bet = get_bet(id=bet_id).first()

        if bet_result:
            await message.channel.send(_("Result of \"{bet}\": `WON`").format_map({"bet": bet.bet}))
        else:
            await message.channel.send(_("Result of \"{bet}\": `LOST`").format_map({"bet": bet.bet}))

        for bet_player in get_user_bet(bet_id=bet_id).all():
            discord_user = await client.get_user_info(get_user(id=bet_player.user_id).first().discord_id)

            if bet_result:
                award = float(bet.rate * bet_player.deposit)
                add_currency_to_user(bet_player.user_id,
                                     Config.CURRENCY_CODE, award)

                await message.channel.send(_("{user} has successfully predicted this bet and won {award} {currency}.").format_map({"user": discord_user.name, "award": award, "currency": Config.CURRENCY_CODE}))
            else:
                await message.channel.send(_("{user} lost {deposit} {currency}.").format_map({"user": discord_user.name, "deposit": bet_player.deposit, "currency": Config.CURRENCY_CODE}))

            session.delete(bet_player)
            session.commit()

        session.delete(bet)
        session.commit()
    else:
        await message.channel.send(_("You don't have access to this command."))
