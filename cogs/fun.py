"""
Fun Cog - Comandos de diversión
Commands: dice, coinflip, rps, 8ball, quote, russian_roulette
"""

import discord
from discord.ext import commands
from discord import app_commands
import random
from typing import Optional


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.eight_ball_responses = [
            "Sí, definitivamente",
            "Es seguro que sí",
            "Outlook bueno",
            "Perspectiva positiva",
            "Pregunta nuevamente más tarde",
            "Concentrate y pregunta de nuevo",
            "Mejor no decirte ahora",
            "No se ve bien",
            "Muy dudoso",
            "Definitivamente no",
            "Sin lugar a dudas",
            "Absolutamente",
            "Probablemente",
            "Tal vez",
            "Nunca jamás"
        ]

    @app_commands.command(
        name="dice",
        description="🎲 Lanza un dado (1-6)"
    )
    async def dice(self, interaction: discord.Interaction):
        """Roll a dice"""
        result = random.randint(1, 6)
        emoji = ["", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"][result]
        
        embed = discord.Embed(
            title="🎲 Tirada de Dado",
            description=f"{emoji} Sacaste un **{result}**",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="coin",
        description="🪙 Lanza una moneda (Cara o Cruz)"
    )
    async def coin(self, interaction: discord.Interaction):
        """Flip a coin"""
        result = random.choice(["Cara", "Cruz"])
        emoji = "🟡" if result == "Cara" else "🔵"
        
        embed = discord.Embed(
            title="🪙 Lanzamiento de Moneda",
            description=f"{emoji} Salió **{result}**",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="rps",
        description="✌️ Piedra, Papel o Tijeras contra el bot"
    )
    @app_commands.describe(choice="Tu opción: piedra, papel o tijeras")
    async def rps(self, interaction: discord.Interaction, choice: str):
        """Rock, Paper, Scissors"""
        choice_lower = choice.lower()
        valid_choices = ["piedra", "papel", "tijeras"]
        
        if choice_lower not in valid_choices:
            await interaction.response.send_message(
                f"❌ Opción inválida. Elige entre: {', '.join(valid_choices)}",
                ephemeral=True
            )
            return
        
        bot_choice = random.choice(valid_choices)
        
        # Determinar ganador
        if choice_lower == bot_choice:
            result = "¡Empate! 🤝"
            color = discord.Color.yellow()
        elif (choice_lower == "piedra" and bot_choice == "tijeras") or \
             (choice_lower == "papel" and bot_choice == "piedra") or \
             (choice_lower == "tijeras" and bot_choice == "papel"):
            result = "¡Ganaste! 🎉"
            color = discord.Color.green()
        else:
            result = "¡Perdiste! 😢"
            color = discord.Color.red()
        
        embed = discord.Embed(
            title="✌️ Piedra, Papel o Tijeras",
            color=color
        )
        embed.add_field(name="Tu opción", value=choice_lower.capitalize(), inline=True)
        embed.add_field(name="Mi opción", value=bot_choice.capitalize(), inline=True)
        embed.add_field(name="Resultado", value=result, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="8ball",
        description="🔮 Pregunta a la bola mágica del destino"
    )
    @app_commands.describe(question="Tu pregunta al destino")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        """Magic 8 ball"""
        response = random.choice(self.eight_ball_responses)
        
        embed = discord.Embed(
            title="🔮 Bola Mágica del Destino",
            color=discord.Color.purple()
        )
        embed.add_field(name="Tu pregunta", value=question, inline=False)
        embed.add_field(name="Respuesta", value=f"**{response}**", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="quote",
        description="💬 Genera una cita aleatoria motivacional"
    )
    async def quote(self, interaction: discord.Interaction):
        """Get a random quote"""
        quotes = [
            "La vida es aquello que sucede mientras estás ocupado haciendo otros planes. - John Lennon",
            "El futuro pertenece a quienes creen en la belleza de sus sueños. - Eleanor Roosevelt",
            "Es durante nuestros momentos más oscuros que debemos enfocarnos en ver la luz. - Aristóteles",
            "Lo único que tenemos que temer es al miedo mismo. - Franklin D. Roosevelt",
            "La única forma de hacer un gran trabajo es amar lo que haces. - Steve Jobs",
            "Si no puedes volar, corre. Si no puedes correr, camina. Si no puedes caminar, arrastra. - Martin Luther King Jr.",
            "Todo lo que siempre quisiste está al otro lado del miedo. - George Addair",
            "Sé la mejor versión de ti mismo. - Wayne Dyer",
            "No busques convertirte en una persona de éxito, busca convertirte en una persona de valor. - Albert Einstein",
            "La vida es lo que sucede cuando estás ocupado haciendo planes. - John Lennon"
        ]
        
        quote = random.choice(quotes)
        
        embed = discord.Embed(
            title="💬 Cita del Día",
            description=quote,
            color=discord.Color.blurple()
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="roulette",
        description="🎰 Ruleta rusa (50% de probabilidad de ganar)"
    )
    async def roulette(self, interaction: discord.Interaction):
        """Russian roulette (fun)"""
        result = random.choice([True, False])
        
        if result:
            embed = discord.Embed(
                title="🎰 Ruleta Rusa",
                description="¡SOBREVIVISTE! 🎉",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="🎰 Ruleta Rusa",
                description="¡BANG! 💀 No tuviste suerte",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="hug",
        description="🤗 Dale un abrazo a alguien"
    )
    @app_commands.describe(user="Usuario a abrazar")
    async def hug(self, interaction: discord.Interaction, user: discord.User):
        """Hug someone"""
        if user.id == interaction.user.id:
            embed = discord.Embed(
                title="🤗 Autorrazo",
                description=f"{interaction.user.mention} se da un abrazo a sí mismo",
                color=discord.Color.pink()
            )
        else:
            embed = discord.Embed(
                title="🤗 Abrazo",
                description=f"{interaction.user.mention} abraza a {user.mention}",
                color=discord.Color.pink()
            )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="rate",
        description="⭐ Califica algo o a alguien (1-10)"
    )
    @app_commands.describe(target="Qué o quién deseas calificar")
    async def rate(self, interaction: discord.Interaction, target: str):
        """Rate something"""
        rating = random.randint(1, 10)
        stars = "⭐" * rating + "☆" * (10 - rating)
        
        embed = discord.Embed(
            title="⭐ Calificación",
            color=discord.Color.gold()
        )
        embed.add_field(name="Objeto", value=target, inline=False)
        embed.add_field(name="Calificación", value=f"{stars} **{rating}/10**", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="choose",
        description="🎲 Elige aleatoriamente entre opciones"
    )
    @app_commands.describe(options="Opciones separadas por comas (ej: pizza, burger, taco)")
    async def choose(self, interaction: discord.Interaction, options: str):
        """Choose randomly from options"""
        choices = [opt.strip() for opt in options.split(",")]
        
        if len(choices) < 2:
            await interaction.response.send_message(
                "❌ Debes proporcionar al menos 2 opciones separadas por comas",
                ephemeral=True
            )
            return
        
        chosen = random.choice(choices)
        
        embed = discord.Embed(
            title="🎲 Elección Aleatoria",
            description=f"Elegí: **{chosen}**",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
