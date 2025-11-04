# --- Tool Registry ---
# ------------------------------------------------------------
# TEGA MVP TOOL REGISTRY
# ------------------------------------------------------------
# Imports all the text-based tools for the neurodivergent learning companion
# ------------------------------------------------------------

from function import (
    generate_chat_lesson,
    evaluate_user_response,
    generate_encouragement_message,
    suggest_next_topic,
    generate_practice_questions,
    summarize_lesson,
)

TOOL_REGISTRY = {
    "generate_chat_lesson": generate_chat_lesson,
    "evaluate_user_response": evaluate_user_response,
    "generate_encouragement_message": generate_encouragement_message,
    "suggest_next_topic": suggest_next_topic,
    "generate_practice_questions": generate_practice_questions,
    "summarize_lesson": summarize_lesson,

    # Add new tools here as MVP expands
}
