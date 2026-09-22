from .students import Student


class Team:
    """Команда студентов, подающая заявку на учебный проект."""

    def __init__(
        self,
        team_id: int,
        name: str,
        members: list[Student] | None = None,
    ) -> None:
        self.id = team_id
        self.name = name
        self.members = members or []

    def add_member(self, student: Student) -> None:
        """Добавляет студента в команду."""
        self.members.append(student)

    def __str__(self) -> str:
        return self.name
