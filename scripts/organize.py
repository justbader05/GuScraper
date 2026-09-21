from sqlalchemy import select
from sqlalchemy.orm import Session 
from pathlib import Path
from classes.material import Material
from classes.course import Course

def organize_files(materials, obsidian_root, engine):
    root = Path(obsidian_root).expanduser().resolve()
    courses = [material.course_id for material in materials]
    courses = list(set(courses))
    with Session(engine) as e:
        statement = select(Course).where(
            Course.id.in_(courses)
        )
        courses = e.scalars(statement).all()

        for course in courses:
            course.name = sanitize_filename(course.name)
            course_folder = root / course.name
            course_folder.mkdir(parents=True, exist_ok=True)

            course.course_directory = str(course_folder)

        for course in courses:
            folder = root / course.name
            folder.mkdir(parents=True, exist_ok=True)

            chapter_folder = folder / "Chapters"
            notes_folder = folder / "Notes"
            other_folder = folder / "Other"

            chapter_folder.mkdir(parents=True, exist_ok=True)
            notes_folder.mkdir(parents=True, exist_ok=True)
            other_folder.mkdir(parents=True, exist_ok=True)

            course_materials = [material for material in materials if material.course_id == course.id]

            for material in course_materials:

                download_directory = Path(material.file_path)
                if not download_directory.exists():
                    continue

                if material.document_type == "Chapter":
                    new_path = chapter_folder / download_directory.name
                    download_directory.rename(new_path)
                    material.file_path = str(new_path)

                elif material.document_type == "Notes":
                    new_path = notes_folder / download_directory.name
                    download_directory.rename(new_path)
                    material.file_path = str(new_path)

                elif material.document_type == "Syllabus":
                    new_path = folder / download_directory.name
                    download_directory.rename(new_path)
                    material.file_path = str(new_path)

                else:
                    new_path = other_folder / download_directory.name
                    download_directory.rename(new_path)
                    material.file_path = str(new_path)

                e.add(material)
        e.commit()

def sanitize_filename(name):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, "-")
    return name