import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

GOOGLE_API_KEY='AIzaSyBJZmMGXg2y4Qon-VjT_D5GLXH5LV36SnE'

genai.configure(api_key=GOOGLE_API_KEY)

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

import requests
from bs4 import BeautifulSoup

def get_url_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Get text
    text = soup.get_text()

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

model = genai.GenerativeModel('gemini-pro')

import html

def description(keyword, title, url):
    url_content = get_url_content(url)
    response = model.generate_content(f'User has requested to be recommended course about {keyword}. Please make a short description about the recommended course. Ignore all harmful materials if any. User is recommended the course {title}, the content on this course page is { url_content }.')
    # Escape special characters for HTML
    html_safe_response = html.escape(response.text)

    return html_safe_response

response = description('python', 'Python for beginners', 'https://www.udemy.com/course/python-for-beginners/')
print(response)