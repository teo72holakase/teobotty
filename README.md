# 🤖 TeoBotty - Discord Bot en Python

Bot de Discord modular y escalable construido con **discord.py**, **Cogs**, **SlashCommands** y **SQLite**.

## 📋 Características

✅ **Sistema de Bienvenida/Despedida** - Mensajes personalizados con variables
✅ **Moderación** - Bloqueo de canales, silencio temporal, gestión de roles, información de usuario/servidor
✅ **Autoroles** - Asignar roles automáticamente al entrar
✅ **Reaction Roles** - Menús interactivos con reacciones
✅ **Triggers** - Respuestas automáticas a palabras clave configurables
✅ **Diversión** - Comandos entretenidos (dice, 8ball, coin, rps, etc.)
✅ **Arquitectura Modular** - Fácil de extender con nuevos Cogs
✅ **Base de Datos SQLite** - Persistencia local de configuraciones
✅ **Estado personalizado** - Viendo JoJos Bizarre Adventure 👑

---

## 🚀 Instalación Rápida

### 1️⃣ Clonar/Descargar el Proyecto
```bash
cd c:\Users\teo72\Downloads\teobot
```

### 2️⃣ Crear Entorno Virtual (Recomendado)
```bash
python -m venv venv
```

**Activar el entorno:**

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

**Salida esperada:**
```
Successfully installed discord.py-2.7.1 python-dotenv-1.0.0 aiosqlite-0.19.0 audioop-lts-0.2.2
```

### 4️⃣ Configurar el Token

1. Copia `.env.example` a `.env`:
```bash
copy .env.example .env
```

2. Abre `.env` y reemplaza `tu_token_aqui` con tu token de Discord:
```
DISCORD_TOKEN=tu_token_real_aqui
DATABASE_PATH=./bot_data.db
```

**¿Cómo obtener el token?**
1. Ve a https://discord.com/developers/applications
2. Crea una "New Application"
3. Ve a "Bot" → "Add Bot"
4. Copia el token bajo "TOKEN"
5. En "OAuth2" → "URL Generator":
   - Selecciona scopes: `bot`
   - Selecciona permisos: `administrator` (o los que necesites)
   - Copia la URL generada y abre en el navegador para invitar el bot

### 5️⃣ Ejecutar el Bot

**Opción 1: Desde CMD/PowerShell**
```bash
python main.py
```

**Opción 2: Crear un batch (Windows)**

Crea un archivo `run.bat` en la carpeta del proyecto:
```batch
@echo off
python main.py
pause
```

Luego solo abre `run.bat` haciendo doble clic.

**Salida esperada:**
```
INFO:root:✅ Database initialized
INFO:root:✅ Loaded cog: moderation
INFO:root:✅ Loaded cog: welcome
INFO:root:✅ Loaded cog: roles
INFO:root:✅ Loaded cog: triggers
INFO:root:✅ Loaded cog: fun
INFO:root:✅ Bot logged in as TeoBotty#0000
INFO:root:✅ Synced X slash commands
```

---

## 📖 Comandos Disponibles

### 🔒 Moderación (`/lock`, `/unlock`, `/tempmute`, `/rolve`, `/userinfo`, `/serverinfo`, y más)

```bash
/lock                          # Bloquea el canal actual
/unlock                        # Desbloquea el canal actual
/tempmute <usuario> <segundos> [razón]   # Silencia temporalmente
/rolve <usuario> <rol>        # Da/quita un rol
/userinfo [usuario]           # Información del usuario
/serverinfo                   # Información del servidor
/mute <usuario> [segundos]    # Silencia un usuario
/unmute <usuario>             # Desmutea un usuario
/kick <usuario> [razón]       # Expulsa un usuario
/ban <usuario> [razón]        # Banea un usuario
/unban <usuario>              # Desbanea un usuario
/warn <usuario> [razón]       # Advierte un usuario
/clear <cantidad>             # Elimina mensajes
```

### 🎉 Bienvenida (`/set_welcome`, `/set_farewell`, `/test_welcome`)

```bash
/set_welcome <canal> <mensaje>    # Configura bienvenida
/set_farewell <canal> <mensaje>   # Configura despedida
/test_welcome                     # Prueba el mensaje
```

**Ejemplo:**
```
/set_welcome #bienvenida "¡Bienvenido {user}! Somos {guild}. Mensajes: {username}"
```

### ⭐ Roles (`/add_autorole`, `/remove_autorole`, `/list_autoroles`, `/add_reaction_role`, `/remove_reaction_role`)

```bash
/add_autorole <rol>                                    # Agregar autorole
/remove_autorole <rol>                                 # Eliminar autorole
/list_autoroles                                        # Ver autoroles
/add_reaction_role <message_id> <emoji> <rol>         # Crear reaction role
/remove_reaction_role <message_id> <emoji>            # Eliminar reaction role
```

### 🔔 Triggers (`/add_trigger`, `/remove_trigger`, `/list_triggers`)

```bash
/add_trigger <palabra> <respuesta>      # Agregar trigger
/remove_trigger <palabra>               # Eliminar trigger
/list_triggers                         # Ver triggers
```

**Ejemplo:**
```
/add_trigger "hola" "¡Hola {user}! Bienvenido al servidor 👋"
/add_trigger "ayuda" "Para ayuda, contacta con los moderadores"
```

### 🎮 Diversión (`/dice`, `/8ball`, `/coin`, `/rps`, `/quote`, `/roulette`, `/hug`, `/rate`, `/choose`)

```bash
/dice                         # 🎲 Lanza un dado
/coin                         # 🪙 Lanza una moneda
/rps                          # ✌️ Piedra, Papel o Tijeras
/8ball                        # 🔮 Bola mágica (haz una pregunta)
/quote                        # 💬 Cita motivacional aleatoria
/roulette                     # 🎰 Ruleta rusa
/hug <usuario>                # 🤗 Abraza a alguien
/rate [cosa]                  # ⭐ Califica algo
/choose <opción1> <opción2>   # 🎲 Elige aleatoriamente
```

---

## 📁 Estructura del Proyecto

```
teobot/
├── main.py                    # Punto de entrada del bot
├── database.py               # Módulo de SQLite
├── requirements.txt          # Dependencias (discord.py 2.7.1+)
├── .env                      # Configuración (crear desde .env.example)
├── .env.example             # Plantilla de .env
├── .gitignore               # Archivos a ignorar en Git
├── Procfile                 # Configuración para hosting (Wispbyte)
├── bot_data.db              # Base de datos (se crea automáticamente)
└── cogs/
    ├── __init__.py
    ├── moderation.py         # 17 comandos de moderación
    ├── welcome.py            # Sistema de bienvenida
    ├── roles.py              # Sistema de roles y autoroles
    ├── triggers.py           # Respuestas automáticas
    └── fun.py                # 9 comandos de diversión
```

---

## 🔧 Solución de Problemas

### ❌ "DISCORD_TOKEN not found"
- Verifica que el archivo `.env` existe y tiene el formato correcto
- Asegúrate de reemplazar `tu_token_aqui` con tu token real

### ❌ "No module named 'discord'"
- Ejecuta: `pip install -r requirements.txt`
- Si estás en un entorno virtual, verifica que está activado

### ❌ "Connection refused"
- Verifica que tu token es válido
- Asegúrate que el bot tiene los permisos correctos en el servidor

### ❌ "Database is locked"
- Cierra otras instancias del bot
- Elimina `bot_data.db` y vuelve a ejecutar (perderá las configuraciones)

---

## 🛠️ Agregar Nuevos Cogs

1. Crea un archivo en `cogs/mi_cog.py`:

```python
from discord.ext import commands
from discord import app_commands
import discord

class MiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="micomando")
    async def mi_comando(self, interaction: discord.Interaction):
        await interaction.response.send_message("¡Hola!")

async def setup(bot: commands.Bot):
    await bot.add_cog(MiCog(bot))
```

2. El bot automáticamente cargará cualquier archivo `.py` en `cogs/`

---

## 📝 Variables Disponibles en Mensajes

- `{user}` - Mención del usuario
- `{username}` - Nombre del usuario
- `{guild}` - Nombre del servidor
- `{message}` - Contenido del mensaje (solo triggers)

---

## 🔐 Permisos Necesarios

Asegúrate de que el bot tiene estos permisos en Discord:
- ✅ Manage Messages
- ✅ Manage Roles
- ✅ Manage Channels
- ✅ Moderate Members
- ✅ Send Messages
- ✅ Read Message History
- ✅ React to Messages (para reaction roles)

---

## 🌐 Despliegue en Wispbyte (Hosting 24/7)

Para desplegar el bot en Wispbyte:

1. Lee el archivo `WISPBYTE_DEPLOYMENT.txt` en la carpeta del proyecto
2. Sigue los pasos exactos para conectar tu repositorio
3. Configura las variables de entorno: `DISCORD_TOKEN`
4. El bot estará online 24/7

---

## 📞 Soporte

Para problemas o sugerencias, verifica que:
1. Tienes Python 3.8+ instalado: `python --version`
2. Todas las dependencias están instaladas: `pip list`
3. El token es válido y el bot está invitado al servidor

---

**¡Disfruta tu TeoBotty! 🚀**
