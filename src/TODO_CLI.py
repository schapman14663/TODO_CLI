import argparse
import json

TODO_FILE = "TODO.json"


def main():
    """main function task tracker cli"""
    parser = argparse.ArgumentParser()

    sub_parsers = parser.add_subparsers(dest="command")

    # Add Task Command
    add_parser = sub_parsers.add_parser("add", help="Add a new task to the TODO list")
    add_parser.add_argument("task", metavar="task")
    add_parser.add_argument(
        "-p",
        "--priority",
        default="medium",
        choices=["low", "medium", "high"],
        help="Indicate how important the task is",
    )
    add_parser.add_argument(
        "-c",
        "--completion",
        default="not started",
        choices=["not started", "in progress", "done"],
        help="indicate current state of the TODO item",
    )

    # View Task Command
    view_parser = sub_parsers.add_parser("view", help="View the TODO list")

    args = parser.parse_args()
    print(args)

    if args.command == "add":
        add_task(args)
    elif args.command == "view":
        view_tasks()


def add_task(args):
    tasks = read_tasks()

    task = args.task
    task_id = len(tasks) + 1
    priority = args.priority
    completion = args.completion

    new_task = {
        "id": task_id,
        "task": task,
        "priority": priority,
        "completion": completion,
    }

    tasks.append(new_task)
    save_task(tasks)

    print(f"Added {task} to TODO list.")


def save_task(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file)


def read_tasks():
    try:
        with open(TODO_FILE, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks


def view_tasks():
    tasks = read_tasks()
    print("TODO List:")
    for task in tasks:
        print(f"Task {task['id']} : {task['task']}")


if __name__ == "__main__":
    main()
