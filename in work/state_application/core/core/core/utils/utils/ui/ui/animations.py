"""
Animations Module
Contains all animated components and effects
"""

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle, Line, Mesh
from kivy.graphics.instructions import InstructionGroup
import math
import random


class StarWidget(Widget):
    """
    Animated star widget for space background
    """
    star_size = NumericProperty(3)
    color = ListProperty([1, 1, 1, 0.8])
    twinkle_speed = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_alpha = random.uniform(0.3, 0.9)
        self.twinkle_offset = random.uniform(0, math.pi * 2)
        Clock.schedule_interval(self.twinkle, 0.1)
        
    def twinkle(self, dt):
        """Animate star twinkling"""
        import time
        t = time.time() * self.twinkle_speed + self.twinkle_offset
        alpha = self.base_alpha + 0.2 * math.sin(t)
        self.color = (1, 1, 1, max(0.1, min(1.0, alpha)))


class BlobCreature(Widget):
    """
    Animated blob creature that reacts to user emotions
    Features organic movement, color changes, and expressions
    """
    
    emotion = StringProperty('neutral')
    primary_color = ListProperty([0, 0.8, 1, 0.9])
    secondary_color = ListProperty([0.2, 0.9, 1, 0.7])
    glow_color = ListProperty([0, 0.8, 1, 0.3])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0
        self.morph_offset = 0
        self.base_scale = 1.0
        self.target_scale = 1.0
        self.eye_expression = 'neutral'
        
        # Animation properties
        self.breath_phase = 0
        self.wobble_phase = random.uniform(0, math.pi * 2)
        
        # Color themes for different emotions
        self.emotion_colors = {
            'neutral': {
                'primary': [0, 0.8, 1, 0.9],
                'secondary': [0.2, 0.9, 1, 0.7],
                'glow': [0, 0.8, 1, 0.3]
            },
            'happy': {
                'primary': [0.2, 1, 0.5, 0.9],
                'secondary': [0.5, 1, 0.7, 0.7],
                'glow': [0.3, 1, 0.6, 0.4]
            },
            'sadness': {
                'primary': [0.3, 0.5, 0.8, 0.85],
                'secondary': [0.4, 0.6, 0.9, 0.6],
                'glow': [0.3, 0.5, 0.8, 0.2]
            },
            'anxiety': {
                'primary': [0.9, 0.7, 0.3, 0.9],
                'secondary': [1, 0.8, 0.4, 0.7],
                'glow': [0.9, 0.7, 0.3, 0.3]
            },
            'panic': {
                'primary': [1, 0.4, 0.4, 0.95],
                'secondary': [1, 0.6, 0.5, 0.7],
                'glow': [1, 0.4, 0.4, 0.4]
            },
            'depression': {
                'primary': [0.4, 0.4, 0.5, 0.8],
                'secondary': [0.5, 0.5, 0.6, 0.6],
                'glow': [0.4, 0.4, 0.5, 0.15]
            },
            'shock': {
                'primary': [0.9, 0.9, 1, 0.9],
                'secondary': [1, 1, 1, 0.7],
                'glow': [0.9, 0.9, 1, 0.4]
            },
            'anger': {
                'primary': [1, 0.3, 0.3, 0.9],
                'secondary': [1, 0.5, 0.4, 0.7],
                'glow': [1, 0.3, 0.3, 0.35]
            },
            'fear': {
                'primary': [0.7, 0.5, 0.9, 0.85],
                'secondary': [0.8, 0.6, 1, 0.65],
                'glow': [0.7, 0.5, 0.9, 0.25]
            },
            'tired': {
                'primary': [0.4, 0.6, 0.8, 0.75],
                'secondary': [0.5, 0.7, 0.9, 0.55],
                'glow': [0.4, 0.6, 0.8, 0.15]
            }
        }
        
        # Bind emotion changes
        self.bind(emotion=self.on_emotion_change)
        
        # Start animation loop
        Clock.schedule_interval(self.update, 1/60)
        
        # Random behaviors
        Clock.schedule_interval(self.random_behavior, random.uniform(3, 8))
        
    def on_emotion_change(self, instance, value):
        """Handle emotion changes with smooth transitions"""
        if value in self.emotion_colors:
            colors = self.emotion_colors[value]
            
            # Animate color transition
            anim = Animation(
                primary_color=colors['primary'],
                secondary_color=colors['secondary'],
                glow_color=colors['glow'],
                duration=0.8,
                t='out_quad'
            )
            anim.start(self)
            
            # Set expression
            self.eye_expression = self._get_expression(value)
            
            # Adjust scale based on emotion
            if value == 'happy':
                self.target_scale = 1.1
            elif value in ['sadness', 'depression', 'tired']:
                self.target_scale = 0.9
            elif value == 'panic':
                self.target_scale = 1.15
            elif value == 'shock':
                self.target_scale = 1.2
            else:
                self.target_scale = 1.0
    
    def _get_expression(self, emotion):
        """Get eye expression for emotion"""
        expressions = {
            'neutral': 'calm',
            'happy': 'happy',
            'sadness': 'sad',
            'anxiety': 'worried',
            'panic': 'scared',
            'depression': 'down',
            'shock': 'wide',
            'anger': 'angry',
            'fear': 'scared',
            'tired': 'sleepy'
        }
        return expressions.get(emotion, 'calm')
    
    def update(self, dt):
        """Main animation update loop"""
        self.time += dt
        
        # Breathing animation
        self.breath_phase += dt * 2
        
        # Smooth scale transition
        self.base_scale += (self.target_scale - self.base_scale) * 0.05
        
        # Trigger redraw
        self.canvas.ask_update()
        
    def random_behavior(self, dt):
        """Perform random cute behaviors"""
        behaviors = ['bounce', 'wobble', 'pulse', 'tilt']
        behavior = random.choice(behaviors)
        
        if behavior == 'bounce':
            anim = Animation(
                y=self.y + 10,
                duration=0.2,
                t='out_quad'
            ) + Animation(
                y=self.y - 10,
                duration=0.2,
                t='in_quad'
            ) + Animation(
                y=self.y,
                duration=0.2,
                t='out_quad'
            )
            anim.start(self)
            
        elif behavior == 'pulse':
            original_scale = self.target_scale
            self.target_scale = original_scale * 1.1
            Clock.schedule_once(lambda dt: setattr(self, 'target_scale', original_scale), 0.3)
            
        elif behavior == 'tilt':
            anim = Animation(
                rotation=10,
                duration=0.3
            ) + Animation(
                rotation=-10,
                duration=0.3
            ) + Animation(
                rotation=0,
                duration=0.3
            )
            anim.start(self)
        
        # Schedule next behavior
        Clock.schedule_once(
            lambda dt: Clock.schedule_once(self.random_behavior, random.uniform(3, 8)),
            1
        )
    
    def on_touch_down(self, touch):
        """React to touch with happy animation"""
        if self.collide_point(*touch.pos):
            # Happy reaction
            original_emotion = self.emotion
            self.emotion = 'happy'
            
            # Return to original emotion after a moment
            Clock.schedule_once(
                lambda dt: setattr(self, 'emotion', original_emotion),
                2
            )
            return True
        return super().on_touch_down(touch)