"""
Helper elements for Taskier app script.
"""
from enum import Enum


class TaskierMenuOption(Enum):
    """Lists the different menu options corresponding to the three
    pages managed by the application.
    """
    SHOW_TASKS = "Show Tasks"
    NEW_TASK = "New Task"
    SHOW_TASK_DETAIL = "Show Task Detail"


class TaskierFilterKey(Enum):
    """Enumerates the different keys used to control the sorting and
    filter options
    """
    SORTING_KEY = "sorting_key"
    SORTING_ORDER = "sorting_order"
    SELECTED_STATUSES = "selected_statuses"
    SELECTED_URGENCIES = "selected_urgencies"
    SELECTED_CONTENT = "selected_content"
