SAMPLE_TEXT = (
    "The operating system manages computer hardware and software resources. "
    "The kernel is the core of the OS. It manages CPU, memory, and device drivers."
)


def test_generate_quiz(client, auth_headers):
    res = client.post("/api/quiz/generate", headers=auth_headers, json={
        "title": "OS Quiz",
        "source_text": SAMPLE_TEXT,
        "question_types": ["mcq", "true_false"],
        "question_count": 3
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "quiz_id" in data
    assert "questions" in data
    assert len(data["questions"]) > 0


def test_get_all_quizzes(client, auth_headers):
    res = client.get("/api/quiz/", headers=auth_headers)
    assert res.status_code == 200
    assert "quizzes" in res.get_json()
    assert isinstance(res.get_json()["quizzes"], list)


def test_get_quiz_by_id(client, auth_headers):
    gen = client.post("/api/quiz/generate", headers=auth_headers, json={
        "title": "Test Quiz",
        "source_text": SAMPLE_TEXT,
        "question_types": ["mcq"],
        "question_count": 2
    })
    assert gen.status_code == 201
    quiz_id = gen.get_json()["quiz_id"]

    res = client.get(f"/api/quiz/{quiz_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["id"] == quiz_id


def test_delete_quiz(client, auth_headers):
    gen = client.post("/api/quiz/generate", headers=auth_headers, json={
        "title": "Delete Me",
        "source_text": SAMPLE_TEXT,
        "question_types": ["true_false"],
        "question_count": 2
    })
    assert gen.status_code == 201
    quiz_id = gen.get_json()["quiz_id"]

    res = client.delete(f"/api/quiz/{quiz_id}", headers=auth_headers)
    assert res.status_code == 200