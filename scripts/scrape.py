from pathlib import Path
import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from classes.course import Course
from classes.user import User
from classes.material import Material
from classes.semester import Semester
from database.engine import engine

def scrape_files(semester_id, download_path):
    courses, current_user = get_user_and_courses(semester_id)

    try:
        driver = initialize_firefox_driver(download_path)
        driver.get("https://mygust.gust.edu.kw/my/")
        if "login" in driver.current_url:
                    login(driver, current_user)

        new_materials = []
        for course in courses:
            url = course.portal_url
            driver.get(url)
            wait_for_page(driver)

            filtered_elements = filter_elements(driver, course)
            for element in filtered_elements:
                link = element.find_element(By.CSS_SELECTOR, '.aalink.stretched-link')
                activity_card = element.find_element(By.CSS_SELECTOR, "[data-region='activity-card']")

                moodle_id = element.get_attribute('id')
                portal_url = link.get_attribute('href')
                name = activity_card.get_attribute('data-activityname')

                path = download_file(link, download_path)
                new_material = Material(moodle_id, portal_url, path, name, course.id)
                new_materials.append(new_material)
                print_new_materials(new_material)
    
    finally:
          driver.quit()
    return new_materials
        

#def scrape_courses():

def wait_for_page(driver, timeout=10):
      WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
      )


def login(driver, current_user):
        email_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'input[name="loginfmt"]:not([type="hidden"])')
            )
        )
        submit_button = WebDriverWait(driver, 10, ignored_exceptions=(StaleElementReferenceException)).until(
            EC.element_to_be_clickable(
                (By.ID, "idSIButton9")
                )
            )
        email_box.send_keys(current_user.school_email)
        submit_button.click()

        password_box = WebDriverWait(driver, 10).until(
              EC.element_to_be_clickable(
                    (By.NAME, "passwd")
              )
        )
        submit_button = WebDriverWait(driver, 10, ignored_exceptions=(StaleElementReferenceException)).until(
            EC.element_to_be_clickable(
                (By.ID, "idSIButton9")
                )
            )
        password_box.send_keys(current_user.email_password)
        submit_button.click()
        
def get_user_and_courses(semester_id):
    with Session(engine) as session:
            statement = select(Course).where(
                Course.semester_id == semester_id)
            courses = session.scalars(statement).all()
    
            current_user = session.scalars(
                select(User).where(User.id == 1)
            ).first()
    return courses, current_user

def filter_elements(driver, course):
    with Session(engine) as session:
        current_materials = session.scalars(
                select(Material).where(
                        Material.course_id == course.id
                )
            ).all()
        
    resource_elements = driver.find_elements(By.CSS_SELECTOR, ".modtype_resource[id]")
    print("Elements found:", len(resource_elements))
    existing_ids = [material.moodle_id for material in current_materials]
    filtered_elements = [
            element for element in resource_elements
            if element.get_attribute("id") not in existing_ids
            ]

    return filtered_elements

def initialize_firefox_driver(download_dir):
    download_dir = Path(download_dir).expanduser().resolve()
    download_dir.mkdir(parents=True, exist_ok=True)

    options = webdriver.FirefoxOptions()

    options.set_preference(
        "browser.download.dir",
        str(download_dir)
    )

    options.set_preference(
        "browser.download.folderList",
        2
    )

    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/pdf,application/octet-stream"
    )

    options.set_preference(
        "pdfjs.disabled",
        True
    )

    driver = webdriver.Firefox(options=options)

    return driver

def download_file(element, download_dir): #This function is completely vibe coded to be honest.
    element.click()

    time.sleep(1)

    while True:
        unfinished_downloads = list(download_dir.glob("*.part"))

        if len(unfinished_downloads) == 0:
            break

        time.sleep(0.2)


    newest_file = None
    newest_time = 0

    for file in download_dir.iterdir():

        if not file.is_file():
             continue

        modified_time = file.stat().st_mtime

        if modified_time > newest_time:
            newest_time = modified_time
            newest_file = file


    path = str(newest_file)
    return path 

def print_new_materials(material):
        print (
            f"""
            ID: {material.moodle_id}
            Portal_url: {material.portal_url}
            Path: {material.file_path}
            Name: {material.name}
            Course ID: {material.course_id}
            File Type: {material.file_type}
            Document Type: {material.document_type}
            """
        )