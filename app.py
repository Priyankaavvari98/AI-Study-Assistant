from flask import Flask, render_template, request, redirect, url_for

from database import (
	initialize_database,
	get_all_notes,
	add_note,
	delete_note
)

from ai_service import summarize_text, generate_quiz, answer_question


app = Flask(__name__)


# Initialize the database
initialize_database()


# Home page
@app.route("/")
def home():
	return render_template("index.html")


# Notes page
@app.route("/notes")
def notes():
	all_notes = get_all_notes()

	return render_template(
		"notes.html",
		notes=all_notes
	)


# Add a note
@app.route("/notes/add", methods=["POST"])
def add_note_route():

	title = request.form["title"]
	content = request.form["content"]

	add_note(title, content)

	return redirect(url_for("notes"))


# Delete a note
@app.route("/notes/delete/<int:note_id>", methods=["POST"])
def delete_note_route(note_id):

	delete_note(note_id)

	return redirect(url_for("notes"))


# Summarize study material
@app.route("/summarize", methods=["GET", "POST"])
def summarize():

	if request.method == "POST":

		text = request.form["text"]

		try:
			summary = summarize_text(text)

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

	return render_template("summarize.html")

# Generate AI quiz
@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if request.method == "POST":

        text = request.form["text"]

        try:

            quiz = generate_quiz(text)

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

    return render_template("quiz.html")
# Ask a question about study material
@app.route("/ask", methods=["GET", "POST"])
def ask():

    if request.method == "POST":

        study_material = request.form["study_material"]
        question = request.form["question"]

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

    return render_template("ask.html")

# Start the application
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
