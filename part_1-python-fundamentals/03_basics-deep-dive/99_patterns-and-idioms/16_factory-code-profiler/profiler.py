"""A simple code profiler."""

import os
import time
from abc import ABC, abstractmethod


class Profiler(ABC):
    """Abstract class that sets the profiler interface."""

    def __init__(self, label: str) -> None:
        """Initialize a Profiler instance."""
        self.label = label

    @abstractmethod
    def start(self) -> None:
        """Initiate a code profiling session."""

    @abstractmethod
    def end(self) -> None:
        """End a code profiling session."""


class _Profiler:
    """Simple code profiler implementation."""

    def __init__(self, label: str) -> None:
        """Instance initializer."""
        self.label = label
        self.last_time = None

    def start(self) -> None:
        """Initiate a code profiling session."""
        self.last_time = time.perf_counter()

    def end(self) -> None:
        """End the code profiling session by logging the execution time."""
        diff = time.perf_counter() - self.last_time
        print(f"Timer {self.label!r} took {diff:.6f} seconds")  # noqa: T201


class _NoOpProfiler:
    """NoOp Profiler implementation using duck-typing (i.e., no class hierarchy)."""

    def start(self) -> None:
        """Do nothing."""

    def end(self) -> None:
        """Do nothing."""


def create_profiler(label: str) -> Profiler:
    """Return a properly configured profiler for the environment (Factory)."""
    if os.getenv("PY_ENV") == "production":
        return _NoOpProfiler()
    return _Profiler(label)
