from .projects import Project
from .teams import Team


class Request:
    """Заявка команды на учебный проект."""

    def __init__(
        self,
        request_id: int,
        project: Project,
        request_date: str,
        team: Team,
    ) -> None:
        self.id = request_id
        self.project = project
        self.request_date = request_date
        self.team = team
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменяет заявку, не удаляя ее из коллекции."""
        self.is_cancelled = True

    def __str__(self) -> str:
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"Заявка команды «{self.team.name}» на проект "
            f"«{self.project.name}» от {self.request_date} ({status})"
        )
