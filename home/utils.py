import pdfplumber
import requests
from django.conf import settings
import os
from django.template.loader import render_to_string
import pdfkit
from playwright.sync_api import sync_playwright



ENDPOINT = os.getenv("GROQ_ENDPOINT")
GROQ_API = os.getenv("GROQ_API")



def call_llm_api(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API}"  }
    prompt = f"Summarize the following text clearly and try to make this short as much as possible: {text}"

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        # "max_tokens": 150
    }

    response = requests.post(ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()

def convert_to_pdf(text):
    try:
        html = render_to_string('pdf_template.html', {'content': text})
        output_dir = os.path.join(settings.BASE_DIR, 'outputpdfs')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'summary.pdf')
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html)
            page.pdf(path=output_path)
            browser.close()
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

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
    
    
def summarize_pdf(file_path, max_length=100):
    text = read_pdf(file_path)
    if text:
        summarized_text  = call_llm_api(text)
        return convert_to_pdf(summarized_text)
    return None