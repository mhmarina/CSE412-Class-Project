# Python Discord Bot Template

This repository is a template that everyone can use for the start of their Discord bot.

Slash commands can take some time to get registered globally, so if you want to test a command you should use
the `@app_commands.guilds()` decorator so that it gets registered instantly. Example:

```py
@commands.hybrid_command(
  name="command",
  description="Command description",
)
@app_commands.guilds(discord.Object(id=GUILD_ID)) # Place guild ID here
```

## How to set up

To set up the bot it was made as simple as possible.

### `config.json` file

There is [`config.json`](config.json) file where you can put the
needed things to edit.

Here is an explanation of what everything is:

| Variable             | What it is                                     |
| -------------------- | ---------------------------------------------- |
| BOT_PREFIX_HERE      | The prefix you want to use for normal commands |
| BOT_INVITE_LINK_HERE | The link to invite the bot                     |

### `.env` file

To set up the token you will have to make use of the [`.env.example`](.env.example) file, you should rename it to `.env` and replace `BOT_TOKEN_HERE` with actual bot's token.

Alternatively you can simply create an environment variable named `TOKEN`.

## How to start

To start the bot you simply need to launch, either in terminal (Linux, Mac & Windows), or in Command Prompt (
Windows)
.

Before running the bot you will need to install all the requirements with this command:

```
python -m pip install -r requirements.txt
```

After that you can start it with

```
python bot.py
```

> **Note:** May need to replace `python` with `py`, `python3`, `python3.11`, etc. depending on what Python versions you have installed on the machine.
