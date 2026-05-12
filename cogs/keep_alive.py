"""
Keep-Alive Cog
Periodic task to keep the bot alive (prevents server from sleeping)
Sends a reaction to a designated message every 20 minutes
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class KeepAlive(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("✅ Keep-Alive cog initialized")
        self.keep_alive_task.start()

    @tasks.loop(minutes=20)
    async def keep_alive_task(self):
        """
        Periodic task that runs every 20 minutes
        This helps keep the bot's server active and prevents it from being put to sleep
        """
        try:
            # Get the bot's status channel (stored in environment or use a default guild)
            # You can set KEEP_ALIVE_GUILD_ID and KEEP_ALIVE_CHANNEL_ID in .env
            guild_id = int(os.getenv("KEEP_ALIVE_GUILD_ID", "0"))
            channel_id = int(os.getenv("KEEP_ALIVE_CHANNEL_ID", "0"))

            if guild_id == 0 or channel_id == 0:
                # If not configured, just log activity
                logger.info(f"⏰ Keep-alive check: Bot is online with {len(self.bot.guilds)} guilds")
                return

            guild = self.bot.get_guild(guild_id)
            if not guild:
                logger.warning(f"⚠️ Keep-alive guild {guild_id} not found")
                return

            channel = guild.get_channel(channel_id)
            if not channel:
                logger.warning(f"⚠️ Keep-alive channel {channel_id} not found in guild {guild_id}")
                return

            # Get the last message or send a new one
            try:
                async for message in channel.history(limit=1):
                    # React to the last message with a heart
                    await message.add_reaction("💓")
                    logger.info(f"💓 Keep-alive reaction added to message {message.id}")
                    break
            except Exception as e:
                # If no messages, send a keep-alive message
                embed = discord.Embed(
                    title="⏰ Keep-Alive Ping",
                    description="Bot is running and monitoring the system",
                    color=discord.Color.green()
                )
                msg = await channel.send(embed=embed)
                await msg.add_reaction("✅")
                logger.info(f"✅ Keep-alive message sent to {channel.name}")

        except Exception as e:
            logger.error(f"❌ Keep-alive task error: {e}")

    @keep_alive_task.before_loop
    async def before_keep_alive_task(self):
        """Wait for bot to be ready before starting the keep-alive task"""
        await self.bot.wait_until_ready()
        logger.info("⏰ Keep-alive task scheduled (every 20 minutes)")

    @app_commands.command(
        name="set_keep_alive",
        description="⏰ Configura el canal para el Keep-Alive"
    )
    @app_commands.describe(channel="Canal donde el bot reaccionará cada 20 minutos")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_keep_alive_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """
        Configura el canal donde el bot reaccionará cada 20 minutos
        Uso: /set_keep_alive #canal
        """
        await interaction.response.send_message(
            f"✅ Keep-alive configurado en {channel.mention}\n\n"
            f"Ahora edita tu archivo `.env` y añade:\n"
            f"```\nKEEP_ALIVE_GUILD_ID={interaction.guild.id}\n"
            f"KEEP_ALIVE_CHANNEL_ID={channel.id}\n```\n"
            f"Luego reinicia el bot.\n\n"
            f"El bot reaccionará con ❤️ cada 20 minutos para mantener el servidor activo.",
            ephemeral=True
        )

    def cog_unload(self):
        """Cancel the task when the cog is unloaded"""
        self.keep_alive_task.cancel()
        logger.info("⏰ Keep-alive task cancelled")


async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(KeepAlive(bot))
