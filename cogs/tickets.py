"""
Tickets Cog
Advanced ticket system with panels, types, and management
"""

import discord
from discord.ext import commands
from discord import app_commands, ui
import json
import datetime
from typing import Optional, List, Dict, Any
import asyncio
import io


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        from main import db
        self.db = db

    # Ticket Type Management
    @app_commands.command(
        name="create_ticket_type",
        description="🎫 Crea un nuevo tipo de ticket"
    )
    @app_commands.describe(
        name="Nombre del tipo de ticket",
        mention_roles="Roles a mencionar (IDs separados por comas)",
        close_permissions="Roles que pueden cerrar (IDs separados por comas)",
        log_channel="Canal para logs",
        category="Categoría de Discord para los tickets"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def create_ticket_type(
        self,
        interaction: discord.Interaction,
        name: str,
        mention_roles: str,
        close_permissions: str,
        log_channel: discord.TextChannel,
        category: discord.CategoryChannel
    ):
        try:
            # Parse role IDs
            mention_role_ids = [int(rid.strip()) for rid in mention_roles.split(',') if rid.strip()]
            close_perm_ids = [int(rid.strip()) for rid in close_permissions.split(',') if rid.strip()]

            # Validate roles exist
            for role_id in mention_role_ids + close_perm_ids:
                role = interaction.guild.get_role(role_id)
                if not role:
                    await interaction.response.send_message(f"❌ Rol con ID {role_id} no encontrado", ephemeral=True)
                    return

            ticket_type_id = await self.db.create_ticket_type(
                interaction.guild.id,
                name,
                json.dumps(mention_role_ids),
                json.dumps(close_perm_ids),
                log_channel.id,
                category.id
            )

            embed = discord.Embed(
                title="✅ Tipo de ticket creado",
                description=f"**{name}** (ID: {ticket_type_id})",
                color=discord.Color.green()
            )
            embed.add_field(name="Roles a mencionar", value=", ".join([f"<@&{rid}>" for rid in mention_role_ids]) or "Ninguno", inline=False)
            embed.add_field(name="Puede cerrar", value=", ".join([f"<@&{rid}>" for rid in close_perm_ids]) or "Solo administradores", inline=False)
            embed.add_field(name="Categoría", value=category.name, inline=True)
            embed.add_field(name="Logs", value=log_channel.mention, inline=True)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message(f"❌ Error en IDs: {e}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="list_ticket_types",
        description="📋 Lista todos los tipos de ticket"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def list_ticket_types(self, interaction: discord.Interaction):
        try:
            ticket_types = await self.db.get_ticket_types(interaction.guild.id)

            if not ticket_types:
                await interaction.response.send_message("❌ No hay tipos de ticket configurados", ephemeral=True)
                return

            embed = discord.Embed(
                title="📋 Tipos de ticket",
                color=discord.Color.blue()
            )

            for tt_id, name, mention_roles, close_perms, log_ch, cat_id in ticket_types:
                mention_list = json.loads(mention_roles) if mention_roles else []
                close_list = json.loads(close_perms) if close_perms else []

                value = f"**ID:** {tt_id}\n"
                value += f"**Mencionar:** {', '.join([f'<@&{rid}>' for rid in mention_list]) or 'Ninguno'}\n"
                value += f"**Cerrar:** {', '.join([f'<@&{rid}>' for rid in close_list]) or 'Admins'}\n"
                value += f"**Categoría:** <#{cat_id}>"

                embed.add_field(name=name, value=value, inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="delete_ticket_type",
        description="🗑️ Elimina un tipo de ticket"
    )
    @app_commands.describe(ticket_type_id="ID del tipo de ticket a eliminar")
    @app_commands.checks.has_permissions(administrator=True)
    async def delete_ticket_type(self, interaction: discord.Interaction, ticket_type_id: int):
        try:
            # Check if ticket type exists
            tt = await self.db.get_ticket_type(ticket_type_id)
            if not tt:
                await interaction.response.send_message("❌ Tipo de ticket no encontrado", ephemeral=True)
                return

            # Check if there are active tickets of this type
            # This would require checking active_tickets table, but for simplicity we'll just delete
            await self.db.delete_ticket_type(ticket_type_id)

            embed = discord.Embed(
                title="✅ Tipo de ticket eliminado",
                description=f"El tipo de ticket **{tt[1]}** ha sido eliminado",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    # Panel Creation - Step 1: Embed Configuration
    @app_commands.command(
        name="create_ticket_panel",
        description="🎫 Crea un panel de tickets (Paso 1: Configurar embed)"
    )
    @app_commands.describe(
        channel="Canal donde crear el panel",
        title="Título del embed",
        description="Descripción del embed",
        color="Color en hex (ej: #FF0000)",
        image="URL de imagen opcional"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def create_ticket_panel_step1(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        title: str,
        description: str,
        color: str = "#3498db",
        image: Optional[str] = None
    ):
        try:
            # Validate color
            if not color.startswith('#') or len(color) != 7:
                await interaction.response.send_message("❌ Color debe ser en formato #RRGGBB", ephemeral=True)
                return

            int(color[1:], 16)  # Validate hex

            # Store temporary data for step 2
            temp_data = {
                "channel_id": channel.id,
                "embed_title": title,
                "embed_description": description,
                "embed_color": color,
                "embed_image": image
            }

            # Send embed preview
            embed = discord.Embed(
                title=title,
                description=description,
                color=int(color[1:], 16)
            )
            if image:
                embed.set_image(url=image)

            embed.set_footer(text="Paso 1 completado. Usa /configure_ticket_panel para continuar.")

            await interaction.response.send_message(embed=embed, ephemeral=True)

            # Store in bot's temp storage (you might want to use a better storage)
            if not hasattr(self.bot, 'temp_panel_data'):
                self.bot.temp_panel_data = {}
            self.bot.temp_panel_data[interaction.user.id] = temp_data

        except ValueError:
            await interaction.response.send_message("❌ Color hex inválido", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    # Panel Creation - Step 2: Ticket Selection Configuration
    @app_commands.command(
        name="configure_ticket_panel",
        description="🎫 Configura las opciones del panel de tickets (Paso 2)"
    )
    @app_commands.describe(
        selection_type="Tipo de selección: button, list, o emoji",
        ticket_config="Configuración de tickets (formato depende del tipo seleccionado)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def configure_ticket_panel_step2(
        self,
        interaction: discord.Interaction,
        selection_type: str,
        ticket_config: str
    ):
        try:
            if not hasattr(self.bot, 'temp_panel_data') or interaction.user.id not in self.bot.temp_panel_data:
                await interaction.response.send_message("❌ Primero completa el paso 1 con /create_ticket_panel", ephemeral=True)
                return

            if selection_type not in ['button', 'list', 'emoji']:
                await interaction.response.send_message("❌ Tipo de selección debe ser: button, list, o emoji", ephemeral=True)
                return

            temp_data = self.bot.temp_panel_data[interaction.user.id]

            # Parse ticket config based on selection type
            options = []

            if selection_type == 'emoji':
                # Format: ticket_id:emoji (ej: 1:🎫,2:📋)
                for config in ticket_config.split(','):
                    parts = config.strip().split(':')
                    if len(parts) != 2:
                        await interaction.response.send_message(f"❌ Formato inválido para emoji: {config}. Usa ID:emoji", ephemeral=True)
                        return

                    tt_id, emoji = parts
                    tt_id = int(tt_id)

                    # Validate ticket type exists
                    tt = await self.db.get_ticket_type(tt_id)
                    if not tt:
                        await interaction.response.send_message(f"❌ Tipo de ticket {tt_id} no existe", ephemeral=True)
                        return

                    options.append({
                        'type_id': tt_id,
                        'emoji': emoji,
                        'type_name': tt[1]  # Store name for embed display
                    })

            elif selection_type == 'button':
                # Format: ticket_id:emoji:text:color (ej: 1:🎫:Crear Ticket:primary)
                for config in ticket_config.split(','):
                    parts = config.strip().split(':')
                    if len(parts) != 4:
                        await interaction.response.send_message(f"❌ Formato inválido para botón: {config}. Usa ID:emoji:texto:color", ephemeral=True)
                        return

                    tt_id, emoji, button_text, btn_color = parts
                    tt_id = int(tt_id)

                    # Validate ticket type exists
                    tt = await self.db.get_ticket_type(tt_id)
                    if not tt:
                        await interaction.response.send_message(f"❌ Tipo de ticket {tt_id} no existe", ephemeral=True)
                        return

                    if btn_color not in ['primary', 'secondary', 'success', 'danger']:
                        await interaction.response.send_message(f"❌ Color de botón inválido: {btn_color}", ephemeral=True)
                        return

                    options.append({
                        'type_id': tt_id,
                        'emoji': emoji,
                        'button_text': button_text,
                        'button_color': btn_color
                    })

            elif selection_type == 'list':
                # Format: ticket_id:position:emoji:text (ej: 1:1:🎫:Reportes)
                position_tracker = {}
                for config in ticket_config.split(','):
                    parts = config.strip().split(':')
                    if len(parts) != 4:
                        await interaction.response.send_message(f"❌ Formato inválido para lista: {config}. Usa ID:posición:emoji:texto", ephemeral=True)
                        return

                    tt_id, position, emoji, option_text = parts
                    tt_id = int(tt_id)
                    position = int(position)

                    # Validate ticket type exists
                    tt = await self.db.get_ticket_type(tt_id)
                    if not tt:
                        await interaction.response.send_message(f"❌ Tipo de ticket {tt_id} no existe", ephemeral=True)
                        return

                    # Check for duplicate positions
                    if position in position_tracker:
                        await interaction.response.send_message(f"❌ Posición {position} duplicada", ephemeral=True)
                        return
                    position_tracker[position] = True

                    options.append({
                        'type_id': tt_id,
                        'position': position,
                        'emoji': emoji,
                        'option_text': option_text
                    })

                # Sort by position
                options.sort(key=lambda x: x['position'])

            # Add selection info to embed for emoji type
            if selection_type == 'emoji':
                emoji_lines = []
                for opt in options:
                    emoji_lines.append(f"**{opt['type_name']}**: {opt['emoji']}")
                if emoji_lines:
                    embed.add_field(
                        name="🎫 Tipos de Ticket Disponibles",
                        value="\n".join(emoji_lines),
                        inline=False
                    )

            # Create the message with appropriate components
            channel = self.bot.get_channel(temp_data['channel_id'])
            if not channel:
                await interaction.response.send_message("❌ Canal no encontrado", ephemeral=True)
                return

            if selection_type == 'button':
                view = TicketButtonView(options, self.db)
                message = await channel.send(embed=embed, view=view)
            elif selection_type == 'list':
                # For list, we'll use a select menu
                view = TicketSelectView(options, self.db)
                await view.populate_options()  # Populate options asynchronously
                message = await channel.send(embed=embed, view=view)
            else:  # emoji
                message = await channel.send(embed=embed)
                for opt in options:
                    await message.add_reaction(opt['emoji'])

            # Save panel to database
            panel_id = await self.db.create_ticket_panel(
                interaction.guild.id,
                channel.id,
                message.id,
                temp_data['embed_title'],
                temp_data['embed_description'],
                temp_data['embed_color'],
                temp_data['embed_image'] or '',
                selection_type,
                json.dumps(options)
            )

            # Clean up temp data
            del self.bot.temp_panel_data[interaction.user.id]

            await interaction.response.send_message(f"✅ Panel creado exitosamente (ID: {panel_id})", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    # Event listeners for ticket creation
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return

        custom_id = interaction.data.get('custom_id', '')
        if not custom_id.startswith('ticket_'):
            return

        if custom_id.startswith('ticket_create_'):
            # Button click
            ticket_type_id = int(custom_id.split('_')[-1])
            await self._create_ticket(interaction, ticket_type_id)

        elif custom_id == 'ticket_select':
            # Select menu
            ticket_type_id = int(interaction.data['values'][0])
            await self._create_ticket(interaction, ticket_type_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        # Check if reaction is on a ticket panel
        panel = await self.db.get_ticket_panel_by_message(payload.message_id)
        if not panel or panel[7] != 'emoji':  # selection_type
            return

        # Find the ticket type for this emoji
        options = json.loads(panel[8])  # ticket_options
        ticket_type_id = None
        for opt in options:
            if opt['emoji'] == str(payload.emoji):
                ticket_type_id = opt['type_id']
                break

        if not ticket_type_id:
            return

        # Get the interaction (we need to create a fake one)
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)

        # Create a minimal interaction-like object
        class FakeInteraction:
            def __init__(self, user, channel, guild):
                self.user = user
                self.channel = channel
                self.guild = guild

            async def response(self):
                return self

            async def send_message(self, content, ephemeral=False):
                await self.channel.send(content)

        fake_interaction = FakeInteraction(user, channel, guild)
        await self._create_ticket(fake_interaction, ticket_type_id)

    async def _create_ticket(self, interaction, ticket_type_id: int):
        """Internal method to create a ticket"""
        try:
            # Check if user already has an open ticket of this type
            user_tickets = await self.db.get_user_tickets(interaction.user.id, interaction.guild.id)
            for ticket in user_tickets:
                if ticket[2] == ticket_type_id and ticket[4] == 'open':
                    await interaction.response.send_message("❌ Ya tienes un ticket abierto de este tipo", ephemeral=True)
                    return

            # Get ticket type info
            tt = await self.db.get_ticket_type(ticket_type_id)
            if not tt:
                await interaction.response.send_message("❌ Tipo de ticket no encontrado", ephemeral=True)
                return

            tt_id, name, mention_roles, close_perms, log_ch, cat_id = tt

            # Get category
            category = interaction.guild.get_channel(cat_id)
            if not category:
                await interaction.response.send_message("❌ Categoría no encontrada", ephemeral=True)
                return

            # Create channel
            channel_name = f"ticket-{interaction.user.name.lower()}-{ticket_type_id}"
            ticket_channel = await interaction.guild.create_text_channel(
                channel_name,
                category=category,
                topic=f"Ticket de {interaction.user} - Tipo: {name}"
            )

            # Set permissions
            await ticket_channel.set_permissions(interaction.guild.default_role, read_messages=False)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

            # Add close permissions
            close_role_ids = json.loads(close_perms) if close_perms else []
            for role_id in close_role_ids:
                role = interaction.guild.get_role(role_id)
                if role:
                    await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)

            # Create ticket in database
            created_at = datetime.datetime.now().isoformat()
            ticket_id = await self.db.create_ticket(
                interaction.guild.id,
                ticket_channel.id,
                interaction.user.id,
                ticket_type_id,
                created_at
            )

            # Send welcome message
            embed = discord.Embed(
                title=f"🎫 {name}",
                description=f"Bienvenido {interaction.user.mention}!\n\nUn miembro del staff te atenderá pronto.",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Ticket ID: {ticket_id}")

            # Mention roles
            mention_role_ids = json.loads(mention_roles) if mention_roles else []
            mentions = " ".join([f"<@&{rid}>" for rid in mention_role_ids])

            await ticket_channel.send(f"{mentions} {interaction.user.mention}", embed=embed)

            # Confirm to user
            await interaction.response.send_message(f"✅ Ticket creado: {ticket_channel.mention}", ephemeral=True)

        except Exception as e:
            print(f"Error creating ticket: {e}")
            try:
                await interaction.response.send_message("❌ Error al crear el ticket", ephemeral=True)
            except:
                pass

    # Ticket Management Commands
    @app_commands.command(
        name="close_ticket",
        description="🔒 Cierra el ticket actual"
    )
    async def close_ticket(self, interaction: discord.Interaction):
        try:
            # Check if in a ticket channel
            ticket_info = await self.db.get_active_ticket(interaction.channel.id)
            if not ticket_info:
                await interaction.response.send_message("❌ Este no es un canal de ticket activo", ephemeral=True)
                return

            ticket_id, guild_id, user_id, ticket_type_id, created_at, status = ticket_info

            # Check permissions
            tt = await self.db.get_ticket_type(ticket_type_id)
            if tt:
                close_perms = json.loads(tt[3]) if tt[3] else []
                has_perm = (
                    interaction.user.guild_permissions.administrator or
                    any(interaction.user.get_role(rid) for rid in close_perms) or
                    interaction.user.id == user_id
                )
                if not has_perm:
                    await interaction.response.send_message("❌ No tienes permiso para cerrar este ticket", ephemeral=True)
                    return

            # Close ticket
            await self.db.close_ticket(ticket_id)

            # Log to log channel
            if tt and tt[4]:  # log_channel_id
                log_channel = self.bot.get_channel(tt[4])
                if log_channel:
                    embed = discord.Embed(
                        title="🎫 Ticket Cerrado",
                        description=f"**Tipo:** {tt[1]}\n**Usuario:** <@{user_id}>\n**Cerrado por:** {interaction.user.mention}",
                        color=discord.Color.red(),
                        timestamp=datetime.datetime.now()
                    )
                    await log_channel.send(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="add_to_ticket",
        description="👥 Añade un usuario al ticket actual"
    )
    @app_commands.describe(user="Usuario a añadir")
    async def add_to_ticket(self, interaction: discord.Interaction, user: discord.User):
        try:
            ticket_info = await self.db.get_active_ticket(interaction.channel.id)
            if not ticket_info:
                await interaction.response.send_message("❌ Este no es un canal de ticket activo", ephemeral=True)
                return

            # Check if user is already in channel
            if user in interaction.channel.members:
                await interaction.response.send_message("❌ El usuario ya está en el ticket", ephemeral=True)
                return

            # Add user to channel
            await interaction.channel.set_permissions(user, read_messages=True, send_messages=True)

            embed = discord.Embed(
                title="👥 Usuario añadido",
                description=f"{user.mention} ha sido añadido al ticket por {interaction.user.mention}",
                color=discord.Color.green()
            )
            await interaction.channel.send(embed=embed)
            await interaction.response.send_message("✅ Usuario añadido", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


# UI Components
class TicketButtonView(ui.View):
    def __init__(self, options: List[Dict], db):
        super().__init__(timeout=None)
        self.db = db

        for opt in options:
            button = ui.Button(
                label=opt.get('button_text', f"Crear {opt['type_id']}"),
                emoji=opt['emoji'],
                style=getattr(discord.ButtonStyle, opt['button_color']),
                custom_id=f"ticket_create_{opt['type_id']}"
            )
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True  # Allow all users to create tickets


class TicketSelectView(ui.View):
    def __init__(self, options: List[Dict], db):
        super().__init__(timeout=None)
        self.db = db
        self.options = options

        # We'll populate the select later when needed
        self.select = ui.Select(
            placeholder="Selecciona un tipo de ticket...",
            options=[],  # Will be populated in callback
            custom_id="ticket_select"
        )
        self.add_item(self.select)

    async def populate_options(self):
        """Populate the select options asynchronously"""
        select_options = []
        for opt in self.options:
            tt = await self.db.get_ticket_type(opt['type_id'])
            if tt:
                select_options.append(discord.SelectOption(
                    label=opt.get('option_text', tt[1]),
                    value=str(opt['type_id']),
                    emoji=opt['emoji']
                ))

        self.select.options = select_options


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))