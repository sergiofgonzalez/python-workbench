"""Illustrate the gotchas when using default arguments with mutable types."""


class Task:
    """A simple Task class that takes title, description, and urgency level."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize a task with title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency
        self.status = "pending"

    def __repr__(self) -> str:
        """Return a string representation of the task."""
        return (
            f"Task(title={self.title!r}, "
            f"description={self.description!r}, "
            f"urgency={self.urgency}, "
            f"status={self.status!r})"
        )


def complete_task(task: Task, *, group: list[str] = []) -> list[str]:  # noqa: B006
    """Mark the task as complete and add it to a group."""
    task.status = "completed"
    group.append(task.title)  # Add the task title to the group
    print(f"Task completed: {task}")
    print(f"Current group: {group}")
    print(f"Group memory address: 0x{id(group):x}")
    return group


def complete_task_v2(task: Task, *, group: list[str] | None = None) -> list[str]:
    """Mark the task as complete and add it to a group."""
    task.status = "completed"
    if group is None:
        group = []
    group.append(task.title)  # Add the task title to the group
    print(f"Task completed: {task}")
    print(f"Current group: {group}")
    print(f"Group memory address: 0x{id(group):x}")
    return group


def main() -> None:
    """Application entry point."""
    homework_task = Task(
        title="Math Homework",
        description="Complete exercises 1-10 from chapter 5",
        urgency=2,
    )
    print(f"Homework Task: {homework_task}")

    play_videogames_task = Task(
        title="Play Videogames",
        description="Finish the latest level in the game",
        urgency=1,
    )
    print(f"Play Videogames Task: {play_videogames_task}")

    watch_movie_task = Task(
        title="Watch Movie",
        description="Watch the latest blockbuster movie",
        urgency=3,
    )
    print(f"Watch Movie Task: {watch_movie_task}")

    boring_tasks = []
    complete_task(homework_task, group=boring_tasks)
    print(f"Boring tasks after completing homework: {boring_tasks}")

    # See how mutable default arguments can lead to unexpected behavior
    fun_tasks = complete_task(play_videogames_task)
    print(f"Fun tasks after completing videogames: {fun_tasks}")
    print(f"Group memory address: 0x{id(fun_tasks):x}")

    # The same group is used for the next task, leading to unexpected results
    other_tasks = complete_task(watch_movie_task)
    print(f"Fun tasks after completing movie: {fun_tasks}")
    print(f"Other tasks after completing movie: {other_tasks}")
    print(f"Fun tasks Group memory address: 0x{id(fun_tasks):x}")
    print(f"Other tasks Group memory address: 0x{id(other_tasks):x}")

    # We can fix it by using a new list for each call
    print("\nUsing complete_task_v2 to avoid mutable default argument issues:")
    fun_tasks_v2 = complete_task_v2(play_videogames_task)
    print(f"Fun tasks after completing videogames (v2): {fun_tasks_v2}")
    print(f"Group memory address (v2): 0x{id(fun_tasks_v2):x}")
    other_tasks_v2 = complete_task_v2(watch_movie_task)
    print(f"Other tasks after completing movie (v2): {other_tasks_v2}")
    print(f"Fun tasks Group memory address (v2): 0x{id(fun_tasks_v2):x}")
    print(f"Other tasks Group memory address (v2): 0x{id(other_tasks_v2):x}")


if __name__ == "__main__":
    main()
