import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
import asyncio
from datetime import datetime, timedelta
import os
import webserver
import time
import random
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# Special User IDs & Messages  (DO NOT CHANGE)
# ──────────────────────────────────────────────

SPECIAL_USER_ID = 791971553831026709
SECONDARY_SPECIAL_USER_ID = 1317434249640673364
TERTIARY_SPECIAL_USER_ID = 1104375851816071208

special_messages = [
  "मालिक, बस इशारा कर दीजिए… काम समझो हो गया!",
  "बड़े भइया, एक शब्द बोलिए… बाकी हम संभाल लेंगे!",
  "सरकार, आपकी सेवा में हमेशा हाज़िर हैं!",
  "मालिक, आदेश दीजिए… प्रतीक्षा में खड़े हैं!",
  "आपका काम हमारी जिम्मेदारी!",
  "बस बता दीजिए क्या करना है!",
  "बड़े सरकार, आपका इशारा ही काफी है!",
  "भइया, आप कहिए और हम लग जाएँ!",
  "आपका भरोसा ही हमारी ताकत है!",
  "सरकार, आपकी बात हमारे लिए आखिरी फैसला है!",
  "बड़े भइया, आपका काम पहले, बाकी सब बाद में!",
]

secondary_messages = [
  "अरे भाई! बोलो क्या मदद चाहिए?",
  "बस बता दो क्या करना है, साथ हैं हम!",
  "चिंता मत करो… काम हो जाएगा!",
  "हम हैं ना, टेंशन काहे लेते हो?",
  "इतना फॉर्मल मत हो, सीधे बोलो!",
  "पिंग आया है मतलब कुछ जरूरी होगा, बताओ!",
  "चलो बताओ क्या सीन है?",
  "कहो भाई, क्या योजना है?"
]

tertiary_messages = [
  "गुरुजी प्रणाम, आदेश मिल गया!",
  "अरे भाई, आपकी बात मान ली गई है!",
  "जो आपने कहा वही सही!",
  "समझ गए गुरु, काम शुरू!",
  "भाई हो तुम, बात कैसे टालें!",
  "ठीक है, जैसा कहा वैसा होगा!",
  "आपकी बात नोट कर ली गई है!",
  "गुरु, आदेश स्वीकार है!"
]

random_messages = [
  "अरे भाई, इतना पिंग क्यों कर रहे हो?",
  "क्या हुआ? दुनिया खत्म हो गई क्या?",
  "शांत रहो मित्र, हम यहीं हैं!",
  "इतनी जल्दी क्या है?",
  "लगता है आज पिंग करने का रिकॉर्ड बनाना है!",
  "भाई थोड़ा आराम भी कर लो!",
  "पिंग मशीन बन गए हो क्या?",
  "काहे हल्ला मचा रहे हो?",
  "अरे भाई, सांस भी ले लो बीच में!",
  "लगता है ध्यान खींचने की पूरी कोशिश है!",
  "काहे बुला रहे हो बार-बार?",
  "लगता है हमें याद बहुत किया जा रहा है!",
  "ध्यान तुमको मिलेगा नहीं इतनी सरलता से।",
  "अरे बस, हम कोई रॉकेटवा नहीं हैं!",
  "लगता है आज तुम्हें बहुत याद आ रहे हैं हम!",
  "अरे भाई, लाइन में लगो… सबका नंबर आएगा!",
  "इतना शोर क्यों मचा रहे हो?",
  "लगता है पिंग करने का नया शौक लगा है!",
  "थोड़ा सब्र भी नाम की चीज होती है!",
  "लगता है हमें बुलाने का अभियान चल रहा है!",
  "इतनी मेहनत पढ़ाई में करते तो टॉपर होते!",
  "इतना पिंग… क्या हम VIP हैं? वो तो हम है ही।",
  "लगता है ध्यान खींचने का मास्टर प्लान है!",
  "लगता है आज पिंग दिवस मनाया जा रहा है!",
  "क्या है?",
  "तुम्हारा अकाउंट बर्बाद करने की ताकत है मुझमे",
  "इतना पिंग उसे कर देते तो आज वो तुम्हारी होती।",
  "डिस्कॉर्ड के अलावा और कोई काम नहीं है क्या?",
  "हमको अब समझ आता है की तुम्हारी मम्मी तुमको क्यों मारती है",
  "एक बार बोल दिया, समझ नहीं आता क्या?",
  "इतना पिंग करोगे तो जवाब और देर से मिलेगा।",
  "बार-बार पिंग करने से काम जल्दी नहीं होता।",
  "इतनी जल्दी है तो खुद ही कर लो काम।",
  "इतना शोर मचाने से कुछ खास नहीं मिलेगा।",
  "बार-बार बुलाने से इज्जत कम होती है।",
  "इतना पिंग देख के लगता है उँगली फँस गई है।",
  "इतना उतावला होना अच्छी आदत नहीं है।",
  "इतना पिंग करोगे तो लोग अनदेखा करना शुरू कर देंगे।",
  "इतना हल्ला करने से बात बड़ी नहीं हो जाती।",
  "इतना शोर करोगे तो कोई गंभीरता से नहीं लेगा।",
]

# ──────────────────────────────────────────────
# Config  (DO NOT CHANGE IDs)
# ──────────────────────────────────────────────

TOKEN                = os.environ.get("TOKEN")
GUILD_ID             = 1418520134590660700
LOG_CHANNEL_ID       = 1481259818529460286
OTHER_LOG_CHANNEL_ID = 1481259505089118268
ALLOWED_CHANNEL_ID   = 1438088796586639380
WELCOME_LOG          = 1481196949033062410
ADMIN_ROLE_ID        = 1425847758404849674

TIME_WINDOW         = 5
MESSAGE_THRESHOLD   = 4
DUPLICATE_THRESHOLD = 3
PING_THRESHOLD      = 5
CAPS_THRESHOLD      = 0.7

# Invite/blocked link automod
BLOCKED_WORDS = ["madarchod"]

# In-memory stores
warn_counts:             dict[int, int]   = {}
user_message_history:    dict[int, list]  = {}
user_duplicate_history:  dict[int, list]  = {}
active_surveys:          set[int]         = set()

ROLE_1_ID    = 123456789012345678
ROLE_2_ID    = 987654321098765432
ROLE_1_EMOJI = "✅"
ROLE_2_EMOJI = "🔵"

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ──────────────────────────────────────────────
# Survey questions  (DO NOT CHANGE)
# ──────────────────────────────────────────────

questions = [
    "What is your ideology?",
    "Do you support Hindi as a common communication network (not in terms of removing any language)?",
    "What are your opinions on RSS and other Sangh organizations?",
    "Opinions on communism?",
    "Opinions on modern history?",
    "Opinions on the current government and the opposition?",
    "Opinions on Savarkar?",
    "Opinions on LGBTQ+ and Feminism?",
    "Opinions on minorities?",
    "Opinions on Muslim Extremism?",
    "Opinions on the varna system and casteism (noting that these are different things).",
    "Opinions on modernization in terms of social activities i.e. Dating."
]

# ──────────────────────────────────────────────
# Embed Helpers
# ──────────────────────────────────────────────

def make_embed(title: str, description: str = "",
               color: disnake.Color = disnake.Color(0x5865F2),
               footer: str = "") -> disnake.Embed:
    e = disnake.Embed(title=title, description=description,
                      color=color, timestamp=datetime.utcnow())
    if footer:
        e.set_footer(text=footer)
    return e

def survey_embed(title, description, color=disnake.Color(0x5865F2)):
    return make_embed(title, description, color,
                      footer="Verification System • Reply in this DM")

def question_embed(question, current, total):
    bar = "█" * current + "░" * (total - current)
    e = disnake.Embed(
        title=f"📋 Question {current} of {total}",
        description=f"**{question}**",
        color=disnake.Color(0x5865F2),
        timestamp=datetime.utcnow()
    )
    e.add_field(name="Progress", value=f"`{bar}` {current}/{total}", inline=False)
    e.set_footer(text="Type your answer • 5 minutes per question • type 'skip' to skip")
    return e

def log_embed(title, user, responses):
    e = disnake.Embed(title=f"📝 {title}",
                      color=disnake.Color(0x57F287),
                      timestamp=datetime.utcnow())
    e.set_author(name=str(user), icon_url=user.display_avatar.url)
    e.set_thumbnail(url=user.display_avatar.url)
    for i, (q, a) in enumerate(responses, 1):
        truncated = a[:1000] + "…" if len(a) > 1000 else a
        e.add_field(name=f"Q{i}. {q[:200]}", value=f"> {truncated}", inline=False)
    e.set_footer(text=f"User ID: {user.id}")
    return e


# ══════════════════════════════════════════════
#  SURVEY
# ══════════════════════════════════════════════

@bot.slash_command(name="start_survey",
                   description="Start the verification survey.",
                   guild_ids=[GUILD_ID])
async def start_survey(interaction: ApplicationCommandInteraction):
    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message(
            embed=survey_embed("❌ Wrong Channel",
                               "This command can only be used in the verification channel.",
                               disnake.Color.red()), ephemeral=True)
        return

    user = interaction.author
    if user.id in active_surveys:
        await interaction.response.send_message(
            embed=survey_embed("⏳ Survey Already Active",
                               "You already have a survey in progress! Check your DMs.",
                               disnake.Color.orange()), ephemeral=True)
        return

    try:
        await user.send(embed=survey_embed(
            "👋 Welcome to the Verification Survey",
            f"Thanks for your interest!\n\nYou'll answer **{len(questions)} questions**.\n\n"
            "**Rules:**\n• 5 minutes per question\n• Answer honestly\n"
            "• Type `skip` to skip a question\n\nLet's go! 🚀"
        ))
    except disnake.Forbidden:
        await interaction.response.send_message(
            embed=survey_embed("❌ DMs Disabled",
                               "Please **enable DMs from server members** in your privacy settings.",
                               disnake.Color.red()), ephemeral=True)
        return

    await interaction.response.send_message(
        embed=survey_embed("✅ Survey Started", "Check your DMs!", disnake.Color.green()),
        ephemeral=True)
    active_surveys.add(user.id)
    asyncio.create_task(_run_survey(user))


async def _run_survey(user: disnake.User):
    responses = []
    check = lambda m: m.author == user and isinstance(m.channel, disnake.DMChannel)
    try:
        for i, question in enumerate(questions, 1):
            await user.send(embed=question_embed(question, i, len(questions)))
            try:
                msg = await bot.wait_for("message", check=check, timeout=300)
                answer = msg.content if msg.content.lower() != "skip" else "*Skipped*"
                responses.append((question, answer))
                ack = disnake.Embed(
                    description=f"✅ Recorded! {'Next question…' if i < len(questions) else 'That was the last one!'}",
                    color=disnake.Color(0x57F287))
                await user.send(embed=ack)
            except asyncio.TimeoutError:
                await user.send(embed=survey_embed(
                    "⏰ Timed Out",
                    f"Question {i} timed out. Survey cancelled.\nUse `/start_survey` to retry.",
                    disnake.Color.red()))
                return

        ch = bot.get_channel(LOG_CHANNEL_ID)
        if ch:
            guild = bot.get_guild(GUILD_ID)
            admin_role = disnake.utils.get(guild.roles, id=ADMIN_ROLE_ID) if guild else None
            role_mention = admin_role.mention if admin_role else ""
            await ch.send(content=role_mention, embed=log_embed(f"Survey — {user.display_name}", user, responses))
        await user.send(embed=survey_embed(
            "🎉 Survey Complete!",
            "Responses sent to admins.\n**Please be patient** — access will be granted soon. ✅",
            disnake.Color(0x57F287)))
    finally:
        active_surveys.discard(user.id)


# ══════════════════════════════════════════════
#  ADMIN COMMANDS
# ══════════════════════════════════════════════

@bot.slash_command(name="clear",
                   description="Delete up to 1000 messages.",
                   options=[disnake.Option("amount", "Messages to delete (1-1000)",
                                           disnake.OptionType.integer, True,
                                           min_value=1, max_value=1000)],
                   default_member_permissions=disnake.Permissions(manage_messages=True))
async def clear(inter: ApplicationCommandInteraction, amount: int):
    if not inter.channel.permissions_for(inter.guild.me).manage_messages:
        await inter.response.send_message("No permission.", ephemeral=True)
        return
    deleted = await inter.channel.purge(limit=amount)
    await inter.response.send_message(f"🗑️ Deleted **{len(deleted)}** messages.", ephemeral=True)


@bot.slash_command(name="admin_send",
                   description="Send a custom embed to a channel. (Admin)",
                   guild_ids=[GUILD_ID])
@commands.has_permissions(administrator=True)
async def admin_send(inter: ApplicationCommandInteraction,
                     channel: disnake.TextChannel, title: str,
                     description: str, color: str = "blue"):
    color_map = {
        "blue": disnake.Color.blue(), "green": disnake.Color.green(),
        "red": disnake.Color.red(),   "yellow": disnake.Color.yellow(),
        "orange": disnake.Color.orange(), "purple": disnake.Color.purple()
    }
    e = disnake.Embed(title=title, description=description,
                      color=color_map.get(color.lower(), disnake.Color.blue()),
                      timestamp=datetime.utcnow())
    await channel.send(embed=e)
    await inter.response.send_message(f"✅ Sent to {channel.mention}!", ephemeral=True)


@bot.slash_command(name="kick",
                   description="Kick a member. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(kick_members=True))
async def kick(inter: ApplicationCommandInteraction,
               member: disnake.Member,
               reason: str = "No reason provided"):
    if member.top_role >= inter.author.top_role:
        await inter.response.send_message("❌ Can't kick equal/higher role.", ephemeral=True)
        return
    try:
        await member.send(embed=make_embed("👢 You were kicked",
            f"**Server:** {inter.guild.name}\n**Reason:** {reason}", disnake.Color.orange()))
    except disnake.Forbidden:
        pass
    await member.kick(reason=reason)
    await inter.response.send_message(embed=make_embed(
        "👢 Member Kicked",
        f"{member.mention} kicked.\n**Reason:** {reason}", disnake.Color.orange()))
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        e = make_embed("👢 Member Kicked", color=disnake.Color.orange())
        e.add_field(name="User",      value=f"{member} ({member.id})", inline=True)
        e.add_field(name="Kicked By", value=inter.author.mention,      inline=True)
        e.add_field(name="Reason",    value=reason,                    inline=False)
        await ch.send(embed=e)


@bot.slash_command(name="ban",
                   description="Ban a member. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(ban_members=True))
async def ban(inter: ApplicationCommandInteraction,
              member: disnake.Member,
              reason: str = "No reason provided",
              delete_days: int = 0):
    if member.top_role >= inter.author.top_role:
        await inter.response.send_message("❌ Can't ban equal/higher role.", ephemeral=True)
        return
    try:
        await member.send(embed=make_embed("🔨 You were banned",
            f"**Server:** {inter.guild.name}\n**Reason:** {reason}", disnake.Color.red()))
    except disnake.Forbidden:
        pass
    await member.ban(reason=reason, delete_message_days=delete_days)
    await inter.response.send_message(embed=make_embed(
        "🔨 Member Banned",
        f"{member.mention} banned.\n**Reason:** {reason}", disnake.Color.red()))
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        e = make_embed("🔨 Member Banned", color=disnake.Color.red())
        e.add_field(name="User",     value=f"{member} ({member.id})", inline=True)
        e.add_field(name="Banned By", value=inter.author.mention,     inline=True)
        e.add_field(name="Reason",   value=reason,                    inline=False)
        await ch.send(embed=e)


@bot.slash_command(name="unban",
                   description="Unban a user by ID. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(ban_members=True))
async def unban(inter: ApplicationCommandInteraction,
                user_id: str, reason: str = "No reason provided"):
    try:
        user = await bot.fetch_user(int(user_id))
        await inter.guild.unban(user, reason=reason)
        await inter.response.send_message(embed=make_embed(
            "✅ User Unbanned", f"{user} has been unbanned.", disnake.Color.green()))
    except (ValueError, disnake.NotFound):
        await inter.response.send_message("❌ User not found or not banned.", ephemeral=True)


@bot.slash_command(name="timeout",
                   description="Timeout a member. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(moderate_members=True))
async def timeout_cmd(inter: ApplicationCommandInteraction,
                      member: disnake.Member,
                      minutes: int = 10,
                      reason: str = "No reason provided"):
    if member.top_role >= inter.author.top_role:
        await inter.response.send_message("❌ Can't timeout equal/higher role.", ephemeral=True)
        return
    until = datetime.utcnow() + timedelta(minutes=minutes)
    await member.timeout(until=until, reason=reason)
    await inter.response.send_message(embed=make_embed(
        "⏱️ Member Timed Out",
        f"{member.mention} timed out for **{minutes}min**.\n**Reason:** {reason}",
        disnake.Color.orange()))


@bot.slash_command(name="untimeout",
                   description="Remove a timeout. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(moderate_members=True))
async def untimeout(inter: ApplicationCommandInteraction, member: disnake.Member):
    await member.timeout(until=None)
    await inter.response.send_message(embed=make_embed(
        "✅ Timeout Removed", f"{member.mention}'s timeout removed.", disnake.Color.green()))


@bot.slash_command(name="warn",
                   description="Warn a member. 3 warnings = auto 1h timeout. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(manage_messages=True))
async def warn(inter: ApplicationCommandInteraction,
               member: disnake.Member,
               reason: str = "No reason provided"):
    warn_counts[member.id] = warn_counts.get(member.id, 0) + 1
    count = warn_counts[member.id]
    try:
        await member.send(embed=make_embed(
            "⚠️ You've been warned",
            f"**Server:** {inter.guild.name}\n**Reason:** {reason}\n**Total Warnings:** {count}",
            disnake.Color.yellow()))
    except disnake.Forbidden:
        pass
    await inter.response.send_message(embed=make_embed(
        "⚠️ Member Warned",
        f"{member.mention} warned. Total: **{count}**\n**Reason:** {reason}",
        disnake.Color.yellow()))
    if count >= 3:
        until = datetime.utcnow() + timedelta(hours=1)
        await member.timeout(until=until, reason="Auto-timeout: 3 warnings")
        await inter.channel.send(embed=make_embed(
            "🤖 Auto-Moderation",
            f"{member.mention} auto-timed out for 1h (3 warnings reached).",
            disnake.Color.red()))


@bot.slash_command(name="warnings",
                   description="Check warnings for a member.",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(manage_messages=True))
async def warnings(inter: ApplicationCommandInteraction, member: disnake.Member):
    count = warn_counts.get(member.id, 0)
    await inter.response.send_message(embed=make_embed(
        "⚠️ Warnings", f"{member.mention} has **{count}** warning(s).",
        disnake.Color.yellow()), ephemeral=True)


@bot.slash_command(name="clearwarnings",
                   description="Clear all warnings for a member. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(administrator=True))
async def clearwarnings(inter: ApplicationCommandInteraction, member: disnake.Member):
    warn_counts.pop(member.id, None)
    await inter.response.send_message(embed=make_embed(
        "✅ Warnings Cleared",
        f"All warnings removed for {member.mention}.", disnake.Color.green()))


@bot.slash_command(name="slowmode",
                   description="Set channel slowmode. 0 to disable. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(manage_channels=True))
async def slowmode(inter: ApplicationCommandInteraction, seconds: int = 0):
    await inter.channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await inter.response.send_message(embed=make_embed(
            "✅ Slowmode Disabled", "Slowmode turned off.", disnake.Color.green()))
    else:
        await inter.response.send_message(embed=make_embed(
            "🐢 Slowmode Enabled",
            f"Slowmode set to **{seconds}s** in {inter.channel.mention}.",
            disnake.Color.orange()))


@bot.slash_command(name="lock",
                   description="Lock a channel. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(manage_channels=True))
async def lock(inter: ApplicationCommandInteraction, reason: str = "No reason provided"):
    ow = inter.channel.overwrites_for(inter.guild.default_role)
    ow.send_messages = False
    await inter.channel.set_permissions(inter.guild.default_role, overwrite=ow)
    await inter.response.send_message(embed=make_embed(
        "🔒 Channel Locked",
        f"{inter.channel.mention} locked.\n**Reason:** {reason}", disnake.Color.red()))


@bot.slash_command(name="unlock",
                   description="Unlock a channel. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(manage_channels=True))
async def unlock(inter: ApplicationCommandInteraction):
    ow = inter.channel.overwrites_for(inter.guild.default_role)
    ow.send_messages = None
    await inter.channel.set_permissions(inter.guild.default_role, overwrite=ow)
    await inter.response.send_message(embed=make_embed(
        "🔓 Channel Unlocked", f"{inter.channel.mention} is now open.", disnake.Color.green()))


@bot.slash_command(name="announce",
                   description="Post an announcement embed. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(administrator=True))
async def announce(inter: ApplicationCommandInteraction,
                   channel: disnake.TextChannel,
                   title: str, message: str,
                   ping_everyone: bool = False):
    e = disnake.Embed(title=f"📣 {title}", description=message,
                      color=disnake.Color(0xFEE75C), timestamp=datetime.utcnow())
    e.set_footer(text=f"Announced by {inter.author}")
    await channel.send(content="@everyone" if ping_everyone else "", embed=e)
    await inter.response.send_message("✅ Announcement sent!", ephemeral=True)


@bot.slash_command(name="serverinfo",
                   description="Display server information.",
                   guild_ids=[GUILD_ID])
async def serverinfo(inter: ApplicationCommandInteraction):
    g = inter.guild
    e = disnake.Embed(title=f"ℹ️ {g.name}",
                      color=disnake.Color(0x5865F2), timestamp=datetime.utcnow())
    if g.icon:
        e.set_thumbnail(url=g.icon.url)
    e.add_field(name="Owner",   value=g.owner.mention if g.owner else "Unknown", inline=True)
    e.add_field(name="Members", value=str(g.member_count), inline=True)
    e.add_field(name="Channels", value=str(len(g.channels)), inline=True)
    e.add_field(name="Roles",   value=str(len(g.roles)), inline=True)
    e.add_field(name="Boosts",  value=str(g.premium_subscription_count), inline=True)
    e.add_field(name="Created", value=g.created_at.strftime("%d %b %Y"), inline=True)
    e.set_footer(text=f"Server ID: {g.id}")
    await inter.response.send_message(embed=e)


@bot.slash_command(name="userinfo",
                   description="Display info about a user.",
                   guild_ids=[GUILD_ID])
async def userinfo(inter: ApplicationCommandInteraction, member: disnake.Member = None):
    member = member or inter.author
    roles  = [r.mention for r in member.roles if r.name != "@everyone"]
    e = disnake.Embed(title=f"👤 {member}", color=member.color, timestamp=datetime.utcnow())
    e.set_thumbnail(url=member.display_avatar.url)
    e.add_field(name="ID",             value=str(member.id), inline=True)
    e.add_field(name="Nickname",       value=member.nick or "None", inline=True)
    e.add_field(name="Bot",            value="Yes" if member.bot else "No", inline=True)
    e.add_field(name="Joined Server",  value=member.joined_at.strftime("%d %b %Y") if member.joined_at else "Unknown", inline=True)
    e.add_field(name="Account Created", value=member.created_at.strftime("%d %b %Y"), inline=True)
    e.add_field(name="Warnings",       value=str(warn_counts.get(member.id, 0)), inline=True)
    e.add_field(name=f"Roles ({len(roles)})",
                value=", ".join(roles) if roles else "None", inline=False)
    await inter.response.send_message(embed=e)


@bot.slash_command(name="role",
                   description="Add or remove a role from a member. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(manage_roles=True))
async def role_cmd(inter: ApplicationCommandInteraction,
                   member: disnake.Member,
                   role: disnake.Role,
                   action: str = commands.Param(choices=["add", "remove"])):
    if role >= inter.guild.me.top_role:
        await inter.response.send_message("❌ I can't manage that role.", ephemeral=True)
        return
    if action == "add":
        await member.add_roles(role)
        await inter.response.send_message(embed=make_embed(
            "✅ Role Added", f"{role.mention} added to {member.mention}.", disnake.Color.green()))
    else:
        await member.remove_roles(role)
        await inter.response.send_message(embed=make_embed(
            "✅ Role Removed", f"{role.mention} removed from {member.mention}.", disnake.Color.orange()))


@bot.slash_command(name="purge_user",
                   description="Delete recent messages from a specific user. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(manage_messages=True))
async def purge_user(inter: ApplicationCommandInteraction,
                     member: disnake.Member, amount: int = 50):
    await inter.response.defer(ephemeral=True)
    deleted = await inter.channel.purge(limit=200, check=lambda m: m.author == member)
    await inter.edit_original_message(
        content=f"🗑️ Deleted **{len(deleted)}** messages from {member.mention}.")


# ══════════════════════════════════════════════
#  FUN COMMANDS
# ══════════════════════════════════════════════

@bot.slash_command(name="coinflip", description="Flip a coin!", guild_ids=[GUILD_ID])
async def coinflip(inter: ApplicationCommandInteraction):
    await inter.response.send_message(embed=make_embed(
        "🪙 Coin Flip", random.choice(["**Heads!**", "**Tails!**"]),
        disnake.Color(0xFEE75C)))


@bot.slash_command(name="roll",
                   description="Roll a dice. Default d6.",
                   guild_ids=[GUILD_ID])
async def roll(inter: ApplicationCommandInteraction, sides: int = 6):
    if sides < 2:
        await inter.response.send_message("❌ Minimum 2 sides.", ephemeral=True)
        return
    await inter.response.send_message(embed=make_embed(
        f"🎲 d{sides} Roll",
        f"{inter.author.mention} rolled **{random.randint(1, sides)}**!",
        disnake.Color(0x57F287)))


@bot.slash_command(name="8ball",
                   description="Ask the magic 8-ball.",
                   guild_ids=[GUILD_ID])
async def eightball(inter: ApplicationCommandInteraction, question: str):
    answers = [
        "✅ It is certain.", "✅ Without a doubt.", "✅ Yes, definitely!",
        "✅ You may rely on it.", "🔮 Ask again later.", "🔮 Cannot predict now.",
        "🔮 Concentrate and ask again.", "❌ Don't count on it.",
        "❌ My reply is no.", "❌ Very doubtful.",
        "✅ As I see it, yes.", "❌ Outlook not so good."
    ]
    e = make_embed("🎱 Magic 8-Ball", color=disnake.Color(0x5865F2))
    e.add_field(name="Question", value=question,                  inline=False)
    e.add_field(name="Answer",   value=random.choice(answers),    inline=False)
    await inter.response.send_message(embed=e)


@bot.slash_command(name="poll",
                   description="Create a quick yes/no poll.",
                   guild_ids=[GUILD_ID])
async def poll(inter: ApplicationCommandInteraction, question: str):
    e = make_embed("📊 Poll", f"**{question}**", disnake.Color(0x5865F2),
                   footer=f"Poll by {inter.author}")
    await inter.response.send_message(embed=e)
    msg = await inter.original_message()
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("🤷")


@bot.slash_command(name="avatar",
                   description="Get someone's avatar.",
                   guild_ids=[GUILD_ID])
async def avatar(inter: ApplicationCommandInteraction, member: disnake.Member = None):
    member = member or inter.author
    e = disnake.Embed(title=f"🖼️ {member}'s Avatar",
                      color=member.color, timestamp=datetime.utcnow())
    e.set_image(url=member.display_avatar.url)
    await inter.response.send_message(embed=e)


@bot.slash_command(name="say",
                   description="Make the bot say something. (Admin)",
                   guild_ids=[GUILD_ID],
                   default_member_permissions=disnake.Permissions(manage_messages=True))
async def say(inter: ApplicationCommandInteraction,
              message: str,
              channel: disnake.TextChannel = None):
    target = channel or inter.channel
    await target.send(message)
    await inter.response.send_message("✅ Sent!", ephemeral=True)


# ══════════════════════════════════════════════
#  EVENTS
# ══════════════════════════════════════════════

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    ch = bot.get_channel(WELCOME_LOG)
    if ch:
        e = disnake.Embed(title="📥 Member Joined",
                          description=f"{member.mention} joined!",
                          color=disnake.Color.green(), timestamp=datetime.utcnow())
        e.set_thumbnail(url=member.display_avatar.url)
        e.set_footer(text=f"ID: {member.id}")
        await ch.send(embed=e)

@bot.event
async def on_member_remove(member):
    ch = bot.get_channel(WELCOME_LOG)
    if ch:
        e = disnake.Embed(title="📤 Member Left",
                          description=f"**{member}** left.",
                          color=disnake.Color.red(), timestamp=datetime.utcnow())
        e.set_thumbnail(url=member.display_avatar.url)
        e.set_footer(text=f"ID: {member.id}")
        await ch.send(embed=e)

@bot.event
async def on_message_delete(message):
    if message.author.bot: return
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        e = make_embed("🗑️ Message Deleted", color=disnake.Color.orange())
        e.add_field(name="User",    value=message.author.mention,          inline=True)
        e.add_field(name="Channel", value=message.channel.mention,         inline=True)
        e.add_field(name="Content", value=message.content[:1000] or "[No Content]", inline=False)
        await ch.send(embed=e)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot or before.content == after.content: return
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        e = make_embed("✏️ Message Edited", color=disnake.Color.yellow())
        e.add_field(name="User",    value=before.author.mention,        inline=True)
        e.add_field(name="Channel", value=before.channel.mention,       inline=True)
        e.add_field(name="Before",  value=before.content[:500] or "[No Content]", inline=False)
        e.add_field(name="After",   value=after.content[:500]  or "[No Content]", inline=False)
        await ch.send(embed=e)

@bot.event
async def on_guild_channel_create(channel):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        async for entry in channel.guild.audit_logs(action=disnake.AuditLogAction.channel_create, limit=1):
            e = make_embed("➕ Channel Created", color=disnake.Color.green())
            e.add_field(name="Channel", value=channel.name,      inline=True)
            e.add_field(name="By",      value=entry.user.mention, inline=True)
            await ch.send(embed=e)

@bot.event
async def on_guild_channel_delete(channel):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        async for entry in channel.guild.audit_logs(action=disnake.AuditLogAction.channel_delete, limit=1):
            e = make_embed("➖ Channel Deleted", color=disnake.Color.red())
            e.add_field(name="Channel", value=channel.name,      inline=True)
            e.add_field(name="By",      value=entry.user.mention, inline=True)
            await ch.send(embed=e)

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel: return
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        e = make_embed("🔊 Voice Update", color=disnake.Color.purple())
        e.add_field(name="User", value=member.mention, inline=True)
        if before.channel: e.add_field(name="Left",   value=before.channel.name, inline=True)
        if after.channel:  e.add_field(name="Joined", value=after.channel.name,  inline=True)
        await ch.send(embed=e)

@bot.event
async def on_member_ban(guild, user):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        await ch.send(embed=make_embed("🔨 User Banned",
            f"{user.mention} (`{user.id}`) banned.", disnake.Color.red()))

@bot.event
async def on_member_unban(guild, user):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        await ch.send(embed=make_embed("✅ User Unbanned",
            f"{user.mention} (`{user.id}`) unbanned.", disnake.Color.green()))

@bot.event
async def on_member_update(before, after):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if not ch: return

    if before.nick != after.nick:
        e = make_embed("📝 Nickname Changed", color=disnake.Color.blue())
        e.add_field(name="User",   value=after.mention,             inline=False)
        e.add_field(name="Before", value=before.nick or before.name, inline=True)
        e.add_field(name="After",  value=after.nick  or after.name,  inline=True)
        await ch.send(embed=e)

    if before.roles != after.roles:
        added   = [r for r in after.roles  if r not in before.roles]
        removed = [r for r in before.roles if r not in after.roles]
        e = make_embed("🎭 Role Update", color=disnake.Color.blurple())
        e.add_field(name="User", value=after.mention, inline=False)
        if added:   e.add_field(name="✅ Added",   value=", ".join(r.mention for r in added),   inline=False)
        if removed: e.add_field(name="❌ Removed", value=", ".join(r.mention for r in removed), inline=False)
        await ch.send(embed=e)

    if before.timed_out_until != after.timed_out_until:
        e = make_embed("⏱️ Timeout Update", color=disnake.Color.red())
        e.add_field(name="User",  value=after.mention, inline=True)
        e.add_field(name="Until", value=str(after.timed_out_until) if after.timed_out_until else "Removed", inline=True)
        await ch.send(embed=e)

    if before.premium_since != after.premium_since:
        e = make_embed("💎 Boost Update", color=disnake.Color(0xFF73FA))
        e.add_field(name="User",   value=after.mention, inline=True)
        e.add_field(name="Status", value="Boosting 🚀" if after.premium_since else "Stopped", inline=True)
        await ch.send(embed=e)

@bot.event
async def on_guild_role_create(role):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        async for entry in role.guild.audit_logs(action=disnake.AuditLogAction.role_create, limit=1):
            e = make_embed("➕ Role Created", color=disnake.Color.green())
            e.add_field(name="Role", value=role.mention,       inline=True)
            e.add_field(name="By",   value=entry.user.mention, inline=True)
            await ch.send(embed=e)

@bot.event
async def on_guild_role_delete(role):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        async for entry in role.guild.audit_logs(action=disnake.AuditLogAction.role_delete, limit=1):
            e = make_embed("➖ Role Deleted", color=disnake.Color.red())
            e.add_field(name="Role", value=role.name,          inline=True)
            e.add_field(name="By",   value=entry.user.mention, inline=True)
            await ch.send(embed=e)

@bot.event
async def on_guild_role_update(before, after):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        async for entry in after.guild.audit_logs(action=disnake.AuditLogAction.role_update, limit=1):
            e = make_embed("✏️ Role Updated", color=disnake.Color.orange())
            e.add_field(name="Before", value=before.name,         inline=True)
            e.add_field(name="After",  value=after.name,          inline=True)
            e.add_field(name="By",     value=entry.user.mention,  inline=False)
            await ch.send(embed=e)

@bot.event
async def on_invite_create(invite):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        async for entry in invite.guild.audit_logs(action=disnake.AuditLogAction.invite_create, limit=1):
            e = make_embed("🔗 Invite Created", color=disnake.Color.green())
            e.add_field(name="URL", value=invite.url,          inline=False)
            e.add_field(name="By",  value=entry.user.mention,  inline=False)
            await ch.send(embed=e)

@bot.event
async def on_invite_delete(invite):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        async for entry in invite.guild.audit_logs(action=disnake.AuditLogAction.invite_delete, limit=1):
            e = make_embed("🔗 Invite Deleted", color=disnake.Color.red())
            e.add_field(name="Code", value=invite.code,        inline=False)
            e.add_field(name="By",   value=entry.user.mention, inline=False)
            await ch.send(embed=e)

@bot.event
async def on_automod_action(action):
    ch = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    if ch:
        e = make_embed("🛡️ AutoMod Action", color=disnake.Color.red())
        e.add_field(name="User",    value=action.user.mention,          inline=True)
        e.add_field(name="Rule",    value=str(action.rule_triggered),   inline=True)
        e.add_field(name="Blocked", value=action.content or "[None]",   inline=False)
        await ch.send(embed=e)


# ══════════════════════════════════════════════
#  MESSAGE HANDLER  (Anti-spam + Automod)
# ══════════════════════════════════════════════

@bot.event
async def on_message(message):

    # ── Mention replies ──
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        print(f"[DEBUG] Bot mentioned by {message.author.id}")
        if message.author.id == SPECIAL_USER_ID:
            await message.channel.send(random.choice(special_messages))
        elif message.author.id == SECONDARY_SPECIAL_USER_ID:
            await message.channel.send(random.choice(secondary_messages))
        elif message.author.id == TERTIARY_SPECIAL_USER_ID:
            await message.channel.send(random.choice(tertiary_messages))
        else:
            await message.channel.send(random.choice(random_messages))

    if message.author.bot:
        return

    # ── Skip all checks for DMs ──
    if not message.guild:
        await bot.process_commands(message)
        return

    user_id      = message.author.id
    current_time = time.time()
    log_ch       = bot.get_channel(OTHER_LOG_CHANNEL_ID)
    admin_role   = disnake.utils.get(message.guild.roles, id=ADMIN_ROLE_ID)

    async def alert(title, fields: dict, color=disnake.Color.red(), delete=False):
        if log_ch and admin_role:
            e = make_embed(title, color=color)
            e.add_field(name="User",    value=message.author.mention,  inline=True)
            e.add_field(name="Channel", value=message.channel.mention, inline=True)
            for k, v in fields.items():
                e.add_field(name=k, value=str(v)[:500], inline=False)
            await log_ch.send(f"{admin_role.mention}", embed=e)
        if delete:
            try:
                await message.delete()
            except disnake.NotFound:
                pass

    # ── Blocked words / invite links ──
    content_lower = message.content.lower()
    for word in BLOCKED_WORDS:
        if word in content_lower:
            await alert("🚫 Blocked Content",
                        {"Content": message.content, "Trigger": f"`{word}`"},
                        delete=True)
            try:
                await message.author.send(embed=make_embed(
                    "🚫 Message Removed",
                    f"Your message in **{message.guild.name}** was removed (blocked content).",
                    disnake.Color.red()))
            except disnake.Forbidden:
                pass
            return

    # ── Rate limiting ──
    user_message_history.setdefault(user_id, [])
    user_message_history[user_id].append(current_time)
    user_message_history[user_id] = [
        t for t in user_message_history[user_id] if t > current_time - TIME_WINDOW
    ]
    if len(user_message_history[user_id]) > MESSAGE_THRESHOLD:
        await alert("🚨 Spam Detected",
                    {"Messages in window": len(user_message_history[user_id]),
                     "Content": message.content},
                    delete=True)
        user_message_history.pop(user_id, None)   # safe pop — fixes KeyError
        return

    # ── Duplicate messages ──
    user_duplicate_history.setdefault(user_id, [])
    user_duplicate_history[user_id].append(message.content)
    if len(user_duplicate_history[user_id]) > DUPLICATE_THRESHOLD:
        if len(set(user_duplicate_history[user_id][-DUPLICATE_THRESHOLD:])) == 1:
            await alert("🔁 Duplicate Spam",
                        {"Content": message.content},
                        delete=True)
            user_duplicate_history.pop(user_id, None)
            return

    # ── Mass pings ──
    if "@everyone" in message.content or "@here" in message.content:
        await alert("📢 Mass Ping", {"Content": message.content}, disnake.Color.orange())

    if len(message.mentions) > PING_THRESHOLD:
        await alert("🔔 Excessive User Pings",
                    {"Count": len(message.mentions), "Content": message.content},
                    disnake.Color.orange())

    # ── Excessive caps ──
    if message.content:
        caps_pct = sum(1 for c in message.content if c.isupper()) / len(message.content)
        if caps_pct > CAPS_THRESHOLD and len(message.content) > 10:
            await alert("🔠 Excessive Caps",
                        {"Caps %": f"{caps_pct:.0%}", "Content": message.content},
                        disnake.Color.orange())

    # ── Emoji spam (>10 unicode emoji) ──
    import unicodedata
    emoji_count = sum(1 for c in message.content
                      if unicodedata.category(c) in ("So", "Sm") or
                         "\U0001F300" <= c <= "\U0001FAFF")
    if emoji_count > 10:
        await alert("😵 Emoji Spam",
                    {"Count": emoji_count, "Content": message.content},
                    disnake.Color.orange())

    await bot.process_commands(message)


webserver.keep_alive()
bot.run(TOKEN)