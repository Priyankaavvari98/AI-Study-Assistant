from flask import Flask, render_template, request, redirect, url_for, session

from werkzeug.utils import secure_filename

from functools import wraps

import os

from pypdf import PdfReader

from docx import Document

from werkzeug.security import generate_password_hash, check_password_hash


from database import (
    initialize_database,
    create_user,
    get_user_by_username,
    get_all_notes,
    add_note,
    delete_note
)


from ai_service import summarize_text, generate_quiz, answer_question


app = Flask(__name__)


# --------------------------------------------------
# Document Upload Settings
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# --------------------------------------------------
# Secret Key Used for Flask Sessions
# --------------------------------------------------

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key-change-this"
)


# --------------------------------------------------
# Initialize Database
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# Check Allowed File Type
# --------------------------------------------------

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# --------------------------------------------------
# Authentication Helper
# --------------------------------------------------

def login_required(route_function):

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("login"))

        return route_function(*args, **kwargs)

    return wrapper


# --------------------------------------------------
# Home / Main Dashboard
# --------------------------------------------------

@app.route("/")
@login_required
def home():

    return render_template("index.html")


# --------------------------------------------------
# Document Upload
# --------------------------------------------------

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    extracted_text = None
    error = None

    if request.method == "POST":

        # Check whether a file was submitted
        if "file" not in request.files:

            error = "No file selected."

            return render_template(
                "upload.html",
                extracted_text=extracted_text,
                error=error
            )

        file = request.files["file"]

        # Check whether the user selected a file
        if file.filename == "":

            error = "No file selected."

            return render_template(
                "upload.html",
                extracted_text=extracted_text,
                error=error
            )

        # Check file type
        if not allowed_file(file.filename):

            error = "Only PDF, DOCX, and TXT files are allowed."

            return render_template(
                "upload.html",
                extracted_text=extracted_text,
                error=error
            )

        # Make filename safe
        filename = secure_filename(file.filename)

        # Create complete file path
        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        # Save uploaded file
        file.save(file_path)

        try:

            # Get file extension
            extension = filename.rsplit(
                ".",
                1
            )[1].lower()

            # ------------------------------------------
            # Extract text from PDF
            # ------------------------------------------

            if extension == "pdf":

                reader = PdfReader(file_path)

                extracted_text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

            # ------------------------------------------
            # Extract text from DOCX
            # ------------------------------------------

            elif extension == "docx":

                document = Document(file_path)

                extracted_text = "\n".join(
                    paragraph.text
                    for paragraph in document.paragraphs
                )

            # ------------------------------------------
            # Read TXT file
            # ------------------------------------------

            elif extension == "txt":

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as text_file:

                    extracted_text = text_file.read()

        except Exception as e:

            error = f"Could not read the document: {str(e)}"

    return render_template(
        "upload.html",
        extracted_text=extracted_text,
        error=error
    )


# --------------------------------------------------
# Register
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # Validate input
        if not username or not password:

            return render_template(
                "register.html",
                error="Username and password are required."
            )

        # Check whether username already exists
        existing_user = get_user_by_username(username)

        if existing_user:

            return render_template(
                "register.html",
                error="Username already exists."
            )

        # Hash password before storing it
        hashed_password = generate_password_hash(password)

        create_user(
            username,
            hashed_password
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# --------------------------------------------------
# Login
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        user = get_user_by_username(
            username
        )

        # Check username and password
        if user and check_password_hash(
            user["password"],
            password
        ):

            # Store logged-in user's information
            session["user_id"] = user["id"]

            session["username"] = user["username"]

            # Go to main dashboard
            return redirect(
                url_for("home")
            )

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template(
        "login.html"
    )


# --------------------------------------------------
# Logout
# --------------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# --------------------------------------------------
# Notes Page
# --------------------------------------------------

@app.route("/notes")
@login_required
def notes():

    user_id = session["user_id"]

    all_notes = get_all_notes(
        user_id
    )

    return render_template(
        "notes.html",
        notes=all_notes
    )


# --------------------------------------------------
# Add a Note
# --------------------------------------------------

@app.route("/notes/add", methods=["POST"])
@login_required
def add_note_route():

    title = request.form["title"]

    content = request.form["content"]

    user_id = session["user_id"]

    add_note(
        title,
        content,
        user_id
    )

    return redirect(
        url_for("notes")
    )


# --------------------------------------------------
# Delete a Note
# --------------------------------------------------

@app.route(
    "/notes/delete/<int:note_id>",
    methods=["POST"]
)
@login_required
def delete_note_route(note_id):

    user_id = session["user_id"]

    delete_note(
        note_id,
        user_id
    )

    return redirect(
        url_for("notes")
    )


# --------------------------------------------------
# Summarize Study Material
# --------------------------------------------------

@app.route(
    "/summarize",
    methods=["GET", "POST"]
)
@login_required
def summarize():

    if request.method == "POST":

        text = request.form["text"]

        try:

            summary = summarize_text(
                text
            )

            return render_template(
                "summarize.html",
                summary=summary,
                text=text
            )

        except Exception as e:

            return render_template(
                "summarize.html",
                summary=f"Error: {str(e)}",
                text=text
            )

    return render_template(
        "summarize.html"
    )


# --------------------------------------------------
# Generate AI Quiz
# --------------------------------------------------

@app.route(
    "/quiz",
    methods=["GET", "POST"]
)
@login_required
def quiz():

    if request.method == "POST":

        text = request.form["text"]

        # Get number of questions selected by user
        number_of_questions = int(
            request.form.get(
                "number_of_questions",
                5
            )
        )

        # Keep the allowed choices simple
        if number_of_questions not in [5, 10, 15]:
            number_of_questions = 5

        try:

            quiz = generate_quiz(
                text,
                number_of_questions
            )

            return render_template(
                "quiz.html",
                quiz=quiz,
                text=text
            )

        except Exception as e:

            return render_template(
                "quiz.html",
                quiz=f"Error: {str(e)}",
                text=text
            )

    return render_template(
        "quiz.html"
    )


# --------------------------------------------------
# Ask a Question About Study Material
# --------------------------------------------------

@app.route(
    "/ask",
    methods=["GET", "POST"]
)
@login_required
def ask():

    if request.method == "POST":

        study_material = request.form[
            "study_material"
        ]

        question = request.form[
            "question"
        ]

        try:

            answer = answer_question(
                study_material,
                question
            )

            return render_template(
                "ask.html",
                answer=answer,
                study_material=study_material,
                question=question
            )

        except Exception as e:

            return render_template(
                "ask.html",
                answer=f"Error: {str(e)}",
                study_material=study_material,
                question=question
            )

    return render_template(
        "ask.html"
    )


# --------------------------------------------------
# Start the Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False
    )