# 🤖 TeoBotty - Discord Bot Modular

> Un bot de Discord profesional y modular con **sistema de tickets avanzado**, gestión de roles, autoroles, sugerencias, votaciones, diversión y más.

## 📋 Tabla de Contenidos

- [✨ Características](#-características)
- [🚀 Instalación](#-instalación)
- [⚙️ Configuración](#️-configuración)
- [📚 Comandos](#-comandos)
  - [🎫 Sistema de Tickets](#-sistema-de-tickets)
  - [🔐 Roles y Autoroles](#-roles-y-autoroles)
  - [💬 Bienvenida y Despedida](#-bienvenida-y-despedida)
  - [🎯 Triggers](#-triggers)
  - [🎉 Diversión](#-diversión)
  - [💡 Sugerencias](#-sugerencias)
  - [🗳️ Votaciones](#️-votaciones)
  - [ℹ️ Información](#️-información)
- [⏰ Keep-Alive (Anti-Sueño)](#️-keep-alive-anti-sueño)
- [🔧 Solución de Problemas](#-solución-de-problemas)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)

---

## ✨ Características

| Característica | Descripción |
|---|---|
| **🎫 Sistema de Tickets** | Panel configurable con reacciones, botones o listas. Múltiples tipos de tickets con permisos personalizados |
| **🔐 Gestión de Roles** | Autoroles automáticos, reaction roles, gestión avanzada |
| **💬 Bienvenida/Despedida** | Mensajes personalizables con variables dinámicas |
| **🎯 Triggers** | Respuestas automáticas basadas en palabras clave |
| **🎉 Diversión** | Dados, monedas, juegos interactivos, citas |
| **💡 Sugerencias** | Sistema completo con embeds automáticos |
| **🗳️ Votaciones** | Crear encuestas con múltiples opciones |
| **🎨 Creador de Embeds** | Constructor interactivo de embeds personalizados |
| **ℹ️ Info** | Información de usuarios y servidor |
| **⏰ Keep-Alive** | Tarea periódica para mantener el servidor activo |
| **🗄️ Base de Datos** | SQLite para almacenamiento persistente |

---

## 🚀 Instalación

### Requisitos
- Python 3.8+
- Token de bot de Discord

### Pasos

1. **Clonar/Descargar el proyecto**
   ```bash
   cd c:\Users\teo72\Downloads\teobot
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Crear archivo `.env`**
   ```bash
   # Copiar desde .env.example o crear manual
   echo DISCORD_TOKEN=tu_token_aqui > .env
   echo DATABASE_PATH=./bot_data.db >> .env
   ```

4. **Ejecutar el bot**
   ```bash
   python main.py
   ```

### Obtener Token de Discord
1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea nueva aplicación
3. Ve a "Bot" y crea un bot
4. Copia el token
5. Invita el bot al servidor con permisos de administrador

---

## ⚙️ Configuración

### Variables de Entorno (.env)
```env
DISCORD_TOKEN=tu_token_real_aqui
DATABASE_PATH=./bot_data.db
KEEP_ALIVE_GUILD_ID=123456789
KEEP_ALIVE_CHANNEL_ID=987654321
```

### Permisos Recomendados
- Administrador (más fácil)
- O permisos específicos: Gestionar roles, canales, mensajes, reaccionar

---

## 📚 Comandos

### � Creador de Embeds

```
/create_embed           # Abre el creador de embeds interactivo
```

**Funcionamiento:**
1. Abre un modal para ingresa el título, descripción y color
2. Muestra botones para editar cada parte del embed
3. Permite previsualizar el embed
4. Opción para enviar a cualquier canal

**Características:**
- Editar título, descripción y color
- Vista previa instantánea
- Seleccionar canal para enviar
- Interfaz intuitiva con botones

---

### �🎫 Sistema de Tickets

Sistema completo de tickets similar a TicketKing/Tickets.gg

#### Crear Tipo de Ticket
```
/create_ticket_type
  nombre: "Soporte"
  mention_roles: "123456789,987654321"
  close_permissions: "123456789"
  log_channel: #ticket-logs
  category: Tickets
```

**Parámetros:**
- `nombre`: Nombre del tipo
- `mention_roles`: Roles a mencionar (IDs separadas por comas)
- `close_permissions`: Roles que pueden cerrar
- `log_channel`: Canal de logs
- `category`: Categoría de Discord

#### Listar Tipos
```
/list_ticket_types      # Ver todos los tipos configurados
```

#### Crear Panel - Paso 1
```
/create_ticket_panel
  channel: #tickets
  title: 📞 Centro de Soporte
  description: Haz click para crear un ticket
  color: #3498DB
  image: https://... (opcional)
```

#### Crear Panel - Paso 2
```
/configure_ticket_panel
  selection_type: "Reacciones (Emoji)"
  ticket_config: "1:🎫,2:📋,3:⚠️"
```

**Tipos de selección:**
- **🎫 Emoji**: Formato `ID:emoji` (ej: `1:🎫,2:📋`)
- **🔘 Botones**: Formato `ID:emoji:texto:color` (ej: `1:🎫:Ticket:primary`)
- **📋 Lista**: Formato `ID:posición:emoji:texto` (ej: `1:1:🎫:Soporte`)

#### Gestionar Tickets
```
/close_ticket           # Cierra el ticket actual
/add_to_ticket @user    # Añade usuario al ticket
```

---

### 🔐 Roles y Autoroles

#### Autoroles
```
/add_autorole @Rol              # Añade autorol
/remove_autorole @Rol           # Elimina autorol
/list_autoroles                 # Ver todos
```

#### Reaction Roles
```
/add_reaction_role
  message_id: 123456789
  emoji: 🎮
  role: @Gamers

/remove_reaction_role 123456789 🎮
```

---

### 💬 Bienvenida y Despedida

```
/set_welcome
  channel: #bienvenida
  message: ¡Bienvenido {user} a {guild}!

/set_farewell
  channel: #despedidas
  message: {username} se fue del servidor

/test_welcome           # Prueba el mensaje
```

**Variables:** `{user}`, `{username}`, `{guild}`

---

### 🎯 Triggers

```
/add_trigger
  keyword: "hola"
  response: "¡Hola {user}! 👋"

/remove_trigger hola
/list_triggers
```

**Variables:** `{user}`, `{username}`, `{message}`

---

### 🎉 Diversión

```
/dice                    # Dado 1-6
/coin                    # Cara o Cruz
/rps piedra              # Piedra, papel, tijeras
/8ball ¿Lluverá?         # Bola mágica
/quote                   # Cita inspiradora
/roulette                # Ruleta rusa
/hug @usuario            # Abrazo
/rate algo               # Califica 1-10
/choose opción1;opción2  # Elige aleatoriamente
```

---

### 💡 Sugerencias

```
/set_suggestions #sugerencias       # Activar sistema
/unset_suggestions                  # Desactivar

# Ahora, mensajes en ese canal se convierten en sugerencias
# Con reacciones automáticas: ⬆️ ⬇️
```

---

### 🗳️ Votaciones

```
/create_poll
  question: "¿Cuál color?"
  options: "Rojo;Azul;Verde"
  everyone: false
  image1: https://... (opcional)
```

---

### ℹ️ Información

```
/userinfo               # Tu información
/userinfo @user         # Info de otro usuario
/serverinfo             # Información del servidor
```

---

## ⏰ Keep-Alive (Anti-Sueño)

**¿Qué es?**
- Tarea automática que se ejecuta cada 20 minutos
- Reacciona a un mensaje en un canal designado
- Mantiene el servidor host activo

**¿Por qué?**
- Hosting gratuito (Railway, Render) suspende bots inactivos
- Esta función lo evita

**¿Cómo configurar?**

1. **Ejecuta el comando en Discord:**
   ```
   /set_keep_alive #canal-importante
   ```
   El bot te mostrará los IDs necesarios

2. **Edita `.env` con los IDs:**
   ```env
   KEEP_ALIVE_GUILD_ID=123456789
   KEEP_ALIVE_CHANNEL_ID=987654321
   ```

3. **Reinicia el bot:**
   ```bash
   python main.py
   ```

**¿Qué hace?**
- Cada 20 minutos reacciona con ❤️ al último mensaje
- Mantiene el servidor "despierto"

**¿Sin configurar?**
- Solo hace logs, el bot sigue funcionando igual

---

## 📝 Prefijo de Comandos

- **Slash commands (/)**: Todos los comandos principales (recomendado)
- **Prefix (°)**: Para comandos legacy si es necesario

---

## 🔧 Solución de Problemas

### ❌ "ModuleNotFoundError: No module named 'discord'"
```bash
pip install -r requirements.txt
```

### ❌ "DISCORD_TOKEN not found"
1. Verifica que `.env` existe
2. Contiene: `DISCORD_TOKEN=tu_token_real`
3. Reinicia el bot

### ❌ Los comandos no aparecen
- Espera 1-5 minutos
- Reinicia Discord
- Verifica permisos del bot

### ❌ El bot no responde
1. Token correcto en `.env`
2. Bot online en Discord
3. Verifica los logs: `python main.py`

### ❌ Error "No module named 'audioop'" (Python 3.14+)
- Las dependencias en `requirements.txt` están actualizadas
- Reinstala: `pip install -r requirements.txt --force-reinstall`

### ❌ Problemas con base de datos
```bash
# Eliminar BD (se recrea automáticamente)
rm bot_data.db
python main.py
```

---

## 📁 Estructura del Proyecto

```
teobot/
├── main.py                  # Archivo principal
├── database.py              # Base de datos SQLite
├── verificar.py             # Script de verificación
├── requirements.txt         # Dependencias Python
├── Procfile                 # Para deploy
├── README.md                # Este archivo
├── .env                     # Variables (crear)
├── .env.example             # Template
└── cogs/                    # Módulos del bot
    ├── __init__.py
    ├── tickets.py           # Sistema de tickets
    ├── roles.py             # Gestión de roles
    ├── welcome.py           # Bienvenida/Despedida
    ├── triggers.py          # Respuestas automáticas
    ├── fun.py               # Diversión
    ├── social.py            # Sugerencias/Votaciones
    ├── info.py              # Información
    └── keep_alive.py        # Keep-Alive
```

---

## 📊 Información Técnica

- **Lenguaje**: Python 3.8+
- **Framework**: discord.py 2.7+
- **Base de Datos**: SQLite3
- **Módulos**: 8 cogs funcionales
- **Comandos**: 40+ slash commands
- **Tablas BD**: 8

---

## 🤝 Soporte

- Verifica los logs en consola
- Lee el código (está comentado)
- Usa `python verificar.py` para debug

---

**¡Tu servidor de Discord nunca fue tan profesional! 🚀**
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
    ├── tickets.py            # Sistema completo de tickets
    ├── welcome.py            # Sistema de bienvenida
    ├── roles.py              # Sistema de roles y autoroles
    ├── triggers.py           # Respuestas automáticas
    ├── social.py             # Sugerencias y votaciones
    └── info.py               # Comandos informativos
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
