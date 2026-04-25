"""
UI Components
Custom widgets and components for the app
"""

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.graphics import Color, Ellipse, Rectangle, Line, RoundedRectangle, Triangle
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
import math


class EmotionBar(BoxLayout):
    """
    Visual progress bar for emotion display
    """
    emotion = StringProperty('neutral')
    value = NumericProperty(0)
    max_value = NumericProperty(10)
    
    # Emotion colors
    emotion_colors = {
        'panic': [1, 0.3, 0.3],
        'anxiety': [1, 0.7, 0.3],
        'sadness': [0.3, 0.5, 0.8],
        'depression': [0.4, 0.4, 0.5],
        'shock': [0.9, 0.9, 1],
        'anger': [1, 0.3, 0.3],
        'fear': [0.7, 0.5, 0.9],
        'tired': [0.4, 0.6, 0.8],
        'neutral': [0, 0.8, 1],
        'happy': [0.2, 1, 0.5]
    }
    
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
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(40)
        self.spacing = dp(10)
        
        # Emotion label
        self.emotion_label = Label(
            text='',
            font_name='ArabicFont',
            font_size=dp(14),
            color=[0.8, 0.9, 1, 1],
            size_hint_x=0.3,
            halign='right'
        )
        self.add_widget(self.emotion_label)
        
        # Progress bar area
        self.bar_widget = Widget(size_hint_x=0.7)
        self.add_widget(self.bar_widget)
        
        self.bind(emotion=self.update_display, value=self.update_display)
        Clock.schedule_once(lambda dt: self.update_display(), 0)
    
    def update_display(self, *args):
        """Update the visual display"""
        emotion = self.emotion
        value = self.value
        
        # Update label
        self.emotion_label.text = self.emotion_names.get(emotion, emotion)
        
        # Redraw bar
        self.bar_widget.canvas.clear()
        
        with self.bar_widget.canvas:
            # Background
            Color(0.1, 0.15, 0.25, 0.8)
            RoundedRectangle(
                pos=self.bar_widget.pos,
                size=self.bar_widget.size,
                radius=[dp(5)]
            )
            
            # Fill
            color = self.emotion_colors.get(emotion, [0, 0.8, 1])
            Color(*color, 0.8)
            
            fill_width = (value / self.max_value) * self.bar_widget.width
            fill_width = max(dp(2), min(fill_width, self.bar_widget.width))
            
            RoundedRectangle(
                pos=self.bar_widget.pos,
                size=(fill_width, self.bar_widget.height),
                radius=[dp(5)]
            )


class GlowingCircle(Widget):
    """
    Animated glowing circle for visual effects
    """
    glow_color = ListProperty([0, 0.8, 1, 0.5])
    pulse_speed = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0
        self.base_radius = 50
        Clock.schedule_interval(self.update, 1/60)
    
    def update(self, dt):
        """Update glow animation"""
        self.time += dt * self.pulse_speed
        
        # Clear and redraw
        self.canvas.clear()
        
        with self.canvas:
            # Outer glow layers
            for i in range(5):
                alpha = 0.1 * (1 - i/5)
                radius = self.base_radius + i * 10 + 5 * math.sin(self.time * 2)
                
                Color(
                    self.glow_color[0],
                    self.glow_color[1],
                    self.glow_color[2],
                    alpha
                )
                
                Ellipse(
                    pos=(
                        self.center_x - radius,
                        self.center_y - radius
                    ),
                    size=(radius * 2, radius * 2)
                )
            
            # Core circle
            Color(*self.glow_color)
            core_radius = self.base_radius * 0.6
            Ellipse(
                pos=(
                    self.center_x - core_radius,
                    self.center_y - core_radius
                ),
                size=(core_radius * 2, core_radius * 2)
            )


class FloatingParticle(Widget):
    """
    Floating particle effect for background ambiance
    """
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(1)
    particle_color = ListProperty([0, 0.8, 1, 0.6])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (dp(4), dp(4))
        Clock.schedule_interval(self.update, 1/60)
    
    def update(self, dt):
        """Update particle position"""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Reset if out of bounds
        parent = self.parent
        if parent:
            if self.y > parent.height:
                self.y = 0
            if self.x < 0:
                self.x = parent.width
            elif self.x > parent.width:
                self.x = 0


class PulseIndicator(Widget):
    """
    Pulsing indicator dot for notifications/status
    """
    active = True
    pulse_color = ListProperty([0, 0.8, 1, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = (dp(12), dp(12))
        self.time = 0
        Clock.schedule_interval(self.update, 1/60)
    
    def update(self, dt):
        """Update pulse animation"""
        if not self.active:
            return
            
        self.time += dt
        
        self.canvas.clear()
        with self.canvas:
            # Pulse effect
            for i in range(3):
                scale = 1 + 0.5 * math.sin(self.time * 3 + i * 0.5)
                alpha = 1 - i * 0.3
                
                Color(
                    self.pulse_color[0],
                    self.pulse_color[1],
                    self.pulse_color[2],
                    alpha * scale
                )
                
                radius = self.width * scale / 2
                Ellipse(
                    pos=(
                        self.center_x - radius,
                        self.center_y - radius
                    ),
                    size=(radius * 2, radius * 2)
                )