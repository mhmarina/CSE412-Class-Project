## How to set up

### `config.json` file

There is [`config.json`](config.json) file where you can put the
needed things to edit.

Here is an explanation of what everything is:

| Variable             | What it is                                     |
| -------------------- | ---------------------------------------------- |
| BOT_PREFIX_HERE      | The prefix you want to use for normal commands |
| BOT_INVITE_LINK_HERE | The link to invite the bot                     |

### `.env` file
Set up the following env variables: <br>
`TOKEN` - This is the Bot token <br>
`DBNAME` - This is the Database name <br>
`DBUSER` - This is the Databse user (for example, "postgres") <br>
`DBPASS` - This is the Database password

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
## Further reading
<link>https://www.writebots.com/discord-bot-token/<link>
<br>
<br>
> **Note:** May need to replace `python` with `py`, `python3`, `python3.11`, etc. depending on what Python versions you have installed on the machine.
