import ollama

# response= ollama.list()

# print(response)


# =====chat ex=====

res = ollama.chat(
    model="llama3.1",
    messages=[{
        "role": "user",
        "content": "Hi, how are you?"}
    ],
    stream=True
)

for chunk in res:
    print(chunk.message.content, end="")