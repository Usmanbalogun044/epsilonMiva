
def generate_short_lesson(topic: str, duration_minutes: int = 5):
    return f"A {duration_minutes}-minute playful lesson on {topic} with quick games"

def explain_text_slowly(text: str):
    return f"Let's break it down slowly: {text} — meaning ... (simplified explanation)."

def create_self_paced_exercise(subject: str, level: str = "General"):
    return f"A self-paced {subject} exercise for {level} level learners, with positive encouragement after each step."

import random

# ────────────────
# MODULE 1: MATHEMATICS
# ────────────────

def generate_math_lesson(topic: str, level: str = "beginner", duration_minutes: int = 3):
    examples = {
        "addition": "Let's start with adding small numbers. For example, 3 + 2 = 5. You can use your fingers or bottle caps to count along!",
        "subtraction": "Subtraction means taking away. If you have 6 sweets and you give 2 to your friend, how many do you have left? (6 - 2 = 4)",
        "multiplication tables": "Let's practice the 2 times table: 2x1=2, 2x2=4, 2x3=6… Great job!",
        "counting money": "Imagine you have one ₦50 note and two ₦20 notes. How much do you have in total? 50 + 20 + 20 = ₦90."
    }
    content = examples.get(topic.lower(), f"Let's learn about {topic}! Start by taking it one step at a time.")
    return {"type": "lesson", "content": f"🧮 {content} (Level: {level}, Duration: {duration_minutes} mins)"}


def explain_math_step_by_step(problem: str):
    steps = [
        f"First, let's look carefully at your problem: {problem}",
        "We’ll solve it one step at a time.",
        "Try to picture it using your fingers or small objects.",
        "Now, let’s do the math together — you can say the numbers aloud.",
        "Nice work! You're getting better each time."
    ]
    return {"type": "explanation", "content": " ".join(steps)}


def generate_word_problem(concept: str, context: str):
    problems = {
        "addition": f"In the {context}, Bola bought 3 oranges and then 2 more. How many oranges does she have now?",
        "subtraction": f"A bus in {context} has 10 passengers. 4 get down at the next stop. How many people remain?",
        "multiplication": f"A trader in the {context} sells 5 baskets of tomatoes, each with 4 tomatoes. How many in total?"
    }
    return {"type": "word_problem", "content": problems.get(concept.lower(), "Let's try a simple problem together!")}


def generate_money_counting_exercise(difficulty: str):
    if difficulty == "easy":
        return {"type": "exercise", "content": "Count the money: ₦20 + ₦10 = ?"}
    elif difficulty == "medium":
        return {"type": "exercise", "content": "You have one ₦50 note, two ₦20 notes, and one ₦10 coin. How much do you have in total?"}
    else:
        return {"type": "exercise", "content": "You spent ₦70 from ₦200. How much is left?"}


def generate_time_telling_activity(format: str):
    if format == "analog":
        return {"type": "activity", "content": "The short hand is on 3 and the long hand is on 12. What time is that? (Hint: it’s 3 o’clock!)"}
    else:
        return {"type": "activity", "content": "The digital clock shows 07:30. That means it’s half past seven."}

# ────────────────
# MODULE 2: ENGLISH
# ────────────────

def generate_phonics_lesson(letters: str):
    return {"type": "lesson", "content": f"Let’s practice the sound of '{letters}'. Say it slowly with me: '{letters}'... Good! Now, can you think of a word that starts with '{letters}'?"}


def generate_sentence_practice(focus: str):
    if focus.lower() == "cvc words":
        return {"type": "exercise", "content": "Let's make short CVC words like 'cat', 'dog', and 'sun'. Read them aloud!"}
    elif focus.lower() == "reading comprehension":
        return {"type": "exercise", "content": "Read this short passage: 'Ada went to the market to buy rice.' What did Ada go to buy?"}
    else:
        return {"type": "exercise", "content": "Let’s build a simple sentence together: 'I am happy.' Now try: 'I am strong.' Great job!"}


def provide_reading_assistance(text: str):
    simplified = text.replace(",", ", ").replace(".", ". ")
    return {"type": "reading_support", "content": f"Here’s the text read slowly: {simplified}. Let’s go over any hard words together."}


def generate_story_based_lesson(theme: str):
    stories = {
        "market": "Ngozi went to Balogun market with her mum. She counted the tomatoes and helped to pay. That’s how she learned to use money!",
        "family": "Tunde helped his grandma cook jollof rice. They counted cups of rice together and talked about family love.",
        "school": "Chidi forgot his pencil, but his friend shared one. They both finished their math work on time."
    }
    story = stories.get(theme.lower(), f"Once upon a time in Nigeria, someone learned something important about {theme}.")
    return {"type": "story", "content": f"📖 {story}"}

# ────────────────
# MODULE 3: LIFE SKILLS
# ────────────────

def explain_real_document(document_type: str, section: str):
    explanations = {
        "bank form": "The 'Account Name' section means the name that appears on your bank account. Write it exactly as it is on your ID card.",
        "job application": "The 'Experience' section is where you describe the kind of work you’ve done before, even if it’s market trading or tailoring.",
        "contract": "The 'Signature' section means you agree to the terms. Always read or ask before you sign."
    }
    return {"type": "document_explanation", "content": explanations.get(document_type.lower(), f"This section '{section}' means the information required in that part of the {document_type}.")}


def teach_basic_budgeting(income: int):
    return {"type": "lesson", "content": f"Let’s plan your ₦{income} wisely. Spend 50% on needs (like food), 30% on wants (like clothes), and save 20%. Small savings add up!"}


def simulate_form_filling(form_type: str):
    steps = {
        "voter registration": "Step 1: Fill in your full name. Step 2: Add your address. Step 3: Write your Local Government Area (LGA).",
        "bank deposit slip": "Write the depositor’s name, amount in numbers and words, then sign. Simple!",
        "POS receipt": "Check your name, amount, and last four digits of your card before confirming."
    }
    return {"type": "simulation", "content": steps.get(form_type.lower(), f"Here’s how to fill out a {form_type}. Take it one step at a time!")}


def simplify_contract_text(text: str):
    simplified = f"This means: {text.lower().replace('hereby', 'you agree').replace('thereof', 'of this').replace('witnesseth', 'shows that')}."
    return {"type": "simplified_text", "content": simplified}
