from sqlalchemy.orm import Session
from classes.user import User
from tkinter import Tk, filedialog
from pathlib import Path
from scripts.scrape import scrape_files 
from scripts.organize import organize_files

def mainmenu(engine):
    is_user = False
    with Session(engine) as e:
        user = e.get(User, 1)
    if user:
        is_user = True

    while True:
            print("Welcome to GuScraper!")
            print("This is a tool that you can use to download and organize all course materials from MyGust.\n")
            if not is_user:
                user = create_user(engine)

            response = input("""
                1.) Start the scraper
                2.) View and Create Semesters
                5.) Change User Settings
""")

def create_user(engine):
    while True:
        try:
            print("Please create a user to proceed")
            email = input("GUST Email: ")
            password = input("Gust Email Password: ")

            print("The system is going to open a prompt.")
            print("Please choose a folder where your class materials will go.")
            folder = choose_root()
            user = User(email, password, folder)

            with Session(engine) as e:
                 e.add(user)
                 e.commit()
                 e.refresh(user)
            
            return user
        
        except Exception as e:
            print (f"ERROR: {e}")

def choose_root():
     root = Tk()
     root.withdraw()

     folder = filedialog.askdirectory(
          title="Select your courses and materials folder."
     )

     root.destroy()

     if not folder:
          return None

     return Path(folder).resolve()