import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from selenium import webdriver
from selenium.webdriver.common.by import By

from classes.course import Course
from classes.user import User
from classes.material import Material
from classes.semester import Semester
from database.engine import engine

def scrape_files(semester_id):

    with Session(engine) as session:
        statement = select(Course.portal_url).where(
            Course.semester_id == semester_id)
        urls = session.scalars(statement).all()
        current_user = session.scalars(
            select(User).where(User.id == 1)
        ).first()

    driver = webdriver.Firefox()
    driver.get("https://mygust.gust.edu.kw/my/")
    if "login" in driver.current_url:
                login(driver, current_user)

    for course_url in urls:
        driver.get(course_url)
        time.sleep(2)
        

#def scrape_courses():


def login(driver, current_user):
        time.sleep(10)
        print("login")
        email_box = driver.find_element(
            By.NAME, "loginfmt"
        )
        submit_button = driver.find_element(
            By.ID, "idSIButton9"
        )
        email_box.send_keys(current_user.school_email)
        submit_button.click()
        time.sleep(3)

        submit_button = driver.find_element(
            By.ID, "idSIButton9"
        )
        password_box = driver.find_element(
            By.NAME, "passwd"
        )
        password_box.send_keys(current_user.email_password)
        submit_button.click()

        time.sleep(3)

        


