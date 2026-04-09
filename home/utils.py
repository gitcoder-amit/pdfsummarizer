import pdfplumber
import requests
from django.conf import settings

ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"


def call_llm_api(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.GROQ_API}"  }
    prompt = f"Summarize the following text clearly and try to make this short as much as possible: {text}"

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }

    response = requests.post(ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()

def read_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    s
    
def summarize_pdf(file_path, max_length=100):
    text = read_pdf(file_path)
    if text:
        summarized_text  = call_llm_api(text)
        return summarized_text
    return None