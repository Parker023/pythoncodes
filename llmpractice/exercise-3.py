import ollama

ollama.create(
    model="oda",
    from_="llama3.1",
    system="You are a very smart assistant who knows everything about One Piece anime",
    parameters={
        "temperature": 0.7
    }
)

resp = ollama.generate(
    model="oda",
    prompt="in luffy's world, who is the best teacher?",
    stream=True,
)

for chunk in resp:
    print(chunk.response, end="",flush=True)

#delete model

ollama.delete(model="oda")