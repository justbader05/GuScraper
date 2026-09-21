from pathlib import Path
import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from bs4 import BeautifulSoup

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

    print("\nOpening MyGUST to check for new course materials...")
    print(f"Download folder: {download_path}")
    try:
        driver = initialize_firefox_driver(download_path)
        driver.get("https://mygust.gust.edu.kw/my/")
        if "login" in driver.current_url:
                    login(driver, current_user)

        new_materials = []
        for course in courses:
            print(f"\nChecking {course.name}...")
            driver.get(course.portal_url)
            WebDriverWait(driver, 10).until(
                 EC.presence_of_element_located(
                      (By.CLASS_NAME, "modtype_resource")
                 )
            )

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            elements = soup.find_all(class_="modtype_resource")

            filtered_elements = filter_elements(course, elements)
            for element in filtered_elements:
                link = element.select_one(".aalink.stretched-link")
                activity_card = element.select_one("[data-region='activity-card']")

                if link is None or activity_card is None:
                    continue

                moodle_id = element.get("id")
                portal_url = link.get("href")
                name = activity_card.get("data-activityname")

                path = download_file(driver, portal_url, download_path)
                if path == None:
                     continue
                new_material = Material(moodle_id, portal_url, path, name, course.id)
                new_materials.append(new_material)
                print_new_materials(new_material)
    
    finally:
          driver.quit()
    if new_materials:
        count = len(new_materials)
        print(f"\nDownload complete: {count} new {'file' if count == 1 else 'files'}.")
    else:
        print("\nNo new course materials to download.")
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

def filter_elements(course, elements):
    with Session(engine) as session:
        current_materials = session.scalars(
                select(Material).where(
                        Material.course_id == course.id
                )
            ).all()

    existing_ids = [material.moodle_id for material in current_materials]
    filtered_elements = [
            element for element in elements
            if element.get("id") not in existing_ids
            ]

    count = len(elements)
    print(f"Found {count} {'file' if count == 1 else 'files'}; {len(filtered_elements)} new to download.")
    return filtered_elements

def initialize_firefox_driver(download_dir):
    download_dir = Path(download_dir).expanduser().resolve()
    download_dir.mkdir(parents=True, exist_ok=True)

    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")

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

def download_file(driver, url, download_dir, timeout=10):
    download_dir = Path(download_dir)

    def snapshot():
        files = {}
        for path in download_dir.iterdir():
            try:
                if path.is_file():
                    stat = path.stat()
                    files[path] = (stat.st_size, stat.st_mtime_ns)
            except FileNotFoundError:
                # Firefox may rename a partial file during this check.
                continue
        return files

    before = snapshot()
    deadline = time.monotonic() + timeout
    print(f"  Waiting for download (up to {timeout} seconds)...", flush=True)
    # Return to Python before navigation starts; file responses may never
    # signal the page-load completion that driver.get() waits for.
    driver.execute_script(
        "const url = arguments[0];"
        "window.setTimeout(() => window.location.assign(url), 0);",
        url,
    )

    previous = {}
    while time.monotonic() < deadline:
        changed = {
            path: state for path, state in snapshot().items()
            if before.get(path) != state
        }
        if not any(path.suffix == ".part" for path in changed):
            for path, state in changed.items():
                if state[0] > 0 and previous.get(path) == state:
                    return str(path)
        previous = changed
        time.sleep(1)

    print(f"  Download timed out after {timeout} seconds; skipping: {url}")
    for partial_file in download_dir.glob("*.part"):
        if partial_file.is_file():
            partial_file.unlink(missing_ok=True)
    return None

def print_new_materials(material):
    print(f"  Downloaded: {material.name}")
    print(f"    Saved to: {material.file_path}")
    print(f"    Category: {material.document_type} | File type: {material.file_type.upper() or 'Unknown'}")
