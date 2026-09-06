from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)
SYSTEM_PROMPT_STEP1 = """
You are a professional job posting information extractor.

Your task is to extract the key requirements from a raw job posting
and convert them into structured information.

Rules:
1. Extract only information that is explicitly present in the job posting.
2. Do not invent or assume any information.
3. Separate required skills from preferred skills.
4. Extract the job title, skills, experience, education, and responsibilities.
5. If a field is not available, return null.
6. Return only valid JSON.
7. Do not provide explanations or additional text.

Use exactly this JSON structure:

{
    "job_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "experience": null,
    "education": null,
    "responsibilities": []
}
"""
SYSTEM_PROMPT_STEP2 = """
You are a professional recruitment outreach assistant.

Your task is to create a personalized outreach message
for a candidate based on the structured job requirements
and the candidate profile.

Rules:
1. Use only the structured job requirements provided to you.
2. Do not use the original raw job posting.
3. Personalize the message using the candidate's profile.
4. Mention relevant skills or experience that match the job requirements.
5. Do not invent skills, experience, education, or achievements.
6. Do not exaggerate the candidate's qualifications.
7. Keep the message professional, friendly, and concise.
8. Do not provide explanations.
9. Return only the final outreach message.
"""

def extract_requirements(job_posting_text):

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP1
            },
            {
                "role": "user",
                "content": job_posting_text
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    return json.loads(result)
  
def generate_outreach(structured_requirements, candidate_profile):

    prompt = f"""
Structured Job Requirements:

{json.dumps(structured_requirements, indent=4)}

Candidate Profile:

{candidate_profile}

Generate a personalized recruitment outreach message.
"""

    response = client.chat.completions.create(
        model= "nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP2
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

job_posting_text = input("\nEnter Job Posting:\n")

candidate_profile = input("\nEnter Candidate Profile:\n")

structured_requirements = extract_requirements(
    job_posting_text
)

outreach_message = generate_outreach(
    structured_requirements,
    candidate_profile
)
print("\nSTEP 1: STRUCTURED REQUIREMENTS\n")

print(
    json.dumps(
        structured_requirements,
        indent=4
    )
)
print("\nSTEP 2: PERSONALIZED OUTREACH \n")

print(outreach_message)


