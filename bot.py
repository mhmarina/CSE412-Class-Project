from json import load as load_json
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    FileHandler,
    Formatter,
    StreamHandler,
    getLogger,
)
from os import getenv, listdir, name, path
from platform import python_version, release, system
from random import choice as rchoice
from sys import exit as sys_exit

from discord import Embed, Game, Intents, Message, __version__
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

from dbconnection import DBManager

if not path.isfile(f"{path.realpath(path.dirname(__file__))}/config.json"):
    sys_exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{path.realpath(path.dirname(__file__))}/config.json") as file:
        config = load_json(file)

"""
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True # `message_content` is required to get the content of the messages
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True

Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = True
intents.message_content = True
intents.presences = True
"""

# import environment variables
load_dotenv()

intents = Intents.default()
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize the database connection
db = DBManager()
db.connect_and_init()

# Global variable for tracking current trivia session
current_session_id = None


"""
Uncomment this if you want to use prefix (normal) commands.
It is recommended to use slash commands and therefore not use prefix commands.

If you want to use prefix commands, make sure to also enable the intent below in the Discord developer portal.
"""
# intents.message_content = True

# Setup both of the loggers


class LoggingFormatter(Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        DEBUG: gray + bold,
        INFO: blue + bold,
        WARNING: yellow + bold,
        ERROR: red,
        CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = getLogger("discord_bot")
logger.setLevel(INFO)

# Console handler
console_handler = StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}",
    "%Y-%m-%d %H:%M:%S",
    style="{",
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=intents,
            help_command=None,
        )
        """
        This creates custom bot variables so that we can access these variables in cogs more easily.

        For example, The config is available using the following code:
        - self.config # In this class
        - bot.config # In this file
        - self.bot.config # In cogs
        """
        self.logger = logger
        self.config = config
        # db_mgr is an object with a connection (conn) and a cursor
        self.db_mgr = DBManager()

    async def init_db(self) -> None:
        self.db_mgr.connect_and_init()
        logger.info("Database connection established.")

    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        for file in listdir(f"{path.realpath(path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    if extension == "general":
                        from cogs.general import setup as general_setup

                        await general_setup(self, self.db_mgr)
                        # await self.load_extension(f"cogs.{extension}", extras={"db": self.db_mgr})
                    else:
                        await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}",
                    )

    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        statuses = ["with you!", "with Krypton!", "with humans!"]
        await self.change_presence(activity=Game(rchoice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {__version__}")
        self.logger.info(f"Python version: {python_version()}")
        self.logger.info(
            f"Running on: {system()} {release()} ({name})",
        )
        self.logger.info("-------------------")
        self.db_mgr.connect_and_init()
        # await self.init_db()
        await self.load_cogs()
        self.status_task.start()

    async def on_message(self, message: Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})",
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs",
            )

    async def on_command_error(self, context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = Embed(
                description="You are not the owner of the bot!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot.",
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot.",
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error

    async def on_ready(self):
        """
        Event triggered when the bot is ready and connected to Discord.
        """
        self.logger.info(f"Bot is ready and logged in as {self.user.name}")

        welcome_message = (
            "🎉    **Welcome to the Trivia Game!**    🎉\n\n"
            "Here are the commands you can use to get started:\n"
            "`!startgame` - Start a new trivia game session.\n"
            "`!question` - Ask a trivia question.\n"
            "`!question <category>` - Ask a trivia question in a specific category.\n"
            "`!categories` - View all available Categories.\n"
            "`!endgame` - End the current trivia game session.\n"
            "`!leaderboard` - View the trivia leaderboard.\n"
            "`!help` - List all available commands.\n\n"
            "To select an answer, simply type the letter and press enter.\n\n"
            "🍀    Enjoy the game and good luck!    🍀"
        )

        for guild in self.guilds:  # Iterate through all the guilds the bot is in
            for channel in guild.text_channels:  # Iterate through all text channels
                if channel.permissions_for(
                    guild.me,
                ).send_messages:  # Check if bot can send messages in the channel
                    try:
                        await channel.send(welcome_message)  # Send the startup message
                        break  # Stop after sending in the first accessible channel in the guild
                    except Exception as e:
                        self.logger.error(
                            f"Failed to send welcome message in {channel.name} of {guild.name}: {e}",
                        )


# Handle bot disconnect
@bot.event
async def on_disconnect():
    db.close()
    logger.info("Bot has disconnected and database connection closed.")


bot = DiscordBot()
# tokens: https://www.writebots.com/discord-bot-token/
TOKEN = getenv("BOT_TOKEN")
bot.run(TOKEN)
