import json
from pathlib import Path

Project = dict[str, object]
DATA_FILE = Path(__file__).parent / "data" / "projects.json"


def load_projects(file_path: Path) -> list[Project]:
    """Загружает список проектов из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        return []
    return data


def save_projects(file_path: Path, projects: list[Project]) -> None:
    """Сохраняет список проектов в JSON-файл."""
    file_path.parent.mkdir(exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(projects, file, ensure_ascii=False, indent=2)
