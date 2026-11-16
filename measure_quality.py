"""Measure three local operations of the task manager prototype."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from statistics import median
from time import perf_counter

from src.task_manager import Task, TaskManager


def measure(size: int, repeats: int = 10) -> dict[str, float | int]:
    create_times = []
    list_times = []
    overdue_times = []
    today = date(2026, 11, 16)

    for _ in range(repeats):
        manager = TaskManager()
        start = perf_counter()
        for task_id in range(size):
            manager.create(
                Task(task_id, f"Task {task_id}", today + timedelta(days=task_id % 30))
            )
        create_times.append(perf_counter() - start)

        start = perf_counter()
        manager.list_tasks()
        list_times.append(perf_counter() - start)

        start = perf_counter()
        manager.overdue(today)
        overdue_times.append(perf_counter() - start)

    return {
        "tasks": size,
        "repeats": repeats,
        "create_all_median_ms": round(median(create_times) * 1000, 3),
        "list_median_ms": round(median(list_times) * 1000, 3),
        "overdue_median_ms": round(median(overdue_times) * 1000, 3),
    }


def main() -> None:
    result = {
        "python": "3.12.14",
        "method": "median of 10 local repetitions; in-memory operations",
        "measurements": [measure(size) for size in (100, 1000, 10000)],
    }
    output = Path(__file__).with_name("quality_metrics.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
