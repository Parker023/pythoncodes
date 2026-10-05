import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.1",
    "prompt": "write a short story on how luffy would be a good marine"
}

response = requests.post(url, json=data, stream=True)

if response.status_code == 200:
    print("Generated text:", end=" ", flush=True)
    for chunk in response.iter_lines():
        if chunk:
            decoded_chunk = chunk.decode("utf-8")
            result = json.loads(decoded_chunk)
            generated_text = result.get('response', "")
            print(generated_text,end="", flush=True)
else:
    print("Error:", response.status_code)
