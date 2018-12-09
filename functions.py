"""
    /functions.py

    Author(s): 
        Utku Tombul (Calabresi)

    Changelog:
        28/02/2018:
            - Initial file commit.
        07/12/2018:
            - Added get_bet, create_bet, get_user_bet, create_user_bet.
"""

import asyncio
import json

from datetime import datetime, timedelta
from config import Config
from extensions import client, logger, session, Base
from models import User, UserRole, UserBet, UserCurrency, Bet, Currency, System
from random import randint
from requests import get


def get_current_date(tz=None):
    """
        Returns current datetime.
    """

    return datetime.now(tz)


def get_user(**arguments):
    """
        Creates a query with the given arguments for user selection. Returns the query.
    """

    query = session.query(User)

    if "id" in arguments:
        query = query.filter_by(id=int(arguments["id"]))

    if "discord_id" in arguments:
        query = query.filter_by(discord_id=arguments["discord_id"])

    return query


def create_user(discord_id):
    """
        Creates a new user in the database. Returns the created user or None if failed.
    """

    user = User(discord_id=discord_id,
                creation_date=get_current_date())

    session.add(user)
    session.commit()

    return user


def give_role_to_user(user_id, role_id):
    """
        Gives a role to the user in database and Discord. Returns the given role or None if failed.
    """

    role = UserRole(user_id=user_id, role_id=role_id)

    session.add(role)
    session.commit()

    return role


def get_user_currency(**arguments):
    """
        Creates a query with the given arguments for user currency selection. Returns the query.
    """

    query = session.query(UserCurrency)

    if "id" in arguments:
        query = query.filter_by(id=int(arguments["id"]))

    if "user_id" in arguments:
        query = query.filter_by(user_id=int(arguments["user_id"]))

    if "short_code" in arguments:
        query = query.filter_by(short_code=str(arguments["short_code"]))

    if "amount" in arguments:
        query = query.filter_by(amount=float(arguments["amount"]))

    return query


def create_user_currency(user_id, short_code):
    """
        Creates a currency for the user. Returns the created currency or None if not exists.
    """

    currency = UserCurrency(user_id=user_id, short_code=short_code, amount=0)
    session.add(currency)
    session.commit()

    return currency


def add_currency_to_user(user_id, short_code, amount):
    """
        Adds specified amount of currency to the user. Returns updated currency.
    """

    currency = get_user_currency(user_id=user_id, short_code=short_code).first()

    if not currency:
        currency = create_user_currency(user_id, short_code)

    currency.amount += amount
    session.commit()

    return currency


def remove_currency_from_user(user_id, short_code, amount):
    """
        Removes specified amount of currency to the user. Returns updated currency.
    """

    currency = get_user_currency(
        user_id=user_id, short_code=short_code).first()

    if not currency:
        currency = create_user_currency(user_id, short_code)

    currency.amount -= amount
    session.commit()

    return currency


def get_angry_message():
    """
        Returns an angry message, because why not?
    """

    return ["Sen burayı ahır mı sandın?!",
            "Paranı da al git!",
            "Hadsiz herif, sen kimsin?",
            "Yüzsüzlüğe bak ya!"][randint(0, 4)]


def get_currency(**arguments):
    """
        Creates a query with given arguments for currency selection. Returns the query.
    """

    query = session.query(Currency)

    if "id" in arguments:
        query = query.filter_by(id=int(arguments["id"]))

    if "short_code" in arguments:
        query = query.filter_by(short_code=str(arguments["short_code"]))

    if "value" in arguments:
        query = query.filter_by(value=float(arguments["value"]))

    return query


def update_currencies():
    """
        Downloads all available currencies and prepares the database.
    """

    response = get("http://apilayer.net/api/live?access_key=%s" % (Config.APILAYER_KEY)).json()

    for currency_code in response["quotes"].keys():
        currency = get_currency(short_code=currency_code[3:]).first()

        if not currency:
            currency = Currency(short_code=currency_code[3:])
            session.add(currency)
            session.commit()

        currency.value = response["quotes"][currency_code] / Config.CURRENCY_DIVIDER
        currency.last_update = get_current_date()
        session.commit()


def convert_currency(base_short_code, target_short_code):
    """
        Converts the base currency to target currency with database ratio.
        Requires database objects.
    """

    if base_short_code == target_short_code:
        return 1

    target_currency = get_currency(short_code=target_short_code).first()

    if base_short_code == Config.CURRENCY_CODE:
        return target_currency.value

    base_currency = get_currency(short_code=base_short_code).first()

    if target_short_code == Config.CURRENCY_CODE:
        return (1 / base_currency.value)

    return (base_currency.value / target_currency.value)


def get_system_variable(variable):
    """
        Returns a system variable from database.
    """

    return session.query(System).filter_by(variable=variable).first()


def create_system_variable(variable, value):
    """
        Creates and returns a system variable with given arguments.
    """

    variable = System(variable=variable, value=value)
    session.add(variable)
    session.commit()

    return variable


def get_bet(**arguments):
    """
        Creates a query with the given arguments for a bet. Returns the query.
    """

    query = session.query(Bet)

    if "id" in arguments:
        query = query.filter_by(id=int(arguments["id"]))

    if "created_by" in arguments:
        query = query.filter_by(created_by=int(arguments["created_by"]))

    if "bet" in arguments:
        query = query.filter_by(bet=str(arguments["bet"]))

    if "rate" in arguments:
        query = query.filter_by(rate=float(arguments["rate"]))

    return query


def create_bet(created_by, bet, rate):
    """
        Creates a currency for the user. Returns the created currency or None if not exists.
    """

    bet = Bet(created_by=created_by, bet=bet, rate=rate)
    session.add(bet)
    session.commit()

    return bet


def get_user_bet(**arguments):
    """
        Creates a query with the given arguments for a bet. Returns the query.
    """

    query = session.query(UserBet)

    if "id" in arguments:
        query = query.filter_by(id=int(arguments["id"]))

    if "user_id" in arguments:
        query = query.filter_by(user_id=int(arguments["user_id"]))

    if "bet_id" in arguments:
        query = query.filter_by(bet_id=int(arguments["bet_id"]))

    if "deposit" in arguments:
        query = query.filter_by(deposit=float(arguments["deposit"]))

    return query


def create_user_bet(user_id, bet_id, deposit):
    """
        Creates a currency for the user. Returns the created currency or None if not exists.
    """

    user_bet = UserBet(user_id=user_id, bet_id=bet_id, deposit=deposit)
    session.add(user_bet)
    session.commit()

    return user_bet


async def send_usage_message(channel, message):
    await client.send_message(channel, "**KULLANIM:** `%s`" % (message))