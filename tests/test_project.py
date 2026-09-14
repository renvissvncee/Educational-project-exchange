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
    project = {"ready": True, "participants": 2}
    assert project_can_be_published(project) is True


def test_project_without_participants_cannot_be_published() -> None:
    project = {"ready": True, "participants": 0}
    assert project_can_be_published(project) is False


def test_available_projects_are_sorted() -> None:
    projects = [
        {"name": "Б", "ready": True, "participants": 1},
        {"name": "А", "ready": True, "participants": 1},
    ]
    available_names = [
        project["name"] for project in get_available_projects(projects)
    ]
    assert available_names == ["А", "Б"]


def test_projects_are_saved_and_loaded(tmp_path) -> None:
    file_path = tmp_path / "projects.json"
    projects = [{"name": "Тест", "ready": True, "participants": 1}]
    save_projects(file_path, projects)
    assert load_projects(file_path) == projects


def test_invalid_json_returns_empty_list(tmp_path) -> None:
    file_path = tmp_path / "projects.json"
    file_path.write_text("{bad json", encoding="utf-8")
    assert load_projects(file_path) == []


def test_project_can_be_found_by_name() -> None:
    projects = [{"id": 1, "name": "Python проект"}]
    assert find_projects(projects, "python") == projects


def test_project_can_be_added() -> None:
    projects = [{"id": 1, "name": "Старый проект"}]
    project = add_project(projects, "Анна", "Новый проект", 2)
    assert project["id"] == 2
    assert len(projects) == 2


def test_project_can_be_deleted_by_id() -> None:
    projects = [{"id": 1, "name": "Проект"}]
    assert delete_project(projects, 1) is True
    assert projects == []


def test_project_statistics_are_calculated() -> None:
    projects = [
        {"ready": True, "participants": 1},
        {"ready": False, "participants": 1},
    ]
    assert get_statistics(projects) == {
        "total": 2,
        "available": 1,
        "unavailable": 1,
    }
