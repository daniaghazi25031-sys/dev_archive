"""
Arabic Text Processor
Handles Arabic text normalization, RTL support, and Iraqi dialect processing
"""

import re
import unicodedata
from typing import List, Tuple


class ArabicProcessor:
    """
    Processes Arabic text with focus on Iraqi dialect support
    Handles normalization, misspellings, and text direction
    """
    
    def __init__(self):
        self._init_normalization_maps()
        self._init_iraqi_dictionary()
        
    def _init_normalization_maps(self):
        """Initialize character normalization mappings"""
        # Arabic letter variants that should be unified
        self.alef_variants = ['أ', 'إ', 'آ', 'ٱ']
        self.yeh_variants = ['ى', 'ي', 'ئ']
        self.teh_marbuta = ['ة', 'ه', 'ت']
        
        # Diacritics to remove
        self.diacritics = [
            '\u064B',  # Fathatan
            '\u064C',  # Dammatan
            '\u064D',  # Kasratan
            '\u064E',  # Fatha
            '\u064F',  # Damma
            '\u0650',  # Kasra
            '\u0651',  # Shadda
            '\u0652',  # Sukun
            '\u0670',  # Dagger alef
        ]
        
    def _init_iraqi_dictionary(self):
        """Initialize Iraqi dialect dictionary for normalization"""
        # Common Iraqi misspellings and their correct forms
        self.iraqi_corrections = {
            # Iraqi "I want" variations
            'ريد': 'اريد',
            'اريد': 'اريد',
            'ودي': 'اريد',
            
            # Iraqi "can/able" variations
            'اكدر': 'اقدر',
            'اكدر': 'اقدر',
            'مكدر': 'ما اقدر',
            
            # Iraqi "now" variations
            'هلأ': 'هالحين',
            'هلحين': 'هالحين',
            'هلوقت': 'هالحين',
            
            # Iraqi "this" variations
            'هاي': 'هذي',
            'هاي': 'هذا',
            'هاذ': 'هذا',
            
            # Iraqi "why" variations
            'ليش': 'ليش',
            'لشنو': 'لماذا',
            
            # Iraqi "what" variations
            'شكد': 'كم',
            'شكو': 'كيف',
            'شني': 'شنو',
            
            # Iraqi intensifiers
            'هواي': 'كثير',
            'وايد': 'كثير',
            'مرة': 'كثير',
            'مره': 'كثير',
            
            # Iraqi "there is/are"
            'اكو': 'في',
            'ماكو': 'ما في',
            
            # Iraqi emotional expressions
            'جنط': 'خوف شديد',
            'جنت': 'خوف شديد',
            'كاهل': 'قلقان',
            'ضايج': 'حزين',
            'مبسوط': 'سعيد',
            'مكروب': 'حزين',
        }
        
        # Common typos and their corrections
        self.typo_corrections = {
            'اني': 'اني',
            'انتي': 'انتي',
            'احنا': 'احنا',
            'كلكم': 'كلكم',
            'الحة': 'الحين',
            'الحنة': 'الحين',
        }
    
    def is_arabic(self, text: str) -> bool:
        """Check if text contains Arabic characters"""
        if not text:
            return False
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
        return bool(arabic_pattern.search(text))
    
    def normalize(self, text: str) -> str:
        """
        Normalize Arabic text for processing
        
        Args:
            text: Input Arabic text
            
        Returns:
            Normalized text with unified characters
        """
        if not text:
            return ""
        
        # Convert to lowercase for mixed text
        normalized = text
        
        # Remove diacritics
        for diacritic in self.diacritics:
            normalized = normalized.replace(diacritic, '')
        
        # Normalize alef variants
        for variant in self.alef_variants:
            normalized = normalized.replace(variant, 'ا')
        
        # Normalize yeh variants at end of word
        normalized = re.sub(r'ى$', 'ي', normalized)
        normalized = re.sub(r'ى(\s)', r'ي\1', normalized)
        
        # Normalize teh marbuta
        normalized = normalized.replace('ة', 'ه')
        
        # Remove tatweel
        normalized = normalized.replace('\u0640', '')
        
        # Normalize whitespace
        normalized = ' '.join(normalized.split())
        
        # Apply Iraqi corrections
        for wrong, correct in self.iraqi_corrections.items():
            # Only replace full words
            normalized = re.sub(r'\b' + wrong + r'\b', correct, normalized)
        
        return normalized
    
    def correct_spelling(self, text: str) -> Tuple[str, List[str]]:
        """
        Attempt to correct common misspellings
        
        Args:
            text: Input text with potential misspellings
            
        Returns:
            Tuple of (corrected_text, list_of_corrections)
        """
        corrections = []
        corrected = text
        
        for wrong, right in self.typo_corrections.items():
            if wrong in corrected:
                corrected = corrected.replace(wrong, right)
                corrections.append(f"{wrong} → {right}")
        
        # Apply Iraqi dialect corrections
        for iraqi, standard in self.iraqi_corrections.items():
            if iraqi in corrected and len(iraqi) > 2:
                # Don't replace, just note the meaning
                corrections.append(f"'{iraqi}' فهمت بمعنى '{standard}'")
        
        return corrected, corrections
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from Arabic text"""
        # Normalize text
        normalized = self.normalize(text)
        
        # Split into words
        words = normalized.split()
        
        # Filter out short words and common stop words
        stop_words = {
            'من', 'الى', 'على', 'في', 'عن', 'مع', 'هذا', 'هذه',
            'التي', 'الذي', 'التي', 'كان', 'كانت', 'هو', 'هي',
            'ان', 'انه', 'اني', 'ما', 'لا', 'لم', 'لن', 'او',
            'و', 'ثم', 'بل', 'لكن', 'لكن', 'حتى', 'اذ', 'اذا'
        }
        
        keywords = [w for w in words if len(w) > 2 and w not in stop_words]
        
        return keywords
    
    def detect_sentiment_words(self, text: str) -> List[Tuple[str, str]]:
        """
        Detect sentiment-bearing words
        
        Returns:
            List of (word, sentiment) tuples
        """
        # Define sentiment word lists
        positive_words = {
            'سعيد', 'سعاده', 'فرح', 'فرحان', 'مبسوط', 'مستانس',
            'حلو', 'جميل', 'زين', 'خير', 'بركة', 'شكرا',
            'حب', 'محبة', 'امان', 'راحة', 'طمأنينة'
        }
        
        negative_words = {
            'حزين', 'حزن', 'زعلان', 'مكروب', 'كئيب', 'ضايج',
            'خايف', 'خوف', 'قلق', 'قلقان', 'توتر', 'متحمس',
            'غضب', 'غاضب', 'عصبي', 'زعل', 'مزعوج',
            'تعب', 'تعبان', 'مرهق', 'كسلان', 'ارهاق',
            'اكتئاب', 'يأس', 'فشل', 'موت', 'جنط'
        }
        
        normalized = self.normalize(text)
        words = normalized.split()
        
        sentiments = []
        for word in words:
            if word in positive_words:
                sentiments.append((word, 'positive'))
            elif word in negative_words:
                sentiments.append((word, 'negative'))
        
        return sentiments
    
    def get_rtl_text(self, text: str) -> str:
        """
        Ensure proper RTL rendering for Arabic text
        
        This handles the RTL/LTR direction properly for display
        """
        if not text:
            return text
        
        # Add RTL mark at the beginning if text is Arabic
        if self.is_arabic(text):
            # RTL mark character
            rtl_mark = '\u202B'
            # LTR mark for numbers/English
            ltr_mark = '\u202A'
            
            # Check for mixed content
            has_english = bool(re.search(r'[a-zA-Z]', text))
            has_numbers = bool(re.search(r'[0-9]', text))
            
            if has_english or has_numbers:
                # Complex mixed text - let the UI handle it
                return text
            else:
                # Pure Arabic text
                return rtl_mark + text
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize Arabic text into words"""
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split by whitespace
        tokens = text.split()
        
        return tokens