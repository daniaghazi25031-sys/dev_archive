"""
Settings Manager
Handles app settings and localization
"""

from core.database import DatabaseManager


class Settings:
    """
    Manages app settings including language and localization
    """
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.language = 'ar'  # Default Arabic
        self._init_localization()
        
    def _init_localization(self):
        """Initialize localization strings"""
        self.strings = {
            'app_name': {
                'ar': 'ستيت',
                'en': 'State'
            },
            'welcome_title': {
                'ar': 'أهلاً وسهلاً!',
                'en': 'Welcome!'
            },
            'welcome_message': {
                'ar': 'اني companion الروحي مالتك. هواي سعيد بالتعرف عليك!',
                'en': "I'm your emotional companion. So happy to meet you!"
            },
            'ask_name': {
                'ar': 'شلون جسمك اعزك؟ (اختياري)',
                'en': 'What should I call you? (optional)'
            },
            'name_placeholder': {
                'ar': 'اكتب اسمك هون...',
                'en': 'Enter your name...'
            },
            'continue': {
                'ar': 'يلا نبدأ',
                'en': "Let's start"
            },
            'input_placeholder': {
                'ar': 'اكتب اي شي وارسل...',
                'en': 'Write anything and send...'
            },
            'send': {
                'ar': 'ارسال',
                'en': 'Send'
            },
            'stats': {
                'ar': 'الاحصائيات',
                'en': 'Statistics'
            },
            'daily_trend': {
                'ar': 'الاتجاه اليومي',
                'en': 'Daily Trend'
            },
            'weekly_summary': {
                'ar': 'ملخص الاسبوع',
                'en': 'Weekly Summary'
            },
            'most_common': {
                'ar': 'المشاعر الاكثر شيوعاً',
                'en': 'Most Common Emotions'
            },
            'friend': {
                'ar': 'صديقي',
                'en': 'Friend'
            },
            'back': {
                'ar': 'رجوع',
                'en': 'Back'
            },
            'settings': {
                'ar': 'الاعدادات',
                'en': 'Settings'
            },
            'language': {
                'ar': 'اللغة',
                'en': 'Language'
            },
            'notifications': {
                'ar': 'التنبيهات',
                'en': 'Notifications'
            },
            'about': {
                'ar': 'عن التطبيق',
                'en': 'About'
            }
        }
    
    def get_text(self, key: str, **kwargs) -> str:
        """Get localized text by key"""
        if key in self.strings:
            text = self.strings[key].get(self.language, self.strings[key].get('ar', key))
            
            # Apply any formatting
            if kwargs:
                try:
                    text = text.format(**kwargs)
                except KeyError:
                    pass
            
            return text
        return key
    
    def set_language(self, lang: str):
        """Set app language"""
        if lang in ['ar', 'en']:
            self.language = lang
            self.db.save_setting('language', lang)
    
    def is_first_launch(self) -> bool:
        """Check if this is first launch"""
        return self.db.get_setting('first_launch', 'true') == 'true'
    
    def set_first_launch_complete(self):
        """Mark first launch as complete"""
        self.db.save_setting('first_launch', 'false')
    
    def get_setting(self, key: str, default=None):
        """Get a setting value"""
        return self.db.get_setting(key, default)
    
    def save_setting(self, key: str, value):
        """Save a setting value"""
        self.db.save_setting(key, value)