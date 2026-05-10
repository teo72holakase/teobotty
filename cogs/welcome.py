"""
Welcome Cog
Commands: set_welcome, set_farewell
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Import database from main module
        from main import db
        self.db = db

    @app_commands.command(
        name="set_welcome",
        description="🎉 Configura el mensaje de bienvenida"
    )
    @app_commands.describe(
        channel="Canal donde enviar el mensaje",
        message="Mensaje personalizado (usa {user}, {username}, {guild})"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message: str
    ):
        """Set welcome message and channel"""
        try:
            await self.db.set_welcome_config(interaction.guild.id, channel.id, message)
            
            embed = discord.Embed(
                title="✅ Bienvenida Configurada",
                description=f"Canal: {channel.mention}\nMensaje: {message}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="set_farewell",
        description="👋 Configura el mensaje de despedida"
    )
    @app_commands.describe(
        channel="Canal donde enviar el mensaje",
        message="Mensaje personalizado (usa {user}, {username}, {guild})"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_farewell(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message: str
    ):
        """Set farewell message and channel"""
        try:
            await self.db.set_farewell_config(interaction.guild.id, channel.id, message)
            
            embed = discord.Embed(
                title="✅ Despedida Configurada",
                description=f"Canal: {channel.mention}\nMensaje: {message}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="test_welcome",
        description="🧪 Prueba el mensaje de bienvenida"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def test_welcome(self, interaction: discord.Interaction):
        """Test welcome message"""
        try:
            welcome_config = await self.db.get_welcome_config(interaction.guild.id)
            
            if not welcome_config:
                await interaction.response.send_message("❌ No hay mensaje de bienvenida configurado", ephemeral=True)
                return
            
            channel_id, message = welcome_config
            channel = interaction.guild.get_channel(channel_id)
            
            if not channel:
                await interaction.response.send_message("❌ Canal no encontrado", ephemeral=True)
                return
            
            test_message = message.format(
                user=interaction.user.mention,
                username=interaction.user.name,
                guild=interaction.guild.name
            )
            
            await channel.send(test_message)
            await interaction.response.send_message(f"✅ Mensaje enviado a {channel.mention}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
