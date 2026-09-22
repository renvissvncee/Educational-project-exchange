class Student:
    """Студент, которому принадлежит учебный проект."""

    def __init__(self, student_id: int = 0, name: str = "") -> None:
        self.id = student_id
        self.name = name

    def __str__(self) -> str:
        return self.name or "Не указан"
