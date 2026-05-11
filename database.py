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

                CREATE TABLE IF NOT EXISTS suggestion_channels (
                    guild_id INTEGER PRIMARY KEY,
                    channel_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS triggers (
                    guild_id INTEGER,
                    trigger_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    response TEXT NOT NULL,
                    UNIQUE(guild_id, keyword)
                );

                CREATE TABLE IF NOT EXISTS ticket_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    name TEXT NOT NULL,
                    mention_roles TEXT,  -- JSON array of role IDs
                    close_permissions TEXT,  -- JSON array of role IDs
                    log_channel_id INTEGER,
                    category_id INTEGER  -- Discord category ID
                );

                CREATE TABLE IF NOT EXISTS ticket_panels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    channel_id INTEGER,
                    message_id INTEGER,
                    embed_title TEXT,
                    embed_description TEXT,
                    embed_color TEXT,
                    embed_image TEXT,
                    selection_type TEXT,  -- 'button', 'list', 'emoji'
                    ticket_options TEXT  -- JSON array of options with different fields based on selection_type
                );

                CREATE TABLE IF NOT EXISTS active_tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    channel_id INTEGER,
                    user_id INTEGER,
                    ticket_type_id INTEGER,
                    created_at TEXT,
                    status TEXT  -- 'open', 'closed'
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

    # Suggestions
    async def set_suggestions_channel(self, guild_id: int, channel_id: int):
        """Set the suggestions channel for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO suggestion_channels (guild_id, channel_id) VALUES (?, ?)",
                (guild_id, channel_id)
            )
            await db.commit()

    async def remove_suggestions_channel(self, guild_id: int):
        """Remove the suggestions channel for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM suggestion_channels WHERE guild_id = ?",
                (guild_id,)
            )
            await db.commit()

    async def get_suggestions_channel(self, guild_id: int) -> Optional[int]:
        """Get the suggestions channel id for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT channel_id FROM suggestion_channels WHERE guild_id = ?",
                (guild_id,)
            )
            row = await cursor.fetchone()
            return row[0] if row else None

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

    # Ticket Types
    async def create_ticket_type(self, guild_id: int, name: str, mention_roles: str, close_permissions: str, log_channel_id: int, category_id: int) -> int:
        """Create a new ticket type and return its ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO ticket_types (guild_id, name, mention_roles, close_permissions, log_channel_id, category_id)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (guild_id, name, mention_roles, close_permissions, log_channel_id, category_id)
            )
            await db.commit()
            return cursor.lastrowid

    async def get_ticket_types(self, guild_id: int) -> List[Tuple]:
        """Get all ticket types for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, name, mention_roles, close_permissions, log_channel_id, category_id FROM ticket_types WHERE guild_id = ?",
                (guild_id,)
            )
            return await cursor.fetchall()

    async def get_ticket_type(self, ticket_type_id: int) -> Optional[Tuple]:
        """Get a specific ticket type"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, name, mention_roles, close_permissions, log_channel_id, category_id FROM ticket_types WHERE id = ?",
                (ticket_type_id,)
            )
            return await cursor.fetchone()

    async def delete_ticket_type(self, ticket_type_id: int):
        """Delete a ticket type"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM ticket_types WHERE id = ?", (ticket_type_id,))
            await db.commit()

    # Ticket Panels
    async def create_ticket_panel(self, guild_id: int, channel_id: int, message_id: int, embed_title: str, embed_description: str, embed_color: str, embed_image: str, selection_type: str, ticket_options: str) -> int:
        """Create a new ticket panel and return its ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO ticket_panels (guild_id, channel_id, message_id, embed_title, embed_description, embed_color, embed_image, selection_type, ticket_options)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (guild_id, channel_id, message_id, embed_title, embed_description, embed_color, embed_image, selection_type, ticket_options)
            )
            await db.commit()
            return cursor.lastrowid

    async def get_ticket_panels(self, guild_id: int) -> List[Tuple]:
        """Get all ticket panels for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, channel_id, message_id, embed_title, embed_description, embed_color, embed_image, selection_type, ticket_options FROM ticket_panels WHERE guild_id = ?",
                (guild_id,)
            )
            return await cursor.fetchall()

    async def get_ticket_panel_by_message(self, message_id: int) -> Optional[Tuple]:
        """Get ticket panel by message ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, guild_id, channel_id, embed_title, embed_description, embed_color, embed_image, selection_type, ticket_options FROM ticket_panels WHERE message_id = ?",
                (message_id,)
            )
            return await cursor.fetchone()

    async def delete_ticket_panel(self, panel_id: int):
        """Delete a ticket panel"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM ticket_panels WHERE id = ?", (panel_id,))
            await db.commit()

    # Active Tickets
    async def create_ticket(self, guild_id: int, channel_id: int, user_id: int, ticket_type_id: int, created_at: str) -> int:
        """Create a new active ticket and return its ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO active_tickets (guild_id, channel_id, user_id, ticket_type_id, created_at, status)
                   VALUES (?, ?, ?, ?, ?, 'open')""",
                (guild_id, channel_id, user_id, ticket_type_id, created_at)
            )
            await db.commit()
            return cursor.lastrowid

    async def get_active_ticket(self, channel_id: int) -> Optional[Tuple]:
        """Get active ticket by channel ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, guild_id, user_id, ticket_type_id, created_at, status FROM active_tickets WHERE channel_id = ? AND status = 'open'",
                (channel_id,)
            )
            return await cursor.fetchone()

    async def close_ticket(self, ticket_id: int):
        """Close a ticket"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE active_tickets SET status = 'closed' WHERE id = ?",
                (ticket_id,)
            )
            await db.commit()

    async def get_user_tickets(self, user_id: int, guild_id: int) -> List[Tuple]:
        """Get all tickets for a user in a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, channel_id, ticket_type_id, created_at, status FROM active_tickets WHERE user_id = ? AND guild_id = ?",
                (user_id, guild_id)
            )
            return await cursor.fetchall()
