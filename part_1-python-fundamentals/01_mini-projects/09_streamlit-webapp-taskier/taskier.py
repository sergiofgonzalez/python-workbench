"""
Task Management application backend logic
"""
import csv
import re
import sqlite3
from enum import IntEnum, Enum
from pathlib import Path
from random import choice
from string import ascii_lowercase
from typing import Optional


class TaskierError(Exception):
    """Wraps Taskier app related errors"""


class TaskierDBOption(Enum):
    """Enumerates different available DB strategies"""

    DB_CSV = "tasks.csv"  # DB backed by a CSV
    DB_SQLITE = "tasks.sqlite"  # DB backed by SQLite


# Default value for DB strategy
APP_DB = TaskierDBOption.DB_CSV.value


class TaskStatus(IntEnum):
    """Enumerates the different status a Task can have"""

    CREATED = 0
    ONGOING = 1
    COMPLETED = 2

    @classmethod
    def formatted_options(cls):
        """Returns a prettified list of strings
        representing the different status a Task
        can have

        Returns:
            list[str]: the prettified list of strings
                representing the different statuses a Task
                can have.
        """
        return [x.name.title() for x in cls]


class Task:
    """Models the Task object"""

    conn: sqlite3.Connection
    """The shared connection to the SQLite database, shared across instances"""

    def __init__(
        self,
        task_id: str,
        title: str,
        desc: str,
        urgency: int,
        status=TaskStatus.CREATED,
        completion_note="",
    ):
        """Initialize the instance object of the Task class

        Args:
            task_id (str): The randomly generated string identifier.
            title (str): The title.
            desc (str): The description.
            urgency (int): The urgency level, 1 - 5.
            status (TaskStatus, optional): The status. Defaults to TaskStatus.CREATED.
            completion_note (str, optional): The note when a task is completed. Defaults to "".
        """
        self.task_id = task_id
        self.title = title
        self.desc = desc
        self.urgency = urgency
        self.status = TaskStatus(status)
        self.completion_note = completion_note

    def save_to_db(self):
        """Save the record to the database"""

        if APP_DB == TaskierDBOption.DB_CSV.value:
            with open(APP_DB, "a", newline="", encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                db_record = self._formatted_db_record()
                csv_writer.writerow(db_record)
        else:
            with self.conn as conn:
                cursor = conn.cursor()
                sql_stmt = "INSERT INTO task VALUES (?, ?, ?, ?, ?, ?);"
                cursor.execute(sql_stmt, self._formatted_db_record())

    def _formatted_db_record(self):
        db_record = (
            self.task_id,
            self.title,
            self.desc,
            self.urgency,
            self.status.value,
            self.completion_note,
        )
        return db_record

    def update_in_db(self):
        """Update the record in the database"""

        if APP_DB == TaskierDBOption.DB_CSV.value:
            updated_record = f"{','.join(map(str, self._formatted_db_record()))}\n"
            with open(APP_DB, "r+", encoding="utf-8") as file:
                saved_records = file.read()
                pattern = re.compile(rf"{self.task_id}.+?\n")
                if re.search(pattern, saved_records):
                    updated_records = re.sub(pattern, updated_record, saved_records)
                    file.seek(0)  # move the file cursor to the beginning of the stream
                    file.truncate()  # remove all data
                    file.write(updated_records)  # rewrite records
                else:
                    raise TaskierError("The task appears to be removed already")
        else:
            with self.conn as conn:
                cursor = conn.cursor()
                count_sql = f"SELECT COUNT(*) FROM task WHERE task_id = {self.task_id!r}"
                row_count = cursor.execute(count_sql).fetchone()[0]
                if row_count > 0:
                    sql_stmt = f"""
                        UPDATE task
                           SET task_id = ?,
                               title = ?,
                               desc = ?,
                               urgency = ?,
                               status = ?,
                               completion_note = ?
                         WHERE task_id = {self.task_id!r}
                    """
                    cursor.execute(sql_stmt, self._formatted_db_record())
                else:
                    raise TaskierError("The task appears to be removed already")

    def delete_from_db(self):
        """Delete the record from the database"""

        if APP_DB == TaskierDBOption.DB_CSV.value:
            with open(APP_DB, "r+", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(self.task_id):
                        lines.remove(line)
                        break
                file.seek(0)
                file.truncate()
                file.writelines(lines)
        else:
            with self.conn as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM task WHERE task_id = {self.task_id!r}")

    def __str__(self) -> str:
        stars = "\u2605" * self.urgency
        return f"{self.title} ({self.desc}) {stars}"

    def __repr__(self) -> str:
        # pylint: disable=C0301:line-too-long
        return f"{self.__class__.__name__}({self.task_id!r}, {self.title!r}, {self.desc!r}, {self.urgency}, {self.status}, {self.completion_note!r})"

    @classmethod
    def task_from_form_entry(cls, title: str, desc: str, urgency: int):
        """Create a task from the form's entry

        Args:
            title (str): The task's title
            desc (str): The task's description
            urgency (int): The task's urgency level (1-5)

        Returns:
            Task: an instance of the Task class
        """
        task_id = cls.random_string()
        task = cls(task_id, title, desc, urgency)
        return task

    @classmethod
    def load_seed_data(cls):
        """Load seeding data for the web app"""

        task0 = cls.task_from_form_entry("Laundry", "Wash clothes", 3)
        task1 = cls.task_from_form_entry("Homework", "Math and Physics", 5)
        task2 = cls.task_from_form_entry("Museum", "Egypt things", 4)
        for task in [task0, task1, task2]:
            task.save_to_db()

    @classmethod
    def create_sqlite_database(cls):
        """Create the SQLite database"""

        with sqlite3.connect(TaskierDBOption.DB_SQLITE.value) as conn:
            cls.conn = conn
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE task (
                    task_id text,
                    title text,
                    desc text,
                    urgency integer,
                    status integer,
                    completion_note text);
            """
            )

    @classmethod
    def load_tasks(
        cls,
        statuses: Optional[list[TaskStatus]] = None,
        urgencies: Optional[list[int]] = None,
        content: str = "",
    ):
        """Load tasks matching specific criteria

        Args:
            statuses (list[TaskStatus], optional): Filter tasks with the specified statuses.
                Defaults to None, meaning no requirements on statuses-.
            urgencies (list[int], optional): Filter tasks with the specified urgencies.
                Defaults to None, meaning no requirements on urgencies.
            content (str, optional): Filter tasks with the specified content (title, desc, or note).
                Defaults to "".

        Returns:
            list[Task]: the list of tasks that match the criteria
        """
        tasks = list()
        if APP_DB == TaskierDBOption.DB_CSV.value:
            with open(APP_DB, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    task_id, title, desc, urgency_str, status_str, note = row
                    urgency = int(urgency_str)
                    status = TaskStatus(int(status_str))
                    if statuses and (status not in statuses):
                        continue
                    if urgencies and (urgency not in urgencies):
                        continue
                    if content and all(
                        [
                            note.find(content) < 0,
                            desc.find(content) < 0,
                            title.find(content) < 0,
                        ]
                    ):
                        continue
                    task = cls(task_id, title, desc, urgency, status, note)
                    tasks.append(task)
        else:
            with cls.conn as conn:
                if statuses is None:
                    statuses_sql = tuple(map(int, TaskStatus))
                else:
                    statuses_sql = tuple(statuses) * 2  # trick: duplicate to be able to use IN
                if urgencies is None:
                    urgencies_sql = tuple(range(1, 6))
                else:
                    urgencies_sql = tuple(urgencies) * 2  # trick: duplicate to be able to use IN
                sql_stmt = f"""
                    SELECT *
                      FROM task
                     WHERE status in {statuses_sql}
                       AND urgency in {urgencies_sql}
                """
                if content:
                    # pylint: disable=C0301:line-too-long
                    sql_stmt += f"and ((completion_note LIKE '%{content}%') OR (desc LIKE '%{content}%') OR (title LIKE '%{content}%'))"
                cursor = conn.cursor()
                cursor.execute(sql_stmt)
                tasks_tuples = cursor.fetchall()
                tasks = [Task(*x) for x in tasks_tuples]
        return tasks

    @staticmethod
    def random_string(length=8):
        """Create a random ASCII string using the specified length

        Args:
            length (int, optional): The desired lenth
        """
        return "".join(choice(ascii_lowercase) for _ in range(length))


def set_db_option(option):
    """Sets the DB strategy to use in the database."""
    # pylint: disable=W0603:global-statement
    global APP_DB
    APP_DB = option
    db_path = Path(option)
    if not db_path.exists():
        if APP_DB == TaskierDBOption.DB_SQLITE.value:
            Task.create_sqlite_database()
        Task.load_seed_data()
    elif APP_DB == TaskierDBOption.DB_SQLITE.value:
        Task.conn = sqlite3.connect(APP_DB)
