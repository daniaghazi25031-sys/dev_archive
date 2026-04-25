"""
Screen Classes
Main application screens and their logic
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.graphics import Color, Ellipse, Rectangle, Line, RoundedRectangle
from kivy.core.text import LabelBase
from kivy.app import App
import random
import time

from ui.animations import StarWidget, BlobCreature
from ui.components import EmotionBar, GlowingCircle
from core.nlp_engine import NLPEngine
from utils.arabic_processor import ArabicProcessor


class WelcomeScreen(Screen):
    """
    First launch welcome screen with name input
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.arabic_processor = ArabicProcessor()
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components"""
        # Main layout
        self.layout = FloatLayout()
        
        # Background gradient effect
        with self.layout.canvas.before:
            Color(0.05, 0.05, 0.12, 1)
            self.bg_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
        
        self.layout.bind(pos=self._update_bg, size=self._update_bg)
        
        # Add stars
        self._create_stars()
        
        # Content layout
        content = BoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(15)
        )
        
        # Spacer
        content.add_widget(Widget(size_hint_y=0.15))
        
        # Welcome title
        self.title_label = Label(
            text='أهلاً وسهلاً!',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(36),
            color=(0, 0.9, 1, 1),
            bold=True,
            size_hint_y=None,
            height=dp(60),
            halign='center'
        )
        content.add_widget(self.title_label)
        
        # Blob creature
        self.blob_container = FloatLayout(size_hint_y=None, height=dp(160))
        self.welcome_blob = BlobCreature(
            size=(dp(150), dp(150)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.blob_container.add_widget(self.welcome_blob)
        content.add_widget(self.blob_container)
        
        # Welcome message
        self.message_label = Label(
            text='اني companion الروحي مالتك.\nهواي سعيد بالتعرف عليك!',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(18),
            color=(0.7, 0.9, 1, 1),
            size_hint_y=None,
            height=dp(80),
            halign='center'
        )
        content.add_widget(self.message_label)
        
        # Spacer
        content.add_widget(Widget(size_hint_y=0.1))
        
        # Name prompt
        self.prompt_label = Label(
            text='شلون جسمك اعزك؟ (اختياري)',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(16),
            color=(0.8, 0.9, 1, 0.9),
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        content.add_widget(self.prompt_label)
        
        # Name input
        from kivy.uix.textinput import TextInput
        self.name_input = TextInput(
            hint_text='اكتب اسمك هون...',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(18),
            multiline=False,
            size_hint_y=None,
            height=dp(55),
            padding=[dp(15), dp(15), dp(15), dp(10)],
            foreground_color=(1, 1, 1, 1),
            background_color=(0.1, 0.15, 0.25, 0.8),
            cursor_color=(0, 0.9, 1, 1),
            hint_text_color=(0.5, 0.6, 0.8, 1),
            write_tab=False
        )
        
        # Style the input
        with self.name_input.canvas.after:
            Color(0, 0.8, 1, 0.5)
            Line(width=dp(2), rounded_rectangle=(
                self.name_input.x, self.name_input.y,
                self.name_input.width, self.name_input.height,
                dp(15)
            ))
        
        self.name_input.bind(pos=self._update_input_border, size=self._update_input_border)
        content.add_widget(self.name_input)
        
        # Spacer
        content.add_widget(Widget(size_hint_y=0.1))
        
        # Continue button
        from kivy.uix.button import Button
        self.continue_btn = Button(
            text='يلا نبدأ',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60),
            background_normal='',
            background_down='',
            background_color=(0, 0.7, 0.9, 1)
        )
        
        with self.continue_btn.canvas.before:
            Color(0, 0.7, 0.9, 1)
            self.btn_rect = RoundedRectangle(radius=[dp(30)])
        
        self.continue_btn.bind(
            pos=self._update_btn,
            size=self._update_btn,
            on_release=self.on_continue,
            state=self._btn_state_change
        )
        content.add_widget(self.continue_btn)
        
        # Spacer
        content.add_widget(Widget(size_hint_y=0.2))
        
        self.layout.add_widget(content)
        self.add_widget(self.layout)
        
        # Animate blob
        Clock.schedule_interval(self._animate_blob, 0.05)
    
    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def _create_stars(self, count=50):
        """Create animated star background"""
        for _ in range(count):
            star = StarWidget(
                size_hint=(None, None),
                size=(dp(random.randint(2, 5)), dp(random.randint(2, 5))),
                pos=(
                    random.randint(0, int(self.layout.width)),
                    random.randint(0, int(self.layout.height))
                ),
                star_size=random.randint(2, 5),
                twinkle_speed=random.uniform(0.5, 2)
            )
            self.layout.add_widget(star, index=0)
    
    def _update_input_border(self, instance, value):
        instance.canvas.after.clear()
        with instance.canvas.after:
            Color(0, 0.8, 1, 0.5)
            Line(width=dp(2), rounded_rectangle=(
                instance.x, instance.y,
                instance.width, instance.height,
                dp(15)
            ))
    
    def _update_btn(self, instance, value):
        instance.canvas.before.clear()
        color = (0, 0.5, 0.7, 1) if instance.state == 'down' else (0, 0.7, 0.9, 1)
        with instance.canvas.before:
            Color(*color)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[dp(30)]
            )
    
    def _btn_state_change(self, instance, value):
        self._update_btn(instance, value)
    
    def _animate_blob(self, dt):
        """Animate the blob creature"""
        # Gentle floating animation
        self.welcome_blob.y = self.welcome_blob.parent.height/2 - 75 + 10 * math.sin(time.time() * 2)
    
    def on_continue(self, instance):
        """Handle continue button press"""
        name = self.name_input.text.strip()
        
        # Save user name
        app = App.get_running_app()
        app.set_user_name(name)
        
        # Animate transition
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *args: self._go_to_main())
        anim.start(self.layout)
    
    def _go_to_main(self):
        """Transition to main screen"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'main'


class MainScreen(Screen):
    """
    Main interaction screen with blob and chat
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nlp_engine = NLPEngine()
        self.arabic_processor = ArabicProcessor()
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components"""
        # Main layout
        self.layout = FloatLayout()
        
        # Background
        with self.layout.canvas.before:
            Color(0.05, 0.05, 0.12, 1)
            self.bg_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
        
        self.layout.bind(pos=self._update_bg, size=self._update_bg)
        
        # Create stars
        self._create_stars()
        
        # Content
        content = BoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Header with greeting and stats button
        header = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        # Stats button
        from kivy.uix.button import Button
        self.stats_btn = Button(
            text='📊',
            font_size=dp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_down='',
            background_color=(0, 0.8, 1, 0.2)
        )
        with self.stats_btn.canvas.before:
            Color(0, 0.8, 1, 0.2)
            RoundedRectangle(radius=[dp(10)])
        self.stats_btn.bind(
            pos=self._update_stats_btn,
            size=self._update_stats_btn,
            on_release=self.show_stats
        )
        header.add_widget(self.stats_btn)
        
        # Spacer
        header.add_widget(Widget(size_hint_x=0.5))
        
        # Greeting
        self.greeting_label = Label(
            text='صباح الخير',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(24),
            color=(0, 0.9, 1, 1),
            bold=True,
            halign='right'
        )
        header.add_widget(self.greeting_label)
        
        content.add_widget(header)
        
        # Blob area
        self.blob_area = FloatLayout(size_hint_y=0.4)
        
        # Glow effect
        self.glow = GlowingCircle(
            size=(dp(200), dp(200)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            glow_color=[0, 0.8, 1, 0.3]
        )
        self.blob_area.add_widget(self.glow)
        
        # Main blob
        self.main_blob = BlobCreature(
            size=(dp(180), dp(180)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.blob_area.add_widget(self.main_blob)
        
        content.add_widget(self.blob_area)
        
        # Response area
        from kivy.uix.scrollview import ScrollView
        self.response_scroll = ScrollView(
            size_hint_y=0.3,
            bar_width=dp(0)
        )
        
        self.response_container = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            size_hint_y=None
        )
        self.response_container.bind(minimum_height=self.response_container.setter('height'))
        
        self.response_label = Label(
            text='اكتب الي ببالك واني اسمعك...',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(16),
            color=(0.8, 0.9, 1, 1),
            halign='right',
            valign='top',
            text_size=(None, None),
            size_hint_y=None,
            padding=(dp(10), dp(10))
        )
        self.response_label.bind(texture_size=self.response_label.setter('size'))
        self.response_container.add_widget(self.response_label)
        self.response_scroll.add_widget(self.response_container)
        
        content.add_widget(self.response_scroll)
        
        # Input area
        input_area = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )
        
        # Send button
        self.send_btn = Button(
            text='ارسال',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(16),
            size_hint_x=None,
            width=dp(85),
            background_normal='',
            background_down='',
            background_color=(0, 0.7, 0.9, 1)
        )
        with self.send_btn.canvas.before:
            Color(0, 0.7, 0.9, 1)
            self.send_btn_rect = RoundedRectangle(radius=[dp(25)])
        self.send_btn.bind(
            pos=self._update_send_btn,
            size=self._update_send_btn,
            on_release=self.send_message
        )
        input_area.add_widget(self.send_btn)
        
        # Message input
        from kivy.uix.textinput import TextInput
        self.message_input = TextInput(
            hint_text='اكتب اي شي وارسال...',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(16),
            multiline=False,
            padding=[dp(15), dp(15), dp(15), dp(10)],
            foreground_color=(1, 1, 1, 1),
            background_color=(0.1, 0.15, 0.25, 0.8),
            cursor_color=(0, 0.9, 1, 1),
            hint_text_color=(0.5, 0.6, 0.8, 1),
            write_tab=False
        )
        self.message_input.bind(
            on_text_validate=self.send_message,
            pos=self._update_msg_input,
            size=self._update_msg_input
        )
        input_area.add_widget(self.message_input)
        
        content.add_widget(input_area)
        self.layout.add_widget(content)
        self.add_widget(self.layout)
        
        # Update greeting based on time
        self._update_greeting()
        Clock.schedule_interval(lambda dt: self._update_greeting(), 3600)
    
    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def _create_stars(self, count=40):
        """Create star background"""
        for _ in range(count):
            star = StarWidget(
                size_hint=(None, None),
                size=(dp(random.randint(2, 4)), dp(random.randint(2, 4))),
                pos=(
                    random.randint(0, int(self.layout.width) if self.layout.width > 0 else 400),
                    random.randint(0, int(self.layout.height) if self.layout.height > 0 else 800)
                ),
                star_size=random.randint(2, 4),
                twinkle_speed=random.uniform(0.5, 2)
            )
            self.layout.add_widget(star, index=0)
    
    def _update_stats_btn(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0.8, 1, 0.2)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[dp(10)]
            )
    
    def _update_send_btn(self, instance, value):
        instance.canvas.before.clear()
        color = (0, 0.5, 0.7, 1) if instance.state == 'down' else (0, 0.7, 0.9, 1)
        with instance.canvas.before:
            Color(*color)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[dp(25)]
            )
    
    def _update_msg_input(self, instance, value):
        instance.canvas.after.clear()
        with instance.canvas.after:
            Color(0, 0.8, 1, 0.3)
            Line(width=dp(1.5), rounded_rectangle=(
                instance.x, instance.y,
                instance.width, instance.height,
                dp(25)
            ))
    
    def _update_greeting(self):
        """Update greeting based on time of day"""
        hour = time.localtime().tm_hour
        
        if 5 <= hour < 12:
            greeting = 'صباح الخير'
        elif 12 <= hour < 17:
            greeting = 'مساء الخير'
        elif 17 <= hour < 21:
            greeting = 'مساء النور'
        else:
            greeting = 'ليلتك سعيدة'
        
        # Add name if available
        app = App.get_running_app()
        name = app.get_user_name()
        if name and name != 'صديقي':
            greeting = f'{greeting}، {name}'
        
        self.greeting_label.text = greeting
    
    def send_message(self, *args):
        """Process and send user message"""
        message = self.message_input.text.strip()
        if not message:
            return
        
        # Clear input
        self.message_input.text = ''
        
        # Get app instance
        app = App.get_running_app()
        
        # Process message
        result = self.nlp_engine.process(
            text=message,
            language=app.settings.language,
            user_name=app.user_name
        )
        
        # Update blob emotion
        self.main_blob.emotion = result['emotion']
        
        # Update response
        self.response_label.text = result['response']
        
        # Animate response
        anim = Animation(opacity=0, duration=0.1) + Animation(opacity=1, duration=0.3)
        anim.start(self.response_label)
        
        # Save to database
        app.save_emotion(
            emotion=result['emotion'],
            user_input=message,
            response=result['response']
        )
    
    def show_stats(self, *args):
        """Navigate to stats screen"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'stats'


class StatsScreen(Screen):
    """
    Statistics and trends screen
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components"""
        # Main layout
        self.layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Background
        with self.layout.canvas.before:
            Color(0.05, 0.05, 0.12, 1)
            self.bg_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
        
        self.layout.bind(pos=self._update_bg, size=self._update_bg)
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        # Back button
        from kivy.uix.button import Button
        self.back_btn = Button(
            text='→',
            font_size=dp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_down='',
            background_color=(0, 0.8, 1, 0.2)
        )
        self.back_btn.bind(on_release=self.go_back)
        header.add_widget(self.back_btn)
        
        # Title
        self.title_label = Label(
            text='الاحصائيات',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(26),
            color=(0, 0.9, 1, 1),
            bold=True
        )
        header.add_widget(self.title_label)
        
        # Spacer
        header.add_widget(Widget(size_hint_x=None, width=dp(50)))
        
        self.layout.add_widget(header)
        
        # Weekly summary card
        self.summary_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(140),
            padding=dp(15),
            spacing=dp(10)
        )
        
        with self.summary_card.canvas.before:
            Color(0.1, 0.15, 0.25, 0.6)
            self.summary_rect = RoundedRectangle(radius=[dp(15)])
        
        self.summary_card.bind(pos=self._update_summary, size=self._update_summary)
        
        self.summary_title = Label(
            text='ملخص الاسبوع',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(18),
            color=(0, 0.9, 1, 1),
            bold=True,
            size_hint_y=None,
            height=dp(30),
            halign='right'
        )
        self.summary_card.add_widget(self.summary_title)
        
        self.summary_text = Label(
            text='تحميل...',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(14),
            color=(0.8, 0.9, 1, 0.9),
            halign='right',
            valign='top',
            text_size=(None, None)
        )
        self.summary_card.add_widget(self.summary_text)
        
        self.layout.add_widget(self.summary_card)
        
        # Section title
        self.section_title = Label(
            text='المشاعر الاكثر شيوعاً',
            font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
            font_size=dp(18),
            color=(0, 0.9, 1, 1),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign='right'
        )
        self.layout.add_widget(self.section_title)
        
        # Emotions list
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(bar_width=dp(0))
        
        self.emotions_list = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(5),
            size_hint_y=None
        )
        self.emotions_list.bind(minimum_height=self.emotions_list.setter('height'))
        
        scroll.add_widget(self.emotions_list)
        self.layout.add_widget(scroll)
        
        # Spacer
        self.layout.add_widget(Widget(size_hint_y=0.3))
        
        self.add_widget(self.layout)
        
        # Load data on enter
        self.bind(on_enter=self.load_stats)
    
    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def _update_summary(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.1, 0.15, 0.25, 0.6)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[dp(15)]
            )
            Color(0, 0.8, 1, 0.2)
            Line(width=dp(1), rounded_rectangle=(
                instance.x, instance.y,
                instance.width, instance.height,
                dp(15)
            ))
    
    def load_stats(self, *args):
        """Load and display statistics"""
        app = App.get_running_app()
        
        # Get weekly stats
        stats = app.get_emotion_stats('week')
        
        # Update summary
        if stats:
            dominant = max(stats, key=stats.get)
            total = sum(stats.values())
            
            # Arabic emotion names
            emotion_names = {
                'panic': 'جنط',
                'anxiety': 'قلق',
                'sadness': 'حزن',
                'depression': 'اكتئاب',
                'shock': 'صدمة',
                'anger': 'غضب',
                'fear': 'خوف',
                'tired': 'تعب',
                'neutral': 'محايد',
                'happy': 'سعادة'
            }
            
            dominant_ar = emotion_names.get(dominant, dominant)
            summary = f'المشاعر السائدة هذا الاسبوع: {dominant_ar}\n'
            summary += f'عدد التفاعلات: {total}'
            
            self.summary_text.text = summary
        else:
            self.summary_text.text = 'لا توجد بيانات كافية بعد.\nاستمر بالتواصل معي!'
        
        # Update emotions list
        self.emotions_list.clear_widgets()
        
        if stats:
            max_count = max(stats.values()) if stats else 1
            
            # Sort by count
            sorted_emotions = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            
            for emotion, count in sorted_emotions[:6]:  # Top 6
                bar = EmotionBar(
                    emotion=emotion,
                    value=count,
                    max_value=max_count
                )
                self.emotions_list.add_widget(bar)
        else:
            no_data = Label(
                text='ابدأ بالكتابة لرؤية احصائياتك!',
                font_name='ArabicFont' if 'ArabicFont' in LabelBase._fonts else 'Roboto',
                font_size=dp(16),
                color=(0.7, 0.8, 0.9, 0.8)
            )
            self.emotions_list.add_widget(no_data)
    
    def go_back(self, *args):
        """Return to main screen"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'


# Widget import fix
from kivy.uix.widget import Widget