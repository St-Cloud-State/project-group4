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

# ------------------- Run the app -------------------
if __name__ == '__main__':
    app.run(debug=True)
