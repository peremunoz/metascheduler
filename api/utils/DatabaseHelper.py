from pathlib import Path
from typing import List
from interfaces.Job import Job
from interfaces.Scheduler import Scheduler
from utils.Singleton import Singleton
import sqlite3

DEFAULT_DATABASE_FILE = Path("./db/db.sqlite3")


class DatabaseHelper(metaclass=Singleton):

    def __init__(self, schedulers: List[Scheduler], database_file: Path = None) -> None:
        if not schedulers:
            raise Exception(
                "At least one scheduler must be provided in database initialization")
        self._db_file = database_file or DEFAULT_DATABASE_FILE
        self._con = sqlite3.connect(self._db_file)
        self._cur = self._con.cursor()
        self._create_tables()
        self._insert_default_queues(schedulers)

    def _insert_default_queues(self, schedulers: List[Scheduler]) -> None:
        for scheduler in schedulers:
            self._cur.execute(
                "INSERT INTO queues (name) VALUES (?)", (scheduler.__str__(),))
        self._con.commit()

    def _create_tables(self) -> None:
        self._create_queues_table()
        self._create_jobs_table()

    def _create_queues_table(self) -> None:
        self._cur.execute('''CREATE TABLE IF NOT EXISTS queues
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)''')
        self._con.commit()

    def _create_jobs_table(self) -> None:
        self._cur.execute('''CREATE TABLE IF NOT EXISTS jobs
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            queue_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            owner TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (queue_id) REFERENCES queues(id))''')
        self._con.commit()

    def _refresh_connection(self) -> None:
        self._con = sqlite3.connect(self._db_file)
        self._cur = self._con.cursor()

    def insert_job(self, job: Job) -> None:
        self._refresh_connection()
        self._cur.execute("INSERT INTO jobs (queue_id, name, created_at, owner, status) VALUES (?, ?, ?, ?, ?)",
                          (job.queue, job.name, job.created_at, job.owner, job.status))
        self._con.commit()

    def get_queue_id(self, queue_name: str) -> int:
        self._refresh_connection()
        self._cur.execute(
            "SELECT id FROM queues WHERE name = ?", (queue_name,))
        row = self._cur.fetchone()
        if row is None:
            raise Exception(f"Queue {queue_name} not found")
        return row[0]

    def get_jobs(self) -> List[Job]:
        self._refresh_connection()
        self._cur.execute("SELECT * FROM jobs")
        rows = self._cur.fetchall()
        print(rows)
        return [Job(*row) for row in rows]
