from models import Project, Student
from project_data import DATA_FILE, load_projects, save_projects
from project_logic import (
    add_project,
    delete_project,
    find_projects,
    get_available_projects,
    get_statistics,
    print_project,
    project_can_be_published,
)


def show_projects(projects: list[Project]) -> None:
    """Показывает проекты, которые можно разместить на бирже."""
    available_projects = get_available_projects(projects)
    if not available_projects:
        print("Доступных проектов нет")
        return

    for project in available_projects:
        print_project(project)


def show_all_projects(projects: list[Project]) -> None:
    """Показывает все проекты из коллекции."""
    if not projects:
        print("Проектов нет")
        return
    for project in projects:
        print("ID:", project.id)
        print_project(project)


def add_project_from_input(projects: list[Project]) -> None:
    """Получает данные из меню и добавляет новый проект."""
    try:
        student_name = input("Студент: ").strip()
        name = input("Название проекта: ").strip()
        participants = int(input("Количество участников: "))
        if not student_name or not name or participants < 0:
            raise ValueError
    except (ValueError, EOFError):
        print("Ошибка: проверьте введенные данные")
        return

    student = Student(name=student_name)
    project = add_project(projects, student, name, participants)
    save_projects(DATA_FILE, projects)
    print("Проект добавлен, ID:", project.id)


def find_projects_from_input(projects: list[Project]) -> None:
    """Ищет и показывает проекты по введенному названию."""
    try:
        query = input("Введите название для поиска: ").strip()
    except EOFError:
        print()
        return

    matches = find_projects(projects, query)
    if not matches:
        print("Проекты не найдены")
        return
    for project in matches:
        print("ID:", project.id)
        print_project(project)


def delete_project_from_input(projects: list[Project]) -> None:
    """Удаляет проект по ID, введенному пользователем."""
    try:
        project_id = int(input("Введите ID проекта: "))
    except (ValueError, EOFError):
        print("Ошибка: ID должен быть целым числом")
        return

    if delete_project(projects, project_id):
        save_projects(DATA_FILE, projects)
        print("Проект удален")
    else:
        print("Проект с таким ID не найден")


def show_statistics(projects: list[Project]) -> None:
    """Показывает статистику по проектам."""
    statistics = get_statistics(projects)
    print("Всего проектов:", statistics["total"])
    print("Доступных для публикации:", statistics["available"])
    print("Недоступных для публикации:", statistics["unavailable"])


def run_menu(projects: list[Project]) -> None:
    """Запускает простое меню работы с учебными проектами."""
    while True:
        print("\n1 - Показать проекты")
        print("2 - Найти проект")
        print("3 - Добавить проект")
        print("4 - Удалить проект")
        print("5 - Показать статистику")
        print("6 - Сохранить данные")
        print("0 - Выйти")
        try:
            command = input("Выберите действие: ")
        except EOFError:
            print()
            return

        if command == "1":
            show_all_projects(projects)
        elif command == "2":
            find_projects_from_input(projects)
        elif command == "3":
            add_project_from_input(projects)
        elif command == "4":
            delete_project_from_input(projects)
        elif command == "5":
            show_statistics(projects)
        elif command == "6":
            save_projects(DATA_FILE, projects)
            print("Данные сохранены")
        elif command == "0":
            return
        else:
            print("Ошибка: выберите 0, 1 или 2")


def main() -> None:
    """Загружает данные и запускает основной сценарий программы."""
    projects = load_projects(DATA_FILE)
    show_projects(projects)
    if projects and project_can_be_published(projects[0]):
        print("Проект можно разместить на бирже")
    run_menu(projects)


if __name__ == "__main__":
    main()
