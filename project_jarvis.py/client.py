from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)