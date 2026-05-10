# TeoBotty - Discord Bot

Un bot de Discord modular y funcional con soporte para moderación, bienvenida, roles y diversión.

## ⚙️ Stack Tecnológico

- Python 3.8+
- discord.py 2.7.1
- SQLite para persistencia
- Arquitectura modular con Cogs

## 🎯 Características

- **Moderación**: lock, kick, ban, warn, clear, mute, unmute y más
- **Bienvenida/Despedida**: Mensajes personalizables
- **Autoroles**: Roles automáticos al entrar
- **Reaction Roles**: Menú interactivo por reacciones
- **Triggers**: Respuestas automáticas por palabras clave
- **Diversión**: dice, 8ball, RPS, hug, rate y más

## 🚀 Inicio Rápido

### Local

```bash
pip install -r requirements.txt
# Edita .env con tu DISCORD_TOKEN
python main.py
```

### Wispbyte Hosting

Ver `WISPBYTE_DEPLOYMENT.txt` para instrucciones completas.

## 📁 Estructura

```
teobot/
├── main.py              # Entrada principal
├── database.py          # SQLite
├── requirements.txt     # Dependencias
├── Procfile            # Para hosting
├── .env.example        # Plantilla
└── cogs/               # Módulos
    ├── moderation.py
    ├── welcome.py
    ├── roles.py
    ├── triggers.py
    └── fun.py
```

## 📝 Comandos

- `/dice` - Lanza un dado
- `/lock` - Bloquea el canal
- `/kick` - Expulsa usuario
- `/ban` - Banea usuario
- `/8ball` - Pregunta a la bola mágica
- Y muchos más...

## 💬 Soporte

Para problemas o preguntas, consulta la documentación incluida.

---

**TeoBotty** © 2026 - Bot de Discord moderno y escalable
