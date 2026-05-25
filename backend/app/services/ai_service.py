import os
import json
import random
from groq import Groq

def truncate_text(text: str, max_words: int = 1500) -> str:
    """Truncate text to stay within Groq's token limits."""
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words])
    return text

# Set this to True when you have a real API key
USE_REAL_API = True


def generate_quiz(source_text: str, question_count: int, question_types: list) -> list:
    """
    Generate quiz questions from lecture notes.
    Uses Groq API if USE_REAL_API is True, otherwise returns mock questions.

    Args:
        source_text: Extracted lecture note text
        question_count: Number of questions to generate
        question_types: List of question types e.g. ['mcq', 'true_false']

    Returns:
        List of question dictionaries
    """
    if USE_REAL_API:
        return _generate_with_groq(source_text, question_count, question_types)
    else:
        return _generate_mock(question_count, question_types)


def _generate_with_groq(source_text: str, question_count: int, question_types: list) -> list:
    """Call the Groq API to generate questions using LLaMA 3."""
    client = Groq(api_key=os.getenv("API_KEY"))

    types_str = ", ".join(question_types)
    source_text = truncate_text(source_text)

    prompt = f"""You are a quiz generator. Given the lecture notes below, generate exactly {question_count} questions.

Return ONLY a valid JSON array. No explanation, no preamble, no markdown formatting, no code blocks.

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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a quiz generator. Always respond with valid JSON only. No markdown, no explanation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=4096
    )

    response_text = response.choices[0].message.content.strip()

    # Strip markdown code blocks if model adds them anyway
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]

    questions = json.loads(response_text)
    return questions


def _generate_mock(question_count: int, question_types: list) -> list:
    """
    Return realistic mock questions for development and testing.
    Simulates what the AI API would return.
    """
    mock_mcq = [
        {
            "type": "mcq",
            "question": "What is the primary role of an operating system?",
            "options": ["A. Manage hardware and software resources", "B. Browse the internet", "C. Write application code", "D. Store user files only"],
            "correct_answer": "A",
            "explanation": "An operating system manages hardware and software resources and provides common services for computer programs."
        },
        {
            "type": "mcq",
            "question": "Which component is considered the core of an operating system?",
            "options": ["A. Shell", "B. Compiler", "C. Kernel", "D. Bootloader"],
            "correct_answer": "C",
            "explanation": "The kernel is the core of the operating system and manages CPU, memory, and device drivers."
        },
        {
            "type": "mcq",
            "question": "What does CPU stand for?",
            "options": ["A. Central Processing Unit", "B. Computer Processing Utility", "C. Core Program Unit", "D. Central Program Utility"],
            "correct_answer": "A",
            "explanation": "CPU stands for Central Processing Unit, which is the primary component that executes instructions."
        },
        {
            "type": "mcq",
            "question": "Which of the following is a function of device drivers?",
            "options": ["A. Compile source code", "B. Allow the OS to communicate with hardware", "C. Manage user accounts", "D. Provide internet access"],
            "correct_answer": "B",
            "explanation": "Device drivers allow the operating system to communicate with hardware devices."
        },
        {
            "type": "mcq",
            "question": "What is memory management in an operating system?",
            "options": ["A. Managing disk space", "B. Controlling network traffic", "C. Allocating and deallocating RAM to processes", "D. Managing user passwords"],
            "correct_answer": "C",
            "explanation": "Memory management involves allocating and deallocating RAM to processes as needed."
        },
    ]

    mock_tf = [
        {
            "type": "true_false",
            "question": "The kernel is responsible for managing CPU and memory resources.",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "The kernel is the core of the OS and directly manages CPU, memory, and device drivers."
        },
        {
            "type": "true_false",
            "question": "An operating system is considered application software.",
            "options": ["True", "False"],
            "correct_answer": "False",
            "explanation": "An operating system is system software, not application software."
        },
        {
            "type": "true_false",
            "question": "Device drivers help the operating system communicate with hardware.",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "Device drivers act as translators between the OS and hardware devices."
        },
        {
            "type": "true_false",
            "question": "A computer can function normally without an operating system.",
            "options": ["True", "False"],
            "correct_answer": "False",
            "explanation": "Without an OS, a computer cannot manage its resources or run application programs."
        },
    ]

    mock_sa = [
        {
            "type": "short_answer",
            "question": "What is the kernel and what is its main function?",
            "options": None,
            "correct_answer": "The kernel is the core of the operating system. It manages CPU, memory, and device drivers.",
            "explanation": "The kernel is the most fundamental part of the OS, handling core system operations."
        },
        {
            "type": "short_answer",
            "question": "Name two resources managed by an operating system.",
            "options": None,
            "correct_answer": "CPU and memory (RAM)",
            "explanation": "Operating systems manage many resources including CPU time, memory, storage, and I/O devices."
        },
        {
            "type": "short_answer",
            "question": "What is the difference between system software and application software?",
            "options": None,
            "correct_answer": "System software manages hardware and provides a platform for applications. Application software performs specific tasks for users.",
            "explanation": "The OS is system software while programs like Word or Chrome are application software."
        },
    ]

    # Build question pool based on requested types
    pool = []
    if "mcq" in question_types:
        pool.extend(mock_mcq)
    if "true_false" in question_types:
        pool.extend(mock_tf)
    if "short_answer" in question_types:
        pool.extend(mock_sa)

    random.shuffle(pool)
    return pool[:question_count]