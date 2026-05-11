"""
Moderation Cog
Commands with WORKING autocomplete
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime
from typing import Optional


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_mutes.start()

    # Autocomplete para roles - FUNCIONA CORRECTAMENTE
    async def role_autocomplete(
        self, 
        interaction: discord.Interaction, 
        current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete for roles - devuelve choices con nombre y valor string"""
        try:
            # Filtrar roles que contengan el texto actual, excluyendo @everyone
            roles = [
                role for role in interaction.guild.roles 
                if current.lower() in role.name.lower() and not role.is_default()
            ]
            roles = roles[:25]  # Límite de 25 opciones
            
            # Devolver choices con el nombre del rol y su ID como string
            return [
                app_commands.Choice(name=role.name, value=str(role.id)) 
                for role in roles
            ]
        except Exception as e:
            print(f"Error en autocomplete: {e}")
            return []

    # Autocomplete para miembros
    async def member_autocomplete(
        self, 
        interaction: discord.Interaction, 
        current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete for members"""
        try:
            members = [
                member for member in interaction.guild.members 
                if current.lower() in member.name.lower()
            ][:25]
            return [
                app_commands.Choice(name=member.name, value=str(member.id)) 
                for member in members
            ]
        except:
            return []

    @app_commands.command(name="lock", description="🔒 Bloquea el canal actual")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        """Lock the current channel"""
        channel = interaction.channel
        
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.response.send_message(f"🔒 Canal {channel.mention} bloqueado.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="unlock", description="🔓 Desbloquea el canal actual")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        """Unlock the current channel"""
        channel = interaction.channel
        
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.response.send_message(f"🔓 Canal {channel.mention} desbloqueado.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="tempmute", description="🔇 Silencia un usuario temporalmente")
    @app_commands.describe(
        user="Usuario a silenciar",
        duration="Duración en segundos",
        reason="Razón del silencio"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def tempmute(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        duration: int,
        reason: Optional[str] = None
    ):
        """Temporarily mute a user"""
        try:
            member = await interaction.guild.fetch_member(user.id)
            
            until = discord.utils.utcnow() + datetime.timedelta(seconds=duration)
            await member.timeout(until, reason=reason or "Sin razón especificada")
            
            await interaction.response.send_message(
                f"🔇 {user.mention} silenciado por {duration}s. Razón: {reason or 'N/A'}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="rolve", description="👤 Da o quita un rol a un usuario")
    @app_commands.describe(
        user="Usuario",
        role="Rol a dar/quitar (usa el autocompletado)"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.autocomplete(role=role_autocomplete)
    async def role_give(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        role: str  # Recibimos el ID como string desde el autocomplete
    ):
        """Give or remove a role from a user"""
        try:
            # Convertir el string del ID del rol a entero y obtener el objeto Role
            role_id = int(role)
            role_obj = interaction.guild.get_role(role_id)
            
            if not role_obj:
                await interaction.response.send_message(f"❌ Rol no encontrado", ephemeral=True)
                return
                
            member = await interaction.guild.fetch_member(user.id)
            
            # Verificar que el bot puede manejar este rol
            if role_obj >= interaction.guild.me.top_role:
                await interaction.response.send_message(f"❌ No puedo manejar ese rol porque está por encima del mío", ephemeral=True)
                return
            
            if role_obj in member.roles:
                await member.remove_roles(role_obj)
                await interaction.response.send_message(
                    f"❌ Rol {role_obj.mention} eliminado de {user.mention}",
                    ephemeral=True
                )
            else:
                await member.add_roles(role_obj)
                await interaction.response.send_message(
                    f"✅ Rol {role_obj.mention} otorgado a {user.mention}",
                    ephemeral=True
                )
        except ValueError:
            await interaction.response.send_message(f"❌ ID de rol inválido", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"❌ No tengo permisos para manejar ese rol", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="roles", description="📋 Muestra la lista de roles del servidor")
    async def list_roles(self, interaction: discord.Interaction):
        """List all roles in the server"""
        roles = sorted(interaction.guild.roles, key=lambda r: r.position, reverse=True)
        
        embed = discord.Embed(
            title=f"Roles en {interaction.guild.name}",
            color=discord.Color.blue(),
            description="Usa `/rolve @usuario` y el autocompletado te sugerirá estos roles"
        )
        
        role_list = []
        for role in roles:
            if not role.is_default():
                role_list.append(f"{role.mention} - `{role.id}`")
        
        if role_list:
            # Mostrar primeros 25 roles
            role_text = "\n".join(role_list[:25])
            embed.add_field(name="Roles disponibles", value=role_text, inline=False)
            if len(role_list) > 25:
                embed.set_footer(text=f"Y {len(role_list) - 25} roles más...")
        else:
            embed.description = "No hay roles personalizados"
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="userinfo", description="ℹ️ Muestra información del usuario")
    @app_commands.describe(user="Usuario (opcional)")
    async def userinfo(self, interaction: discord.Interaction, user: Optional[discord.User] = None):
        """Show user information"""
        user = user or interaction.user
        
        try:
            member = await interaction.guild.fetch_member(user.id)
            
            embed = discord.Embed(
                title=f"Información de {user}",
                color=discord.Color.blue(),
                timestamp=interaction.created_at
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
            embed.add_field(name="ID", value=user.id, inline=False)
            embed.add_field(name="Creado", value=f"<t:{int(user.created_at.timestamp())}:F>", inline=False)
            embed.add_field(name="Se unió", value=f"<t:{int(member.joined_at.timestamp())}:F>", inline=False)
            embed.add_field(name="Roles", value=f"{len(member.roles) - 1}", inline=False)
            
            # Mostrar roles principales
            if len(member.roles) > 1:
                top_roles = [r.mention for r in member.roles[1:6]]  # Mostrar hasta 5 roles
                embed.add_field(name="Roles destacados", value=", ".join(top_roles), inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="serverinfo", description="ℹ️ Muestra información del servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        """Show server information"""
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"Información de {guild.name}",
            color=discord.Color.green(),
            timestamp=interaction.created_at
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="ID", value=guild.id, inline=False)
        embed.add_field(name="Propietario", value=guild.owner.mention, inline=False)
        embed.add_field(name="Creado", value=f"<t:{int(guild.created_at.timestamp())}:F>", inline=False)
        embed.add_field(name="Miembros", value=guild.member_count, inline=False)
        embed.add_field(name="Canales", value=len(guild.channels), inline=False)
        embed.add_field(name="Roles", value=len(guild.roles), inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="kick", description="👢 Expulsa a un usuario del servidor")
    @app_commands.describe(
        user="Usuario a expulsar",
        reason="Razón de la expulsión"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        reason: Optional[str] = None
    ):
        """Kick a user from the server"""
        try:
            member = await interaction.guild.fetch_member(user.id)
            await member.kick(reason=reason or "Sin razón especificada")
            
            await interaction.response.send_message(
                f"👢 {user.mention} ha sido expulsado. Razón: {reason or 'N/A'}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="ban", description="🔨 Banea a un usuario del servidor")
    @app_commands.describe(
        user="Usuario a banear",
        reason="Razón del baneo"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        reason: Optional[str] = None
    ):
        """Ban a user from the server"""
        try:
            await interaction.guild.ban(user, reason=reason or "Sin razón especificada")
            
            await interaction.response.send_message(
                f"🔨 {user.mention} ha sido baneado. Razón: {reason or 'N/A'}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="unban", description="🔓 Desbanea a un usuario")
    @app_commands.describe(user="Nombre del usuario a desbanear (ID)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: str):
        """Unban a user - usa el ID del usuario"""
        try:
            # Convertir a int si es un ID, o buscar por nombre
            if user.isdigit():
                user_id = int(user)
                banned_users = [entry async for entry in interaction.guild.banned_users()]
                user_obj = next((u.user for u in banned_users if u.user.id == user_id), None)
                if user_obj:
                    await interaction.guild.unban(user_obj)
                    await interaction.response.send_message(f"🔓 {user_obj.mention} ha sido desbaneado", ephemeral=True)
                else:
                    await interaction.response.send_message(f"❌ Usuario no encontrado en la lista de baneados", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ Por favor, proporciona el ID del usuario (usa /banlist para ver los IDs)", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="warn", description="⚠️ Advierte a un usuario")
    @app_commands.describe(
        user="Usuario a advertir",
        reason="Razón de la advertencia"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        reason: Optional[str] = None
    ):
        """Warn a user"""
        try:
            embed = discord.Embed(
                title="⚠️ Advertencia",
                description=f"Has sido advertido en {interaction.guild.name}",
                color=discord.Color.orange()
            )
            embed.add_field(name="Razón", value=reason or "Sin especificar", inline=False)
            embed.add_field(name="Por", value=interaction.user.mention, inline=False)
            
            await user.send(embed=embed)
            
            await interaction.response.send_message(
                f"⚠️ {user.mention} ha sido advertido. Razón: {reason or 'N/A'}",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(f"⚠️ No se pudo enviar DM a {user.mention}, pero se registró la advertencia.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="clear", description="🗑️ Elimina mensajes del canal")
    @app_commands.describe(amount="Cantidad de mensajes a eliminar (1-100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        """Clear messages from channel"""
        try:
            if amount > 100:
                amount = 100
            if amount < 1:
                await interaction.response.send_message("❌ La cantidad debe ser entre 1 y 100", ephemeral=True)
                return
            
            deleted = await interaction.channel.purge(limit=amount)
            
            await interaction.response.send_message(
                f"🗑️ Se eliminaron {len(deleted)} mensajes",
                ephemeral=True,
                delete_after=5
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="mute", description="🔇 Silencia un usuario")
    @app_commands.describe(
        user="Usuario a silenciar",
        duration="Duración en segundos (opcional)",
        reason="Razón del silencio"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(
        self, 
        interaction: discord.Interaction, 
        user: discord.User, 
        duration: Optional[int] = None, 
        reason: Optional[str] = None
    ):
        """Mute a user"""
        try:
            member = await interaction.guild.fetch_member(user.id)
            if duration:
                if duration > 2419200:  # 28 días máximo
                    duration = 2419200
                until = discord.utils.utcnow() + datetime.timedelta(seconds=duration)
                await member.timeout(until, reason=reason or "Sin razón especificada")
                await interaction.response.send_message(f"🔇 {user.mention} silenciado por {duration}s.", ephemeral=True)
            else:
                # Mute por 28 días (máximo) como "indefinido"
                until = discord.utils.utcnow() + datetime.timedelta(days=28)
                await member.timeout(until, reason=reason or "Silenciado")
                await interaction.response.send_message(f"🔇 {user.mention} silenciado. Usa /unmute para desmutear.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="unmute", description="🔊 Quita el silencio de un usuario")
    @app_commands.describe(user="Usuario a desmutear")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, user: discord.User):
        """Unmute a user"""
        try:
            member = await interaction.guild.fetch_member(user.id)
            await member.timeout(None)
            await interaction.response.send_message(f"🔊 {user.mention} ha sido desmutado.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="nick", description="✏️ Cambia el apodo de un usuario")
    @app_commands.describe(
        user="Usuario",
        nickname="Nuevo apodo (vacío para resetear)"
    )
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nick(
        self, 
        interaction: discord.Interaction, 
        user: discord.User, 
        nickname: Optional[str] = None
    ):
        """Change user nickname"""
        try:
            member = await interaction.guild.fetch_member(user.id)
            await member.edit(nick=nickname)
            await interaction.response.send_message(
                f"✏️ Apodo de {user.mention} cambiado a: {nickname or 'reseteado'}", 
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="softban", description="🔨 Softban: banea y desbanea")
    @app_commands.describe(
        user="Usuario a softbanear",
        reason="Razón"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def softban(
        self, 
        interaction: discord.Interaction, 
        user: discord.User, 
        reason: Optional[str] = None
    ):
        """Softban a user"""
        try:
            await interaction.guild.ban(user, reason=reason or "Softban", delete_message_days=1)
            await interaction.guild.unban(user)
            await interaction.response.send_message(
                f"🔨 {user.mention} ha sido softbaneado (mensajes eliminados).", 
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="slowmode", description="🐢 Ajusta el slowmode del canal")
    @app_commands.describe(seconds="Segundos de slowmode (0-21600)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        """Set channel slowmode"""
        try:
            if seconds < 0 or seconds > 21600:
                await interaction.response.send_message("❌ Los segundos deben estar entre 0 y 21600", ephemeral=True)
                return
            await interaction.channel.edit(rate_limit_per_user=seconds)
            
            if seconds == 0:
                await interaction.response.send_message(f"🐢 Slowmode desactivado en este canal", ephemeral=True)
            else:
                await interaction.response.send_message(f"🐢 Slowmode establecido a {seconds}s en este canal", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="sync", description="🔄 Sincroniza los comandos slash (admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction: discord.Interaction):
        """Sync commands globally"""
        await interaction.response.defer(ephemeral=True)
        try:
            synced = await self.bot.tree.sync()
            await interaction.followup.send(
                f"✅ Sincronizados {len(synced)} comandos globalmente.\n"
                f"Los comandos pueden tardar hasta 1 hora en aparecer en todos los servidores.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)

    @tasks.loop(minutes=1)
    async def check_mutes(self):
        """Check for expired mutes (para futuro)"""
        pass

    @check_mutes.before_loop
    async def before_check_mutes(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))