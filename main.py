"""
TeoBotty - Discord Bot
Main file with bot initialization and Cogs loader
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from database import Database
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./bot_data.db")

if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN not found in .env file!")

# Initialize bot with TeoBotty name
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.guilds = True

bot = commands.Bot(command_prefix=None, intents=intents)
db = Database(DATABASE_PATH)


@bot.event
async def on_ready():
    """Called when bot is ready"""
    logger.info(f"✅ Bot logged in as {bot.user}")

    # Sync commands per guild for immediate availability
    total_synced = 0
    for guild in bot.guilds:
        try:
            synced = await bot.tree.sync(guild=discord.Object(id=guild.id))
            total_synced += len(synced)
            logger.info(f"✅ Synced {len(synced)} commands for guild {guild.name} ({guild.id})")
        except Exception as e:
            logger.error(f"❌ Error syncing guild {guild.id}: {e}")

    # Also attempt a global sync (will be eventual)
    try:
        global_synced = await bot.tree.sync()
        logger.info(f"✅ Globally synced {len(global_synced)} commands")
    except Exception as e:
        logger.error(f"❌ Error global syncing: {e}")

    # Set presence
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="JoJos Bizarre Adventure 👑")
    )
    logger.info("✅ Status set to: Watching JoJos Bizarre Adventure")


@bot.event
async def on_member_join(member: discord.Member):
    """Called when a member joins the guild"""
    guild_id = member.guild.id
    
    # Send welcome message
    welcome_config = await db.get_welcome_config(guild_id)
    if welcome_config:
        channel_id, message = welcome_config
        channel = member.guild.get_channel(channel_id)
        if channel:
            welcome_message = message.format(
                user=member.mention,
                username=member.name,
                guild=member.guild.name
            )
            try:
                await channel.send(welcome_message)
            except Exception as e:
                logger.error(f"Error sending welcome message: {e}")
    
    # Apply autoroles
    autoroles = await db.get_autoroles(guild_id)
    for role_id in autoroles:
        role = member.guild.get_role(role_id)
        if role:
            try:
                await member.add_roles(role)
                logger.info(f"Added autorole {role.name} to {member.name}")
            except Exception as e:
                logger.error(f"Error adding autorole: {e}")


@bot.event
async def on_member_remove(member: discord.Member):
    """Called when a member leaves the guild"""
    guild_id = member.guild.id
    
    # Send farewell message
    farewell_config = await db.get_farewell_config(guild_id)
    if farewell_config:
        channel_id, message = farewell_config
        channel = member.guild.get_channel(channel_id)
        if channel:
            farewell_message = message.format(
                user=member.mention,
                username=member.name,
                guild=member.guild.name
            )
            try:
                await channel.send(farewell_message)
            except Exception as e:
                logger.error(f"Error sending farewell message: {e}")


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """Called when a reaction is added"""
    if payload.user_id == bot.user.id:
        return
    
    emoji = str(payload.emoji)
    reaction_role = await db.get_reaction_role(payload.message_id, emoji)
    
    if reaction_role:
        guild_id, channel_id, role_id = reaction_role
        guild = bot.get_guild(guild_id)
        if guild:
            member = guild.get_member(payload.user_id)
            role = guild.get_role(role_id)
            if member and role:
                try:
                    await member.add_roles(role)
                    logger.info(f"Added reaction role {role.name} to {member.name}")
                except Exception as e:
                    logger.error(f"Error adding reaction role: {e}")


@bot.event
async def on_message(message: discord.Message):
    """Called when a message is sent"""
    if message.author.bot:
        return
    
    # Check for triggers
    guild_id = message.guild.id if message.guild else None
    if guild_id:
        triggers = await db.get_all_triggers(guild_id)
        for keyword, response in triggers:
            if keyword.lower() in message.content.lower():
                response_text = response.format(
                    user=message.author.mention,
                    username=message.author.name,
                    message=message.content
                )
                try:
                    await message.reply(response_text, mention_author=False)
                except Exception as e:
                    logger.error(f"Error sending trigger response: {e}")
                break
    
    await bot.process_commands(message)


async def load_cogs():
    """Load all cogs from the cogs folder"""
    cogs_folder = "cogs"
    for filename in os.listdir(cogs_folder):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                logger.info(f"✅ Loaded cog: {cog_name}")
            except Exception as e:
                logger.error(f"❌ Failed to load cog {cog_name}: {e}")


async def main():
    """Main function"""
    await db.initialize()
    logger.info("✅ Database initialized")
    
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
