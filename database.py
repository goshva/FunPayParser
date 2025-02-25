import sqlite3
from contextlib import contextmanager
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="funpay.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Initialize the database with necessary tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id TEXT UNIQUE,
                    title TEXT,
                    price REAL,
                    seller TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def add_item(self, item_id: str, title: str, price: float, seller: str):
        """Add or update an item in the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO items (item_id, title, price, seller)
                VALUES (?, ?, ?, ?)
            ''', (item_id, title, price, seller))
            conn.commit()

    def get_item(self, item_id: str):
        """Retrieve an item from the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items WHERE item_id = ?', (item_id,))
            return cursor.fetchone()

    def log_event(self, level: str, message: str):
        """Log an event to the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (level, message)
                VALUES (?, ?)
            ''', (level, message))
            conn.commit()