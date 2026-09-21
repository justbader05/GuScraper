from tkinter import Tk, filedialog
from pathlib import Path
from datetime import date
from getpass import getpass

from sqlalchemy import select, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from classes.user import User
from classes.semester import Semester
from classes.course import Course
from console import clear_screen

from scripts.scrape import scrape_files 
from scripts.organize import organize_files

FIELD_LABELS = {
    "id": "ID",
    "school_email": "GUST email",
    "email_password": "GUST password",
    "semester_id": "Semester ID",
    "season": "Season",
    "start_date": "Start date",
    "end_date": "End date",
    "directory": "Semester folder",
    "name": "Name",
    "portal_url": "MyGUST course URL",
    "course_directory": "Course folder",
}


def field_label(key):
    return FIELD_LABELS.get(key, key.replace("_", " ").capitalize())


def pause():
    input("\nPress Enter to continue...")


def choose_semester(semesters, prompt):
    selection_error = False
    while True:
        clear_screen()
        print("\nAvailable semesters:")
        for index, semester in enumerate(semesters, start=1):
            print(f"  {index}. {semester.season} ({semester.start_date} to {semester.end_date})")
        if selection_error:
            print(f"Please enter a number from 1 to {len(semesters)}, or BACK to cancel.")
        response = input(prompt).strip()
        if response.upper() == "BACK":
            return None
        try:
            selection = int(response)
        except ValueError:
            selection = 0
        if 1 <= selection <= len(semesters):
            return semesters[selection - 1]
        selection_error = True


def mainmenu(engine):
    user = initialize_user(engine)
    while True:
            clear_screen()
            print("\nWelcome to GuScraper!")
            print("Download and organize your course materials from MyGUST.")

            response = input("""
  1. How to use GuScraper
  2. Download course materials
  3. View or add semesters
  4. View or add courses
  5. Create or edit your GUST account
  6. Settings (not available yet)

Choose an option (1-6): """).strip()
            clear_screen()
            
            match response:
                case "1":
                        print("""
How to use GuScraper

Each semester has a folder for its course materials.

  1. Add a semester and choose where to save its materials.
  2. Add your courses and their MyGUST URLs to that semester.
  3. Choose 'Create or edit your GUST account' and select your current semester.
  4. Choose 'Download course materials'.
     New files are downloaded and organized into course folders.

GuScraper uses your GUST email and password to sign in to MyGUST.
These details are stored in a database on your computer.
""")
                case "2":
                        if not user:
                           print("No account is configured. Downloads require a GUST account.")
                           print("Choose option 5 to create your account first.")
                        else:
                            folder = Path(user.semester.directory).expanduser().resolve()
                            organize_files(scrape_files(user.semester.id, folder), folder, engine)
                case "3":
                      interaction_menu(engine, Semester)
                      continue
                case "4":
                      interaction_menu(engine, Course)
                      continue
                case "5":
                      user = create_user(engine) or user
                case "6":
                      print("Settings are not available yet. Please choose an option from 1 to 5.")
                case _:
                      print("Please enter a number from 1 to 6.")
            pause()

def create_user(engine):
    clear_screen()
    try:
        print("\nSet up your GUST account")
        print("Enter the credentials you use to sign in to MyGUST.")
        print("Leave the email blank to return to the menu.")
        email = input("GUST email: ").strip()
        if not email:
            print("Account setup cancelled.")
            return None

        password_error = False
        while True:
            clear_screen()
            print("\nSet up your GUST account")
            print(f"GUST email: {email}")
            if password_error:
                print("Please enter your GUST password.")
            password = getpass("GUST password: ")
            if password.strip():
                break
            password_error = True

        with Session(engine) as session:
            semesters = session.scalars(select(Semester).order_by(Semester.id)).all()

        if semesters:
            semester = choose_semester(
                semesters, "Choose your current semester by number, or BACK to cancel: "
            )
            if semester is None:
                print("Account setup cancelled.")
                return None
        else:
            clear_screen()
            print("\nNo semesters yet. Add your current semester to continue.")
            pause()
            semester = creation_menu(engine, Semester)
            if semester is None:
                print("Account setup cancelled. No account was saved.")
                return None

        with Session(engine) as session:
            user = session.get(User, 1)
            editing_user = user is not None
            if user is None:
                user = User(id=1)
                session.add(user)
            user.school_email = email
            user.email_password = password
            user.semester_id = semester.id
            session.commit()

        user = initialize_user(engine)
        action = "updated" if editing_user else "created"
        print(f"Account {action} successfully. Choose option 2 to download course materials.")
        return user
    except SQLAlchemyError:
        print("Could not complete account setup. Check that the database is available and try again.")
        return None

def choose_root():
     root = Tk()
     root.withdraw()

     folder = filedialog.askdirectory(
          title="Choose a folder for your course materials"
     )

     root.destroy()

     if not folder:
          return None

     return Path(folder).resolve()

def initialize_user(engine):
    with Session(engine) as e:
        return e.get(User, 1, options=[joinedload(User.semester)])

def interaction_menu(engine, model):
    with Session(engine) as e:
        while True:
            objects = e.scalars(select(model)).all()
            columns = inspect(model).column_attrs

            clear_screen()
            print(f"\n{model.__name__} list")
            if not objects:
                print(f"No {model.__name__.lower()}s yet. Type CREATE to add one.")

            for index, obj in enumerate(objects, start=1):
                values = []
                for column in columns:
                    value = getattr(obj, column.key)
                    values.append(f"{field_label(column.key)}: {value if value is not None else 'Not set'}")

                print(f"  {index}. " + " | ".join(values))

            response = input(
                f"\nType CREATE to add a {model.__name__.lower()}, or BACK to return: "
            ).strip()

            if response.upper() == "BACK":
                return

            elif response.upper() == "CREATE":
                creation_menu(engine, model)
                pause()
                continue

            try:
                response = int(response)

            except ValueError:
                print("Please type CREATE to add an entry, or BACK to return.")
                pause()
                continue

            if not 1 <= response <= len(objects):
                print("That entry isn't in the list. Type CREATE to add one, or BACK to return.")
                pause()
                continue

            print("Removing entries is not available yet. Type CREATE to add an entry, or BACK to return.")
            pause()
            
def creation_menu(engine, model): #To be honest I vibe coded this because I've got better shit to do than make a cli menu.
    mapper = inspect(model)
    data = {}

    if model is Course:
        with Session(engine) as session:
            semesters = session.scalars(select(Semester).order_by(Semester.id)).all()
        if not semesters:
            clear_screen()
            print("No semesters yet. Add a semester from option 3 in the main menu before creating a course.")
            return None

    for column in mapper.columns:

        # Skip auto-generated primary keys
        if column.primary_key and column.autoincrement:
            continue

        # The organizer assigns the course folder after downloading materials.
        if model is Course and column.key == "course_directory":
            continue

        clear_screen()
        print(f"\nAdd a {model.__name__.lower()}")
        print("Fill in the details below. Fields marked optional can be left blank.\n")

        if model is Semester and column.key == "directory":
            print("Choose a folder for this semester's materials in the folder picker.")
            value = choose_root()
            if not value:
                print("No folder selected. The semester was not added.")
                return

            data[column.key] = str(value)
            continue

        if model is Course and column.key == "semester_id":
            semester = choose_semester(
                semesters, "Choose a semester for this course by number, or BACK to cancel: "
            )
            if semester is None:
                print("Course creation cancelled. No course was saved.")
                return None
            data[column.key] = semester.id
            continue

        optional = " (optional)" if column.nullable or column.default is not None else ""
        python_type = column.type.python_type
        hint = " (YYYY-MM-DD)" if python_type is date else ""
        value = input(f"{field_label(column.key)}{hint}{optional}: ")

        # Allow nullable/default columns to be skipped
        if value == "":
            if column.nullable or column.default is not None:
                continue

        # Basic type conversion
        try:
            value = date.fromisoformat(value) if python_type is date else python_type(value)
        except ValueError:
            print(f"Couldn't use that value for {field_label(column.key).lower()}. The {model.__name__.lower()} was not added.")
            return

        data[column.key] = value

    new_object = model(**data)

    with Session(engine) as session:
        session.add(new_object)
        session.commit()
        session.refresh(new_object)

    print(f"\n{model.__name__} added successfully.")

    return new_object

        
