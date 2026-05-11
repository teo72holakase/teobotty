"""
Info Cog
Commands: userinfo, serverinfo
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import datetime


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="ℹ️ Muestra información del usuario")
    @app_commands.describe(user="Usuario (opcional)")
    async def userinfo(self, interaction: discord.Interaction, user: Optional[discord.User] = None):
        """Show user information"""
        user = user or interaction.user

        # Try to get member info if in guild
        member = None
        if interaction.guild:
            try:
                member = await interaction.guild.fetch_member(user.id)
            except:
                member = None

        embed = discord.Embed(
            title=f"Información de {user.display_name}",
            color=user.color if user.color != discord.Color.default() else discord.Color.blue()
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        embed.add_field(name="Nombre", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Bot", value="Sí" if user.bot else "No", inline=True)

        if member:
            embed.add_field(name="Apodo", value=member.nick or "Ninguno", inline=True)
            embed.add_field(name="Se unió", value=member.joined_at.strftime("%d/%m/%Y %H:%M") if member.joined_at else "Desconocido", inline=True)
            embed.add_field(name="Cuenta creada", value=user.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)

            # Roles
            roles = [role.mention for role in member.roles[1:]]  # Exclude @everyone
            if roles:
                embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles[:10]), inline=False)
                if len(roles) > 10:
                    embed.set_footer(text=f"Y {len(roles) - 10} roles más...")
            else:
                embed.add_field(name="Roles", value="Ninguno", inline=False)
        else:
            embed.add_field(name="Cuenta creada", value=user.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="serverinfo", description="ℹ️ Muestra información del servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        """Show server information"""
        guild = interaction.guild

        embed = discord.Embed(
            title=f"Información de {guild.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Dueño", value=guild.owner.mention if guild.owner else "Desconocido", inline=True)
        embed.add_field(name="Creado", value=guild.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)

        embed.add_field(name="Miembros", value=guild.member_count, inline=True)
        embed.add_field(name="Canales", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)

        # Channel counts
        text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
        voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
        categories = len([c for c in guild.channels if isinstance(c, discord.CategoryChannel)])

        embed.add_field(name="Canales de texto", value=text_channels, inline=True)
        embed.add_field(name="Canales de voz", value=voice_channels, inline=True)
        embed.add_field(name="Categorías", value=categories, inline=True)

        # Boost info
        embed.add_field(name="Nivel de boost", value=guild.premium_tier, inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)

        # Features
        features = [f.replace('_', ' ').title() for f in guild.features]
        if features:
            embed.add_field(name="Características", value=", ".join(features[:5]), inline=False)
            if len(features) > 5:
                embed.set_footer(text=f"Y {len(features) - 5} características más...")

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))