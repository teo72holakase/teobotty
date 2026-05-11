# 🤖 TeoBotty - Discord Bot Completo

> Un bot de Discord modular y avanzado con sistema de tickets profesional, moderación, roles, sugerencias, votaciones y mucho más.

## 📋 Tabla de Contenidos

- [🚀 Instalación](#-instalación)
- [⚙️ Configuración](#️-configuración)
- [📚 Comandos](#-comandos)
  - [🎫 Sistema de Tickets](#-sistema-de-tickets)
  - [👮 Moderación](#-moderación)
  - [👥 Roles y Autoroles](#-roles-y-autoroles)
  - [💬 Bienvenida y Despedida](#-bienvenida-y-despedida)
  - [🎯 Triggers](#-triggers)
  - [🎉 Diversión](#-diversión)
  - [💡 Sugerencias](#-sugerencias)
  - [🗳️ Votaciones](#️-votaciones)
  - [ℹ️ Información](#️-información)
- [🔧 Solución de Problemas](#-solución-de-problemas)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🤝 Contribución](#-contribución)

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- Token de bot de Discord

### Pasos de Instalación

1. **Clona o descarga el proyecto**
   ```bash
   cd c:\Users\teo72\Downloads\teobot
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura el token de Discord**
   - Crea un archivo `.env` en la raíz del proyecto
   - Agrega tu token:
   ```
   DISCORD_TOKEN=tu_token_aqui
   DATABASE_PATH=./bot_data.db
   ```

4. **Ejecuta el bot**
   ```bash
   python main.py
   ```

### Obtener Token de Discord
1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea una nueva aplicación
3. Ve a la pestaña "Bot" y crea un bot
4. Copia el token
5. Invita el bot a tu servidor con permisos de administrador

---

## ⚙️ Configuración

### Variables de Entorno (.env)
```env
DISCORD_TOKEN=tu_token_real_aqui
DATABASE_PATH=./bot_data.db
```

### Permisos Recomendados del Bot
- Administrador (para funcionalidades completas)
- O permisos específicos:
  - Gestionar roles
  - Gestionar canales
  - Gestionar mensajes
  - Banear miembros
  - Expulsar miembros
  - Moderar miembros

---

## 📚 Comandos

### 🎫 Sistema de Tickets

Sistema completo de tickets similar a TicketKing/Tickets.gg

#### Configuración de Tipos de Tickets
- `/create_ticket_type <name> <mention_roles> <close_permissions> <log_channel> <archive_channel> <category>`
  - Crea un nuevo tipo de ticket
  - `mention_roles`: IDs de roles separados por comas
  - `close_permissions`: IDs de roles que pueden cerrar tickets

- `/list_ticket_types`
  - Muestra todos los tipos de ticket configurados

#### Creación de Paneles de Tickets (2 pasos)
**Paso 1:** `/create_ticket_panel <channel> <title> <description> <color> [image]`
- Configura el embed del panel
- `color`: Color en formato hex (#FF0000)

**Paso 2:** `/configure_ticket_panel <selection_type> <ticket_config>`
- Configura cómo seleccionar tickets
- `selection_type`: `button`, `list`, o `emoji`
- `ticket_config`: Formato depende del tipo:
  - **Emoji**: `ID:emoji` (ej: `1:🎫,2:📋`)
  - **Botón**: `ID:emoji:texto:color` (ej: `1:🎫:Crear Ticket:primary`)
  - **Lista**: `ID:posición:emoji:texto` (ej: `1:1:🎫:Reportes`)

#### Gestión de Tickets
- `/close_ticket`
  - Cierra el ticket actual (verifica permisos)

- `/add_to_ticket <user>`
  - Añade un usuario al ticket actual

### 👮 Moderación

*Nota: El cog de moderación fue removido. Los comandos de moderación están disponibles en otros cogs.*

### 👥 Roles y Autoroles

#### Autoroles
- `/add_autorole <role>`
  - Añade un rol que se asigna automáticamente a nuevos miembros

- `/remove_autorole <role>`
  - Elimina un autorol

- `/list_autoroles`
  - Muestra todos los autoroles configurados

#### Reaction Roles
- `/add_reaction_role <message_id> <emoji> <role>`
  - Crea un rol que se asigna al reaccionar a un mensaje
  - El bot añade automáticamente el emoji al mensaje

- `/remove_reaction_role <message_id> <emoji>`
  - Elimina un reaction role

### 💬 Bienvenida y Despedida

- `/set_welcome <channel> <message>`
  - Configura mensaje de bienvenida
  - Variables disponibles: `{user}`, `{username}`, `{guild}`

- `/set_farewell <channel> <message>`
  - Configura mensaje de despedida
  - Variables disponibles: `{user}`, `{username}`, `{guild}`

- `/test_welcome`
  - Prueba el mensaje de bienvenida

### 🎯 Triggers

Sistema de respuestas automáticas por palabras clave

- `/add_trigger <keyword> <response>`
  - Añade una respuesta automática
  - Variables disponibles: `{user}`, `{username}`, `{message}`

- `/remove_trigger <keyword>`
  - Elimina un trigger

- `/list_triggers`
  - Muestra todos los triggers configurados

### 🎉 Diversión

- `/dice`
  - Lanza un dado (1-6)

- `/coin`
  - Lanza una moneda (Cara/Cruz)

- `/rps <choice>`
  - Piedra, papel o tijeras contra el bot

- `/8ball <question>`
  - Pregunta a la bola mágica del destino

- `/quote`
  - Cita motivacional aleatoria

- `/roulette`
  - Ruleta rusa (50% de probabilidad)

- `/hug <user>`
  - Abraza a un usuario

- `/rate <target>`
  - Califica algo o alguien (1-10)

- `/choose <options>`
  - Elige aleatoriamente entre opciones

### 💡 Sugerencias

Sistema de sugerencias con embeds automáticos

- `/set_suggestions <channel>`
  - Configura el canal de sugerencias

- `/unset_suggestions`
  - Elimina el canal de sugerencias

**Funcionamiento automático:**
- Los mensajes en el canal configurado se convierten automáticamente en embeds
- Se añade el autor, foto de perfil y contenido
- Reacciones automáticas: ⬆️ (aprobar) y ⬇️ (rechazar)
- Soporte para imágenes adjuntas

### 🗳️ Votaciones

- `/create_poll <question> <options> [everyone] [image1] [image2] [image3]`
  - Crea una votación con múltiples opciones
  - `options`: Separadas por `;` (ej: `Sí;No;Tal vez`)
  - `everyone`: `true` para mencionar @everyone
  - Soporte hasta 3 imágenes

### ℹ️ Información

- `/userinfo [user]`
  - Información detallada de un usuario
  - Roles, fecha de unión, cuenta creada, etc.

- `/serverinfo`
  - Información del servidor
  - Miembros, canales, roles, nivel de boost, etc.

---

## 🔧 Solución de Problemas

### Problemas Comunes

#### ❌ "ModuleNotFoundError: No module named 'discord'"
**Solución:**
```bash
pip install -r requirements.txt
```

#### ❌ "No module named 'audioop'" (Python 3.14+)
**Solución:** Las dependencias ya están actualizadas en `requirements.txt` para ser compatibles.

#### ❌ "DISCORD_TOKEN not found in .env file"
**Solución:**
1. Asegúrate de que el archivo `.env` existe
2. Verifica que contiene: `DISCORD_TOKEN=tu_token_real`
3. Reinicia el bot

#### ❌ Los comandos no aparecen en Discord
**Solución:**
- Espera hasta 1 hora para que Discord sincronice los comandos
- Reinicia el bot
- Verifica que el bot tiene permisos de aplicación.commands

#### ❌ Error de permisos en comandos
**Solución:**
- Asegúrate de que el bot tiene los permisos necesarios
- Para comandos administrativos, el usuario debe tener permisos de administrador

#### ❌ El bot no responde
**Solución:**
1. Verifica que el token es correcto
2. Comprueba que el bot está online en Discord
3. Revisa los logs de la consola para errores

#### ❌ Problemas con la base de datos
**Solución:**
- Elimina `bot_data.db` y reinicia el bot (se recreará automáticamente)
- Asegúrate de que la carpeta tiene permisos de escritura

### Comandos de Debug

Ejecuta `python verificar.py` para verificar que todo está configurado correctamente.

### Logs y Debugging

El bot muestra logs detallados en la consola:
- ✅ Cogs cargados exitosamente
- ✅ Base de datos inicializada
- ✅ Comandos sincronizados
- ❌ Errores específicos

---

## 📁 Estructura del Proyecto

```
teobot/
├── main.py              # Archivo principal del bot
├── database.py          # Gestión de base de datos SQLite
├── verificar.py         # Script de verificación
├── requirements.txt     # Dependencias Python
├── Procfile            # Para deployment en hosting
├── .env                # Variables de entorno (crear)
├── .env.example        # Plantilla de variables
├── .gitignore          # Archivos ignorados por Git
├── README.md           # Esta documentación
└── cogs/               # Módulos del bot
    ├── fun.py          # Comandos de diversión
    ├── info.py         # Comandos informativos
    ├── roles.py        # Gestión de roles
    ├── social.py       # Sugerencias y votaciones
    ├── tickets.py      # Sistema de tickets
    ├── triggers.py     # Respuestas automáticas
    ├── welcome.py      # Bienvenida y despedida
    └── __init__.py     # Inicialización de cogs
```

---

## 🤝 Contribución

### Agregar Nuevos Cogs
1. Crea un nuevo archivo en `cogs/nombre_cog.py`
2. Implementa la clase cog heredando de `commands.Cog`
3. Agrega la función `setup(bot)` al final
4. El bot cargará automáticamente el nuevo cog

### Convenciones de Código
- Usa comandos slash (`app_commands`) para nueva funcionalidad
- Incluye descripciones detalladas en los comandos
- Maneja errores apropiadamente
- Usa embeds para respuestas visuales
- Documenta las funciones con docstrings

### Reportar Bugs
Si encuentras un bug, incluye:
- Pasos para reproducirlo
- Mensaje de error completo
- Versión de Python y discord.py
- Sistema operativo

---

## 📄 Licencia

Este proyecto es de uso personal. Siéntete libre de modificarlo y adaptarlo a tus necesidades.

---

**TeoBotty** - Bot de Discord moderno, modular y escalable 🤖✨
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
