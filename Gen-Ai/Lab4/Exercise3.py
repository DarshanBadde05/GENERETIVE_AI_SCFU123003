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
You are a professional meeting transcript analyzer.

Your task is to extract what was discussed in the meeting.

Rules:
1. Summarize only information present in the transcript.
2. Identify the main topics discussed.
3. Do not invent information.
4. Do not identify action items yet.
5. Keep the summary short and clear.
6. Return only valid JSON.
7. Do not provide explanations.

Use this format:

{
    "discussion_summary": [
        "topic 1",
        "topic 2",
        "topic 3"
    ]
}
"""
SYSTEM_PROMPT_STEP2 = """
You are a professional meeting action-item extractor.

Your task is to identify action items from the discussion summary.

Rules:
1. Use ONLY the discussion summary provided.
2. Do not use the original meeting transcript.
3. Identify tasks that need to be completed.
4. Identify the owner of each task if mentioned.
5. Identify the deadline if mentioned.
6. If the owner is missing, mark it as "Missing".
7. If the deadline is missing, mark it as "Missing".
8. Do not invent owners or deadlines.
9. Flag missing information.
10. Return only valid JSON.
11. Do not provide explanations.

Use this format:

{
    "action_items": [
        {
            "task": "",
            "owner": "",
            "deadline": "",
            "flag": ""
        }
    ]
}
"""
SYSTEM_PROMPT_STEP3 = """
You are a professional task-table formatter.

Your task is to convert the action items into a structured task table.

Rules:
1. Use ONLY the action items provided.
2. Do not add new tasks.
3. Do not change owners or deadlines.
4. Keep missing information as "Missing".
5. Include the flag for missing information.
6. Return only valid JSON.
7. Do not provide explanations.

Use this format:

{
    "tasks": [
        {
            "task": "",
            "owner": "",
            "deadline": "",
            "status": ""
        }
    ]
}
"""
def extract_discussion(transcript_text):

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP1
            },
            {
                "role": "user",
                "content": transcript_text
            }
        ],
        max_tokens=500,
        temperature=0.2
    )

    result = response.choices[0].message.content.strip()

    return json.loads(result)


def extract_action_items(discussion):

    discussion_json = json.dumps(discussion, indent=4)

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP2
            },
            {
                "role": "user",
                "content": discussion_json
            }
        ],
        max_tokens=500,
        temperature=0.2
    )

    result = response.choices[0].message.content.strip()

    return json.loads(result)

def create_task_table(action_items):

    action_items_json = json.dumps(action_items, indent=4)

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_STEP3
            },
            {
                "role": "user",
                "content": action_items_json
            }
        ],
        max_tokens=500,
        temperature=0.2
    )

    result = response.choices[0].message.content.strip()

    return json.loads(result)

transcript_text = input("\nEnter Meeting Transcript:\n")

discussion = extract_discussion(transcript_text)

action_items = extract_action_items(discussion)


task_table = create_task_table(action_items)

