from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


# --------------------------------------------------
# Function to clean JSON response
# --------------------------------------------------

def clean_json(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# --------------------------------------------------
# STEP 1 - DISCUSSION SUMMARY
# --------------------------------------------------

SYSTEM_PROMPT_STEP1 = """
You are a professional meeting transcript analyzer.

Extract the main things discussed in the meeting.

Rules:
- Use only information from the transcript.
- Do not invent information.
- Do not create action items.
- Return ONLY valid JSON.
- Do not use markdown.

Return exactly:

{
    "discussion_summary": [
        "topic 1",
        "topic 2"
    ]
}
"""


def extract_discussion(transcript):

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP1
            },
            {
                "role": "user",
                "content": transcript
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    result = clean_json(result)

    return json.loads(result)


# --------------------------------------------------
# STEP 2 - ACTION ITEMS
# --------------------------------------------------

SYSTEM_PROMPT_STEP2 = """
You are a professional meeting action-item extractor.

Identify action items from the discussion summary.

Rules:
- Use ONLY the discussion summary.
- Do not use the original transcript.
- Do not invent information.
- If owner is missing, write "Missing".
- If deadline is missing, write "Missing".
- Flag missing owner or deadline.
- Return ONLY valid JSON.
- Do not use markdown.

Return exactly:

{
    "action_items": [
        {
            "task": "task name",
            "owner": "person or Missing",
            "deadline": "date or Missing",
            "flag": "Missing owner/deadline or None"
        }
    ]
}
"""


def extract_action_items(discussion):

    discussion_text = json.dumps(discussion)

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP2
            },
            {
                "role": "user",
                "content": discussion_text
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    result = clean_json(result)

    return json.loads(result)


# --------------------------------------------------
# STEP 3 - TASK TABLE
# --------------------------------------------------

SYSTEM_PROMPT_STEP3 = """
You are a professional task table formatter.

Convert the action items into a final structured task table.

Rules:
- Use ONLY the provided action items.
- Do not add new tasks.
- Do not change the owner or deadline.
- Keep "Missing" when information is missing.
- Return ONLY valid JSON.
- Do not use markdown.

Return exactly:

{
    "tasks": [
        {
            "task": "task name",
            "owner": "owner",
            "deadline": "deadline",
            "status": "Ready or Needs information"
        }
    ]
}
"""


def create_task_table(action_items):

    action_text = json.dumps(action_items)

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP3
            },
            {
                "role": "user",
                "content": action_text
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    result = clean_json(result)

    return json.loads(result)


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

transcript = input("\nEnter Meeting Transcript:\n")


# STEP 1
discussion = extract_discussion(transcript)


# STEP 2
action_items = extract_action_items(discussion)


# STEP 3
task_table = create_task_table(action_items)


# --------------------------------------------------
# DISPLAY OUTPUT
# --------------------------------------------------

print("\n========== STEP 1: DISCUSSION SUMMARY ==========\n")
print(json.dumps(discussion, indent=4))


print("\n========== STEP 2: ACTION ITEMS ==========\n")
print(json.dumps(action_items, indent=4))


print("\n========== STEP 3: FINAL TASK TABLE ==========\n")
print(json.dumps(task_table, indent=4))


print("\nProgram completed.")