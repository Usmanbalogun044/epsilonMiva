
tools = [

    {
        "type": "function",
        "function": {
            "name": "generate_short_lesson",
            "description": "Generate a short, game-like lesson plan for a child with ADHD who learns best through play and visuals.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The learning topic, e.g. 'basic multiplication' or 'parts of speech'."
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Approximate duration for the lesson (short, 5–10 minutes recommended)."
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "explain_text_slowly",
            "description": "Read and simplify a piece of text word-by-word for a learner with dyslexia, ensuring clear, shame-free explanation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to explain slowly, such as a contract clause or bank form sentence."
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_self_paced_exercise",
            "description": "Design a step-by-step exercise that allows a learner to go at their own speed, with encouragement and no timers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "The school subject or concept, e.g. 'fractions' or 'photosynthesis'."
                    },
                    "level": {
                        "type": "string",
                        "description": "The learner's level or class, e.g. 'JSS2', 'Primary 5'."
                    }
                },
                "required": ["subject"]
            }
        }
    },
    

    # ────────────────
    # MODULE 1: MATHEMATICS
    # ────────────────
    {
        "type": "function",
        "function": {
            "name": "generate_math_lesson",
            "description": "Generate an adaptive mathematics lesson based on the topic and level of difficulty.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The math concept to teach, e.g. 'addition', 'multiplication tables', or 'counting money'."
                    },
                    "level": {
                        "type": "string",
                        "description": "The learner's level, e.g. 'beginner', 'intermediate', 'advanced'."
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Lesson duration, usually 2–5 minutes for focus retention."
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "explain_math_step_by_step",
            "description": "Explain a math problem slowly and clearly, step-by-step, using visual or voice cues.",
            "parameters": {
                "type": "object",
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "The math problem to explain, e.g. '12 + 8' or 'If you have 3 apples and get 2 more...'"
                    }
                },
                "required": ["problem"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_word_problem",
            "description": "Create a simple, visual math word problem based on real Nigerian life contexts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "concept": {
                        "type": "string",
                        "description": "The math concept, e.g. 'addition', 'subtraction', 'multiplication'."
                    },
                    "context": {
                        "type": "string",
                        "description": "Real-world Nigerian context, e.g. 'market', 'transport', 'savings'."
                    }
                },
                "required": ["concept", "context"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_money_counting_exercise",
            "description": "Generate an interactive money-counting exercise using Nigerian Naira notes and coins.",
            "parameters": {
                "type": "object",
                "properties": {
                    "difficulty": {
                        "type": "string",
                        "description": "Difficulty level, e.g. 'easy', 'medium', 'hard'."
                    }
                },
                "required": ["difficulty"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_time_telling_activity",
            "description": "Generate a time-telling exercise using analog and digital clock examples.",
            "parameters": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Clock type, e.g. 'analog' or 'digital'."
                    }
                },
                "required": ["format"]
            }
        }
    },

    # ────────────────
    # MODULE 2: ENGLISH
    # ────────────────
    {
        "type": "function",
        "function": {
            "name": "generate_phonics_lesson",
            "description": "Create a phonics or letter-recognition lesson with sound and visual examples.",
            "parameters": {
                "type": "object",
                "properties": {
                    "letters": {
                        "type": "string",
                        "description": "Letters or sounds to focus on, e.g. 'a', 'b', 'c', or 'sh'."
                    }
                },
                "required": ["letters"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_sentence_practice",
            "description": "Generate short sentence-building or comprehension activities for English learners.",
            "parameters": {
                "type": "object",
                "properties": {
                    "focus": {
                        "type": "string",
                        "description": "Focus area, e.g. 'CVC words', 'simple sentences', 'reading comprehension'."
                    }
                },
                "required": ["focus"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "provide_reading_assistance",
            "description": "Read and simplify English text slowly for users who struggle with reading or dyslexia.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The passage or sentence to read and explain slowly."
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_story_based_lesson",
            "description": "Generate a short story-based learning activity grounded in Nigerian culture and daily life.",
            "parameters": {
                "type": "object",
                "properties": {
                    "theme": {
                        "type": "string",
                        "description": "Theme of the story, e.g. 'market', 'family', 'school', or 'transport'."
                    }
                },
                "required": ["theme"]
            }
        }
    },

    # ────────────────
    # MODULE 3: LIFE SKILLS
    # ────────────────
    {
        "type": "function",
        "function": {
            "name": "explain_real_document",
            "description": "Explain sections of a real-world document like a bank form or job application in simple language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_type": {
                        "type": "string",
                        "description": "Type of document, e.g. 'bank form', 'job application', 'contract'."
                    },
                    "section": {
                        "type": "string",
                        "description": "Specific section or question from the document."
                    }
                },
                "required": ["document_type", "section"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "teach_basic_budgeting",
            "description": "Generate a practical budgeting lesson using simple Nigerian daily examples.",
            "parameters": {
                "type": "object",
                "properties": {
                    "income": {
                        "type": "integer",
                        "description": "Monthly or weekly income for the scenario."
                    }
                },
                "required": ["income"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "simulate_form_filling",
            "description": "Create an interactive walkthrough for filling out real-world forms like voter registration or ATM slips.",
            "parameters": {
                "type": "object",
                "properties": {
                    "form_type": {
                        "type": "string",
                        "description": "Type of form, e.g. 'voter registration', 'bank deposit slip', or 'POS receipt'."
                    }
                },
                "required": ["form_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "simplify_contract_text",
            "description": "Simplify and explain contract or legal terms in plain, Nigerian English.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Contract or legal clause to simplify."
                    }
                },
                "required": ["text"]
            }
        }
    }
]
