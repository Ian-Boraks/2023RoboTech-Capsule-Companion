import os
import openai

messages_init = [
  {"role": "system", "content": "You are a therapist that specializes in males aged 18."}
]

messages = []

def init_openai():
  openai.api_key = os.getenv("OPENAI_API_KEY")
  reset_messages()

def add_message(message: str):
  global messages
  messages.append({"role": "user", "content": message})
  res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.4,
    max_tokens=400,
  )
  messages.append(res["choices"][0]["message"])
  return res["choices"][0]["message"]["content"]

def reset_messages():
  global messages
  messages = messages_init
  