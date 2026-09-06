import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
    api_key=os.getenv("GROQ_API_KEY")
)
parser = StrOutputParser()

# STEP 1
# Bug Report → Structured Bug Report
prompt1 = PromptTemplate(
    template="""
You are a bug report analyzer.

Convert this messy bug report into:

Steps to Reproduce:
Expected Behavior:
Actual Behavior:
Severity:

Bug Report:
{bug_report}
""",
    input_variables=["bug_report"]
)
chain1 = prompt1 | llm | parser

# STEP 2

prompt2 = PromptTemplate(
    template="""
You are a QA engineer.

Check this bug report and find missing information.

Bug Report:
{structured_bug}

Tell me what information is missing.
""",
    input_variables=["structured_bug"]
)
chain2 = prompt2 | llm | parser

prompt3 = PromptTemplate(
    template="""
You are a software developer.

Create a prioritized fix plan.

Structured Bug Report:
{structured_bug}

Missing Information:
{gaps}

Give:

Priority:
Steps to Fix:
Testing Plan:
""",
    input_variables=["structured_bug", "gaps"]
)
chain3 = prompt3 | llm | parser

bug_report_text = input("Enter Bug Report: ")
result1 = chain1.invoke({
    "bug_report": bug_report_text
})

print("\n----- STEP 1 -----")
print(result1)

result2 = chain2.invoke({
    "structured_bug": result1
})

print("\n----- STEP 2 -----")
print(result2)

result3 = chain3.invoke({
    "structured_bug": result1,
    "gaps": result2
})

print("\n----- STEP 3 -----")
print(result3)