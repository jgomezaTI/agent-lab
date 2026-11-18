from __future__ import annotations


class SyntheticCustomerData:
    """Read-only fixture standing in for a customer-approved API or database view."""

    def __init__(self) -> None:
        self._grades: dict[tuple[str, str], list[dict[str, object]]] = {}

    def set_grades(self, customer_id: str, course_id: str, grades: list[dict[str, object]]) -> None:
        self._grades[(customer_id, course_id)] = list(grades)

    def get_course_grades(self, customer_id: str, course_id: str) -> dict[str, object]:
        return {"customer_id": customer_id, "course_id": course_id, "grades": list(self._grades.get((customer_id, course_id), []))}
