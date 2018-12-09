"""
    /extensions.py

    Author(s): 
        Utku Tombul (Calabresi)

    Changelog:
        28/02/2018: 
            - Initial file commit.
        09/12/2018:
            - Added localization support.
"""

from config import Config


import discord
client = discord.Client()


import logging
logger = logging.getLogger("JustBot")


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(Config.SQLALCHEMY_ENGINE)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

import gettext

l18n = gettext.translation("messages", localedir="locale", languages=[Config.BOT_LANGUAGE])
