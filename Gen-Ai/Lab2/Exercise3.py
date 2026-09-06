# Exercise 3 — Coding Assistant
# Build an app that debugs Python code.
# Required functionality:
# Accepts two separate inputs: a broken code snippet and its error message
# Returns the corrected code and a one-line explanation, clearly separated in the output
# Correctly handles at least 3 different error types when tested
# Upload to GitHub.

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def debug_code(code, error):

    prompt = f"""
You are a Python coding assistant.

Fix the Python code based on the error message.

Broken Code:
{code}

Error Message:
{error}

Return the answer in exactly this format:

CORRECTED CODE:
<corrected code>

EXPLANATION:
<one-line explanation>

Do not add extra explanations.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()


print("Enter your broken Python code:")
broken_code = input()

error_message = input("Enter Error Message: ")

result = debug_code(
    broken_code,
    error_message
)

print("\n===== DEBUG RESULT =====")
print(result)
