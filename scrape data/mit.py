from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv

# Create a new Chrome browser instance
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to the target URL
url = "https://ocw.mit.edu/search/?f=Lecture%20Videos&s=department_course_numbers.sort_coursenum&type=course"
driver.get(url)

# Wait for the dynamic content to load
wait = WebDriverWait(driver, 10)
courses_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.search-results-area div:nth-child(2) > section > article")))

course_data = []

for course in courses_element:
    # Scroll to the course element
    driver.execute_script("arguments[0].scrollIntoView();", course)

    course_title_element = course.find_element(By.CSS_SELECTOR, ".lr-row.course-title > a")
    course_url_element = course.find_element(By.CSS_SELECTOR, ".lr-row.course-title > a")
    course_id_element = course.find_element(By.CSS_SELECTOR, ".lr-row.resource-header > div")

    course_title = course_title_element.text if course_title_element else ""
    course_url = course_url_element.get_attribute("href") if course_url_element else ""
    course_id = course_id_element.text if course_id_element else ""

    course_data.append({"id": course_id, "title": course_title, "url": course_url})

# Save course data to a CSV file
with open("course_data.csv", mode="w", newline="", encoding="utf-8") as file:
    fieldnames = ["id", "title", "url"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for course in course_data:
        writer.writerow(course)

print("Course data saved to course_data.csv")

# Close the browser
driver.quit()