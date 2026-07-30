from openai import OpenAI

client = OpenAI(api_key="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")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Say hello, I am Jarvis."}
    ]
)

print(response.choices[0].message.content)