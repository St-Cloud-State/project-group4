# models.py
import sqlite3

# function returns a connection to the SQLite database.
# also configures the connection to return rows as dictionaries
# (so you can access columns by name).
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Connects to the database file (or creates it if it doesn't exist)
    conn.row_factory = sqlite3.Row         # Enables name-based access to columns (e.g., row['name'])
    return conn

# function initializes the database and creates the tables if they don't already exist.
def init_db():
    conn = get_db_connection()             # Get database connection
    cursor = conn.cursor()                 # Create a cursor object to execute SQL commands

    # Create the 'students' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each student
            name TEXT NOT NULL,                    -- Student name (required)
            address TEXT                           -- Student address (optional)
        )
    ''')

    # Create the 'courses' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each course
            rubric TEXT NOT NULL,                  -- Course rubric (e.g., CSCI, MATH)
            number TEXT NOT NULL,                  -- Course number (e.g., 414)
            name TEXT NOT NULL,                    -- Full course name
            credits INTEGER NOT NULL               -- Number of credits
        )
    ''')

    # Create the 'sections' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each section
            course_id INTEGER NOT NULL,            -- Foreign key referencing a course
            semester TEXT NOT NULL,                -- Semester (e.g., Fall 2024)
            FOREIGN KEY (course_id) REFERENCES courses(id) -- Link to courses table
        )
    ''')

    # Create the 'registrations' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each registration
            student_id INTEGER NOT NULL,            -- Foreign key referencing a student
            section_id INTEGER NOT NULL,            -- Foreign key referencing a section
            FOREIGN KEY (student_id) REFERENCES students(id), -- Link to students table
            FOREIGN KEY (section_id) REFERENCES sections(id) -- Link to sections table
        )
    ''')

    conn.commit()     # Save the changes to the database
    conn.close()      # Close the connection when done
