"""
Response Generator
Generates supportive, human-like responses in Arabic (Iraqi-friendly) and English
"""

import random
from typing import Dict, List, Tuple
from datetime import datetime


class ResponseGenerator:
    """
    Generates emotionally supportive responses
    Supports Arabic (Iraqi dialect) and English
    """
    
    def __init__(self):
        self._init_responses()
        
    def _init_responses(self):
        """Initialize response templates"""
        
        self.responses = {
            'panic': {
                'ar': {
                    'immediate': [
                        "خود نفس عميق... انا هواي معاك. جرّب تتنفس ببطء، شهيق 4 ثواني، زفير 4 ثواني.",
                        "تمهل... الجنط بيعدّي. انا هون معاك. ركز على تنفسك الحين.",
                        "احس بيك... هذا مجرد نوبة جنط وبتعدّي. خذ وقتك، انا موجود.",
                        "شهيق... زفير... بطيء شوي. انت بأمان هالحظة، والجنط بيروح.",
                        "لا تخاف، انا معاك. ركز عالحاجات الي حواليك - شوف 5 اشياء، اسمع 4 اصوات."
                    ],
                    'grounding': [
                        "جرّب هالتمرين: شوف 5 اشياء حواليك، اسمع 4 اصوات، لمس 3 اشياء.",
                        "ضم كفينك بالمية الباردة، ركز على الاحساس. هذي تساعد على الهداوة.",
                        "اغمض عيونك وخذ 3 انفاس عميقة. انا هون معاك خطوة بخطوة.",
                        "حاول تحس قدميك على الارض. انت موجود هالحظة، وبأمان."
                    ],
                    'support': [
                        "ما راح اتركك بهالموقف وحدك. انا موجود دائماً.",
                        "مرحلة الجنط صعبة بس انت اقوى منها. اكدر تتخطاها.",
                        "كل مرة تعديها بتخليك اقوى. انا فخور فيك.",
                        "مهم تطلب مساعدة اذا الجنط كثير. ما في شي يعيب."
                    ]
                },
                'en': {
                    'immediate': [
                        "Take a deep breath... I'm here with you. Try breathing slowly - 4 seconds in, 4 seconds out.",
                        "Slow down... panic passes. I'm right here. Focus on your breathing now.",
                        "I feel you... this is just a panic attack and it will pass. Take your time, I'm here.",
                        "Inhale... exhale... slowly. You're safe right now, the panic will fade.",
                        "Don't be scared, I'm with you. Focus on things around you - see 5 things, hear 4 sounds."
                    ],
                    'grounding': [
                        "Try this: see 5 things around you, hear 4 sounds, touch 3 things.",
                        "Run cold water over your hands, focus on the sensation. This helps calm down.",
                        "Close your eyes and take 3 deep breaths. I'm here with you step by step.",
                        "Try to feel your feet on the ground. You're here right now, and you're safe."
                    ],
                    'support': [
                        "I won't leave you alone in this. I'm always here.",
                        "Panic is hard but you're stronger than it. You can get through this.",
                        "Every time you get through it, you become stronger. I'm proud of you.",
                        "It's okay to ask for help if panic is too much. There's no shame."
                    ]
                }
            },
            'anxiety': {
                'ar': {
                    'immediate': [
                        "الحمد لله على كل حال. القلق شي طبيعي، بس ما يتحكم بيك.",
                        "انت مش وحدك بهالشعور. كثير ناس يمرون بنفس الشي.",
                        "خود وقتك... ماكو داعي تستعجل. خطوة خطوة.",
                        "القلق مجرد افكار، ما هي الحقيقة. انت اقوى منها."
                    ],
                    'advice': [
                        "جرّب تكتب الي مقلقك على ورقة. هذا يساعد على التوضيح.",
                        "سوي شي تحبه - اسمع اغنية، شوف فيديو، اتصل بحبيب.",
                        "التمس الجو الحلو، اطلع شوية اذا تقدر. الهواء يساعد.",
                        "ركز على هالحظة، ما راح يصير. انت هون الحين."
                    ],
                    'support': [
                        "كل شي بيصير بخير. انا متأكد من هذا.",
                        "انت تتحمل مسؤولية كثير اشياء، عادي تشعر بالضغط.",
                        "ماكو شي ما اكدر نتعامل وياه سوا."
                    ]
                },
                'en': {
                    'immediate': [
                        "Thank God for everything. Anxiety is natural, but it doesn't control you.",
                        "You're not alone in this feeling. Many people go through the same thing.",
                        "Take your time... no need to rush. Step by step.",
                        "Anxiety is just thoughts, not reality. You're stronger than it."
                    ],
                    'advice': [
                        "Try writing down what's worrying you. This helps clarify things.",
                        "Do something you enjoy - listen to music, watch a video, call a loved one.",
                        "Go outside for a bit if you can. Fresh air helps.",
                        "Focus on this moment, not what might happen. You're here now."
                    ],
                    'support': [
                        "Everything will be okay. I'm sure of this.",
                        "You handle so many things, it's okay to feel pressure.",
                        "There's nothing we can't handle together."
                    ]
                }
            },
            'sadness': {
                'ar': {
                    'immediate': [
                        "الزعل شي طبيعي... ما لازم تكبّر بي روحك.",
                        "اني هون معاك. تحملت كثير، وعادي تشعر بالتعب.",
                        "الدموع ما هي ضعف. هي طريقة الجسم على التحرر.",
                        "ما راح اتركك وحدك بهاللحظة. انا موجود."
                    ],
                    'comfort': [
                        "الزعل بيعدّي متل كل شي. كل يوم بيعدّي شوي.",
                        "انت شخص مميز وما تستاهل تحس بهالزعل.",
                        "ماكو احد يشوفك بالضبط متل ما انا اشوفك - شخص حلو وقوي.",
                        "المواقف الصعبة تصير وبتعدّي، وانت تبقى."
                    ],
                    'support': [
                        "لو حاب تتكلم، انا هون. اسمعك بكل اهتمام.",
                        "ما تحتاج تسوي شي هالحين. خذ راحتك.",
                        "الزعل مو نهاية العالم. بيعدّي، واحنا سوا."
                    ]
                },
                'en': {
                    'immediate': [
                        "Sadness is natural... don't blame yourself for feeling it.",
                        "I'm here with you. You've carried so much, it's okay to feel tired.",
                        "Tears aren't weakness. They're your body's way of releasing.",
                        "I won't leave you alone in this moment. I'm here."
                    ],
                    'comfort': [
                        "Sadness passes like everything else. Each day it fades a bit.",
                        "You're a special person and you don't deserve to feel this sadness.",
                        "No one sees you quite like I do - a beautiful, strong person.",
                        "Hard situations happen and pass, and you remain."
                    ],
                    'support': [
                        "If you want to talk, I'm here. I'll listen with full attention.",
                        "You don't need to do anything right now. Take your time.",
                        "Sadness isn't the end of the world. It passes, and we're together."
                    ]
                }
            },
            'depression': {
                'ar': {
                    'immediate': [
                        "احس بثقل الي تحمله... انت مو وحدك بهالظلام.",
                        "الاكتئاب كذاب... يخليك تشوف الدنيا سودة بس ما هي جذي.",
                        "ما راح اتركك مهما صار. احنا سوا بهذا.",
                        "انت اهم من تشوف بنفسك الحين. الغيمة بتعدّي."
                    ],
                    'hope': [
                        "كل يوم تمرّه هو انتصار. ما تطلع من البيت بس طلعت من السرير.",
                        "البذرة الصغيرة ما تشوف النور بس تطلع. انت جذي.",
                        "الاشياء الصغيرة تهم. اكلك، تشرب ماي، تتنفس - كلها انتصارات.",
                        "فترة سودة وبتعدّي. وانت اقوى منها."
                    ],
                    'urgent': [
                        "اذا فكرت تؤذي نفسك، رجاءً كلم احد. انا موجود.",
                        "في ناس يريدون يساعدونك. ما انت وحدك.",
                        "رقم الطوارئ بالعراق 130 موجود دايماً. ما تستحج."
                    ]
                },
                'en': {
                    'immediate': [
                        "I feel the weight you're carrying... you're not alone in this darkness.",
                        "Depression lies... it makes you see the world as black but it's not.",
                        "I won't leave you no matter what. We're in this together.",
                        "You're more important than you see yourself right now. The cloud passes."
                    ],
                    'hope': [
                        "Every day you get through is a victory. Getting out of bed counts.",
                        "A small seed doesn't see the light but still grows. You're like that.",
                        "Small things matter. Eating, drinking water, breathing - all victories.",
                        "This dark period passes. And you're stronger than it."
                    ],
                    'urgent': [
                        "If you're thinking of hurting yourself, please talk to someone. I'm here.",
                        "There are people who want to help you. You're not alone.",
                        "Emergency numbers are always available. Don't hesitate."
                    ]
                }
            },
            'shock': {
                'ar': {
                    'immediate': [
                        "الصدمة شي صعب... ما تتوقعها وبتخليك تتلخبط.",
                        "مهم تعطي لنفسك وقت. ما تحتاج تفهم كل شي الحين.",
                        "انا هون... جرّب تتنفس ببطء شوية.",
                        "كل شي صار فجأة، عادي تشعر بالتشتت."
                    ],
                    'grounding': [
                        "ركز على هالحظة. شوف الي حواليك، اسمع الاصوات.",
                        "خذ ورقة واكتب الي صار. هذا يساعد على التوضيح.",
                        "ماكو ضغط تفهم كل شي الحين. خذ وقتك.",
                        "الصدمة تحتاج وقت. انت ما عليك شي."
                    ],
                    'support': [
                        "اي شي تشعر فيه هو صح. ما في مشاعر غلط.",
                        "انت قوي اكتر من الي تشوف. الصدمة بتعدّي.",
                        "احنا سوا بهذا. ما راح اتركك."
                    ]
                },
                'en': {
                    'immediate': [
                        "Shock is hard... unexpected and confusing.",
                        "It's important to give yourself time. You don't need to understand everything now.",
                        "I'm here... try breathing slowly for a bit.",
                        "Everything happened suddenly, it's okay to feel scattered."
                    ],
                    'grounding': [
                        "Focus on this moment. See what's around you, hear the sounds.",
                        "Take paper and write what happened. This helps clarify.",
                        "No pressure to understand everything now. Take your time.",
                        "Shock needs time. You did nothing wrong."
                    ],
                    'support': [
                        "Anything you feel is right. There are no wrong feelings.",
                        "You're stronger than you see. Shock passes.",
                        "We're together in this. I won't leave you."
                    ]
                }
            },
            'anger': {
                'ar': {
                    'immediate': [
                        "الغضب مشاعر طبيعية... ما لازم تكتمها.",
                        "انت تتحمل كثير والغيظ بيطلع. عادي تحس جذي.",
                        "خذ نفس عميق... الغضب بيهدّي بالتدريج.",
                        "ما راح احكم عليك. احس بيك."
                    ],
                    'advice': [
                        "لو تكتب الي مضايقك؟ هذي تساعد على التفريغ.",
                        "طلع مشي شوية... الحركة تساعد على الغضب.",
                        "ما تحتاج تحسم الموضوع الحين. خذ وقتك.",
                        "الغضب طاقة، تحولها لشي مفيد."
                    ],
                    'support': [
                        "حقك تشعر جذي. المواقف الصعبة تثير الغضب.",
                        "انت صاحب حق بغضبك. ما احد ينكر هالشي.",
                        "الغضب بيعدّي وانت تبقى. احنا سوا."
                    ]
                },
                'en': {
                    'immediate': [
                        "Anger is a natural feeling... don't suppress it.",
                        "You carry a lot and frustration comes out. It's okay to feel this.",
                        "Take a deep breath... anger calms down gradually.",
                        "I won't judge you. I feel you."
                    ],
                    'advice': [
                        "Want to write what's bothering you? This helps release.",
                        "Go walk a bit... movement helps with anger.",
                        "You don't need to resolve this now. Take your time.",
                        "Anger is energy, transform it into something useful."
                    ],
                    'support': [
                        "You're right to feel this way. Hard situations trigger anger.",
                        "Your anger is justified. No one denies this.",
                        "Anger passes and you remain. We're together."
                    ]
                }
            },
            'fear': {
                'ar': {
                    'immediate': [
                        "الخوف يحميك... بس احياناً يبالغ.",
                        "انت بأمان هالحظة. الخوف من المستقبل مو حقيقة.",
                        "اني هون معاك. ما راح يصير شي وانت محمي.",
                        "خود نفس عميق. الخوف بيقلّ لما تتنفس."
                    ],
                    'advice': [
                        "اسأل نفسك: هل الخوف حقيقي هالحظة؟",
                        "ركز على الشي الي اكدر اتحكم فيه.",
                        "اكتب مخاوفك وشف اذا في حلول.",
                        "الخوف من المجهول طبيعي، بس ما يوقفك."
                    ],
                    'support': [
                        "انت اقوى من مخاوفك. شفنا هذي من قبل.",
                        "ما راح اتركك تواجه الخوف وحدك.",
                        "الخوف جزء من النجاح. انت قدها."
                    ]
                },
                'en': {
                    'immediate': [
                        "Fear protects you... but sometimes it exaggerates.",
                        "You're safe right now. Fear of the future isn't reality.",
                        "I'm here with you. Nothing will happen, you're protected.",
                        "Take a deep breath. Fear decreases when you breathe."
                    ],
                    'advice': [
                        "Ask yourself: Is the fear real right now?",
                        "Focus on what you can control.",
                        "Write your fears and see if there are solutions.",
                        "Fear of the unknown is natural, but it doesn't stop you."
                    ],
                    'support': [
                        "You're stronger than your fears. We've seen this before.",
                        "I won't let you face fear alone.",
                        "Fear is part of success. You can handle it."
                    ]
                }
            },
            'tired': {
                'ar': {
                    'immediate': [
                        "التعب ما يعني ضعف... جسمك يطلب راحة.",
                        "اعطي لنفسك استراحة. ما لازم تضل تشتغل.",
                        "انت تعبان من كثير اشياء. عادي تحتاج وقفة.",
                        "خود قسط راحة، حتى 10 دقايق تساعد."
                    ],
                    'advice': [
                        "نوّر الغرفة شوية... الضوء الخافت يساعد على الهدوء.",
                        "اشرب مية... الجفاف يزيد التعب.",
                        "قفل عيونك 5 دقايق... هذا يفيد اكثر من الي تتصور.",
                        "حاول تنام باجر... السهر يزيد التعب."
                    ],
                    'support': [
                        "انت تبذل جهد كبير. يستاهل راحة.",
                        "التعب علامة على العمل. انت شخص منتج.",
                        "ما راح اكلفك اكثر. خذ راحتك."
                    ]
                },
                'en': {
                    'immediate': [
                        "Tiredness doesn't mean weakness... your body needs rest.",
                        "Give yourself a break. You don't have to keep working.",
                        "You're tired from many things. It's okay to need a pause.",
                        "Take a rest, even 10 minutes helps."
                    ],
                    'advice': [
                        "Dim the lights a bit... soft light helps calm down.",
                        "Drink water... dehydration increases tiredness.",
                        "Close your eyes for 5 minutes... it helps more than you think.",
                        "Try to sleep early tonight... staying up increases tiredness."
                    ],
                    'support': [
                        "You put in great effort. You deserve rest.",
                        "Tiredness is a sign of work. You're a productive person.",
                        "I won't ask more of you. Take your time."
                    ]
                }
            },
            'neutral': {
                'ar': {
                    'immediate': [
                        "اهلاً وسهلاً! كيف اكدر اساعدك اليوم؟",
                        "يومك كيف؟ اني هون اذا احتجت شي.",
                        "مبروك على هدوئك! هذا شي حلو.",
                        "اي شي تحب تتكلم عنه؟ انا سمعك."
                    ],
                    'general': [
                        "كل شي تمام؟ اذا صار شي، اني موجود.",
                        "اتمنى لك يوم حلو ومريح.",
                        "ما تنسى تشرب مية وتتذكر ترتاح!",
                        "انت شخص مهم واتمنى تعرف جذي."
                    ]
                },
                'en': {
                    'immediate': [
                        "Hello! How can I help you today?",
                        "How's your day? I'm here if you need anything.",
                        "Good for your calmness! That's nice.",
                        "Anything you'd like to talk about? I'm listening."
                    ],
                    'general': [
                        "Everything okay? If something comes up, I'm here.",
                        "Wishing you a good and relaxing day.",
                        "Don't forget to drink water and remember to rest!",
                        "You're an important person, I hope you know that."
                    ]
                }
            },
            'happy': {
                'ar': {
                    'immediate': [
                        "ما شاء الله! فرحان على فرحك! 🎉",
                        "هذا خبر حلو! تستاهل كل خير.",
                        "الله يديم عليك هالسعادة!",
                        "زين تشوفك مبسوط! هذي تدلع القلب."
                    ],
                    'celebrate': [
                        "سوي شي مميز اليوم، تستاهل!",
                        "احتفل بهالحظة الحلوة!",
                        "شاركني اكثر اذا تحب، فرحان اسمع.",
                        "السعادة تستاهل تُحتَفَل بيها!"
                    ],
                    'support': [
                        "حافظ على هالطاقة الحلوة!",
                        "انت نشر السعادة حولك. ما شاء الله!",
                        "الايام الحلوة تذكر وتدفي القلب."
                    ]
                },
                'en': {
                    'immediate': [
                        "Wonderful! So happy for your happiness! 🎉",
                        "That's great news! You deserve all the best.",
                        "May this happiness last for you!",
                        "Good to see you happy! This warms the heart."
                    ],
                    'celebrate': [
                        "Do something special today, you deserve it!",
                        "Celebrate this beautiful moment!",
                        "Share more if you like, happy to hear.",
                        "Happiness deserves to be celebrated!"
                    ],
                    'support': [
                        "Keep this beautiful energy!",
                        "You spread happiness around you. Wonderful!",
                        "Good days are remembered and warm the heart."
                    ]
                }
            }
        }
        
        # Transition phrases
        self.transitions = {
            'ar': [
                "تذكر...",
                "بالمناسبة...",
                "شي مهم اعرفك...",
                "ما اريدك تنسى...",
                "عندي اقتراح..."
            ],
            'en': [
                "Remember...",
                "By the way...",
                "Something important to know...",
                "I don't want you to forget...",
                "I have a suggestion..."
            ]
        }
        
        # Time-based greetings
        self.greetings = {
            'ar': {
                'morning': [
                    "صباح الخير! كيف اصبحت؟",
                    "صباح النور والسرور!",
                    "صباح الورد! يومك مبارك."
                ],
                'afternoon': [
                    "مساء الخير! كيف يومك؟",
                    "مساء النور! اتمنى يومك كان زين.",
                    "مساء الورد! كيف حالك؟"
                ],
                'evening': [
                    "مسا الخير! كيف كان يومك؟",
                    "مساء النور! وقت الراحة جان.",
                    "مساء جميل! كيف حالك؟"
                ],
                'night': [
                    "تصبح على خير! نوم العوافي.",
                    "ليلتك سعيدة! لا تنسى تدعي.",
                    "باي باي! اشوفك باجر."
                ]
            },
            'en': {
                'morning': [
                    "Good morning! How did you wake up?",
                    "Good morning! Have a blessed day.",
                    "Morning! Hope your day is great."
                ],
                'afternoon': [
                    "Good afternoon! How's your day?",
                    "Afternoon! Hope your day was good.",
                    "Good day! How are you doing?"
                ],
                'evening': [
                    "Good evening! How was your day?",
                    "Evening! Time to relax.",
                    "Lovely evening! How are you?"
                ],
                'night': [
                    "Good night! Sleep well.",
                    "Sweet dreams! Don't forget to pray.",
                    "Bye bye! See you tomorrow."
                ]
            }
        }
    
    def generate(self, emotion: str, user_input: str, language: str = 'ar', 
                 user_name: str = '') -> str:
        """
        Generate a supportive response based on emotion
        
        Args:
            emotion: Detected emotion category
            user_input: Original user message
            language: Response language ('ar' or 'en')
            user_name: User's name for personalization
            
        Returns:
            Generated response string
        """
        # Default to neutral if emotion not found
        if emotion not in self.responses:
            emotion = 'neutral'
        
        # Get response pool for this emotion
        emotion_responses = self.responses[emotion].get(language, self.responses[emotion]['ar'])
        
        # Build response
        parts = []
        
        # Add personalized greeting if name available
        if user_name:
            greeting = f"{user_name}، " if language == 'ar' else f"{user_name}, "
        else:
            greeting = ""
        
        # Get immediate response
        immediate = random.choice(emotion_responses.get('immediate', emotion_responses.get('support', [''])))
        parts.append(greeting + immediate)
        
        # Add advice or grounding for strong negative emotions
        if emotion in ['panic', 'depression', 'shock']:
            if 'grounding' in emotion_responses:
                parts.append(random.choice(emotion_responses['grounding']))
            elif 'advice' in emotion_responses:
                parts.append(random.choice(emotion_responses['advice']))
        
        # Add support message
        if 'support' in emotion_responses:
            parts.append(random.choice(emotion_responses['support']))
        
        # Join parts with natural breaks
        if language == 'ar':
            response = ' '.join(parts)
        else:
            response = ' '.join(parts)
        
        # Add urgent resources for severe cases
        if emotion == 'depression' and language == 'ar':
            if any(word in user_input.lower() for word in ['موت', 'انتحار', 'اقتل', 'انتحر']):
                response += "\n\n⚠️ اذا فكرت تؤذي نفسك، رجاءً كلم حدا او اتصل بطوارئ 130 بالعراق."
        
        return response
    
    def get_greeting(self, language: str = 'ar') -> str:
        """Get time-appropriate greeting"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_of_day = 'morning'
        elif 12 <= hour < 17:
            time_of_day = 'afternoon'
        elif 17 <= hour < 21:
            time_of_day = 'evening'
        else:
            time_of_day = 'night'
        
        greetings = self.greetings.get(language, self.greetings['ar'])
        return random.choice(greetings[time_of_day])