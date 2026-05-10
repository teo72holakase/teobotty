"""
Roles Cog
Commands: add_autorole, remove_autorole, add_reaction_role, remove_reaction_role
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        from main import db
        self.db = db

    @app_commands.command(
        name="add_autorole",
        description="⭐ Añade un rol que se asigna automáticamente al unirse"
    )
    @app_commands.describe(role="Rol a asignar automáticamente")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_autorole(self, interaction: discord.Interaction, role: discord.Role):
        """Add an autorole"""
        try:
            await self.db.add_autorole(interaction.guild.id, role.id)
            
            embed = discord.Embed(
                title="✅ Autorole Agregado",
                description=f"El rol {role.mention} se asignará automáticamente a nuevos miembros",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="remove_autorole",
        description="❌ Elimina un autorole"
    )
    @app_commands.describe(role="Rol a eliminar")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_autorole(self, interaction: discord.Interaction, role: discord.Role):
        """Remove an autorole"""
        try:
            await self.db.remove_autorole(interaction.guild.id, role.id)
            
            embed = discord.Embed(
                title="✅ Autorole Eliminado",
                description=f"El rol {role.mention} ya no se asignará automáticamente",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="list_autoroles",
        description="📋 Muestra todos los autoroles del servidor"
    )
    async def list_autoroles(self, interaction: discord.Interaction):
        """List all autoroles"""
        try:
            autoroles = await self.db.get_autoroles(interaction.guild.id)
            
            if not autoroles:
                await interaction.response.send_message("❌ No hay autoroles configurados", ephemeral=True)
                return
            
            roles_text = "\n".join([
                f"• <@&{role_id}>" for role_id in autoroles
            ])
            
            embed = discord.Embed(
                title="📋 Autoroles",
                description=roles_text,
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="add_reaction_role",
        description="🎯 Crea un rol que se asigna al reaccionar"
    )
    @app_commands.describe(
        message_id="ID del mensaje",
        emoji="Emoji de reacción",
        role="Rol a asignar"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_reaction_role(
        self,
        interaction: discord.Interaction,
        message_id: str,
        emoji: str,
        role: discord.Role
    ):
        """Add a reaction role"""
        try:
            msg_id = int(message_id)
            
            # Validate emoji is a single emoji
            if len(emoji) > 10:
                await interaction.response.send_message("❌ El emoji es demasiado largo", ephemeral=True)
                return
            
            await self.db.add_reaction_role(
                interaction.guild.id,
                msg_id,
                interaction.channel.id,
                emoji,
                role.id
            )
            
            embed = discord.Embed(
                title="✅ Reaction Role Agregado",
                description=f"Reacción: {emoji}\nRol: {role.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ ID de mensaje inválido", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="remove_reaction_role",
        description="❌ Elimina un reaction role"
    )
    @app_commands.describe(
        message_id="ID del mensaje",
        emoji="Emoji de reacción"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_reaction_role(
        self,
        interaction: discord.Interaction,
        message_id: str,
        emoji: str
    ):
        """Remove a reaction role"""
        try:
            msg_id = int(message_id)
            await self.db.remove_reaction_role(msg_id, emoji)
            
            embed = discord.Embed(
                title="✅ Reaction Role Eliminado",
                description=f"Reacción: {emoji}",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ ID de mensaje inválido", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))
