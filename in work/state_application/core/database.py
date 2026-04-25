"""
Database Manager
Handles SQLite database operations for persistent storage
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from kivy.utils import platform


class DatabaseManager:
    """
    Manages SQLite database for user data, emotions, and settings
    """
    
    def __init__(self):
        self.db_path = self._get_db_path()
        self.conn = None
        self.cursor = None
        
    def _get_db_path(self):
        """Get appropriate database path based on platform"""
        if platform == 'android':
            from android.storage import primary_external_storage_path
            db_dir = os.path.join(primary_external_storage_path(), 'StateApp')
            os.makedirs(db_dir, exist_ok=True)
            return os.path.join(db_dir, 'state.db')
        else:
            db_dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(db_dir, '..', 'state.db')
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # User settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Emotion entries table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emotion TEXT NOT NULL,
                user_input TEXT,
                ai_response TEXT,
                language TEXT DEFAULT 'ar',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Mood tracking table (daily summary)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_daily (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE,
                dominant_emotion TEXT,
                emotion_counts TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Notification history
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def save_setting(self, key, value):
        """Save or update a setting"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        self.conn.commit()
    
    def get_setting(self, key, default=None):
        """Get a setting value"""
        self.cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else default
    
    def save_emotion_entry(self, emotion, user_input, response, language='ar'):
        """Save an emotion entry"""
        self.cursor.execute('''
            INSERT INTO emotions (emotion, user_input, ai_response, language)
            VALUES (?, ?, ?, ?)
        ''', (emotion, user_input, response, language))
        self.conn.commit()
        
        # Update daily mood summary
        self._update_daily_summary()
    
    def _update_daily_summary(self):
        """Update daily mood summary"""
        today = datetime.now().date()
        
        # Get today's emotions
        self.cursor.execute('''
            SELECT emotion, COUNT(*) as count
            FROM emotions
            WHERE DATE(created_at) = ?
            GROUP BY emotion
            ORDER BY count DESC
        ''', (today.isoformat(),))
        
        results = self.cursor.fetchall()
        if results:
            dominant_emotion = results[0][0]
            emotion_counts = json.dumps({r[0]: r[1] for r in results})
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO mood_daily (date, dominant_emotion, emotion_counts)
                VALUES (?, ?, ?)
            ''', (today.isoformat(), dominant_emotion, emotion_counts))
            self.conn.commit()
    
    def get_emotion_stats(self, period='week'):
        """Get emotion statistics for a period"""
        if period == 'week':
            days = 7
        elif period == 'month':
            days = 30
        else:
            days = 7
            
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        self.cursor.execute('''
            SELECT emotion, COUNT(*) as count
            FROM emotions
            WHERE created_at >= ?
            GROUP BY emotion
            ORDER BY count DESC
        ''', (since,))
        
        return dict(self.cursor.fetchall())
    
    def get_recent_emotions(self, limit=50):
        """Get recent emotion entries"""
        self.cursor.execute('''
            SELECT emotion, user_input, ai_response, created_at
            FROM emotions
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        return self.cursor.fetchall()
    
    def get_daily_mood_trend(self, days=7):
        """Get daily mood trend"""
        since = (datetime.now() - timedelta(days=days)).date()
        
        self.cursor.execute('''
            SELECT date, dominant_emotion, emotion_counts
            FROM mood_daily
            WHERE date >= ?
            ORDER BY date ASC
        ''', (since.isoformat(),))
        
        results = []
        for row in self.cursor.fetchall():
            results.append({
                'date': row[0],
                'dominant': row[1],
                'counts': json.loads(row[2]) if row[2] else {}
            })
        
        return results
    
    def save_notification(self, message):
        """Save a sent notification"""
        self.cursor.execute('''
            INSERT INTO notifications (message)
            VALUES (?)
        ''', (message,))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()