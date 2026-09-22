from models import Project, Student
from project_data import load_projects, save_projects
from project_logic import (
    add_project,
    delete_project,
    find_projects,
    get_available_projects,
    get_statistics,
    project_can_be_published,
)


def test_ready_project_can_be_published() -> None:
    project = Project(participants=2, ready=True)
    assert project_can_be_published(project) is True


def test_project_without_participants_cannot_be_published() -> None:
    project = Project(participants=0, ready=True)
    assert project_can_be_published(project) is False


def test_available_projects_are_sorted() -> None:
    projects = [
        Project(name="Б", ready=True, participants=1),
        Project(name="А", ready=True, participants=1),
    ]
    available_names = [
        project.name for project in get_available_projects(projects)
    ]
    assert available_names == ["А", "Б"]


def test_projects_are_saved_and_loaded(tmp_path) -> None:
    file_path = tmp_path / "projects.json"
    projects = [
        Project(
            student=Student(name="Анна"),
            name="Тест",
            ready=True,
            participants=1,
        )
    ]
    save_projects(file_path, projects)
    loaded_projects = load_projects(file_path)
    assert isinstance(loaded_projects[0], Project)
    assert loaded_projects[0].name == "Тест"
    assert isinstance(loaded_projects[0].student, Student)
    assert loaded_projects[0].student.name == "Анна"


def test_invalid_json_returns_empty_list(tmp_path) -> None:
    file_path = tmp_path / "projects.json"
    file_path.write_text("{bad json", encoding="utf-8")
    assert load_projects(file_path) == []


def test_project_can_be_found_by_name() -> None:
    project = Project(project_id=1, name="Python проект")
    assert find_projects([project], "python") == [project]


def test_project_can_be_added() -> None:
    projects = [Project(project_id=1, name="Старый проект")]
    project = add_project(
        projects,
        Student(name="Анна"),
        "Новый проект",
        2,
    )
    assert project.id == 2
    assert isinstance(projects[1], Project)
    assert len(projects) == 2


def test_project_can_be_deleted_by_id() -> None:
    projects = [Project(project_id=1, name="Проект")]
    assert delete_project(projects, 1) is True
    assert projects == []


def test_project_statistics_are_calculated() -> None:
    projects = [
        Project(ready=True, participants=1),
        Project(ready=False, participants=1),
    ]
    assert get_statistics(projects) == {
        "total": 2,
        "available": 1,
        "unavailable": 1,
    }


def test_project_has_object_api() -> None:
    project = Project(
        1,
        Student(name="Анна"),
        "Биржа",
        2,
        True,
        "2026-09-22",
    )
    assert str(project) == "Биржа (Анна)"
    assert project.can_be_published() is True


def test_student_has_object_api() -> None:
    student = Student(1, "Анна")
    assert student.id == 1
    assert student.name == "Анна"
    assert str(student) == "Анна"


def test_project_can_be_created_from_data() -> None:
    project = Project.from_data(
        {"id": 1, "name": "Биржа", "participants": 2, "ready": True}
    )
    assert project.id == 1
    assert project.name == "Биржа"
    assert isinstance(project.student, Student)
    assert project.student.name == ""
