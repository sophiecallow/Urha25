# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# import json

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# QUIZ_FILE = 'quizzes.json'


# @app.after_request
# def add_header(response):
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
#     return response


# def load_data(file_path):
#     """Load quiz data from the JSON file."""
#     try:
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {}

# def save_data(data, file_path):
#     """Save quiz data to the JSON file."""
#     with open(file_path, 'w') as f:
#         json.dump(data, f, indent=4)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == 'admin' and password == 'password':
#             session['username'] = username
#             return redirect(url_for('admin'))
#         else:
#             return 'Invalid credentials', 401
#     return render_template('login.html')

# @app.route('/admin')
# def admin():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     quizzes = load_data(QUIZ_FILE)
#     return render_template('admin.html', quizzes=quizzes)

# @app.route('/admin/get_quiz/<quiz_name>')
# def get_quiz(quiz_name):
#     """Retrieve a specific quiz."""
#     quizzes = load_data(QUIZ_FILE)
#     quiz = quizzes.get(quiz_name)

#     if quiz:
#         return jsonify({"name": quiz_name, "questions": quiz})
#     else:
#         return jsonify({"error": "Quiz not found"}), 404

# @app.route('/admin/edit', methods=['GET', 'POST'])
# def create_or_edit_quiz():
#     """Create or edit a quiz."""
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         quiz_name = request.form['quiz_name']
#         questions = []

#         for i in range(1, 11):  # Allow up to 10 questions
#             question = request.form.get(f'question-{i}')
#             answer = request.form.get(f'answer-{i}')
#             if question and answer:  # Skip empty question-answer pairs
#                 questions.append({'question': question, 'answer': answer})

#         quizzes = load_data(QUIZ_FILE)
#         quizzes[quiz_name] = questions
#         save_data(quizzes, QUIZ_FILE)

#         return redirect(url_for('admin'))

#     quiz_name = request.args.get('quiz_name')
#     quizzes = load_data(QUIZ_FILE)
#     current_questions = quizzes.get(quiz_name, []) if quiz_name else []

#     return render_template('admin_edit.html', quiz_name=quiz_name, current_questions=current_questions)

# @app.route('/admin/delete/<quiz_name>', methods=['GET'])
# def delete_quiz(quiz_name):
#     """Delete a quiz."""
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     quizzes = load_data(QUIZ_FILE)
#     if quiz_name in quizzes:
#         del quizzes[quiz_name]
#         save_data(quizzes, QUIZ_FILE)

#     return redirect(url_for('admin'))

# @app.route('/logout')
# def logout():
#     """Logout the user."""
#     session.pop('username', None)
#     return redirect(url_for('index'))

# @app.route('/quizzes')
# def quizzes():
#     """Display a list of all quizzes for users."""
#     quizzes = load_data(QUIZ_FILE)
#     return render_template('quizzes.html', quizzes=quizzes)


# @app.route('/quiz/<quiz_name>')
# def quiz(quiz_name):
#     # Load your quiz data
#     quizzes = load_data(QUIZ_FILE)
#     questions = quizzes.get(quiz_name, [])
#     if not questions:
#         return "Quiz not found!", 404

#     # Get the current question index
#     question_index = int(request.args.get('question', 0))  # Default to the first question
#     question_index = max(0, min(question_index, len(questions) - 1))  # Keep within range

#     # Calculate progress
#     total_questions = len(questions)
#     progress = ((question_index + 1) / total_questions) * 100

#     # Render template with variables
#     return render_template(
#         'quiz_navigation.html',
#         quiz_name=quiz_name,
#         question=questions[question_index],
#         question_index=question_index,
#         total_questions=total_questions,
#         progress=progress
#     )




# # if __name__ == '__main__':
# #     app.run(debug=True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

QUIZ_FILE = 'quizzes.json'

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

def load_data(file_path):
    """Load quiz data from the JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data, file_path):
    """Save quiz data to the JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def login_required(f):
    """Decorator to check if the user is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    quizzes = load_data(QUIZ_FILE)
    return render_template('admin.html', quizzes=quizzes)

@app.route('/admin/get_quiz/<quiz_name>')
@login_required
def get_quiz(quiz_name):
    """Retrieve a specific quiz."""
    quizzes = load_data(QUIZ_FILE)
    quiz = quizzes.get(quiz_name)

    if quiz:
        return jsonify({"name": quiz_name, "questions": quiz})
    else:
        return jsonify({"error": "Quiz not found"}), 404

@app.route('/admin/edit', methods=['GET', 'POST'])
@login_required
def create_or_edit_quiz():
    """Create or edit a quiz."""
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        questions = []

        for i in range(1, 11):  # Allow up to 10 questions
            question = request.form.get(f'question-{i}')
            answer = request.form.get(f'answer-{i}')
            if question and answer:  # Skip empty question-answer pairs
                questions.append({'question': question, 'answer': answer})

        quizzes = load_data(QUIZ_FILE)
        quizzes[quiz_name] = questions
        save_data(quizzes, QUIZ_FILE)

        return redirect(url_for('admin'))

    quiz_name = request.args.get('quiz_name')
    quizzes = load_data(QUIZ_FILE)
    current_questions = quizzes.get(quiz_name, []) if quiz_name else []

    return render_template('admin_edit.html', quiz_name=quiz_name, current_questions=current_questions)

@app.route('/admin/delete/<quiz_name>', methods=['GET'])
@login_required
def delete_quiz(quiz_name):
    """Delete a quiz."""
    quizzes = load_data(QUIZ_FILE)
    if quiz_name in quizzes:
        del quizzes[quiz_name]
        save_data(quizzes, QUIZ_FILE)

    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    """Logout the user."""
    session.pop('username', None)
    return redirect(url_for('index'))

# @app.route('/quizzes')
# def quizzes():
#     """Display a list of all quizzes for users."""
#     quizzes = load_data(QUIZ_FILE)
#     return render_template('quizzes.html', quizzes=quizzes)

@app.route('/quizzes')
def quizzes():
    """Display a list of all quizzes for users."""
    quizzes = load_data(QUIZ_FILE)
    return render_template('quizzes.html', quizzes=quizzes)  # Render HTML template



# @app.route('/quiz/<quiz_name>', methods=['GET', 'POST'])
# def quiz(quiz_name):
#     """Handle quiz navigation."""
#     quizzes = load_data(QUIZ_FILE)
#     questions = quizzes.get(quiz_name, [])
#     if not questions:
#         return "Quiz not found!", 404

#     # Track user progress using session
#     if quiz_name not in session:
#         session[quiz_name] = 0  # Initialize progress

#     progress = session[quiz_name]

#     if request.method == 'POST':
#         user_answer = request.form.get('answer')
#         if user_answer:  # Simulate answer validation
#             progress += 1
#             session[quiz_name] = progress

#     if progress >= len(questions):
#         return render_template('quiz_completed.html', quiz_name=quiz_name)

#     question = questions[progress]
#     return render_template(
#         'quiz_navigation.html',
#         quiz_name=quiz_name,
#         question=question,
#         progress=progress + 1,
#         total_questions=len(questions),
#     )

@app.route('/quiz/<quiz_name>')
def quiz(quiz_name):
    # Load your quiz data
    quizzes = load_data(QUIZ_FILE)
    questions = quizzes.get(quiz_name, [])
    if not questions:
        return "Quiz not found!", 404

    # Get the current question index
    question_index = int(request.args.get('question', 0))  # Default to the first question
    question_index = max(0, min(question_index, len(questions) - 1))  # Keep within range

    # Calculate progress
    total_questions = len(questions)
    progress = ((question_index + 1) / total_questions) * 100

    # Render template with variables
    return render_template(
        'quiz_navigation.html',
        quiz_name=quiz_name,
        question=questions[question_index],
        question_index=question_index,
        total_questions=total_questions,
        progress=progress
    )
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Railway's PORT or default to 5000
    app.run(host='0.0.0.0', port=port)