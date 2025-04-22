# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import get_db_connection, init_db

# Initialize the Flask app
app = Flask(__name__)

# On app startup, initialize the database (create tables if needed)
with app.app_context():
    init_db()

# ------------------- Homepage -------------------
@app.route('/')
def index():
    return render_template('base.html')  # Can link to add/list pages

# ------------------- Add Student -------------------
@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Grab form inputs
        name = request.form['name']
        address = request.form['address']
        
        # Insert student into database
        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, address) VALUES (?, ?)', (name, address))
        conn.commit()
        conn.close()

        # Redirect to list of students
        return redirect(url_for('list_students'))

    # If GET, render form
    return render_template('add_student.html')

# ------------------- List Students -------------------
@app.route('/students')
def list_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('list_students.html', students=students)

# ------------------- Add Course -------------------
@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        # Get form data
        rubric = request.form['rubric']
        number = request.form['number']
        name = request.form['name']
        credits = request.form['credits']

        # Insert into DB
        conn = get_db_connection()
        conn.execute('INSERT INTO courses (rubric, number, name, credits) VALUES (?, ?, ?, ?)',
                     (rubric, number, name, credits))
        conn.commit()
        conn.close()

        return redirect(url_for('list_courses'))

    return render_template('add_course.html')

# ------------------- List Courses (Filter by Rubric) -------------------
@app.route('/courses')
def list_courses():
    rubric = request.args.get('rubric')  # Optional ?rubric=CSCI
    conn = get_db_connection()
    if rubric:
        courses = conn.execute('SELECT * FROM courses WHERE rubric = ?', (rubric.upper(),)).fetchall()
    else:
        courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return render_template('list_courses.html', courses=courses)

# ------------------- Add Section -------------------
@app.route('/add-section', methods=['GET', 'POST'])
def add_section():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses').fetchall()  # Get courses for dropdown

    if request.method == 'POST':
        course_id = request.form['course_id']
        semester = request.form['semester']

        conn.execute('INSERT INTO sections (course_id, semester) VALUES (?, ?)', (course_id, semester))
        conn.commit()
        conn.close()

        return redirect(url_for('list_sections'))

    conn.close()
    return render_template('add_section.html', courses=courses)

# ------------------- List Sections (Filter by Course) -------------------
@app.route('/sections')
def list_sections():
    course_id = request.args.get('course_id')  # Optional ?course_id=5
    conn = get_db_connection()
    if course_id:
        sections = conn.execute('SELECT * FROM sections WHERE course_id = ?', (course_id,)).fetchall()
    else:
        sections = conn.execute('SELECT * FROM sections').fetchall()
    conn.close()
    return render_template('list_sections.html', sections=sections)

# ------------------- Add Student to a Section -------------------
@app.route('/add-registration', methods=['GET', 'POST'])
def add_registration():
    conn = get_db_connection()
    students = conn.execute('SELECT id, name FROM students').fetchall()  # Get students for dropdown
    sections = conn.execute('''SELECT sections.id AS section_id, sections.semester, courses.rubric, courses.number
        FROM sections
        JOIN courses ON sections.course_id = courses.id''').fetchall() # Get sections for dropdown

    if request.method == 'POST':
        student_id = request.form['student_id']
        section_id = request.form['section_id']
        conn.execute('INSERT INTO registrations (student_id, section_id) VALUES (?, ?)', 
                       (student_id, section_id))
        conn.commit()
        return redirect(url_for('list_students_in_section', section_id=section_id))

    conn.close()
    return render_template('add_registration.html', students=students, sections=sections)


# ------------------- List Students in a Section -------------------
@app.route('/section-students', methods=['GET', 'POST'])
def list_students_in_section():
    conn = get_db_connection()
    
    # Get all sections for the dropdown
    sections = conn.execute('''SELECT sections.id AS section_id, sections.semester, courses.rubric, courses.number
                               FROM sections
                               JOIN courses ON sections.course_id = courses.id''').fetchall()

    # If a section is selected
    section_id = request.args.get('section_id')
    if section_id:
        # Get the section details
        section = conn.execute('''SELECT sections.id, sections.semester, courses.rubric, courses.number
                                  FROM sections
                                  JOIN courses ON sections.course_id = courses.id
                                  WHERE sections.id = ?''', (section_id,)).fetchone()

        # Get all students in the selected section
        students = conn.execute('''SELECT students.name, students.address
                                   FROM registrations
                                   JOIN students ON registrations.student_id = students.id
                                   WHERE registrations.section_id = ?''', (section_id,)).fetchall()

        return render_template('list_section_students.html', sections=sections, section=section, students=students)

    conn.close()
    return render_template('list_section_students.html', sections=sections, students=None)


# ------------------- List Courses Student is in  -------------------
@app.route('/students-courses', methods=['GET', 'POST'])
def list_students_courses():
    conn = get_db_connection()

    # Get all students for the dropdown
    students = conn.execute('SELECT id AS student_id, name FROM students').fetchall()

    # If a student is selected
    student_id = request.args.get('student_id')
    if student_id:
        # Get the student's details
        student = conn.execute('SELECT id, name FROM students WHERE id = ?', (student_id,)).fetchone()

        # Get all courses the selected student is registered in
        courses = conn.execute('''SELECT courses.rubric, courses.number, sections.semester 
                                  FROM registrations
                                  JOIN sections ON registrations.section_id = sections.id
                                  JOIN courses ON sections.course_id = courses.id
                                  WHERE registrations.student_id = ?''', (student_id,)).fetchall()

        return render_template('list_student_courses.html', students=students, student=student, courses=courses)

    conn.close()
    return render_template('list_student_courses.html', students=students, student=None, courses=None)
    

# ------------------- Run the app -------------------
if __name__ == '__main__':
    app.run(debug=True)
