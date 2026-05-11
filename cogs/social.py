"""
Social Cog
Commands: set_suggestions, unset_suggestions, create_poll
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, List


class Social(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        from main import db
        self.db = db

    @app_commands.command(
        name="set_suggestions",
        description="📥 Configura un canal de sugerencias"
    )
    @app_commands.describe(channel="Canal donde se recibirán sugerencias")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_suggestions(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel
    ):
        try:
            await self.db.set_suggestions_channel(interaction.guild.id, channel.id)

            embed = discord.Embed(
                title="✅ Canal de sugerencias configurado",
                description=f"Las sugerencias ahora se recibirán en {channel.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="unset_suggestions",
        description="❌ Quita el canal de sugerencias"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def unset_suggestions(self, interaction: discord.Interaction):
        try:
            await self.db.remove_suggestions_channel(interaction.guild.id)

            embed = discord.Embed(
                title="✅ Canal de sugerencias eliminado",
                description="Ya no hay canal configurado para sugerencias",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="create_poll",
        description="🗳️ Crea una votación con varias opciones"
    )
    @app_commands.describe(
        question="Pregunta de la votación",
        options="Opciones separadas por ; (por ejemplo: Sí;No;Tal vez)",
        everyone="Mencionar @everyone en el mensaje de la votación",
        image1="Imagen opcional 1",
        image2="Imagen opcional 2",
        image3="Imagen opcional 3"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def create_poll(
        self,
        interaction: discord.Interaction,
        question: str,
        options: str,
        everyone: Optional[bool] = False,
        image1: Optional[discord.Attachment] = None,
        image2: Optional[discord.Attachment] = None,
        image3: Optional[discord.Attachment] = None
    ):
        try:
            choices = [choice.strip() for choice in options.split(";") if choice.strip()]
            if len(choices) < 2:
                await interaction.response.send_message(
                    "❌ Debes enviar al menos 2 opciones separadas con `;`",
                    ephemeral=True
                )
                return

            if len(choices) > 9:
                await interaction.response.send_message(
                    "❌ El número máximo de opciones es 9",
                    ephemeral=True
                )
                return

            emoji_options = [
                "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"
            ]
            embed = discord.Embed(
                title="🗳️ Nueva votación",
                description=f"**{question}**",
                color=discord.Color.blurple()
            )
            embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.display_avatar.url
            )

            option_lines = []
            for index, choice in enumerate(choices):
                option_lines.append(f"{emoji_options[index]} {choice}")
            embed.add_field(name="Opciones", value="\n".join(option_lines), inline=False)

            attachments: List[discord.Attachment] = [a for a in (image1, image2, image3) if a is not None]
            files: List[discord.File] = []
            if attachments:
                for attachment in attachments:
                    try:
                        files.append(await attachment.to_file())
                    except Exception:
                        pass

                first_image = attachments[0]
                if first_image.content_type and first_image.content_type.startswith("image/"):
                    embed.set_image(url=f"attachment://{first_image.filename}")

            content = "@everyone" if everyone else None
            await interaction.response.send_message(content=content, embed=embed, files=files)
            poll_message = await interaction.original_response()

            for index in range(len(choices)):
                await poll_message.add_reaction(emoji_options[index])
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        suggestion_channel_id = await self.db.get_suggestions_channel(message.guild.id)
        if suggestion_channel_id != message.channel.id:
            return

        content = message.content.strip()
        if not content and not message.attachments:
            return

        embed = discord.Embed(
            title="💡 Nueva sugerencia",
            description=content if content else "(Sin texto)",
            color=discord.Color.green()
        )
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.display_avatar.url
        )
        embed.set_footer(text=f"Sugerido por {message.author}")

        files: List[discord.File] = []
        if message.attachments:
            for attachment in message.attachments:
                try:
                    files.append(await attachment.to_file())
                except Exception:
                    pass
            first_attachment = message.attachments[0]
            if first_attachment.content_type and first_attachment.content_type.startswith("image/"):
                embed.set_image(url=f"attachment://{first_attachment.filename}")

            attachment_names = [attachment.filename for attachment in message.attachments]
            if len(attachment_names) > 1:
                embed.add_field(
                    name="Archivos",
                    value="\n".join(attachment_names),
                    inline=False
                )

        try:
            await message.delete()
        except Exception:
            pass

        suggestion_message = await message.channel.send(embed=embed, files=files)
        try:
            await suggestion_message.add_reaction("⬆️")
            await suggestion_message.add_reaction("⬇️")
        except Exception:
            pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Social(bot))
