import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
import asyncio
from datetime import datetime, timedelta
import os

TOKEN = os.environ.get('TOKEN')
GUILD_ID = 1333667547006107708
LOG_CHANNEL_ID = 1348264999730155621
ALLOWED_CHANNEL_ID = 1349565123857223711

# Anti-raid and anti-nuke thresholds
RAID_THRESHOLD = 5  # Number of joins within RAID_TIME_WINDOW to trigger anti-raid
RAID_TIME_WINDOW = 10  # Time window in seconds to check for raids
NUKE_THRESHOLD = 3  # Number of deletions within NUKE_TIME_WINDOW to trigger anti-nuke
NUKE_TIME_WINDOW = 10  # Time window in seconds to check for nukes
SPAM_THRESHOLD = 5  # Number of messages within SPAM_TIME_WINDOW to trigger anti-spam
SPAM_TIME_WINDOW = 10  # Time window in seconds to check for spam

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Track joins, deletions, and messages for anti-raid, anti-nuke, and anti-spam
join_timestamps = []
delete_timestamps = []
user_message_timestamps = {}

questions = [
"What is your ideology?",
"Do you support hindi imposition in terms of an equal network of communication, not in terms of removing a language.",
"What are you opinions on RSS and other sangh?",
"Opinions on communism?",
"Opinions on the modern history?",
"Opinions on the current government and the opposition?",
"Opinions on savarkar?",
"Opinions on LGBTQ+ and Feminism?",
"Opinions on minorities?",
"Opinions on Muslim Extremism?",
"Opinions on caste system and casteism, as both are different things.",
"Opinions on modernization in terms of social activies ie. Dating."
]

@bot.slash_command(
    name="start_survey",
    description="Start a survey with predefined questions.",
    guild_ids=[GUILD_ID]
)
async def start_survey(interaction: ApplicationCommandInteraction):
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("This command can only be used in the verification channel.", ephemeral=True)
        return

    user = interaction.author
    responses = []

    try:
        await user.send("Starting the survey! Answer the following questions:")
    except disnake.Forbidden:
        await interaction.response.send_message("I couldn't send you a DM. Please check your privacy settings.", ephemeral=True)
        return

    await interaction.response.send_message("I've sent you a DM with the survey questions!", ephemeral=True)

    def check(m):
        return m.author == user and isinstance(m.channel, disnake.DMChannel)

    for question in questions:
        await user.send(question)
        try:
            msg = await bot.wait_for("message", check=check, timeout=300)
            responses.append(f"**{question}** {msg.content}")
        except:
            await user.send("Time's up! Survey canceled.")
            return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(title=f"Survey Responses from {user.display_name}", color=disnake.Color.blue())
        embed.description = "\n".join(responses)
        await log_channel.send(embed=embed)
    else:
        await user.send("Log channel not found. Please check the configuration.")
        return

    await user.send("Survey completed! Please wait until an admin gives you the access.")

@bot.slash_command(
    name="admin_send",
    description="Send a message as an embed (Admin only).",
    guild_ids=[GUILD_ID]
)
@commands.has_permissions(administrator=True)
async def admin_send(interaction: ApplicationCommandInteraction, channel: disnake.TextChannel, title: str, description: str, color: str = "blue"):
    color = color.lower()
    if color == "blue":
        embed_color = disnake.Color.blue()
    elif color == "green":
        embed_color = disnake.Color.green()
    elif color == "red":
        embed_color = disnake.Color.red()
    elif color == "yellow":
        embed_color = disnake.Color.yellow()
    else:
        embed_color = disnake.Color.blue()  # Default to blue if color is not recognized

    embed = disnake.Embed(title=title, description=description, color=embed_color)
    await channel.send(embed=embed)
    await interaction.response.send_message(f"Embed sent to {channel.mention}!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and synced commands.")

    registered_commands = await bot.fetch_global_commands()
    command_names = [cmd.name for cmd in registered_commands]
    print(f"Registered Slash Commands: {command_names}")

@bot.event
async def on_member_join(member):
    global join_timestamps

    # Log the join event
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(
            title="Member Joined",
            description=f"{member.mention} has joined the server.",
            color=disnake.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await log_channel.send(embed=embed)

    # Anti-raid system
    now = datetime.utcnow()
    join_timestamps.append(now)

    # Remove timestamps older than the time window
    join_timestamps = [timestamp for timestamp in join_timestamps if now - timestamp <= timedelta(seconds=RAID_TIME_WINDOW)]

    # Check if the number of joins exceeds the threshold
    if len(join_timestamps) >= RAID_THRESHOLD:
        # Ban all users who joined recently
        for timestamp in join_timestamps:
            await member.guild.ban(member, reason="Anti-raid system triggered.")
        
        # Send an alert to the log channel
        if log_channel:
            embed = disnake.Embed(
                title="🚨 Anti-Raid Triggered 🚨",
                description=f"**{len(join_timestamps)} users joined within {RAID_TIME_WINDOW} seconds. Banned all suspicious users.**",
                color=disnake.Color.red()
            )
            await log_channel.send(embed=embed)

        join_timestamps = []

@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(
            title="Member Left",
            description=f"{member.mention} has left the server.",
            color=disnake.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    global delete_timestamps

    # Anti-nuke system
    now = datetime.utcnow()
    delete_timestamps.append(now)

    # Remove timestamps older than the time window
    delete_timestamps = [timestamp for timestamp in delete_timestamps if now - timestamp <= timedelta(seconds=NUKE_TIME_WINDOW)]

    # Check if the number of deletions exceeds the threshold
    if len(delete_timestamps) >= NUKE_THRESHOLD:
        # Fetch the audit logs to find the user responsible
        async for entry in channel.guild.audit_logs(action=disnake.AuditLogAction.channel_delete, limit=1):
            user = entry.user
            await user.ban(reason="Anti-nuke system triggered.")
            break

        # Send an alert to the log channel
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = disnake.Embed(
                title="🚨 Anti-Nuke Triggered 🚨",
                description=f"**{len(delete_timestamps)} channels were deleted within {NUKE_TIME_WINDOW} seconds. Banned the user responsible.**",
                color=disnake.Color.red()
            )
            await log_channel.send(embed=embed)

        # Reset the delete timestamps
        delete_timestamps = []

@bot.event
async def on_message(message):
    # Anti-spam system
    if message.author.bot:
        return

    user_id = message.author.id
    now = datetime.utcnow()

    if user_id not in user_message_timestamps:
        user_message_timestamps[user_id] = []

    user_message_timestamps[user_id].append(now)

    # Remove timestamps older than the time window
    user_message_timestamps[user_id] = [timestamp for timestamp in user_message_timestamps[user_id] if now - timestamp <= timedelta(seconds=SPAM_TIME_WINDOW)]

    # Check if the number of messages exceeds the threshold
    if len(user_message_timestamps[user_id]) >= SPAM_THRESHOLD:
        # Mute the user
        mute_role = disnake.utils.get(message.guild.roles, name="Muted")
        if not mute_role:
            # Create the mute role if it doesn't exist
            mute_role = await message.guild.create_role(name="Muted")
            for channel in message.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)

        await message.author.add_roles(mute_role, reason="Anti-spam system triggered.")
        await message.channel.send(f"{message.author.mention} has been muted for spamming.")

        # Send an alert to the log channel
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = disnake.Embed(
                title="🚨 Anti-Spam Triggered 🚨",
                description=f"**{message.author.mention} was muted for spamming.**",
                color=disnake.Color.red()
            )
            await log_channel.send(embed=embed)

        # Reset the message timestamps for the user
        user_message_timestamps[user_id] = []

    await bot.process_commands(message)

bot.run(TOKEN)
