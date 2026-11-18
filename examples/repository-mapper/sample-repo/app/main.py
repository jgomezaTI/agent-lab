from app.grades import get_grades


def get_course_notes(course_id: str):
    return get_grades(course_id)
