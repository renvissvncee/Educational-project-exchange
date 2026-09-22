from datetime import date

from .students import Student


class Project:
    """Учебный проект, размещаемый на бирже."""

    def __init__(
        self,
        project_id: int = 0,
        student: Student | None = None,
        name: str = "",
        participants: int = 0,
        ready: bool = False,
        publication_date: str = "",
    ) -> None:
        self.id = project_id
        self.student = student or Student()
        self.name = name
        self.participants = participants
        self.ready = ready
        self.publication_date = publication_date

    def __str__(self) -> str:
        return f"{self.name} ({self.student.name})"

    def can_be_published(self) -> bool:
        """Проверяет, готов ли проект для размещения на бирже."""
        return self.ready and self.participants > 0

    @classmethod
    def from_data(cls, data: dict[str, object]) -> "Project":
        """Создаёт проект из словаря."""
        project_id = data.get("id", 0)
        participants = data.get("participants", 0)
        student_data = data.get("student", "")
        if isinstance(student_data, dict):
            student_id = student_data.get("id", 0)
            student_name = student_data.get("name", "")
            student = Student(
                student_id=student_id if isinstance(student_id, int) else 0,
                name=str(student_name),
            )
        else:
            student = Student(name=str(student_data))

        return cls(
            project_id=project_id if isinstance(project_id, int) else 0,
            student=student,
            name=str(data.get("name", "")),
            participants=(
                participants if isinstance(participants, int) else 0
            ),
            ready=bool(data.get("ready", False)),
            publication_date=str(data.get("publication_date", "")),
        )

    def to_data(self) -> dict[str, object]:
        """Преобразует проект в словарь для JSON."""
        return {
            "id": self.id,
            "student": self.student.name,
            "name": self.name,
            "participants": self.participants,
            "ready": self.ready,
            "publication_date": self.publication_date,
        }


def project_can_be_published(project: Project) -> bool:
    """Проверяет готовность одного проекта."""
    return project.can_be_published()


def get_available_projects(projects: list[Project]) -> list[Project]:
    """Возвращает готовые проекты, отсортированные по названию."""
    return sorted(
        (project for project in projects if project_can_be_published(project)),
        key=lambda project: project.name,
    )


def find_projects(projects: list[Project], query: str) -> list[Project]:
    """Ищет проекты по части названия без учета регистра."""
    search_query = query.casefold()
    return [
        project
        for project in projects
        if search_query in project.name.casefold()
    ]


def add_project(
    projects: list[Project],
    student: Student,
    name: str,
    participants: int,
) -> Project:
    """Создаёт и добавляет проект с новым числовым идентификатором."""
    project_id = max((project.id for project in projects), default=0) + 1
    project = Project(
        project_id=project_id,
        student=student,
        name=name,
        participants=participants,
        ready=True,
        publication_date=date.today().isoformat(),
    )
    projects.append(project)
    return project


def delete_project(projects: list[Project], project_id: int) -> bool:
    """Удаляет проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            projects.remove(project)
            return True
    return False


def get_statistics(projects: list[Project]) -> dict[str, int]:
    """Возвращает статистику доступности проектов."""
    available_count = sum(
        project_can_be_published(project) for project in projects
    )
    return {
        "total": len(projects),
        "available": available_count,
        "unavailable": len(projects) - available_count,
    }


def print_project(project: Project) -> None:
    """Печатает основные сведения об учебном проекте."""
    publication_date = project.publication_date or date.today().isoformat()
    print("Студент:", project.student)
    print("Проект:", project.name or "Без названия")
    print("Количество участников:", project.participants)
    print("Дата:", publication_date)
