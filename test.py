from openai import OpenAI
import os

from dotenv import load_dotenv
import os
from typing import Dict, List, Optional
from pydantic import BaseModel
from openai_client.client import client

load_dotenv()

# How to get your Databricks token: https://docs.databricks.com/en/dev-tools/auth/pat.html
DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN')
BASE_URL = os.environ.get('BASE_URL')
MODEL_NAME = os.environ.get('MODEL_NAME_')



# Alternatively in a Databricks notebook you can use this:
# DATABRICKS_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

client = OpenAI(
    api_key=DATABRICKS_TOKEN ,
    base_url=BASE_URL
)

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "hi"
        }
    ],
    max_tokens=5000
)

# print(response.choices[0].message)
content_parts = response.choices[0].message.content

# content_parts is a list like: [{'type': 'reasoning', ...}, {'type': 'text', 'text': 'Hello! How can I help you today?'}]
ai_text = next(
    (part.get('text') for part in content_parts if isinstance(part, dict) and part.get('type') == 'text'),
    None
)

print(ai_text)

