ollama_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_laws_and_regulations",
            "description": "Search and retrieve summaries or key provisions from GDPR, NDPA 2023, HIPAA, and CCPA for comparison.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The keyword or question to search for within data privacy laws, e.g., 'data breach notification in GDPR'."
                    },
                    "jurisdiction": {
                        "type": "string",
                        "enum": ["GDPR", "NDPA 2023", "HIPAA", "CCPA", "All"],
                        "description": "Specify which regulation to search."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_regulations",
            "description": "Compare GDPR, NDPA 2023, HIPAA, and CCPA across specific privacy categories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of privacy aspects to compare, e.g., ['data subject rights', 'penalties', 'data breach response']."
                    }
                },
                "required": ["categories"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_literature",
            "description": "Summarize academic papers or industry sources related to cloud database privacy or legal frameworks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Full text or abstract of a research paper or article."
                    },
                    "word_limit": {
                        "type": "integer",
                        "description": "Desired length of the summary in words.",
                        "default": 200
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_apa_reference",
            "description": "Generate an APA 7th edition formatted citation for a source.",
            "parameters": {
                "type": "object",
                "properties": {
                    "author": {"type": "string", "description": "Author(s) of the source."},
                    "year": {"type": "string", "description": "Publication year."},
                    "title": {"type": "string", "description": "Title of the source."},
                    "source_type": {
                        "type": "string",
                        "enum": ["journal", "book", "website", "report"],
                        "description": "Type of the source for correct formatting."
                    },
                    "url": {"type": "string", "description": "URL or DOI if available."}
                },
                "required": ["author", "year", "title", "source_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_case_study",
            "description": "Analyze how privacy laws apply to the EduCloud University System (EUS) scenario.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue": {"type": "string", "description": "Specific incident or privacy challenge from the EduCloud case."},
                    "law_framework": {
                        "type": "string",
                        "enum": ["GDPR", "NDPA 2023", "HIPAA", "CCPA"],
                        "description": "The regulation to analyze the issue against."
                    }
                },
                "required": ["issue", "law_framework"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_section_draft",
            "description": "Generate a draft of a specific research paper section following APA and rubric standards.",
            "parameters": {
                "type": "object",
                "properties": {
                    "section_name": {
                        "type": "string",
                        "enum": ["Introduction", "Literature Review", "Methodology", "Findings", "Conclusions"],
                        "description": "Which section of the academic paper to generate."
                    },
                    "focus": {
                        "type": "string",
                        "description": "The key theme or focus for that section, e.g., 'GDPR vs NDPA compliance in EduCloud'."
                    }
                },
                "required": ["section_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "export_report",
            "description": "Export the entire paper or a section to a document file (PDF or DOCX).",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The full academic text to export."},
                    "format": {
                        "type": "string",
                        "enum": ["pdf", "docx"],
                        "description": "Output file format."
                    },
                    "filename": {
                        "type": "string",
                        "description": "Desired output filename.",
                        "default": "comparative_study"
                    }
                },
                "required": ["content", "format"]
            }
        }
    }
]