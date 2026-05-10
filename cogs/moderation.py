"""
Moderation Cog
Commands: lock, tempmute, role give, userinfo, serverinfo
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime
from typing import Optional


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.muted_users = {}  # {user_id: unmute_time}
        self.check_mutes.start()

    async def role_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete for roles"""
        try:
            roles = [r for r in interaction.guild.roles if current.lower() in r.name.lower()][:25]
            return [app_commands.Choice(name=r.name, value=str(r.id)) for r in roles]
        except:
            return []

    async def member_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete for members"""
        try:
            members = [m for m in interaction.guild.members if current.lower() in m.name.lower()][:25]
            return [app_commands.Choice(name=m.name, value=str(m.id)) for m in members]
        except:
            return []

    @app_commands.command(
        name="lock",
        description="🔒 Bloquea el canal actual para que nadie pueda enviar mensajes"
    )
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

    @app_commands.command(
        name="unlock",
        description="🔓 Desbloquea el canal actual"
    )
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

    @app_commands.command(
        name="tempmute",
        description="🔇 Silencia un usuario temporalmente"
    )
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

    @app_commands.command(
        name="rolve",
        description="👤 Da o quita un rol a un usuario"
    )
    @app_commands.describe(
        user="Usuario",
        role="Rol a dar/quitar"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.autocomplete(role=role_autocomplete)
    async def role_give(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        role: discord.Role
    ):
        """Give or remove a role from a user"""
        try:
            member = await interaction.guild.fetch_member(user.id)
            
            if role in member.roles:
                await member.remove_roles(role)
                await interaction.response.send_message(
                    f"❌ Rol {role.mention} eliminado de {user.mention}",
                    ephemeral=True
                )
            else:
                await member.add_roles(role)
                await interaction.response.send_message(
                    f"✅ Rol {role.mention} otorgado a {user.mention}",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="userinfo",
        description="ℹ️ Muestra información del usuario"
    )
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
            embed.add_field(name="Creado", value=user.created_at.strftime("%d/%m/%Y %H:%M"), inline=False)
            embed.add_field(name="Se unió", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=False)
            embed.add_field(name="Roles", value=f"{len(member.roles) - 1}", inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="serverinfo",
        description="ℹ️ Muestra información del servidor"
    )
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
        embed.add_field(name="Creado", value=guild.created_at.strftime("%d/%m/%Y %H:%M"), inline=False)
        embed.add_field(name="Miembros", value=guild.member_count, inline=False)
        embed.add_field(name="Canales", value=len(guild.channels), inline=False)
        embed.add_field(name="Roles", value=len(guild.roles), inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="kick",
        description="👢 Expulsa a un usuario del servidor"
    )
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

    @app_commands.command(
        name="ban",
        description="🔨 Banea a un usuario del servidor"
    )
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

    @app_commands.command(
        name="unban",
        description="🔓 Desbanea a un usuario"
    )
    @app_commands.describe(user="Usuario a desbanear")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User):
        """Unban a user"""
        try:
            await interaction.guild.unban(user)
            
            await interaction.response.send_message(
                f"🔓 {user.mention} ha sido desbaneado",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="warn",
        description="⚠️ Advierte a un usuario"
    )
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
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="clear",
        description="🗑️ Elimina mensajes del canal"
    )
    @app_commands.describe(amount="Cantidad de mensajes a eliminar (máx 100)")
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


    @app_commands.command(
        name="mute",
        description="🔇 Silencia un usuario indefinidamente o por un tiempo opcional (segundos)"
    )
    @app_commands.describe(
        user="Usuario a silenciar",
        duration="Duración en segundos (opcional)",
        reason="Razón del silencio"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, user: discord.User, duration: Optional[int] = None, reason: Optional[str] = None):
        """Mute a user (indefinite or for duration)"""
        try:
            member = await interaction.guild.fetch_member(user.id)
            if duration:
                until = discord.utils.utcnow() + datetime.timedelta(seconds=duration)
                await member.timeout(until, reason=reason or "Sin razón especificada")
                await interaction.response.send_message(f"🔇 {user.mention} silenciado por {duration}s.", ephemeral=True)
            else:
                # Mute for max allowed duration (28 days) as indefinite
                until = discord.utils.utcnow() + datetime.timedelta(days=28)
                await member.timeout(until, reason=reason or "Silenciado indefinidamente (hasta desmute)")
                await interaction.response.send_message(f"🔇 {user.mention} silenciado indefinidamente. Usa /unmute para quitarlo.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="unmute",
        description="🔊 Quita el silencio de un usuario"
    )
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

    @app_commands.command(
        name="nick",
        description="✏️ Cambia el apodo de un usuario"
    )
    @app_commands.describe(user="Usuario", nickname="Nuevo apodo (vacío para reset)")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nick(self, interaction: discord.Interaction, user: discord.User, nickname: Optional[str] = None):
        """Change user nickname"""
        try:
            member = await interaction.guild.fetch_member(user.id)
            await member.edit(nick=nickname)
            await interaction.response.send_message(f"✏️ Apodo de {user.mention} cambiado a: {nickname or 'reseteado'}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="softban",
        description="🔨 Softban: banea y desbanea para eliminar mensajes recientes"
    )
    @app_commands.describe(user="Usuario a softbanear", reason="Razón")
    @app_commands.checks.has_permissions(ban_members=True)
    async def softban(self, interaction: discord.Interaction, user: discord.User, reason: Optional[str] = None):
        """Softban a user (ban then unban to purge messages)"""
        try:
            await interaction.guild.ban(user, reason=reason or "Softban", delete_message_days=1)
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"🔨 {user.mention} ha sido softbaneado (mensajes eliminados).", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="slowmode",
        description="🐢 Ajusta el slowmode del canal (segundos)"
    )
    @app_commands.describe(seconds="Segundos de slowmode (0 para desactivar)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        """Set channel slowmode"""
        try:
            if seconds < 0 or seconds > 21600:
                await interaction.response.send_message("❌ Los segundos deben estar entre 0 y 21600", ephemeral=True)
                return
            await interaction.channel.edit(rate_limit_per_user=seconds)
            await interaction.response.send_message(f"🐢 Slowmode establecido a {seconds}s en este canal", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(
        name="sync",
        description="🔄 Sincroniza los comandos slash (admin only)"
    )
    @app_commands.describe(guild_id="ID opcional del servidor para sincronizar")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction: discord.Interaction, guild_id: Optional[int] = None):
        """Sync commands to Discord (global or guild)"""
        try:
            if guild_id:
                guild = discord.Object(id=guild_id)
                synced = await self.bot.tree.sync(guild=guild)
                await interaction.response.send_message(f"✅ Sincronizado {len(synced)} comandos en el servidor {guild_id}", ephemeral=True)
            else:
                synced = await self.bot.tree.sync()
                await interaction.response.send_message(f"✅ Sincronizado globalmente {len(synced)} comandos", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @tasks.loop(seconds=10)
    async def check_mutes(self):
        """Check if any mutes have expired"""
        # Placeholder for future persistent mute handling
        return

    @check_mutes.before_loop
    async def before_check_mutes(self):
        """Wait until bot is ready"""
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
