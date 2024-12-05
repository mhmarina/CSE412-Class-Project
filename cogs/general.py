from datetime import datetime
from platform import python_version

from discord import (
    Embed,
    Forbidden,
    Interaction,
    Message,
    TextStyle,
    User,
    app_commands,
)
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Modal, TextInput
from dotenv import load_dotenv

# import environment variables
load_dotenv()


class FeedbackForm(Modal, title="Feedback"):
    feedback = TextInput(
        label="What do you think about this bot?",
        style=TextStyle.long,
        placeholder="Type your answer here...",
        required=True,
        max_length=256,
    )

    async def on_submit(self, interaction: Interaction):
        self.interaction = interaction
        self.answer = str(self.feedback)
        self.stop()


class General(commands.Cog, name="general"):
    def __init__(self, bot, db) -> None:
        self.bot = bot
        self.db = db
        self.current_session_id = None
        self.context_menu_user = app_commands.ContextMenu(
            name="Grab ID",
            callback=self.grab_id,
        )
        self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(
            name="Remove spoilers",
            callback=self.remove_spoilers,
        )
        self.bot.tree.add_command(self.context_menu_message)

    @commands.command()
    async def test(self, ctx: Context):
        """A simple test command."""
        await ctx.send("The bot is working!")

    # insert user if DNE
    async def insert_user(self, ctx):
        user_id = ctx.author.id  # Discord user ID
        username = ctx.author.name  # Discord username
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM users WHERE u_userid = %s;",
                [user_id],
            )
            user_exists = self.db.cursor.fetchone()[0]

            if not user_exists:
                # If user does not exist, add them to the database
                self.db.insert_user(user_id, username)
                print(f"User {username} (ID: {user_id}) added to the database.")
            else:
                print(
                    f"User {username} (ID: {user_id}) already exists in the database.",
                )
            return 0

        except Exception as e:
            print(f"Error checking/adding user: {e}")
            await ctx.send(f"Error adding user to the database: {e}")
            return 1

    @commands.command(name="categories")
    async def print_categories(self, ctx: Context):
        categories = self.db.select_distinct_categories()
        categoriesString = ""
        for category in categories:
            categoriesString += category[0] + "\n"

        await ctx.send(
            "There are questions in the following categories: \n" + categoriesString,
        )
        return

    @commands.command(name="startgame")
    async def start_game(self, ctx: Context):
        """Start a new trivia game."""
        if self.current_session_id is not None:
            await ctx.send("A game is already in progress!")
            return

        # add user to DB if DNE
        error = await self.insert_user(ctx)
        if error == 1:
            return

        # Create a new trivia session
        self.current_session_id = int(datetime.now().timestamp())
        start_time = datetime.now()

        try:
            self.db.insert_trivia_session(self.current_session_id, start_time)
            await ctx.send(
                f"Trivia game started! Session ID: {self.current_session_id}",
            )
        except Exception as e:
            print(f"Error starting trivia session: {e}")
            await ctx.send(f"Error starting trivia session: {e}")
            self.current_session_id = None

    @commands.command(name="endgame")
    async def end_game(self, ctx: Context):
        """End the current trivia game."""
        if self.current_session_id is None:
            await ctx.send("No game is currently in progress.")
            return

        stop_time = datetime.now()
        self.db.update_session_stop_time(self.current_session_id, stop_time)
        await ctx.send(f"Trivia game ended! Session ID: {self.current_session_id}")
        self.current_session_id = None

    @commands.command(name="question")
    async def ask_question(self, ctx: Context, category=None):
        """Ask a trivia question with multiple-choice answers during an active game."""
        if self.current_session_id is None:
            await ctx.send(
                "No trivia game is currently in progress. Use !startgame to begin.",
            )
            return

        # Fetch a random question
        question = None
        if category:
            question = self.db.get_question_cat(category)
            if not question:
                await ctx.send(f'No questions found under category: "{category}".\n')
                await self.print_categories(ctx)
                return
        else:
            question = self.db.get_random_question()
            if not question:
                await ctx.send("No questions available.")
                return

        # Fetch corresponding answers for the question
        answers = self.db.get_answers_for_question(question[0])
        if not answers:
            await ctx.send("No answers available for this question.")
            return

        # Format the question and answers
        question_text = f"Category: {question[2]}\nQuestion: {question[3]}"
        answer_text = "\n".join(
            [f"{answer[0].upper()}: {answer[2]}" for answer in answers],
        )
        full_text = f"{question_text}\n\n**Answers:**\n{answer_text}"

        # Send the question and answers to the Discord channel
        await ctx.send(full_text)

        def check(msg):
            return msg.author != self.bot.user and msg.channel == ctx.channel

        # Wait for the user's answer
        try:
            answer = await self.bot.wait_for("message", check=check, timeout=30)
            # add user to db if doesn't exist:
            error = await self.insert_user(ctx)
            if error == 1:
                return

            correct_answers = [ans for ans in answers if ans[3]]  # Get correct answers
            if any(ans[0].lower() == answer.content.lower() for ans in correct_answers):
                await ctx.send("🎉 Correct!")
                self.db.insert_play(ctx.author.id, self.current_session_id, 10)
                # Update the `asked` table with the correct answer
                self.db.insert_asked(
                    session_id=self.current_session_id,
                    question_id=question[0],
                    answered_by=ctx.author.id,
                    answer=answer.content.lower(),
                    is_correct=True,
                )
            else:
                await ctx.send("❌ Incorrect!")
                self.db.insert_play(ctx.author.id, self.current_session_id, 10)
                # Update the `asked` table with the incorrect answer
                self.db.insert_asked(
                    session_id=self.current_session_id,
                    question_id=question[0],
                    answered_by=ctx.author.id,
                    answer=answer.content.lower(),
                    is_correct=False,
                )
        except TimeoutError:
            await ctx.send("⏰ Time's up!")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx: Context):
        """Display the leaderboard."""
        try:
            users = self.db.get_top_users(limit=10)
        except Exception as e:
            await ctx.send(f"Error retrieving leaderboard: {e}")
            return

        if not users:
            await ctx.send("No users found on the leaderboard.")
            return

        leaderboard_message = "🏆 **Leaderboard** 🏆\n"
        for rank, user in enumerate(users, start=1):
            leaderboard_message += f"{rank}. {user[1]} - {user[2]} points\n"

        await ctx.send(leaderboard_message)

    # Message context menu command
    async def remove_spoilers(
        self,
        interaction: Interaction,
        message: Message,
    ) -> None:
        """
        Removes the spoilers from the message. This command requires the MESSAGE_CONTENT intent to work properly.

        :param interaction: The application command interaction.
        :param message: The message that is being interacted with.
        """
        spoiler_attachment = None
        for attachment in message.attachments:
            if attachment.is_spoiler():
                spoiler_attachment = attachment
                break
        embed = Embed(
            title="Message without spoilers",
            description=message.content.replace("||", ""),
            color=0xBEBEFE,
        )
        if spoiler_attachment is not None:
            embed.set_image(url=attachment.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # User context menu command
    async def grab_id(
        self,
        interaction: Interaction,
        user: User,
    ) -> None:
        """
        Grabs the ID of the user.

        :param interaction: The application command interaction.
        :param user: The user that is being interacted with.
        """
        embed = Embed(
            description=f"The ID of {user.mention} is `{user.id}`.",
            color=0xBEBEFE,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="help",
        description="List all commands the bot has loaded.",
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = Embed(
            title="Help",
            description="List of available commands:",
            color=0xBEBEFE,
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(),
                value=f"```{help_text}```",
                inline=False,
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = Embed(
            description="Used [Krypton's](https://krypton.ninja) template",
            color=0xBEBEFE,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="Krypton#7331", inline=True)
        embed.add_field(
            name="Python Version:",
            value=f"{python_version()}",
            inline=True,
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        num_roles = len(roles)
        if num_roles > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying [50/{num_roles}] Roles")
        roles = ", ".join(roles)

        embed = Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0xBEBEFE,
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}",
        )
        embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        embed = Embed(
            description=f"Invite me by clicking [here]({self.bot.config['invite_link']}).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="server",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    async def server(self, context: Context) -> None:
        """
        Get the invite link of the discord server of the bot for some support.

        :param context: The hybrid command context.
        """
        embed = Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/mTBrXyWxAF).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except Forbidden:
            await context.send(embed=embed)

    @app_commands.command(
        name="feedback",
        description="Submit a feedback for the owners of the bot",
    )
    async def feedback(self, interaction: Interaction) -> None:
        """
        Submit a feedback for the owners of the bot.

        :param context: The hybrid command context.
        """
        feedback_form = FeedbackForm()
        await interaction.response.send_modal(feedback_form)

        await feedback_form.wait()
        interaction = feedback_form.interaction
        await interaction.response.send_message(
            embed=Embed(
                description="Thank you for your feedback, the owners have been notified about it.",
                color=0xBEBEFE,
            ),
        )

        app_owner = (await self.bot.application_info()).owner
        await app_owner.send(
            embed=Embed(
                title="New Feedback",
                description=f"{interaction.user} (<@{interaction.user.id}>) has submitted a new feedback:\n```\n{feedback_form.answer}\n```",
                color=0xBEBEFE,
            ),
        )


async def setup(bot, db) -> None:
    await bot.add_cog(General(bot, db))
