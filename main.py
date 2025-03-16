import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
import asyncio
from datetime import datetime, timedelta
import os
import webserver
import time
import random

random_messages = [
    "अरे तोहार अइया मैया सैया काहे पिंग पिंग कर रहे हो?",
    "कौछि है बे?",
    "मूरख है का रहे तुमका कितनी बार बोले है पिंग मति करो",
    "अभी रुको कट्टा निकालते है",
    "ओये! मोबाइल में घुस जाऊँ का?",
    "बड़ा तेज बन रहा है? ठहर, अभी गुंडागर्दी ON करते हैं!",
    "बेवकूफी की भी सीमा होती है, तेरा पिंग उस सीमा से बाहर है!",
    "क्या बे! पिंग से बवाल मचाएगा? अभी ईंट से ईंट बजा देंगे!",
    "दिमाग का दही मत कर, वरना आचार बना दूँगा!",
    "ठहर, अभी तुम्हारे पिंग की बारात निकालते हैं!",
    "गली में आ, बात करते हैं!",
    "कट्टा ही नहीं, पूरी गुंडों की बारात लेकर आएंगे तेरे पिंग का रिसेप्शन करने!",
    "अबे कउन पिंगवा पिंगवा खेलत है? मोहल्ला समझे हो का?",
    "अबे तोहार बाप का फोन है का? पिंगवा रोके का ना?",
    "भी लठिया संग दर्शन कराएंगे!",
    "अबे, दिमाग न खराब कर, नाहीं कद्दू काटे जइसन फाड़ देंगे!",
    "एक बार और पिंग किया तो ससुरा नेटवर्के संग धूल चटा देंगे!",
    "रुक बे, अभी चमड़वा उधड़वा के बेल्ट सिलवा देंगे!",
    "अबे बकैती कम कर, नाहीं ईंटा से ईंट बजा देंगे!",
    "अबे पिंगवा मारे के ठेका ले रखे हो का? हाथ रोक ले नाहीं उँगरी तोड़े का पड़ेगा!",
    "एक बार और पिंग किया ना... तो पूरा सर्वर ही फूंक देंगे!",
    "का बे, पिंगवा मार मार के नेता बने का सोच रहे हो?",
    "ठहर बे, अभी तोहार अकॉउंटवा हैक करते है",
    "अबे, का बवाल मचाए हो? हम कोई सरकारी बाबू हैं का, जो बार-बार पिंग कर रहे हो?",
    "रुक बे, अभी तोहार पिंगवा को परमानेंट 'No Response' में डाल देते हैं!",
    "का बे? इत्ता पिंगवा मार रहे हो, सर्वरवा तेरा खानदानी जागीर है का?",
    "अबे तोहार हाथवा फिसल गया का? नाहीं तोहर 'Mute' पक्का!",
    "अबे, 5 बार से जादा पिंग करने पर कानूनी कार्रवाई होगी, समझा?",
    "देख बे, पिंगवा मार-मार के हमारा BP बढ़ा दिया, ठहर अबे ब्लॉकवा मारते हैं!",
    "बेटा तुम ई न भूलो की हम सर्वर के बॉट है और हमारे पास साड़ी परमिशन है",
    "बेटा तमंचे में जितने छर्रे है सब तुम्हारे पिछवाड़े में ठोक देंगे",

    "काय रे! का जरूरत पड़ी मोरे नाम लइके?",
  "अबे! हमका शांति से रहइ द, नाहीं त परे रहब थप्पड़!",
  "कहत हउँ, दुबारा मोरे नाम लीनव त कान धराइ देब!",
  "तू का समझा हमका? एतनेई फुरसत बा हमरे लगे?",
  "अब न बुलइह मोरे नाम, नाहीं त भौकाल होई!",
  "का रे! मोका फालतू परेशान कइके जान प्यारी नईखे?",
  "बुलावल बाटे, अब का करब? गोली मारब कि हटब?",
  "कहिन त अइके देखाई देब, तब बुझाई असल ग़ुंडा के!",
  "नाम लइन से पहिले सौ बेर सोचिह, नाहीं त खुदे पछतइब!",
  "अब दुबारा पिंग करब त किडनी बेचवा देब!",
  "गुंडा के नाम जुबान प अकसर नईखे लावत, समझल?",
  "बाप बुलइह त आइब, नाहीं त दूर रहिह!",
  "का हो? एतनेई शौक बाटे तकलीफ लेवे के?",
  "अबे! हम गुंडा बानी, नाम लेबू त हड्डी गिनाई!",
  "ग़लती से मोरे नाम लियऊ ह, केहू के जरूरत नईखे इहाँ!"
]

TOKEN = os.environ.get("TOKEN")
GUILD_ID = 1333667547006107708
LOG_CHANNEL_ID = 1348264999730155621
OTHER_LOG_CHANNEL_ID = 1337295229124087838
ALLOWED_CHANNEL_ID = 1349565123857223711
WELCOME_LOG = 1349573548066213888

ADMIN_ROLE_ID = 1333670552405147679

TIME_WINDOW = 5  # Time window in seconds
MESSAGE_THRESHOLD = 4  # Max messages allowed in time window
DUPLICATE_THRESHOLD = 3  # Max duplicate messages allowed
PING_THRESHOLD = 5  # Max user mentions allowed
CAPS_THRESHOLD = 0.7  # 70% caps is considered spam


user_message_history = {}
user_duplicate_history = {}

ROLE_1_ID = 123456789012345678
ROLE_2_ID = 987654321098765432
ROLE_1_EMOJI = "✅"
ROLE_2_EMOJI = "🔵"

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

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
    name="clear",
    description="Delete up to 1000 messages in this channel.",
    options=[
        disnake.Option(
            name="amount",
            description="Number of messages to delete (1-1000).",
            type=disnake.OptionType.integer,
            required=True,
            min_value=1,
            max_value=1000
        )
    ],
    default_member_permissions=disnake.Permissions(manage_messages=True)  # Restrict to users with "Manage Messages" permission

    
)

async def clear(inter: disnake.ApplicationCommandInteraction, amount: int):
    # Check if the bot has permission to manage messages
    if not inter.channel.permissions_for(inter.guild.me).manage_messages:
        await inter.response.send_message("I don't have permission to delete messages in this channel.", ephemeral=True)
        return

    # Delete the messages
    deleted = await inter.channel.purge(limit=amount)
    await inter.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)


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
    elif color == "orange":
        embed_color = disnake.Color.orange()
    elif color == "purple":
        embed_color = disnake.Color.purple()
    else:
        embed_color = disnake.Color.blue()  # Default to blue if color is not recognized

    embed = disnake.Embed(title=title, description=description, color=embed_color)
    await channel.send(embed=embed)
    await interaction.response.send_message(f"Embed sent to {channel.mention}!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and synced commands.")

@bot.event
async def on_member_join(member):
    log_channel = bot.get_channel(WELCOME_LOG)
    if log_channel:
        embed = disnake.Embed(
            title="Member Joined",
            description=f"{member.mention} has joined the server.",
            color=disnake.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await log_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(WELCOME_LOG)
    if log_channel:
        embed = disnake.Embed(
            title="Member Left",
            description=f"{member.mention} has left the server.",
            color=disnake.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await log_channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        if before.nick != after.nick:
            embed = disnake.Embed(title="Nickname Change", color=disnake.Color.blue())
            embed.add_field(name="Before", value=before.nick or before.name, inline=True)
            embed.add_field(name="After", value=after.nick or after.name, inline=True)
            await log_channel.send(embed=embed)
        if before.avatar != after.avatar:
            embed = disnake.Embed(title="Profile Picture Changed", color=disnake.Color.blue())
            embed.set_thumbnail(url=after.avatar.url)
            await log_channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(title="Message Deleted", color=disnake.Color.orange())
        embed.add_field(name="User", value=message.author.mention, inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Content", value=message.content or "[No Content]", inline=False)
        await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel and before.content != after.content:
        embed = disnake.Embed(title="Message Edited", color=disnake.Color.yellow())
        embed.add_field(name="User", value=before.author.mention, inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        embed.add_field(name="Before", value=before.content or "[No Content]", inline=False)
        embed.add_field(name="After", value=after.content or "[No Content]", inline=False)
        await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        async for entry in channel.guild.audit_logs(action=disnake.AuditLogAction.channel_delete, limit=1):
            embed = disnake.Embed(title="Channel Created", color=disnake.Color.red())
            embed.add_field(name="Channel Name", value=channel.name, inline=False)
            embed.add_field(name="Created By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        async for entry in channel.guild.audit_logs(action=disnake.AuditLogAction.channel_delete, limit=1):
            embed = disnake.Embed(title="Channel Deleted", color=disnake.Color.red())
            embed.add_field(name="Channel Name", value=channel.name, inline=False)
            embed.add_field(name="Deleted By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        if before.channel != after.channel:
            embed = disnake.Embed(title="Voice Channel Update", color=disnake.Color.purple())
            embed.add_field(name="User", value=member.mention, inline=True)
            if before.channel:
                embed.add_field(name="Left", value=before.channel.name, inline=True)
            if after.channel:
                embed.add_field(name="Joined", value=after.channel.name, inline=True)
            await log_channel.send(embed=embed)

@bot.event
async def on_member_ban(guild, user):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(title="User Banned", description=f"{user.mention} was banned.", color=disnake.Color.red())
        await log_channel.send(embed=embed)

@bot.event
async def on_member_unban(guild, user):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(title="User Unbanned", description=f"{user.mention} was unbanned.", color=disnake.Color.green())
        await log_channel.send(embed=embed)

@bot.event
async def on_reaction_add(reaction, user):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(title="Reaction Added", color=disnake.Color.blue())
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Message", value=reaction.message.content[:100], inline=False)
        embed.add_field(name="Emoji", value=str(reaction.emoji), inline=True)
        await log_channel.send(embed=embed)

@bot.event
async def on_reaction_remove(reaction, user):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(title="Reaction Removed", color=disnake.Color.orange())
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Message", value=reaction.message.content[:100], inline=False)
        embed.add_field(name="Emoji", value=str(reaction.emoji), inline=True)
        await log_channel.send(embed=embed)


@bot.event
async def on_member_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]
            embed = disnake.Embed(title="Role Update", color=disnake.Color.blue())
            embed.add_field(name="User", value=after.mention, inline=True)
            if added_roles:
                embed.add_field(name="Added Roles", value=", ".join(r.mention for r in added_roles), inline=False)
            if removed_roles:
                embed.add_field(name="Removed Roles", value=", ".join(r.mention for r in removed_roles), inline=False)
            await log_channel.send(embed=embed)
        
        if before.timed_out_until != after.timed_out_until:
            embed = disnake.Embed(title="User Timeout", color=disnake.Color.red())
            embed.add_field(name="User", value=after.mention, inline=True)
            if after.timed_out_until:
                embed.add_field(name="Timed Out Until", value=str(after.timed_out_until), inline=False)
            else:
                embed.add_field(name="Timeout Removed", value="User is no longer timed out.", inline=False)
            await log_channel.send(embed=embed)
        
        if before.premium_since != after.premium_since:
            embed = disnake.Embed(title="User Boosted", color=disnake.Color.pink())
            embed.add_field(name="User", value=after.mention, inline=True)
            if after.premium_since:
                embed.add_field(name="Boosted the Server", value="Yes", inline=False)
            else:
                embed.add_field(name="Stopped Boosting", value="Yes", inline=False)
            await log_channel.send(embed=embed)


@bot.event
async def on_guild_role_create(role):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who created the role
        async for entry in role.guild.audit_logs(action=disnake.AuditLogAction.role_create, limit=1):
            embed = disnake.Embed(title="Role Created", description=role.mention, color=disnake.Color.green())
            embed.add_field(name="Created By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_role_delete(role):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who deleted the role
        async for entry in role.guild.audit_logs(action=disnake.AuditLogAction.role_delete, limit=1):
            embed = disnake.Embed(title="Role Deleted", description=role.name, color=disnake.Color.red())
            embed.add_field(name="Deleted By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_role_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the role
        async for entry in after.guild.audit_logs(action=disnake.AuditLogAction.role_update, limit=1):
            embed = disnake.Embed(title="Role Updated", color=disnake.Color.orange())
            embed.add_field(name="Before", value=before.name, inline=True)
            embed.add_field(name="After", value=after.name, inline=True)
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_thread_create(thread):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who created the thread
        async for entry in thread.guild.audit_logs(action=disnake.AuditLogAction.thread_create, limit=1):
            embed = disnake.Embed(title="Thread Created", description=thread.name, color=disnake.Color.green())
            embed.add_field(name="Created By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_thread_delete(thread):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who deleted the thread
        async for entry in thread.guild.audit_logs(action=disnake.AuditLogAction.thread_delete, limit=1):
            embed = disnake.Embed(title="Thread Deleted", description=thread.name, color=disnake.Color.red())
            embed.add_field(name="Deleted By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the guild
        async for entry in after.audit_logs(action=disnake.AuditLogAction.guild_update, limit=1):
            embed = disnake.Embed(title="Guild Updated", color=disnake.Color.purple())
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_invite_create(invite):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who created the invite
        async for entry in invite.guild.audit_logs(action=disnake.AuditLogAction.invite_create, limit=1):
            embed = disnake.Embed(title="Invite Created", description=invite.url, color=disnake.Color.green())
            embed.add_field(name="Created By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_invite_delete(invite):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who deleted the invite
        async for entry in invite.guild.audit_logs(action=disnake.AuditLogAction.invite_delete, limit=1):
            embed = disnake.Embed(title="Invite Deleted", description=invite.code, color=disnake.Color.red())
            embed.add_field(name="Deleted By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_emojis_update(guild, before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the emojis
        async for entry in guild.audit_logs(action=disnake.AuditLogAction.emoji_update, limit=1):
            embed = disnake.Embed(title="Emojis Updated", color=disnake.Color.blue())
            embed.add_field(name="Before", value=str(len(before)), inline=True)
            embed.add_field(name="After", value=str(len(after)), inline=True)
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the channel
        async for entry in after.guild.audit_logs(action=disnake.AuditLogAction.channel_update, limit=1):
            embed = disnake.Embed(title="Channel Updated", color=disnake.Color.orange())
            embed.add_field(name="Channel", value=after.mention, inline=False)
            if before.name != after.name:
                embed.add_field(name="Name Changed", value=f"{before.name} → {after.name}", inline=False)
            if before.topic != after.topic:
                embed.add_field(name="Topic Changed", value=f"{before.topic} → {after.topic}", inline=False)
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_webhooks_update(channel):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the webhook
        async for entry in channel.guild.audit_logs(action=disnake.AuditLogAction.webhook_update, limit=1):
            embed = disnake.Embed(title="Webhook Updated", description=f"Webhook updated in {channel.mention}", color=disnake.Color.blue())
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_scheduled_event_create(event):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who created the event
        async for entry in event.guild.audit_logs(action=disnake.AuditLogAction.scheduled_event_create, limit=1):
            embed = disnake.Embed(title="Scheduled Event Created", description=event.name, color=disnake.Color.green())
            embed.add_field(name="Created By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_scheduled_event_delete(event):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who deleted the event
        async for entry in event.guild.audit_logs(action=disnake.AuditLogAction.scheduled_event_delete, limit=1):
            embed = disnake.Embed(title="Scheduled Event Deleted", description=event.name, color=disnake.Color.red())
            embed.add_field(name="Deleted By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_scheduled_event_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the event
        async for entry in after.guild.audit_logs(action=disnake.AuditLogAction.scheduled_event_update, limit=1):
            embed = disnake.Embed(title="Scheduled Event Updated", description=after.name, color=disnake.Color.orange())
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_stickers_update(guild, before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the stickers
        async for entry in guild.audit_logs(action=disnake.AuditLogAction.sticker_update, limit=1):
            embed = disnake.Embed(title="Stickers Updated", color=disnake.Color.blue())
            embed.add_field(name="Before", value=str(len(before)), inline=True)
            embed.add_field(name="After", value=str(len(after)), inline=True)
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_stage_instance_create(stage_instance):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who started the stage
        async for entry in stage_instance.guild.audit_logs(action=disnake.AuditLogAction.stage_instance_create, limit=1):
            embed = disnake.Embed(title="Stage Started", description=stage_instance.channel.name, color=disnake.Color.green())
            embed.add_field(name="Started By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_stage_instance_delete(stage_instance):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who ended the stage
        async for entry in stage_instance.guild.audit_logs(action=disnake.AuditLogAction.stage_instance_delete, limit=1):
            embed = disnake.Embed(title="Stage Ended", description=stage_instance.channel.name, color=disnake.Color.red())
            embed.add_field(name="Ended By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_stage_instance_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the stage
        async for entry in after.guild.audit_logs(action=disnake.AuditLogAction.stage_instance_update, limit=1):
            embed = disnake.Embed(title="Stage Updated", description=after.channel.name, color=disnake.Color.orange())
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_automod_action(action):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(title="AutoMod Action", color=disnake.Color.red())
        embed.add_field(name="User", value=action.user.mention, inline=True)
        embed.add_field(name="Rule", value=action.rule_triggered, inline=True)
        embed.add_field(name="Content Blocked", value=action.content or "[No Content]", inline=False)
        await log_channel.send(embed=embed)

@bot.event
async def on_thread_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel:
        # Fetch audit logs to find who updated the thread
        async for entry in after.guild.audit_logs(action=disnake.AuditLogAction.thread_update, limit=1):
            embed = disnake.Embed(title="Thread Updated", color=disnake.Color.orange())
            embed.add_field(name="Thread", value=after.name, inline=False)
            embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
            await log_channel.send(embed=embed)

@bot.event
async def on_presence_update(before, after):
    log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if log_channel and before.status != after.status:
        embed = disnake.Embed(title="User Presence Updated", color=disnake.Color.blue())
        embed.add_field(name="User", value=after.mention, inline=True)
        embed.add_field(name="Before", value=str(before.status), inline=True)
        embed.add_field(name="After", value=str(after.status), inline=True)
        await log_channel.send(embed=embed)


@bot.event
async def on_message(message):

    if bot.user.mentioned_in(message):
        random_message = random.choice(random_messages)
        await message.channel.send(random_message)
    
    if message.author.bot:
        return

    # Anti-Spam
    user_id = message.author.id
    current_time = time.time()

    if user_id not in user_message_history:
        user_message_history[user_id] = []

    user_message_history[user_id].append(current_time)

    # Remove old timestamps
    user_message_history[user_id] = [
        t for t in user_message_history[user_id] if t > current_time - TIME_WINDOW
    ]

    if len(user_message_history[user_id]) > MESSAGE_THRESHOLD:
        log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
        admin_role = disnake.utils.get(message.guild.roles, id=ADMIN_ROLE_ID)
        if log_channel and admin_role:
            embed = disnake.Embed(title="Possible Spam Detected", color=disnake.Color.red())
            embed.add_field(name="User", value=message.author.mention, inline=False)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            embed.add_field(name="Message Content", value=message.content, inline=False)
            embed.add_field(name="Message Count", value=str(len(user_message_history[user_id])), inline=False)
            await log_channel.send(f"{admin_role.mention} High priority spam detected!", embed=embed)
            await message.delete()  # Delete the spam messages
            del user_message_history[user_id]  # Reset the user message history
            return  # Exit to prevent other checks.

    # Duplicate Message Detection
    if user_id not in user_duplicate_history:
        user_duplicate_history[user_id] = []

    user_duplicate_history[user_id].append(message.content)

    if len(user_duplicate_history[user_id]) > DUPLICATE_THRESHOLD:
        if len(set(user_duplicate_history[user_id][-DUPLICATE_THRESHOLD:])) == 1:  # Check if the last N messages are the same
            log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
            admin_role = disnake.utils.get(message.guild.roles, id=ADMIN_ROLE_ID)
            if log_channel and admin_role:
                embed = disnake.Embed(title="Possible Duplicate Message Spam", color=disnake.Color.red())
                embed.add_field(name="User", value=message.author.mention, inline=False)
                embed.add_field(name="Channel", value=message.channel.mention, inline=False)
                embed.add_field(name="Message Content", value=message.content, inline=False)
                await log_channel.send(f"{admin_role.mention} High priority duplicate message spam detected!", embed=embed)
                await message.delete()
                del user_duplicate_history[user_id]
                return

    # Excessive Pings
    if "@everyone" in message.content or "@here" in message.content:
        log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
        admin_role = disnake.utils.get(message.guild.roles, id=ADMIN_ROLE_ID)
        if log_channel and admin_role:
            embed = disnake.Embed(title="Excessive Ping Detected", color=disnake.Color.orange())
            embed.add_field(name="User", value=message.author.mention, inline=False)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            embed.add_field(name="Message Content", value=message.content, inline=False)
            await log_channel.send(f"{admin_role.mention} Possible mass ping detected!", embed=embed)

    if len(message.mentions) > PING_THRESHOLD:
        log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
        admin_role = disnake.utils.get(message.guild.roles, id=ADMIN_ROLE_ID)
        if log_channel and admin_role:
            embed = disnake.Embed(title="Excessive User Pings Detected", color=disnake.Color.orange())
            embed.add_field(name="User", value=message.author.mention, inline=False)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            embed.add_field(name="Message Content", value=message.content, inline=False)
            embed.add_field(name="Number of Pings", value=str(len(message.mentions)), inline=False)
            await log_channel.send(f"{admin_role.mention} Possible mass user ping detected!", embed=embed)

    # Excessive Caps
    caps_percentage = sum(1 for c in message.content if c.isupper()) / len(message.content) if message.content else 0
    if caps_percentage > CAPS_THRESHOLD and len(message.content) > 10:  # Add length check to avoid false positives
        log_channel = bot.get_channel(OTHER_LOG_CHANNEL_ID)
        admin_role = disnake.utils.get(message.guild.roles, id=ADMIN_ROLE_ID)
        if log_channel and admin_role:
            embed = disnake.Embed(title="Excessive Caps Detected", color=disnake.Color.orange())
            embed.add_field(name="User", value=message.author.mention, inline=False)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            embed.add_field(name="Message Content", value=message.content, inline=False)
            embed.add_field(name="Caps Percentage", value=f"{caps_percentage:.2%}", inline=False)
            await log_channel.send(f"{admin_role.mention} Possible excessive caps detected!", embed=embed)

    await bot.process_commands(message)  # Process commands after checking for spam

webserver.keep_alive()
bot.run(TOKEN)
