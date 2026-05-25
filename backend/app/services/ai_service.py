import os
import json
import anthropic


def generate_quiz(source_text: str, question_count: int, question_types: list) -> list:
    """
    Generate quiz questions from lecture notes using Claude API.

    Args:
        source_text: Extracted lecture note text
        question_count: Number of questions to generate
        question_types: List of question types e.g. ['mcq', 'true_false']

    Returns:
        List of question dictionaries
    """
    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    types_str = ", ".join(question_types)

    prompt = f"""You are a quiz generator. Given the lecture notes below, generate exactly {question_count} questions.

Return ONLY a valid JSON array. No explanation, no preamble, no markdown formatting.

Question types to generate: {types_str}

Format each question exactly like this:
[
  {{
    "type": "mcq",
    "question": "...",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "correct_answer": "A",
    "explanation": "..."
  }},
  {{
    "type": "true_false",
    "question": "...",
    "options": ["True", "False"],
    "correct_answer": "True",
    "explanation": "..."
  }},
  {{
    "type": "short_answer",
    "question": "...",
    "options": null,
    "correct_answer": "...",
    "explanation": "..."
  }}
]

Lecture Notes:
{source_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text.strip()

    # Parse JSON response
    questions = json.loads(response_text)
    return questions