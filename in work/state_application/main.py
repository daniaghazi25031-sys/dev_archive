"""
State App - Mental Health Companion
Main entry point for the application
"""

import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.utils import platform
from kivy.resources import resource_add_path

# Add paths
if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))
else:
    resource_add_path(os.path.dirname(os.path.abspath(__file__)))

from ui.screens import WelcomeScreen, MainScreen, StatsScreen
from core.database import DatabaseManager
from core.notification_manager import NotificationManager
from utils.settings import Settings

# Register Arabic font
FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'fonts')
ARABIC_FONT = os.path.join(FONT_PATH, 'NotoSansArabic-Regular.ttf')

if os.path.exists(ARABIC_FONT):
    LabelBase.register(name='ArabicFont', fn_regular=ARABIC_FONT)


class StateApp(App):
    """
    Main Application Class
    Handles app initialization, screen management, and core functionality
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
        self.notification_manager = None
        self.settings = None
        self.user_name = ""
        self.current_emotion = "neutral"
        
    def build(self):
        """Build the application UI"""
        # Set window properties
        Window.clearcolor = (0.05, 0.05, 0.12, 1)  # Dark space background
        
        # Initialize database
        self.db = DatabaseManager()
        self.db.initialize_database()
        
        # Initialize settings
        self.settings = Settings(self.db)
        
        # Initialize notifications (Android only)
        if platform == 'android':
            self.notification_manager = NotificationManager()
            Clock.schedule_once(lambda dt: self.setup_notifications(), 2)
        
        # Load user data
        self.load_user_data()
        
        # Create screen manager
        sm = ScreenManager(transition=FadeTransition(duration=0.5))
        
        # Add screens based on first launch
        if self.settings.is_first_launch():
            sm.add_widget(WelcomeScreen(name='welcome'))
        else:
            sm.add_widget(MainScreen(name='main'))
        
        sm.add_widget(StatsScreen(name='stats'))
        
        return sm
    
    def load_user_data(self):
        """Load user data from database"""
        self.user_name = self.db.get_setting('user_name', '')
        self.settings.language = self.db.get_setting('language', 'ar')
        
    def setup_notifications(self):
        """Setup periodic motivational notifications"""
        if self.notification_manager:
            self.notification_manager.schedule_notifications()
    
    def get_user_name(self):
        """Get stored user name"""
        return self.user_name or self.get_localized_text('friend')
    
    def set_user_name(self, name):
        """Save user name to database"""
        self.user_name = name
        self.db.save_setting('user_name', name)
        self.settings.set_first_launch_complete()
    
    def get_localized_text(self, key, **kwargs):
        """Get text in current language"""
        return self.settings.get_text(key, **kwargs)
    
    def save_emotion(self, emotion, user_input, response):
        """Save emotion data to database"""
        self.db.save_emotion_entry(emotion, user_input, response)
        self.current_emotion = emotion
        
    def get_emotion_stats(self, period='week'):
        """Get emotion statistics"""
        return self.db.get_emotion_stats(period)
    
    def on_stop(self):
        """Clean up on app close"""
        if self.db:
            self.db.close()


def main():
    """Main entry point"""
    app = StateApp()
    app.run()


if __name__ == '__main__':
    main()