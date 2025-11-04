# ------------------------------------------------------------
# TEGA MVP TOOL FUNCTIONS - Text-based AI Learning Companion
# ------------------------------------------------------------
# Author: Tega Hackathon Team
# Version: MVP 1.0
# ------------------------------------------------------------

from random import choice, randint
import textwrap

# ------------------------------------------------------------
# 1. Generate Chat Lesson
# ------------------------------------------------------------
def generate_chat_lesson(subject, topic, learning_mode, difficulty_level="Beginner"):
    """
    Generate a short, text-based adaptive lesson for neurodivergent learners.
    """
    intros = [
        f"Hi friend! Let’s learn about {topic} today.",
        f"Welcome back! We’ll take small steps through {topic}.",
        f"Ready to explore {topic}? Don’t worry, we’ll go slowly together."
    ]
    
    base_lesson = {
        "Mathematics": f"In {topic}, we use everyday examples — like counting oranges or naira notes — to understand the concept.",
        "English": f"In {topic}, we’ll practice reading and writing with simple Nigerian words and short sentences.",
        "Life Skills": f"This {topic} lesson will help you handle real-life things, like reading forms or budgeting your money."
    }
    
    pacing_tip = {
        "Standard": "You can go at your own pace.",
        "ADHD": "We’ll keep it short and fun, with mini steps.",
        "Dyslexia": "We’ll use clear text and simple words.",
        "Processing Delay": "Take your time; I’ll repeat things if needed."
    }
    
    return {
        "intro": choice(intros),
        "lesson_text": textwrap.fill(base_lesson.get(subject, ""), 80),
        "tip": pacing_tip[learning_mode],
        "suggested_duration": "3–5 minutes"
    }

# ------------------------------------------------------------
# 2. Evaluate User Response
# ------------------------------------------------------------
def evaluate_user_response(question, user_response, learning_mode):
    """
    Evaluate a learner’s response and provide gentle feedback.
    """
    positive_feedback = [
        "That’s a great effort!",
        "Nice try! You’re getting closer.",
        "Good thinking — let’s build on that."
    ]
    
    hint_templates = [
        "Think about how you’d use this in the market or at home.",
        "Let’s try reading the question again, slowly.",
        "You can look for clues in the example we discussed."
    ]
    
    return {
        "feedback": choice(positive_feedback),
        "hint": choice(hint_templates),
        "next_step": "Would you like to try another example?"
    }

# ------------------------------------------------------------
# 3. Generate Encouragement Message
# ------------------------------------------------------------
def generate_encouragement_message(context, user_name="Friend"):
    """
    Generate motivational, affirming messages in a friendly tone.
    """
    messages = {
        "LessonStart": f"Welcome, {user_name}! Let’s learn something new together — one small step at a time.",
        "CorrectAnswer": f"Nice work, {user_name}! You understood that perfectly.",
        "Retry": f"It’s okay to try again, {user_name}. Every attempt makes you stronger.",
        "EndOfLesson": f"You did amazing today, {user_name}! Be proud of your progress.",
        "Encouragement": f"Keep it up, {user_name}. Learning is not a race — you’re doing great!"
    }
    return {"message": messages.get(context, messages["Encouragement"])}

# ------------------------------------------------------------
# 4. Suggest Next Topic
# ------------------------------------------------------------
def suggest_next_topic(subject, completed_topics, performance):
    """
    Suggest the next topic based on completed lessons and performance.
    """
    next_topics = {
        "Mathematics": ["Counting Money", "Addition", "Subtraction", "Time Telling"],
        "English": ["Phonics", "Simple Sentences", "Story Reading", "Spelling"],
        "Life Skills": ["Filling a Form", "Using an ATM", "Budgeting", "Reading Labels"]
    }
    
    possible = [t for t in next_topics[subject] if t not in completed_topics]
    next_topic = choice(possible) if possible else "Revision Time"
    
    level = "Beginner" if performance < 50 else "Intermediate" if performance < 80 else "Advanced"
    
    return {
        "recommended_topic": next_topic,
        "suggested_level": level,
        "note": f"Your performance shows steady progress! Let's try {next_topic} next."
    }

# ------------------------------------------------------------
# 5. Generate Practice Questions
# ------------------------------------------------------------
def generate_practice_questions(topic, difficulty_level="Easy", question_count=3):
    """
    Create short text-based practice questions for chat interaction.
    """
    sample_questions = {
        "Addition": [
            "What is 2 + 3?",
            "If you have 4 oranges and buy 2 more, how many do you have?",
            "Add 5 and 7 together."
        ],
        "Phonics": [
            "What sound does the letter 'B' make?",
            "Which word starts with the same sound as 'cat'?",
            "Can you spell the word 'dog'?"
        ],
        "Filling a Form": [
            "Where do you write your name on a form?",
            "What does 'Date of Birth' mean?",
            "What should you write under 'Address'?"
        ]
    }
    
    chosen = sample_questions.get(topic, ["Let's practice together. Can you tell me one example?"])
    selected = chosen[:question_count]
    
    return {"topic": topic, "questions": selected, "difficulty": difficulty_level}

# ------------------------------------------------------------
# 6. Summarize Lesson
# ------------------------------------------------------------
def summarize_lesson(lesson_content, learning_mode):
    """
    Provide a short, encouraging summary after a lesson.
    """
    summary_templates = {
        "Standard": "Today you learned something new! You understood the main ideas and practiced a few examples.",
        "ADHD": "We kept it short and focused — great job staying with it!",
        "Dyslexia": "You did really well working through the text and examples carefully.",
        "Processing Delay": "You took your time and understood things step by step — that’s perfect!"
    }
    
    return {
        "summary": textwrap.fill(summary_templates[learning_mode], 80),
        "next_action": "Would you like to review or move to a new topic?"
    }
