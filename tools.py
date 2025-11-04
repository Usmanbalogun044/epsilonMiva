
ollama_tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_chat_lesson",
            "description": "Generate a short, text-based lesson that feels conversational and adaptive to the user's level and learning mode.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "enum": ["Mathematics", "English", "Life Skills"],
                        "description": "The subject for the chat-based lesson."
                    },
                    "topic": {
                        "type": "string",
                        "description": "Specific topic for the lesson, e.g., 'Addition', 'Reading simple sentences', 'Filling a bank form'."
                    },
                    "learning_mode": {
                        "type": "string",
                        "enum": ["Standard", "ADHD", "Dyslexia", "Processing Delay"],
                        "description": "Customizes lesson pacing and tone for neurodivergent learners."
                    },
                    "difficulty_level": {
                        "type": "string",
                        "enum": ["Beginner", "Intermediate", "Advanced"],
                        "default": "Beginner",
                        "description": "Defines lesson complexity."
                    }
                },
                "required": ["subject", "topic", "learning_mode"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_user_response",
            "description": "Evaluate a learner's text answer, provide gentle feedback, and offer hints if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The question or prompt asked by the AI tutor."},
                    "user_response": {"type": "string", "description": "User's text-based answer to evaluate."},
                    "learning_mode": {
                        "type": "string",
                        "enum": ["Standard", "ADHD", "Dyslexia", "Processing Delay"],
                        "description": "Used to adjust tone and feedback pacing."
                    }
                },
                "required": ["question", "user_response"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_encouragement_message",
            "description": "Generate a supportive, patient, and motivating message to keep the learner engaged.",
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "enum": ["LessonStart", "CorrectAnswer", "Retry", "EndOfLesson", "Encouragement"],
                        "description": "Context of the message to tailor tone."
                    },
                    "user_name": {
                        "type": "string",
                        "description": "User’s name or nickname for personalization.",
                        "default": "Friend"
                    }
                },
                "required": ["context"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_next_topic",
            "description": "Suggest the next best topic or lesson based on completed topics and progress trends.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "enum": ["Mathematics", "English", "Life Skills"],
                        "description": "Current subject area."
                    },
                    "completed_topics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of completed lesson topics."
                    },
                    "performance": {
                        "type": "number",
                        "description": "Average learner performance score (0–100)."
                    }
                },
                "required": ["subject", "completed_topics"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_practice_questions",
            "description": "Create short, interactive text-based exercises or questions related to a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "The lesson topic for which to create practice questions."},
                    "difficulty_level": {
                        "type": "string",
                        "enum": ["Easy", "Medium", "Hard"],
                        "default": "Easy",
                        "description": "Difficulty level of questions."
                    },
                    "question_count": {
                        "type": "integer",
                        "description": "How many practice questions to generate.",
                        "default": 3
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_lesson",
            "description": "Summarize the key takeaways from a completed chat-based lesson in simple, supportive language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lesson_content": {
                        "type": "string",
                        "description": "Full text or structured content of the completed lesson."
                    },
                    "learning_mode": {
                        "type": "string",
                        "enum": ["Standard", "ADHD", "Dyslexia", "Processing Delay"],
                        "description": "Adjusts summary pacing and phrasing."
                    }
                },
                "required": ["lesson_content"]
            }
        }
    }
]


tools = [
    {
      "type": "function",
      "function": {
        "name": "generate_chat_lesson",
        "description": "Generate a short, text-based lesson that feels conversational and adaptive to the user's level and learning mode.",
        "parameters": {
          "type": "object",
          "properties": {
            "subject": {
              "type": "string",
              "enum": ["Mathematics", "English", "Life Skills"],
              "description": "The subject for the chat-based lesson."
            },
            "topic": {
              "type": "string",
              "description": "Specific topic for the lesson, e.g., 'Addition', 'Reading simple sentences', 'Filling a bank form'."
            },
            "learning_mode": {
              "type": "string",
              "enum": ["Standard", "ADHD", "Dyslexia", "Processing Delay"],
              "description": "Customizes lesson pacing and tone for neurodivergent learners."
            },
            "difficulty_level": {
              "type": "string",
              "enum": ["Beginner", "Intermediate", "Advanced"],
              "default": "Beginner",
              "description": "Defines lesson complexity."
            }
          },
          "required": ["subject", "topic", "learning_mode"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "evaluate_user_response",
        "description": "Evaluate a learner's text answer, provide gentle feedback, and offer hints if needed.",
        "parameters": {
          "type": "object",
          "properties": {
            "question": {
              "type": "string",
              "description": "The question or prompt asked by the AI tutor."
            },
            "user_response": {
              "type": "string",
              "description": "User's text-based answer to evaluate."
            },
            "learning_mode": {
              "type": "string",
              "enum": ["Standard", "ADHD", "Dyslexia", "Processing Delay"],
              "description": "Used to adjust tone and feedback pacing."
            }
          },
          "required": ["question", "user_response"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "generate_encouragement_message",
        "description": "Generate a supportive, patient, and motivating message to keep the learner engaged.",
        "parameters": {
          "type": "object",
          "properties": {
            "context": {
              "type": "string",
              "enum": ["LessonStart", "CorrectAnswer", "Retry", "EndOfLesson", "Encouragement"],
              "description": "Context of the message to tailor tone."
            },
            "user_name": {
              "type": "string",
              "description": "User’s name or nickname for personalization.",
              "default": "Friend"
            }
          },
          "required": ["context"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "suggest_next_topic",
        "description": "Suggest the next best topic or lesson based on completed topics and progress trends.",
        "parameters": {
          "type": "object",
          "properties": {
            "subject": {
              "type": "string",
              "enum": ["Mathematics", "English", "Life Skills"],
              "description": "Current subject area."
            },
            "completed_topics": {
              "type": "array",
              "items": { "type": "string" },
              "description": "List of completed lesson topics."
            },
            "performance": {
              "type": "number",
              "description": "Average learner performance score (0–100)."
            }
          },
          "required": ["subject", "completed_topics"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "generate_practice_questions",
        "description": "Create short, interactive text-based exercises or questions related to a topic.",
        "parameters": {
          "type": "object",
          "properties": {
            "topic": {
              "type": "string",
              "description": "The lesson topic for which to create practice questions."
            },
            "difficulty_level": {
              "type": "string",
              "enum": ["Easy", "Medium", "Hard"],
              "default": "Easy",
              "description": "Difficulty level of questions."
            },
            "question_count": {
              "type": "integer",
              "description": "How many practice questions to generate.",
              "default": 3
            }
          },
          "required": ["topic"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "summarize_lesson",
        "description": "Summarize the key takeaways from a completed chat-based lesson in simple, supportive language.",
        "parameters": {
          "type": "object",
          "properties": {
            "lesson_content": {
              "type": "string",
              "description": "Full text or structured content of the completed lesson."
            },
            "learning_mode": {
              "type": "string",
              "enum": ["Standard", "ADHD", "Dyslexia", "Processing Delay"],
              "description": "Adjusts summary pacing and phrasing."
            }
          },
          "required": ["lesson_content"]
        }
      }
    }
  ]
