import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def completion(prompt: str):
  res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a therapist that specializes in males aged 18."},
      {"role": "user", "content": prompt},
    ],
    temperature=0.4,
    max_tokens=400,
  )
  print(res["choices"][0]["message"]["content"])
