from flask import Flask, request, render_template
from Coursera.recommend import recommend_coursera
from UDEMY.recommend import recommend_udemy
from NPTEL.recommend import recommend_nptel 
from MIT.recommend import recommend_mit


# GEMINI
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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
    response = model.generate_content(f'User has requested to be recommended course about {keyword}. Please make a short description about the recommended course. Ignore all harmful materials if any. If the course is not related about the search keyword, this maybe possible because such courses are not offered. Please tell user that the course is not related to keyword, sorry for that but they can check out this altnernative. You have to make description about the course in respect to the keyword user has asked for. User is recommended the course {title}, the content on this course page is { url_content }.')
    # Escape special characters for HTML
    html_safe_response = html.escape(response.text)

    return html_safe_response

# response = description('python', 'Python for beginners', 'https://www.udemy.com/course/python-for-beginners/')
# print(response)


def process_udemy_course(course):
    return {
        'title': course['course_title'],
        'url': course['url']
    }

def process_coursera_course(course):
    return {
        'title': course['Course Title'],
        'url': course['Course Url']
    }

def process_nptel_course(course):
    return {
        'title': course['Course Name'],
        'url': course['NPTEL URL']
    }


app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         user_input = request.form.get('user_input')
#         udemy_recommendations = recommend_udemy(user_input).to_dict('records')   # call the recommend_courses function for Udemy
#         print(udemy_recommendations)
#         coursera_recommendations = recommend_coursera(user_input).to_dict('records')   # call the recommend_courses function for Coursera
#         print(coursera_recommendations)
#         nptel_recommendations = recommend_nptel(user_input).to_dict('records')   # call the recommend_courses function for NPTEL
#         print(nptel_recommendations)
#         return render_template('results.html', udemy=udemy_recommendations, coursera=coursera_recommendations, nptel=nptel_recommendations)
#     return render_template('index.html')

# from markdown import markdown

# ...
from markdown import markdown
import pandas as pd


# Load the CSV file
df = pd.read_csv('merged.csv')
df_udemy = pd.read_csv('udemy_courses.csv')
df_coursera = pd.read_csv('CourseraDataset.csv')
df_mit = pd.read_csv('mit.csv')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        udemy_recommendations = recommend_udemy(user_input).to_dict('records')   # call the recommend_courses function for Udemy
        coursera_recommendations = recommend_coursera(user_input).to_dict('records')
        nptel_recommendations = recommend_nptel(user_input).to_dict('records')   # call the recommend_courses function for NPTEL
        mit_recommendations = recommend_mit(user_input).to_dict('records')   # call the recommend_courses function for MIT

        return render_template('results.html', udemy=udemy_recommendations, coursera=coursera_recommendations, nptel=nptel_recommendations, mit=mit_recommendations, user_input=user_input)
    return render_template('index.html')

@app.route('/about_udemy', methods=['GET'])
def about_udemy():
    user_input = request.args.get('user_input')
    course_title = request.args.get('course')
    course_row = df_udemy.loc[df_udemy['course_title'] == course_title]
    try:
        desc = markdown(description(user_input, course_title, course_row['url'].values[0]))
    except Exception:
        desc = ''
    return desc

@app.route('/about_coursera', methods=['GET'])
def about_coursera():
    user_input = request.args.get('user_input')
    course_title = request.args.get('course')
    course_row = df_coursera.loc[df_coursera['Course Title'] == course_title]
    try:
        desc = markdown(description(user_input, course_title, course_row['Course Url'].values[0]))
    except Exception:
        desc = ''
    return desc

@app.route('/about_nptel', methods=['GET'])
def about_nptel():
    user_input = request.args.get('user_input')
    print(user_input)
    course_title = request.args.get('course')
    course_row = df.loc[df['Course Name'] == course_title]
    try:
        desc = markdown(description(keyword=user_input, title=course_title, url=course_row['NPTEL URL'].values[0]))
    except Exception:
        desc = ''
    return desc

@app.route('/about_mit', methods=['GET'])
def about_mit():
    user_input = request.args.get('user_input')
    course_title = request.args.get('course')
    course_row = df_mit.loc[df_mit['Course Title'] == course_title]
    try:
        desc = markdown(description(user_input, course_title, course_row['URL'].values[0]))
    except Exception:
        desc = ''
    return desc

if __name__ == '__main__':
    app.run(debug=True)