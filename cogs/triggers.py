"""
Triggers Cog
Commands: add_trigger, remove_trigger, list_triggers
Sistema de respuestas automáticas por palabras clave
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional


class Triggers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        from main import db
        self.db = db

    async def trigger_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete for trigger keywords"""
        try:
            triggers = await self.db.get_all_triggers(interaction.guild.id)
            keywords = [trigger[0] for trigger in triggers]
            
            # Filter based on current input
            filtered = [k for k in keywords if current.lower() in k.lower()][:25]
            return [app_commands.Choice(name=k, value=k) for k in filtered]
        except:
            return []

    @app_commands.command(
        name="add_trigger",
        description="🔔 Añade una respuesta automática para una palabra clave"
    )
    @app_commands.describe(
        keyword="Palabra clave a detectar",
        response="Respuesta automática (usa {user}, {username}, {message})"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def add_trigger(
        self,
        interaction: discord.Interaction,
        keyword: str,
        response: str
    ):
        """Add a trigger command"""
        try:
            keyword_lower = keyword.lower()
            await self.db.add_trigger(interaction.guild.id, keyword_lower, response)
            
            embed = discord.Embed(
                title="✅ Trigger Agregado",
                description=f"Palabra clave: **{keyword}**\nRespuesta: {response}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="remove_trigger",
        description="❌ Elimina un trigger"
    )
    @app_commands.describe(keyword="Palabra clave a eliminar")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.autocomplete(keyword=trigger_autocomplete)
    async def remove_trigger(self, interaction: discord.Interaction, keyword: str):
        """Remove a trigger command"""
        try:
            keyword_lower = keyword.lower()
            await self.db.remove_trigger(interaction.guild.id, keyword_lower)
            
            embed = discord.Embed(
                title="✅ Trigger Eliminado",
                description=f"Palabra clave: **{keyword}**",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="list_triggers",
        description="📋 Muestra todos los triggers del servidor"
    )
    async def list_triggers(self, interaction: discord.Interaction):
        """List all triggers for the guild"""
        try:
            triggers = await self.db.get_all_triggers(interaction.guild.id)
            
            if not triggers:
                await interaction.response.send_message("❌ No hay triggers configurados", ephemeral=True)
                return
            
            trigger_list = []
            for keyword, response in triggers:
                trigger_list.append(f"**{keyword}** → {response}")
            
            # Split into multiple messages if too long
            description = "\n".join(trigger_list)
            
            if len(description) > 4000:
                chunks = [description[i:i+4000] for i in range(0, len(description), 4000)]
                for i, chunk in enumerate(chunks):
                    embed = discord.Embed(
                        title=f"📋 Triggers (Parte {i+1})",
                        description=chunk,
                        color=discord.Color.blue()
                    )
                    if i == 0:
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="📋 Triggers",
                    description=description,
                    color=discord.Color.blue()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Triggers(bot))
