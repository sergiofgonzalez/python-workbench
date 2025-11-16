"""Illustrate the use of else in while loops."""
from typing import NamedTuple


class Task(NamedTuple):
    """A task with a title, description, and urgency level."""

    title: str
    desc: str
    urgency: int


tasks = [
    Task("Toaster", "Clean the toaster", 2),
    Task("Camera", "Export photos", 4),
    Task("Homework", "Physics and math", 5),
    Task("Floor", "Mop the floor", 3),
    Task("Internet", "Upgrade plan", 5),
    Task("Laundry", "Wash clothes", 3),
    Task("Museum", "Egypt exhibit", 4),
    Task("Utility", "Pay bills", 5),
]

def complete_tasks_with_break(resting_threshold: int) -> None:
    """Complete tasks until resting threshold is reached."""
    while len(tasks) > 0:
        task_to_complete = tasks.pop()
        resting_threshold -= task_to_complete.urgency
        print(f"Completed: {task_to_complete}")
        if resting_threshold < 0:
            print("Coffee break now!")
            break
    else:
        print("Party! Completed all the tasks!")

def main() -> None:
    """Application entry point."""
    complete_tasks_with_break(7)
    print("===")
    complete_tasks_with_break(25)



if __name__ == "__main__":
    main()
