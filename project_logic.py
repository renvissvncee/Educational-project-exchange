from datetime import date

from project_data import Project


def project_can_be_published(project: Project) -> bool:
    """Проверяет, готов ли проект для размещения на бирже."""
    participants = project.get("participants", 0)
    return (
        bool(project.get("ready"))
        and isinstance(participants, int)
        and participants > 0
    )


def get_available_projects(projects: list[Project]) -> list[Project]:
    """Возвращает готовые проекты, отсортированные по названию."""
    available = (
        project for project in projects if project_can_be_published(project)
    )
    return sorted(
        available,
        key=lambda project: str(project.get("name", "")),
    )


def find_projects(projects: list[Project], query: str) -> list[Project]:
    """Ищет проекты по части названия без учета регистра."""
    search_query = query.casefold()
    return [
        project
        for project in projects
        if search_query in str(project.get("name", "")).casefold()
    ]


def add_project(
    projects: list[Project],
    student: str,
    name: str,
    participants: int,
) -> Project:
    """Добавляет проект с новым числовым идентификатором."""
    project_ids = [
        project.get("id", 0)
        for project in projects
        if isinstance(project.get("id", 0), int)
    ]
    project_id = max(project_ids, default=0) + 1
    project = {
        "id": project_id,
        "student": student,
        "name": name,
        "participants": participants,
        "ready": True,
        "publication_date": date.today().isoformat(),
    }
    projects.append(project)
    return project


def delete_project(projects: list[Project], project_id: int) -> bool:
    """Удаляет проект по идентификатору и сообщает об успехе."""
    for project in projects:
        if project.get("id") == project_id:
            projects.remove(project)
            return True
    return False


def get_statistics(projects: list[Project]) -> dict[str, int]:
    """Возвращает общие сведения о доступности проектов."""
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
    publication_date = project.get(
        "publication_date",
        date.today().isoformat(),
    )
    print("Студент:", project.get("student", "Не указан"))
    print("Проект:", project.get("name", "Без названия"))
    print(
        "Количество участников:",
        project.get("participants", 0),
    )
    print("Дата:", publication_date)
