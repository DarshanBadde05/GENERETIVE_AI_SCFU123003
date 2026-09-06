from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


SYSTEM_PROMPT=""" 
            Your task is to expand a one-line product idea into a structured pitch.
            Extract these three things:

1. Problem - What problem does the product solve? 2. Solution - How does the product solve the problem?
3. Target User - Who will use the product?

Rules:
- Use only the information available from the product idea.
- Do not invent specific facts.
- Keep the information clear and concise.
- Return only valid JSON.
- Do not provide explanations.

Return exactly this format:

{
    "problem": "",
    "solution": "",
    "target_user": ""
}
"""
def exapand_product_idea(Product_idea):
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": Product_idea
            }
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content.strip()
    return json.loads(result)
  
SYSTEM_PROMPT_STEP2 = """
You are a professional startup pitch writer.

Your task is to create a short investor-style pitch paragraph
using ONLY the structured product information provided.

Rules:
1. Use only the structured information.
2. Do not use the original product idea.
3. Do not add new facts.
4. Clearly explain the problem and solution.
5. Mention the target user.
6. Make the pitch professional and convincing.
7. Keep it short.
8. Return only the pitch paragraph.
9. Do not provide explanations.
"""
def generate_pitch(structured_pitch):

    structured_json = json.dumps(
        structured_pitch,
        indent=4
    )

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP2
            },
            {
                "role": "user",
                "content": structured_json
            }
        ],
        max_tokens=500,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
product_idea = input(
    "\nEnter Product Idea:\n"
)
structured_pitch = exapand_product_idea(
    product_idea
)
pitch_paragraph = generate_pitch(
    structured_pitch
)
print("\n========== STEP 1: STRUCTURED PITCH ==========\n")

print(
    json.dumps(
        structured_pitch,
        indent=4
    )
)
print( "\n========== STEP 2: INVESTOR PITCH ==========\n")
print(pitch_paragraph)


