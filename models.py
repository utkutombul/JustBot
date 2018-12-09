# -*- coding: utf-8 -*-

"""
    /models.py

    Author(s): 
        Utku Tombul (Calabresi)

    Changelog:
        28/02/2018:
            - Initial file commit.
        07/12/2018:
            - Added Bet, UserBet.
"""

from extensions import Base, session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text


class User(Base):
    """
        Database model class for users.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    discord_id = Column(String(32))
    creation_date = Column(DateTime)


class UserRole(Base):
    """
        Database model class for user roles.
    """

    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(String(32))


class UserDetail(Base):
    """
        Database model class for user details.
    """

    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class UserBet(Base):
    """
        Database model class for user bets.
    """

    __tablename__ = "user_bets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bet_id = Column(Integer, ForeignKey("bets.id"))
    deposit = Column(Float)


class UserCurrency(Base):
    """
        Database model class for user currencies.
    """

    __tablename__ = "user_currencies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    short_code = Column(String(3))
    amount = Column(Float)


class Bet(Base):
    """
        Database model class for bets.
    """

    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    bet = Column(Text)
    rate = Column(Float)


class Currency(Base):
    """
        Database model class for currencies.
    """

    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    short_code = Column(String(3))
    value = Column(Float)


class System(Base):
    """
        Database model class for system variables.
    """

    __tablename__ = "system"

    id = Column(Integer, primary_key=True)
    variable = Column(String(64))
    value = Column(Text)