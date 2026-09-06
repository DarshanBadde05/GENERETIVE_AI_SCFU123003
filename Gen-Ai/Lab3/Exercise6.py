# Exercise 6 — Iterative Content Refiner
# Build a prompt that takes a draft and revises it to fix one specific issue, across multiple rounds.
# Input: `draft_text`, `issue_to_fix`
# Output: a revised version of the text that resolves that specific issue, run for at least 3 rounds
# Upload to GitHub.

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def refine_content(draft_text, issue_to_fix):

    prompt = f"""
You are a professional content editor.

Revise the following draft text.

Issue to Fix:
{issue_to_fix}

Draft Text:
{draft_text}

Rules:
1. Fix only the specified issue.
2. Preserve the original meaning.
3. Improve the text naturally.
4. Do not add explanations.
5. Return only the revised text.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

draft_text = input("Enter Draft Text: ")

issue_to_fix = input("Enter Issue to Fix: ")

print("\n========== ROUND 1 ==========")

result1 = refine_content(
    draft_text,
    issue_to_fix
)

print(result1)

print("\n========== ROUND 2 ==========")

result2 = refine_content(
    result1,
    issue_to_fix
)

print(result2)

print("\n========== ROUND 3 ==========")

result3 = refine_content(
    result2,
    issue_to_fix
)

print(result3)

print("\n========== FINAL REFINED TEXT ==========")

print(result3)