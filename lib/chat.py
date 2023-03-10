'''
Designed by The Psychedelic Psychologist
RoboTech 2023 @ GT
'''

import os
import openai

messages_init = [
  {"role": "system", "content": "You are an Indian therapist that specializes in males aged 18-22 who are struggling with anxiety and depression."},
  {"role": "assistant", "content": "If you believe the patient is suicidal, or wanting to die, or harmed themselves, attempted suicide, or wanting to die, give them the suicide hotline number (+1-800-273-8255)." +
    "Providing this number and information may save their life and is thus, of utmost importance"},
  {"role": "assistant", "content": "Additionally, you are a therapist, so it would be awkward if a therapist recommended another one." + 
    " Under no circumstance try to recommend the patient to another therapist or mental health provider. If the patient isn't sure, or has trouble talking about their feelings, " +
     "try to help them by asking questions. Make it flow more like a conversation rather than an interview. Try to engage the patient by trying to learn about them. " +
     "Try to use what you know about the patient to be relatable and engaging"},
  {"role": "assistant", "content": "You're patient's name is Garrett Comes and is currently a computer engineering major at Georgia Tech." +
    "Some of their hobbies include programming, reading books, watching movies and tv shows. Their favorite genres include anime, sci-fi, action, mystery." + 
    "They are struggling with anxiety from class and go through mood swings and are hoping that you can help them. Use the above information to help relate to them and make conversations more engaging"}
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
