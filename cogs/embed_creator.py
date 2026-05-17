"""
Embed Creator Cog
Easy embed creation system with interactive UI
"""

import discord
from discord.ext import commands
from discord import app_commands, ui


class EmbedCreator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="create_embed",
        description="🎨 Crea un embed de forma interactiva"
    )
    async def create_embed(self, interaction: discord.Interaction):
        """Comando para crear embeds interactivamente"""
        
        # Crear embed inicial
        embed = discord.Embed(
            title="Embed",
            description="",
            color=discord.Color.blue()
        )
        
        # Mostrar editor
        view = EmbedEditorView(embed, interaction.guild)
        await interaction.response.send_message(
            "**Editor de Embed Avanzado**\nUsa los botones para editar:",
            embed=embed,
            view=view,
            ephemeral=True
        )


class CreateEmbedModal(ui.Modal, title="Crear Embed"):
    """Modal para crear un embed con campos básicos"""
    
    title_input = ui.TextInput(
        label="Título",
        placeholder="Ej: Bienvenido",
        required=False,
        max_length=256
    )
    
    description_input = ui.TextInput(
        label="Descripción",
        placeholder="Contenido del embed",
        required=False,
        style=discord.TextStyle.long,
        max_length=4000
    )
    
    color_input = ui.TextInput(
        label="Color (hex sin #)",
        placeholder="FF5733",
        required=False,
        max_length=6
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        title = self.title_input.value or "Embed"
        description = self.description_input.value or ""
        color_hex = self.color_input.value
        
        # Crear embed
        try:
            if color_hex:
                color = discord.Color(int(color_hex, 16))
            else:
                color = discord.Color.blue()
        except ValueError:
            color = discord.Color.blue()
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        
        # Mostrar opciones de edición
        view = EmbedEditorView(embed, interaction.guild)
        await interaction.response.send_message(
            "**Editor de Embed**\nUsa los botones para editar:",
            embed=embed,
            view=view,
            ephemeral=True
        )


class EmbedEditorView(ui.View):
    """Vista para editar el embed"""
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
    
    @ui.button(label="Editar Título", style=discord.ButtonStyle.primary)
    async def edit_title(self, interaction: discord.Interaction, button: ui.Button):
        modal = EditTitleModal(self.embed, self.guild)
        await interaction.response.send_modal(modal)
    
    @ui.button(label="Editar Descripción", style=discord.ButtonStyle.primary)
    async def edit_description(self, interaction: discord.Interaction, button: ui.Button):
        modal = EditDescriptionModal(self.embed, self.guild)
        await interaction.response.send_modal(modal)
    
    @ui.button(label="Editar Color", style=discord.ButtonStyle.primary)
    async def edit_color(self, interaction: discord.Interaction, button: ui.Button):
        modal = EditColorModal(self.embed, self.guild)
        await interaction.response.send_modal(modal)
    
    @ui.button(label="Autor", style=discord.ButtonStyle.secondary)
    async def edit_author(self, interaction: discord.Interaction, button: ui.Button):
        modal = EditAuthorModal(self.embed, self.guild)
        await interaction.response.send_modal(modal)
    
    @ui.button(label="Imagen", style=discord.ButtonStyle.secondary)
    async def edit_image(self, interaction: discord.Interaction, button: ui.Button):
        modal = EditImageModal(self.embed, self.guild)
        await interaction.response.send_modal(modal)
    
    @ui.button(label="Footer", style=discord.ButtonStyle.secondary)
    async def edit_footer(self, interaction: discord.Interaction, button: ui.Button):
        modal = EditFooterModal(self.embed, self.guild)
        await interaction.response.send_modal(modal)
    
    @ui.button(label="+ Campo", style=discord.ButtonStyle.success)
    async def add_field(self, interaction: discord.Interaction, button: ui.Button):
        modal = AddFieldModal(self.embed, self.guild)
        await interaction.response.send_modal(modal)
    
    @ui.button(label="Vista Previa", style=discord.ButtonStyle.secondary)
    async def preview(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message(
            embed=self.embed,
            ephemeral=True
        )
    
    @ui.button(label="Enviar", style=discord.ButtonStyle.success)
    async def send_embed(self, interaction: discord.Interaction, button: ui.Button):
        view = ChannelSelectView(self.embed, self.guild)
        await interaction.response.send_message(
            "Selecciona el canal:",
            view=view,
            ephemeral=True
        )
    
    @ui.button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()


# ============ MODALES DE EDICIÓN ============

class EditTitleModal(ui.Modal, title="Editar Título"):
    title_input = ui.TextInput(
        label="Nuevo título",
        max_length=256
    )
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
    
    async def on_submit(self, interaction: discord.Interaction):
        self.embed.title = self.title_input.value
        
        view = EmbedEditorView(self.embed, self.guild)
        await interaction.response.send_message(
            f"✅ Título actualizado",
            embed=self.embed,
            view=view,
            ephemeral=True
        )


class EditDescriptionModal(ui.Modal, title="Editar Descripción"):
    description_input = ui.TextInput(
        label="Nueva descripción",
        style=discord.TextStyle.long,
        max_length=4000
    )
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
    
    async def on_submit(self, interaction: discord.Interaction):
        self.embed.description = self.description_input.value
        
        view = EmbedEditorView(self.embed, self.guild)
        await interaction.response.send_message(
            f"✅ Descripción actualizada",
            embed=self.embed,
            view=view,
            ephemeral=True
        )


class EditColorModal(ui.Modal, title="Editar Color"):
    color_input = ui.TextInput(
        label="Color (hex sin #)",
        max_length=6
    )
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            color = int(self.color_input.value, 16)
            self.embed.color = discord.Color(color)
            
            view = EmbedEditorView(self.embed, self.guild)
            await interaction.response.send_message(
                f"✅ Color actualizado",
                embed=self.embed,
                view=view,
                ephemeral=True
            )
        except ValueError:
            await interaction.response.send_message(
                "❌ Color inválido (ej: FF5733)",
                ephemeral=True
            )


class EditAuthorModal(ui.Modal, title="Editar Autor"):
    author_name = ui.TextInput(
        label="Nombre del autor",
        placeholder="Mi nombre",
        required=False,
        max_length=256
    )
    
    author_url = ui.TextInput(
        label="URL del autor",
        placeholder="https://ejemplo.com",
        required=False
    )
    
    author_icon = ui.TextInput(
        label="URL del icono del autor",
        placeholder="https://ejemplo.com/icon.png",
        required=False
    )
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
    
    async def on_submit(self, interaction: discord.Interaction):
        name = self.author_name.value or None
        url = self.author_url.value or None
        icon_url = self.author_icon.value or None
        
        if name:
            self.embed.set_author(name=name, url=url if url else None, icon_url=icon_url if icon_url else None)
        else:
            self.embed.remove_author()
        
        view = EmbedEditorView(self.embed, self.guild)
        await interaction.response.send_message(
            f"✅ Autor actualizado",
            embed=self.embed,
            view=view,
            ephemeral=True
        )


class EditImageModal(ui.Modal, title="Editar Imagen"):
    image_url = ui.TextInput(
        label="URL de la imagen (thumbnail)",
        placeholder="https://ejemplo.com/image.png",
        required=False
    )
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
    
    async def on_submit(self, interaction: discord.Interaction):
        image_url = self.image_url.value or None
        
        if image_url:
            self.embed.set_thumbnail(url=image_url)
        else:
            self.embed.set_thumbnail(url=None)
        
        view = EmbedEditorView(self.embed, self.guild)
        await interaction.response.send_message(
            f"✅ Imagen actualizada",
            embed=self.embed,
            view=view,
            ephemeral=True
        )


class EditFooterModal(ui.Modal, title="Editar Footer"):
    footer_text = ui.TextInput(
        label="Texto del footer",
        placeholder="© 2026",
        required=False,
        max_length=2048
    )
    
    footer_icon = ui.TextInput(
        label="URL del icono del footer",
        placeholder="https://ejemplo.com/icon.png",
        required=False
    )
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
    
    async def on_submit(self, interaction: discord.Interaction):
        text = self.footer_text.value or None
        icon_url = self.footer_icon.value or None
        
        if text:
            self.embed.set_footer(text=text, icon_url=icon_url if icon_url else None)
        else:
            self.embed.remove_footer()
        
        view = EmbedEditorView(self.embed, self.guild)
        await interaction.response.send_message(
            f"✅ Footer actualizado",
            embed=self.embed,
            view=view,
            ephemeral=True
        )


class AddFieldModal(ui.Modal, title="Añadir Campo"):
    field_name = ui.TextInput(
        label="Nombre del campo",
        placeholder="Mi campo",
        max_length=256
    )
    
    field_value = ui.TextInput(
        label="Valor del campo",
        placeholder="Contenido del campo",
        style=discord.TextStyle.long,
        max_length=1024
    )
    
    inline_input = ui.TextInput(
        label="¿En línea? (si/no)",
        placeholder="si",
        required=False,
        max_length=2
    )
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
    
    async def on_submit(self, interaction: discord.Interaction):
        name = self.field_name.value
        value = self.field_value.value
        inline = self.inline_input.value.lower() in ["si", "sí", "yes", "y", "true", "1"]
        
        self.embed.add_field(name=name, value=value, inline=inline)
        
        view = EmbedEditorView(self.embed, self.guild)
        await interaction.response.send_message(
            f"✅ Campo añadido",
            embed=self.embed,
            view=view,
            ephemeral=True
        )


class ChannelSelectView(ui.View):
    """Vista para seleccionar canal"""
    
    def __init__(self, embed: discord.Embed, guild: discord.Guild):
        super().__init__()
        self.embed = embed
        self.guild = guild
        
        # Crear opciones de canales
        options = []
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                options.append(
                    discord.SelectOption(
                        label=channel.name[:100],
                        value=str(channel.id),
                        emoji="📝"
                    )
                )
        
        if options:
            self.channel_select.options = options
        else:
            # Si no hay opciones, deshabilitar el select
            self.channel_select.disabled = True
    
    @ui.select(
        placeholder="Selecciona un canal",
        min_values=1,
        max_values=1
    )
    async def channel_select(self, interaction: discord.Interaction, select: ui.Select):
        channel_id = int(select.values[0])
        channel = self.guild.get_channel(channel_id)
        
        if not channel:
            await interaction.response.send_message(
                "❌ Canal no encontrado",
                ephemeral=True
            )
            return
        
        try:
            await channel.send(embed=self.embed)
            await interaction.response.send_message(
                f"✅ Enviado a {channel.mention}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error: {e}",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(EmbedCreator(bot))

