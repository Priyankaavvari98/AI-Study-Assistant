# AI Study Assistant Toy Project

## Project Description

AI Study Assistant is a small web application designed to
help students study and organize their learning material.

The application uses the Google Gemini API to provide AI-powered study
features.

## Major Functionalities

The project implements the following major functionalities:

### 1. Study Notes Management

Users can create, view, and delete study notes. The notes are stored
using a SQLite database.

### 2. AI Text Summarization

Users can enter study material and generate a concise AI-powered summary
using the Google Gemini API.

### 3. AI Quiz Generation

Users can provide study material and generate practice multiple-choice
questions with answer choices, correct answers, and explanations.

### 4. AI Question Answering

Users can provide study material and ask questions about it. The AI
generates an answer based on the provided study material.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- SQLite
- Google Gemini API
- Git
- GitHub

## AI Tools Used

The project was developed using AI-assisted coding tools.

### ChatGPT and Claude

ChatGPT was used for:

- Project planning
- Generating and improving code
- Understanding Python and Flask concepts
- Debugging errors
- Troubleshooting the application
- Improving project documentation

### GitHub Copilot

GitHub Copilot was used as an AI-assisted coding tool during development.

### Google Gemini API

The Google Gemini API is integrated into the application to provide:

- Text summarization
- Quiz generation
- Question answering

## Open-Source Reference Project

The project was developed with reference to the following open-source
project:

**AI Study Assistant - Flask Web Application**

GitHub repository:

https://github.com/JiteshShelke/AI-Study-Assistant-Flask

The reference project was selected because it provides comparable
AI-powered study functionality using a Flask web application.

The reference project helped provide ideas for the scope and functionality
of this project. However, the implementation in this repository was
developed independently using AI-assisted development tools rather than
copying the reference project's source code.

## Project Structure

```text
AI-Study-Assistant/
│
├── app.py
├── ai_service.py
├── database.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── notes.html
│   ├── summarize.html
│   ├── quiz.html
│   └── ask.html
│
└── static/
    └── style.css
