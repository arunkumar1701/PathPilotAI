import google.generativeai as genai
import sys

sys.stdout.reconfigure(encoding='utf-8')

api_key = "AIzaSyBD98sRRFUxstk0Iz7RvmMqFUqKKwvrTH8"
genai.configure(api_key=api_key)

print("Listing models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
