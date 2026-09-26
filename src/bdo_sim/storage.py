"""Transactional lifetime statistics, outside the executable/resources."""

import json
import sqlite3
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

from .engine import Report


class History:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        with self.connect() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, created TEXT DEFAULT CURRENT_TIMESTAMP, payload TEXT NOT NULL)"
            )

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path)
        try:
            with db:
                yield db
        finally:
            db.close()

    def save(self, report: Report):
        payload = dict(
            seed=report.seed,
            basket=report.basket,
            inventory=dict(report.inventory),
            opened=dict(report.opened),
            status=report.status,
            pending=report.pending,
        )
        with self.connect() as db:
            db.execute("INSERT INTO runs(payload) VALUES (?)", (json.dumps(payload, ensure_ascii=False),))

    def totals(self):
        inventory, opened = Counter(), Counter()
        count = 0
        with self.connect() as db:
            for (payload,) in db.execute("SELECT payload FROM runs"):
                row = json.loads(payload)
                inventory.update(row["inventory"])
                opened.update(row["opened"])
                count += 1
        return count, inventory, opened
