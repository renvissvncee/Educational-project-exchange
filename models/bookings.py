from .projects import Project
from .students import Student


class Booking:
    """Бронирование учебного проекта студентом."""

    def __init__(
        self,
        booking_id: int,
        project: Project,
        booking_date: str,
        student: Student,
    ) -> None:
        self.id = booking_id
        self.project = project
        self.booking_date = booking_date
        self.student = student
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменяет бронирование, не удаляя его из коллекции."""
        self.is_cancelled = True

    def __str__(self) -> str:
        status = "отменено" if self.is_cancelled else "активно"
        return (
            f"Бронирование проекта «{self.project.name}» "
            f"студентом {self.student.name} на {self.booking_date} "
            f"({status})"
        )
