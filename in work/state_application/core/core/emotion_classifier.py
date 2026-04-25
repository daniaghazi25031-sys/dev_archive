"""
Emotion Classifier
Analyzes text to determine emotional state with Arabic/Iraqi dialect support
"""

import re
from typing import Tuple, Dict, List
from utils.arabic_processor import ArabicProcessor


class EmotionClassifier:
    """
    Lightweight emotion classifier supporting Arabic (especially Iraqi dialect)
    and English with misspelling tolerance
    """
    
    def __init__(self):
        self.arabic_processor = ArabicProcessor()
        self._init_emotion_patterns()
        self._init_iraqi_patterns()
        self._init_english_patterns()
        
    def _init_emotion_patterns(self):
        """Initialize emotion keyword patterns"""
        # Emotion categories with intensity weights
        self.emotions = {
            'panic': {'weight': 1.0, 'keywords': {}},
            'anxiety': {'weight': 0.8, 'keywords': {}},
            'sadness': {'weight': 0.7, 'keywords': {}},
            'depression': {'weight': 0.9, 'keywords': {}},
            'shock': {'weight': 0.85, 'keywords': {}},
            'anger': {'weight': 0.6, 'keywords': {}},
            'fear': {'weight': 0.75, 'keywords': {}},
            'tired': {'weight': 0.4, 'keywords': {}},
            'neutral': {'weight': 0.1, 'keywords': {}},
            'happy': {'weight': 0.3, 'keywords': {}}
        }
    
    def _init_iraqi_patterns(self):
        """Initialize Iraqi Arabic dialect patterns"""
        # Iraqi dialect keywords with common misspellings
        iraqi_patterns = {
            'panic': {
                'keywords': [
                    # "I'm having a panic attack" variations
                    'جنط', 'جنت', 'جنتط', 'جنطه', 'جنتي',
                    # "I'm scared" / "fear"
                    'خايف', 'خائف', 'خييف', 'خيفان', 'خوف',
                    # "My heart is racing"
                    'كلبي يرتجف', 'قلبي يرتجف', 'كلبي يدق',
                    # "I can't breathe"
                    'ما اقدر اتنفس', 'ما أقدر أتنفس', 'صدري يضيق',
                    # Panic expressions
                    'وكت', 'وكته', 'حاله', 'اتعبت'
                ],
                'phrases': [
                    'جنط عليه', 'خايف موت', 'كلبي يدق بسرعه',
                    'ما اكدر اتنفس', 'صدري ضيق', 'احس بجنط'
                ]
            },
            'anxiety': {
                'keywords': [
                    'قلق', 'قلقان', 'متوتر', 'توتر', 'ضايج',
                    'كاهل', 'احس بضغط', 'متحمس', 'مش مرتاح',
                    'سترس', 'stress', 'قلقان'
                ],
                'phrases': [
                    'متوتر كثير', 'قلقان على', 'كاهل من',
                    'ما ني مرتاح', 'ضغط نفسي'
                ]
            },
            'sadness': {
                'keywords': [
                    'حزين', 'حزن', 'زعلان', 'زعل', 'مكروب',
                    'كئيب', 'دمع', 'بجي', 'ابجي', 'مبسوط',
                    'وحيد', 'وحدة', 'متعب', 'تعبان',
                    # Misspelled variations
                    'حزينن', 'زعللان', 'كئييب'
                ],
                'phrases': [
                    'زعلان من', 'حزين على', 'مكروب على',
                    'احس بفراغ', 'وحيد', 'ما حدا يفهمني',
                    'روحي تعبانة'
                ]
            },
            'depression': {
                'keywords': [
                    'اكتئاب', 'مكتئب', 'يأس', 'يائس', 'فشل',
                    'ما عاد', 'ما عاد اريد', 'ما تك', 'موت',
                    'انتحار', 'اقتل', 'ميت', 'ماموت',
                    'فاضي', 'فراغ', 'لا معنى', 'بلا معنى',
                    # Iraqi expressions for hopelessness
                    'خلاص', 'تعبان روحيا', 'ما عاد الهم'
                ],
                'phrases': [
                    'ما عاد الهم احيا', 'تعبان روحيا',
                    'حياتي بلا معنى', 'فشلت', 'ما عاد اقدر',
                    'اكره حياتي', 'ودي اموت', 'ما عادني قادر'
                ]
            },
            'shock': {
                'keywords': [
                    'صدمة', 'مصدوم', 'صدم', 'انهيار', 'انهارت',
                    'ما صدقت', 'مستغرب', 'غريب', 'كارثة',
                    'فجاة', 'مفاجأة', 'مفاجاة'
                ],
                'phrases': [
                    'صدمتني', 'مصدوم من', 'انهيت',
                    'ما متوقعة', 'صدمة كبيرة', 'كارثة'
                ]
            },
            'anger': {
                'keywords': [
                    'غاضب', 'غضب', 'زعل', 'عصبي', 'عصبية',
                    'اعصب', 'حارق', 'يحرق', 'مستفز'
                ],
                'phrases': [
                    'معصب من', 'زعلان على', 'يحرق دمي',
                    'مستفزني', 'كافر'
                ]
            },
            'fear': {
                'keywords': [
                    'خوف', 'خائف', 'خايف', 'مرعوب', 'رعب',
                    'فزع', 'فزاعة', 'هول'
                ],
                'phrases': [
                    'خايف من', 'مرعوب من', 'فزعت من',
                    'احس بخوف'
                ]
            },
            'tired': {
                'keywords': [
                    'تعب', 'تعبان', 'مرهق', 'ارهاق', 'كسلان',
                    'نوم', 'ناعس', 'سهران', 'تعب جسد',
                    'طاقة', 'ما عندي طاقة'
                ],
                'phrases': [
                    'تعبان كثير', 'ما عندي طاقة',
                    'ارهاق شديد', 'ودي انام', 'سهران'
                ]
            },
            'neutral': {
                'keywords': [
                    'عادي', 'مثل ما هو', 'طبيعي', 'تمام',
                    'زين', 'مستمر', 'عادي جدا'
                ],
                'phrases': [
                    'كل شيء عادي', 'ما صار شي',
                    'يوم عادي', 'تمام الحمد لله'
                ]
            },
            'happy': {
                'keywords': [
                    'سعيد', 'سعاده', 'فرح', 'فرحان', 'مبسوط',
                    'مستانس', 'سويت', 'حلو', 'جميل',
                    'شكرا', 'ممنون', 'امتنان'
                ],
                'phrases': [
                    'مبسوط كثير', 'فرحان', 'يوم حلو',
                    'شكرا الك', 'الله يوفقك'
                ]
            }
        }
        
        self.iraqi_patterns = iraqi_patterns
    
    def _init_english_patterns(self):
        """Initialize English patterns with common misspellings"""
        english_patterns = {
            'panic': {
                'keywords': [
                    'panic', 'panik', 'panicking', 'panick', 'panc',
                    'scared', 'skared', 'freaking out', 'freakin',
                    'cant breathe', 'cannot breathe', 'heart racing',
                    'hyperventilating', 'attack'
                ],
                'phrases': [
                    'having a panic attack', 'panic attack',
                    'cant breath', 'my heart', 'freaking out'
                ]
            },
            'anxiety': {
                'keywords': [
                    'anxious', 'anxiety', 'anxity', 'anxiou',
                    'worried', 'worry', 'nervous', 'nervos',
                    'stress', 'stressed', 'stressd', 'tense',
                    'overthinking', 'over thinking'
                ],
                'phrases': [
                    'feeling anxious', 'so worried', 'stressed out',
                    'anxiety attack', 'overthinking everything'
                ]
            },
            'sadness': {
                'keywords': [
                    'sad', 'sadd', 'unhappy', 'crying', 'cry', 'cri',
                    'tears', 'down', 'lonely', 'lonly', 'alone',
                    'miss', 'missing', 'grief', 'heartbroken'
                ],
                'phrases': [
                    'feeling sad', 'so sad', 'im sad', 'really down',
                    'feeling lonely', 'miss them', 'want to cry'
                ]
            },
            'depression': {
                'keywords': [
                    'depressed', 'depression', 'depressd', 'depres',
                    'hopeless', 'worthless', 'empty', 'no point',
                    'suicidal', 'kill myself', 'end it', 'die',
                    'tired of life', 'nothing matters', 'give up'
                ],
                'phrases': [
                    'feeling depressed', 'so depressed', 'want to die',
                    'no reason to live', 'tired of everything',
                    'nothing matters anymore', 'hate my life'
                ]
            },
            'shock': {
                'keywords': [
                    'shocked', 'shock', 'shok', 'devastated',
                    'disaster', 'unbelievable', 'unexpected',
                    'trauma', 'traumatic'
                ],
                'phrases': [
                    'cant believe', 'in shock', 'so shocked',
                    'didnt expect', 'completely unexpected'
                ]
            },
            'anger': {
                'keywords': [
                    'angry', 'angery', 'mad', 'furious', 'pissed',
                    'frustrated', 'annoyed', 'irritated', 'rage'
                ],
                'phrases': [
                    'so angry', 'really mad', 'pissed off',
                    'frustrating', 'makes me mad'
                ]
            },
            'fear': {
                'keywords': [
                    'afraid', 'fear', 'terrified', 'horrified',
                    'petrified', 'scary', 'nightmare'
                ],
                'phrases': [
                    'im afraid', 'so scared', 'terrified of',
                    'really afraid'
                ]
            },
            'tired': {
                'keywords': [
                    'tired', 'exhausted', 'exausted', 'fatigue',
                    'sleepy', 'drained', 'worn out', 'burnout'
                ],
                'phrases': [
                    'so tired', 'really exhausted', 'no energy',
                    'completely drained', 'need sleep'
                ]
            },
            'neutral': {
                'keywords': [
                    'okay', 'ok', 'fine', 'normal', 'alright',
                    'nothing', 'bored', 'meh', 'whatever'
                ],
                'phrases': [
                    'im okay', 'everything fine', 'nothing special',
                    'just normal'
                ]
            },
            'happy': {
                'keywords': [
                    'happy', 'hapy', 'glad', 'joy', 'excited',
                    'great', 'awesome', 'amazing', 'wonderful',
                    'blessed', 'grateful', 'thankful'
                ],
                'phrases': [
                    'feeling happy', 'so happy', 'really glad',
                    'great day', 'feeling blessed', 'thank you'
                ]
            }
        }
        
        self.english_patterns = english_patterns
    
    def classify(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Classify the emotional content of text
        
        Args:
            text: Input text (Arabic or English)
            
        Returns:
            Tuple of (primary_emotion, confidence, all_scores)
        """
        if not text or not text.strip():
            return 'neutral', 0.5, {'neutral': 0.5}
        
        # Detect language
        is_arabic = self.arabic_processor.is_arabic(text)
        
        # Normalize text
        if is_arabic:
            normalized = self.arabic_processor.normalize(text)
            patterns = self.iraqi_patterns
        else:
            normalized = text.lower().strip()
            patterns = self.english_patterns
        
        # Calculate emotion scores
        scores = {}
        
        for emotion, data in patterns.items():
            score = 0.0
            
            # Check keywords
            for keyword in data['keywords']:
                if keyword in normalized:
                    # Higher score for exact matches
                    score += 1.0
                    
                    # Check for intensity words
                    intensity_words = ['كثير', 'very', 'so', 'really', 'جدًا', 'مره', 'مرت']
                    for iw in intensity_words:
                        if iw in normalized:
                            score *= 1.3
            
            # Check phrases (higher weight)
            for phrase in data['phrases']:
                if phrase in normalized:
                    score += 2.0
            
            scores[emotion] = score
        
        # If no emotion detected, check for context
        if sum(scores.values()) == 0:
            scores = self._analyze_context(text, normalized, is_arabic)
        
        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            scores = {k: v/total for k, v in scores.items()}
        else:
            scores['neutral'] = 1.0
        
        # Get primary emotion
        primary = max(scores, key=scores.get)
        confidence = scores[primary]
        
        # Apply intensity modifiers
        primary, confidence = self._adjust_intensity(
            primary, confidence, text, is_arabic
        )
        
        return primary, confidence, scores
    
    def _analyze_context(self, original: str, normalized: str, is_arabic: bool) -> Dict[str, float]:
        """Analyze context when no keywords match"""
        scores = {'neutral': 0.5}
        
        # Check for emoticons and emojis
        sad_emoticons = [':(', ':((', ':‚' '😭', '😢', '😞', '😔']
        happy_emoticons = [':)', ':))', ':D', '😊', '🙂', '😄']
        anxious_emoticons = ['😰', '😱', '😨']
        
        for emot in sad_emoticons:
            if emot in original:
                scores['sadness'] = scores.get('sadness', 0) + 0.5
        
        for emot in happy_emoticons:
            if emot in original:
                scores['happy'] = scores.get('happy', 0) + 0.5
        
        for emot in anxious_emoticons:
            if emot in original:
                scores['panic'] = scores.get('panic', 0) + 0.5
        
        # Check for punctuation patterns
        if '!' in original or '!!' in original:
            scores['anxiety'] = scores.get('anxiety', 0) + 0.2
        if '...' in original:
            scores['sadness'] = scores.get('sadness', 0) + 0.2
        
        return scores
    
    def _adjust_intensity(self, emotion: str, confidence: float, text: str, is_arabic: bool) -> Tuple[str, float]:
        """Adjust emotion intensity based on modifiers"""
        
        # High intensity indicators
        high_intensity = [
            'موووت', 'جدًا', 'كثير', 'مره', 'very', 'so', 'really',
            'extremely', 'تماماً', 'اكثر', 'very much'
        ]
        
        # Low intensity indicators
        low_intensity = [
            'شوي', 'قليل', 'a little', 'bit', 'somewhat', 'kinda'
        ]
        
        text_lower = text.lower()
        
        for word in high_intensity:
            if word in text_lower:
                confidence = min(confidence * 1.3, 1.0)
                break
        
        for word in low_intensity:
            if word in text_lower:
                confidence *= 0.7
                break
        
        return emotion, confidence