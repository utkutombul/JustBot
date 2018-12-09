"""
    /config.py

    Author(s): 
        Utku Tombul (Calabresi)

    Changelog:
        28/02/2018: 
            - Initial file commit.
        09/12/2018:
            - Added localization support.
"""


class Config(object):
    """
        Base configuration class.
    """

    BOT_NAME = "Justitia"
    BOT_LANGUAGE = "tr_TR"

    # Application token, required to initialize the bot.
    # To obtain it, you must create a new application through Discord developer services.
    APPLICATION_TOKEN = ""

    # Command prefix is used in beginning of each command and it's how JustBot understands which messages are commands or not.
    COMMAND_PREFIX = "."

    # Sqlalchemy settings.
    SQLALCHEMY_ENGINE = "sqlite:///JustBot.db"

    # Master user is host of the bot and has access to everything.
    MASTER_USER = ""

    # Currency settings of the server, used for currency exchange, casino, levels, etc.
    CURRENCY_CODE = "JC"
    CURRENCY_NAME = "JustCoin"
    CURRENCY_DIVIDER = 1000

    # currencylayer API key for automated currency updates.
    # https://currencylayer.com/
    APILAYER_KEY = ""

    # Special channels' ids.
    # Recond channel is a special channel where bot logs (deleted messages, banned and quitted people etc.) are posted for administrator purposes.
    RECORD_CHANNEL_ID = ""
