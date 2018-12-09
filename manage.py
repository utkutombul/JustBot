"""
    /manage.py

    Author(s): 
        Utku Tombul (Calabresi)

    Changelog:
        28/02/2018:
            - Initial file commit.
        09/12/2018: 
            - Removed "run.py" and renamed "main.py" to "manage.py" and added support for runtime arguments.
"""

import asyncio
import os
import sys

from config import Config
from extensions import client, logger, engine, Base, l18n

import commands
import events
import logging


def configure_logger():
    """
        Handles the logging configuration.
    """

    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=("error.log"), encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)


def configure_db():
    """
        Handles the database configuration.
    """

    Base.metadata.bind = engine
    Base.metadata.create_all()


def start_bot(config=None):
    """
        Starts the bot with the given config.
    """

    if not config:
        config = Config

    configure_logger()
    configure_db()
    l18n.install()
    
    client.run(config.APPLICATION_TOKEN)


if __name__ == "__main__":
    args = sys.argv

    if args[1] == "runbot":
        try:
            start_bot(eval(args[2]))
        except Exception as e:
            start_bot()
    elif args[1] == "createtables":
        configure_db()

