import json

from ollama import chat
from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int
    skills: list[str]


response = chat(
    model="qwen2.5-coder:7b",
    messages=[
        {
            "role": "system",
            "content": "Return valid JSON only."
        },
        {
            "role": "user",
            "content": """
Extract:

name: Antony
age: 21
skills: Java, Python, SQL
"""
        }
    ],
    format="json"
)

data = json.loads(response.message.content)

person = Person(**data)

print(person)
print("Name:", person.name)
print("Age:", person.age)
print("Skills:", person.skills)