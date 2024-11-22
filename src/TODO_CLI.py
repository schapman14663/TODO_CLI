import argparse
import json
from datetime import datetime

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
    add_parser.add_argument(
        "-d", "--due-date", default="N/A", help="set date the TODO list item is due"
    )

    # View Task Command
    view_parser = sub_parsers.add_parser("view", help="View the TODO list")
    view_parser.add_argument(
        "-s",
        "--sort",
        nargs="*",
        help="select sort mode for TODO list",
    )

    # Edit Task Commands
    edit_parser = sub_parsers.add_parser("edit", help="edit task in TODO list")
    edit_parser.add_argument("task_id", type=int, help="id of task to edit")
    edit_parser.add_argument(
        "-p",
        "--priority",
        choices=["low", "medium", "high"],
        help="the updated priority of the TODO item",
    )
    edit_parser.add_argument(
        "-c",
        "--completion",
        choices=["not started", "in progress", "done"],
        help="the updated completion status of the TODO item",
    )

    # Delete Task Command
    delete_parser = sub_parsers.add_parser("delete", help="delete task from TODO list")
    delete_parser.add_argument("task_id", type=int, help="id of task to be deleted")

    args = parser.parse_args()
    print(args)

    if args.command == "add":
        add_task(args)
    if args.command == "view":
        view_tasks(args)
    if args.command == "edit":
        edit_task(args)
    if args.command == "delete":
        delete_task(args)


def add_task(args):
    tasks = read_tasks()

    task = args.task
    task_id = len(tasks) + 1
    priority = args.priority
    completion = args.completion
    due_date = args.due_date

    new_task = {
        "id": task_id,
        "task": task,
        "priority": priority,
        "completion": completion,
        "due_date": due_date,
    }

    tasks.append(new_task)
    save_task(tasks)

    print(f"Added {task} to TODO list.")


def save_task(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file)


def edit_task(args):
    update_task_priority(args)
    update_task_completion(args)


def delete_task(args):
    tasks = read_tasks()
    task_id = args.task_id

    for task in tasks:
        if task_id == task["id"]:
            tasks.remove(task)
            save_task(tasks)
            print(f"TASK {task_id} DELETED")
            return
    print(f"{task_id} NOT FOUND")


def read_tasks():
    try:
        with open(TODO_FILE, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks


def view_tasks(args):

    if args.sort:
        tasks = sort_tasks(args)
    else:
        tasks = read_tasks()

    print("| task id | priority | completion status | due date | task")
    for task in tasks:
        print(
            f"| {task['id']} | {task['priority']} | {task['completion']} | {task['due_date']} | {task['task']} "
        )


def update_task_priority(args):
    print(args)
    tasks = read_tasks()
    task_id = args.task_id
    new_priority = args.priority

    for task in tasks:
        if task_id == task["id"]:
            task["priority"] = new_priority
            save_task(tasks)
            print(f"task priority changed to {new_priority}")
            return
    print(f"task {task_id} not found")


def update_task_completion(args):
    print(args)
    tasks = read_tasks()
    task_id = args.task_id
    new_completion = args.completion

    for task in tasks:
        if task_id == task["id"]:
            task["completion"] = new_completion
            save_task(tasks)
            print(f"task priority changed to {new_completion}")
            return
    print(f"task {task_id} not found")


def sort_tasks(args):
    tasks = read_tasks()
    sort_case = args.sort

    print(sort_case)

    for i in range(0, len(sort_case))[::-1]:
        tasks.sort(key=lambda task: (task[sort_case[i]]))
    return tasks


if __name__ == "__main__":
    main()
