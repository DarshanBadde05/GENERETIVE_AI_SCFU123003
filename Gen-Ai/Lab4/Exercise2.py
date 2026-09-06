from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

Extract_Core_Claims = """     
You are a professional news article fact extractor.

Your task is to extract the important factual claims from the
given news article.

Rules:
1. Extract only claims explicitly stated in the article.
2. Do not add opinions, assumptions, or information from outside sources.
3. Keep each claim short and clear.
4. Include only important factual claims.
5. Return the claims as a JSON list.
6. Return only valid JSON.
7. Do not provide explanations.

Example:
[
    "Company X launched a new electric car.",
    "The car has a range of 500 km.",
    "The car costs ₹20 lakh."
]
"""

Generate_Fact_Card = """
You are a professional news fact-card generator.

Create a short fact card using ONLY the extracted claims provided.

Rules:
1. Do not use the original news article.
2. Use only the extracted claims.
3. Create one clear headline.
4. Provide exactly 3 bullet points.
5. Add a short source confidence note.
6. Do not add facts that are not present in the claims.
7. Do not add opinions or assumptions.
8. Keep the fact card concise.
9. Return only the fact card.

Format:

Headline: <headline>

• <point 1>
• <point 2>
• <point 3>

Source Confidence: <short confidence note>
"""

def Claims(news_article_text):

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": Extract_Core_Claims
            },
            {
                "role": "user",
                "content": news_article_text
            }
        ],
        max_tokens=500,
        temperature=0.2
    )

    claims_text = response.choices[0].message.content.strip()

    # Convert AI JSON text into Python object
    claims = json.loads(claims_text)

    return claims

def Fact_Card(claims):

    # Convert Python list into JSON text
    claims_json = json.dumps(claims, indent=4)

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": Generate_Fact_Card
            },
            {
                "role": "user",
                "content": claims_json
            }
        ],
        max_tokens=500,
        temperature=0.2
    )

    fact_card = response.choices[0].message.content.strip()

    return fact_card

article_text = input("\nEnter News Article:\n")

claims = Claims(article_text)

fact_card = Fact_Card(claims)

print("\n  STEP 1: EXTRACTED CLAIMS  \n")

print(json.dumps(claims, indent=4))


print("\n  STEP 2: FACT CARD  \n")

print(fact_card)