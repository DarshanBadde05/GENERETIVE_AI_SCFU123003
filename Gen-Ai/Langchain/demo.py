import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
    # other params...
)

messages = [
    ("system", "You are a helpful assistant that translates English to French. Translate the user sentence.",),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)

print(ai_msg.content)


from langchain_core.prompts import PromptTemplate

# Instantiation using from_template (recommended)
prompt = PromptTemplate.from_template("Say {foo}")
prompt.format(foo="bar")

# Instantiation using initializer
prompt = PromptTemplate(template="Say {foo}")