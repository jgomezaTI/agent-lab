from app.grades import get_grades


def test_empty_fixture():
    assert get_grades("course-1")["grades"] == []
