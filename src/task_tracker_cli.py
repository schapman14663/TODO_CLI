import argparse


def main():
    """main function task tracker cli"""
    print("Hello World")

    tasks = []
    parser = argparse.ArgumentParser(prog="task_tracker")
    parser.add_argument("task", nargs="+")
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
