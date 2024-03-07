# import requests
# from bs4 import BeautifulSoup
# import csv

# # Send a GET request to the URL
# response = requests.get('https://ocw.aprende.org/courses/')

# # Parse the HTML content of the page with BeautifulSoup
# soup = BeautifulSoup(response.text, 'html.parser')

# # Open the CSV file in write mode with UTF-8 encoding
# with open('mit.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     # Write the header
#     writer.writerow(["Course Number", "Course Title", "URL"])

#     # Iterate over the table numbers
#     for table_number in range(8, 120, 3):
#         # Find all the rows in the current table
#         rows = soup.select(f'#course_wrapper > table:nth-child({table_number}) > tbody > tr')

#         # For each row, find the course number, course title, and URL
#         for row in rows:
#             course_number = row.select_one('td:nth-child(1) > a').text.strip()
#             course_title = row.select_one('td:nth-child(2) > a').text.strip()
#             url = 'https://ocw.aprende.org' + row.select_one('td:nth-child(2) > a')['href']

#             # Write the data to the CSV file
#             writer.writerow([course_number, course_title, url])

import requests
from bs4 import BeautifulSoup
import csv

# Send a GET request to the URL
response = requests.get('https://ocw.aprende.org/courses/')

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Open the CSV file in write mode with UTF-8 encoding
with open('mitNEW.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Course Number", "Course Title", "URL"])

    # Iterate over the table numbers
    for table_number in range(8, 120):
        # Find the current table
        table = soup.select_one(f'#course_wrapper > table:nth-child({table_number}) > tbody')

        # If the table exists, find all the rows in it
        if table is not None:
            rows = table.select('tr')

            # For each row, find the course number, course title, and URL
            for row in rows:
                course_number = row.select_one('td:nth-child(1) > a').text.strip()
                course_title = row.select_one('td:nth-child(2) > a').text.strip()
                url = 'https://ocw.aprende.org' + row.select_one('td:nth-child(2) > a')['href']

                # Write the data to the CSV file
                writer.writerow([course_number, course_title, url])