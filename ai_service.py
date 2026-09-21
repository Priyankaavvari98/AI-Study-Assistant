import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def summarize_text(text):
	prompt = f"""
You are an AI study assistant.

Summarize the following study material clearly and concisely.

Include:
- A short overview
- Important concepts
- Key points

Study material:

{text}
"""

	response = client.models.generate_content(
		model="gemini-3.6-flash",
		contents=prompt
	)

	return response.text
def generate_quiz(text):

    prompt = f"""
You are an AI study assistant.

Create a practice quiz based ONLY on the study material provided below.

Generate 5 multiple-choice questions.

For each question:
- Provide 4 answer choices labeled A, B, C, and D.
- Clearly identify the correct answer.
- Give a short explanation of why the answer is correct.

Format the quiz clearly.

Study material:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text
def answer_question(study_material, question):

    prompt = f"""
You are an AI study assistant.

Answer the student's question using ONLY the study material
provided below.

If the answer cannot be found in the study material, clearly say:

"The answer is not available in the provided study material."

Do not make up information.

Study material:

{study_material}

Student's question:

{question}

Provide a clear and easy-to-understand answer.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text