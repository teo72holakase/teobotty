"""
Database module for TeoBot
Handles SQLite operations for welcome, autoroles, reaction roles, and triggers
"""

import aiosqlite
import os
from typing import Optional, List, Dict, Tuple


class Database:
    def __init__(self, db_path: str = "./bot_data.db"):
        self.db_path = db_path

    async def initialize(self):
        """Initialize database tables if they don't exist"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS welcome_config (
                    guild_id INTEGER PRIMARY KEY,
                    welcome_channel_id INTEGER,
                    welcome_message TEXT,
                    farewell_channel_id INTEGER,
                    farewell_message TEXT
                );

                CREATE TABLE IF NOT EXISTS autoroles (
                    guild_id INTEGER,
                    role_id INTEGER,
                    PRIMARY KEY (guild_id, role_id)
                );

                CREATE TABLE IF NOT EXISTS reaction_roles (
                    guild_id INTEGER,
                    message_id INTEGER,
                    channel_id INTEGER,
                    emoji TEXT,
                    role_id INTEGER,
                    PRIMARY KEY (message_id, emoji)
                );

                CREATE TABLE IF NOT EXISTS triggers (
                    guild_id INTEGER,
                    trigger_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    response TEXT NOT NULL,
                    UNIQUE(guild_id, keyword)
                );
            """)
            await db.commit()

    # Welcome Config
    async def set_welcome_config(self, guild_id: int, channel_id: int, message: str):
        """Set welcome channel and message"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR REPLACE INTO welcome_config (guild_id, welcome_channel_id, welcome_message)
                   VALUES (?, ?, ?)""",
                (guild_id, channel_id, message)
            )
            await db.commit()

    async def set_farewell_config(self, guild_id: int, channel_id: int, message: str):
        """Set farewell channel and message"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR REPLACE INTO welcome_config (guild_id, farewell_channel_id, farewell_message)
                   VALUES (?, ?, ?)""",
                (guild_id, channel_id, message)
            )
            await db.commit()

    async def get_welcome_config(self, guild_id: int) -> Optional[Tuple]:
        """Get welcome configuration for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT welcome_channel_id, welcome_message FROM welcome_config WHERE guild_id = ?",
                (guild_id,)
            )
            return await cursor.fetchone()

    async def get_farewell_config(self, guild_id: int) -> Optional[Tuple]:
        """Get farewell configuration for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT farewell_channel_id, farewell_message FROM welcome_config WHERE guild_id = ?",
                (guild_id,)
            )
            return await cursor.fetchone()

    # Autoroles
    async def add_autorole(self, guild_id: int, role_id: int):
        """Add an autorole"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO autoroles (guild_id, role_id) VALUES (?, ?)",
                (guild_id, role_id)
            )
            await db.commit()

    async def remove_autorole(self, guild_id: int, role_id: int):
        """Remove an autorole"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM autoroles WHERE guild_id = ? AND role_id = ?",
                (guild_id, role_id)
            )
            await db.commit()

    async def get_autoroles(self, guild_id: int) -> List[int]:
        """Get all autoroles for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT role_id FROM autoroles WHERE guild_id = ?",
                (guild_id,)
            )
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    # Reaction Roles
    async def add_reaction_role(self, guild_id: int, message_id: int, channel_id: int, emoji: str, role_id: int):
        """Add a reaction role"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR REPLACE INTO reaction_roles (guild_id, message_id, channel_id, emoji, role_id)
                   VALUES (?, ?, ?, ?, ?)""",
                (guild_id, message_id, channel_id, emoji, role_id)
            )
            await db.commit()

    async def get_reaction_role(self, message_id: int, emoji: str) -> Optional[Tuple]:
        """Get reaction role by message and emoji"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT guild_id, channel_id, role_id FROM reaction_roles WHERE message_id = ? AND emoji = ?",
                (message_id, emoji)
            )
            return await cursor.fetchone()

    async def remove_reaction_role(self, message_id: int, emoji: str):
        """Remove a reaction role"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM reaction_roles WHERE message_id = ? AND emoji = ?",
                (message_id, emoji)
            )
            await db.commit()

    # Triggers
    async def add_trigger(self, guild_id: int, keyword: str, response: str):
        """Add a trigger"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO triggers (guild_id, keyword, response) VALUES (?, ?, ?)",
                (guild_id, keyword, response)
            )
            await db.commit()

    async def remove_trigger(self, guild_id: int, keyword: str):
        """Remove a trigger"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM triggers WHERE guild_id = ? AND keyword = ?",
                (guild_id, keyword)
            )
            await db.commit()

    async def get_trigger_response(self, guild_id: int, keyword: str) -> Optional[str]:
        """Get trigger response for a keyword"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT response FROM triggers WHERE guild_id = ? AND keyword = ?",
                (guild_id, keyword)
            )
            row = await cursor.fetchone()
            return row[0] if row else None

    async def get_all_triggers(self, guild_id: int) -> List[Tuple]:
        """Get all triggers for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT keyword, response FROM triggers WHERE guild_id = ?",
                (guild_id,)
            )
            return await cursor.fetchall()
