University Registration System — Phase 1
This is a Flask-based web application for managing a university registration system. It allows users to:

Add students, courses, and course sections

List all students, courses (with optional rubric filter), and sections

This is Phase 1 of the CSCI 414/514 group project, built using:

Python (Flask) — for server-side logic

SQLite — for the database

HTML + Jinja2 — for templating

JavaScript — for basic form interaction and validation

How the System Works

models.py:
Handles database connection and schema creation.

Defines three tables: students, courses, and sections.

Automatically creates the database file (database.db) on first run.

app.py:
The main Flask application.

Defines routes for adding and listing students, courses, and sections.

Initializes the database on app startup.

templates/:
Contains all HTML pages for forms and lists.

Uses Jinja2 to dynamically render content from the database.

static/:
Contains styling (style.css) and interactivity (script.js).

script.js adds:

A confirmation popup on form submission.

Auto-capitalization for rubric input fields.

How to run the app:

Python is included in the Repo with the proper instalation of Flask (obviously)

Project structure
The structure is already correct as is though if needed-
-to be checked it should be as follows:
university_reg/
├── app.py
├── models.py
├── database.db (auto-created after running)
├── templates/
│   ├── base.html
│   ├── add_student.html
│   ├── list_students.html
│   ├── add_course.html
│   ├── list_courses.html
│   ├── add_section.html
│   └── list_sections.html
├── static/
│   ├── style.css
│   └── script.js

Once confirming everything is correct (again it should be already) -
- Run the app from the Project1 directory by running 'python app.py'
Then open your browser and go to:
http://127.0.0.1:5000

You should now be able to see the directory system where you can-
-Add students, courses, and sections.
-List them all.
-Test any other functionality you want, I added some filters and auto capitilization.

Notes
The database is stored locally in database.db and is created automatically.

You do not need to manually create any tables or schema.
