# 🤖 TeoBotty

Bot modular de Discord con sistema de tickets, roles, sugerencias, votaciones y más.

## ✨ Características principales

- Ticket system con tipos y paneles de selección (emoji, botones, lista)
- Autoroles automáticos y reaction roles
- Bienvenida / despedida con mensajes personalizados
- Triggers basados en palabras clave
- Sistema de sugerencias con reacciones
- Votaciones con opciones separadas por `;`
- Creador de embeds interactivo
- Keep-alive automático para evitar que el host suspenda el bot
- Almacenamiento persistente en SQLite

## 🚀 Instalación

1. Activa tu entorno virtual (recomendado):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. Instala dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
3. Crea un archivo `.env` en la raíz del proyecto con los valores necesarios.
4. Ejecuta el bot:
   ```powershell
   python main.py
   ```

## ⚙️ Configuración

Crea `.env` con al menos estas variables:

```env
DISCORD_TOKEN=tu_token_real_aqui
DATABASE_PATH=./bot_data.db
```

Opcionalmente, agrega estas variables para el Keep-Alive:

```env
KEEP_ALIVE_GUILD_ID=123456789
KEEP_ALIVE_CHANNEL_ID=987654321
```

> `DISCORD_TOKEN` es obligatorio. `KEEP_ALIVE_*` solo se usa si quieres que el bot reaccione periódicamente en un canal.

## 📚 Comandos principales

### Bienvenida / despedida
- `/set_welcome`
- `/set_farewell`
- `/test_welcome`

### Roles
- `/add_autorole`
- `/remove_autorole`
- `/list_autoroles`
- `/add_reaction_role`
- `/remove_reaction_role`

### Triggers
- `/add_trigger`
- `/remove_trigger`
- `/list_triggers`

### Tickets
- `/create_ticket_type`
- `/list_ticket_types`
- `/delete_ticket_type`
- `/create_ticket_panel`
- `/configure_ticket_panel`

### Social
- `/set_suggestions`
- `/unset_suggestions`
- `/create_poll`

### Utilidad
- `/create_embed`
- `/set_keep_alive`

## 📝 Notas de uso

- El bot usa **slash commands** (`/`) y no depende de un prefijo clásico.
- Las sugerencias se generan automáticamente cuando un mensaje se publica en el canal configurado con `/set_suggestions`.
- La tarea de keep-alive se ejecuta cada 20 minutos y reaccionará en el canal configurado.

## 📁 Estructura del proyecto

```
teobot/
├── main.py
├── database.py
├── verificar.py
├── requirements.txt
├── Procfile
├── README.md
├── .env
└── cogs/
    ├── __init__.py
    ├── tickets.py
    ├── roles.py
    ├── welcome.py
    ├── triggers.py
    ├── fun.py
    ├── social.py
    ├── info.py
    └── keep_alive.py
```

## 🛠️ Problemas comunes

- `ModuleNotFoundError: No module named 'discord'` → instala dependencias con `pip install -r requirements.txt`
- `DISCORD_TOKEN not found` → verifica que `.env` contenga `DISCORD_TOKEN`
- Comandos no aparecen → espera unos minutos y verifica permisos del bot
- El bot no responde → ejecuta `python main.py` y revisa la consola

## 📄 Licencia

Proyecto de uso personal. Modifica y adapta según tus necesidades.
