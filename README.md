# JustBot
*Other languages:* [Türkçe](https://github.com/utkutombul/JustBot/blob/master/README.tr.md)

JustBot is a Discord bot written in Python for beginners, as an example or boilerplate. It has examples of basic database usage and structure via SQLAlchemy (SQLite, but can be easily converted to MySQL or any other preference), command structuring in a simple and neat way, and Discord event handling.

## Requirements
An environment of Python 3.6+ (below untested).

## Installation
You can use pip to install requirements from `requirements.txt`.

```
pip install -r requirements.txt
```

After it's all processed and done, make sure you have edited `config.py` according to your own settings! You can run the bot with;

```
python manage.py runbot
```

## Configuration
JustBot uses a simple file to handle all of your configuration. Simply go to `config.py` and edit the things there.

## FAQ
### How is the localization handled?
Localization is handled with Python's gettext libraries. However, I used Babel's extractor and compiler to create and compile .po and .mo files. If you'd like to do so with your translations of your own or simply want to translate to another language, you'll need Babel.

```
pip install babel
```

Next, you'll need to extract all your marked strings.

```
pybabel extract . -o locale/base.pot
```

If you have changed the base of code a lot and need to retranslate everything from scratch, it's better to use init argument. I used `en_US` below as an example, you need to change it to your own desired language.

```
pybabel init -l en_US -i locale/base.pot -d locale
```

If you'd like to update current translations instead, simply replace `init` with `update`.

```
pybabel update -l en_US -i locale/base.pot -d locale
```

Next, go to `locale/(your_language)/LC_MESSAGES` directory and edit `messages.pot` to translate. You can use any text editor or a better GUI like Poedit, depends on your preference. After you're done, compile your edited files.

```
pybabel compile -d locale
```

You're done! Don't forget to change the language on `BOT_LANGUAGE` in `config.py`.

### How to translate commands?
Commands are differently and not used in gettext context, so you'll need to modify the function names from `commands.py` to translate commands. Command arguments are still within gettext context in base version and can be translated via .po files.