# ## Exercise 5 — Multi-language Translator

# Build a prompt that translates a sentence into a target language at a given formality level.

# **Input:** `sentence`, `target_language`, `formality`

# **Output:** a translated sentence matching the requested formality level

# **Upload to GitHub.**
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API")
)


def translate_sentence(sentence, target_language, formality):

    prompt = f"""
You are a professional multilingual translator.

Translate the sentence into the requested target language.

Sentence:
{sentence}

Target Language:
{target_language}

Formality:
{formality}

Rules:
1. Preserve the original meaning.
2. Match the requested formality level.
3. Use proper grammar.
4. Do not add explanations.
5. Return only the translated sentence.
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

sentence = input("Enter Sentence: ")
target_language = input("Enter Target Language: ")
formality = input("Enter Formality (Formal/Informal): ")


result = translate_sentence(
    sentence,
    target_language,
    formality
)

print("\n========== TRANSLATION ==========")
print(result)

