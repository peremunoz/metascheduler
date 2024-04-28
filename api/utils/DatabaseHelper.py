from pathlib import Path
from interfaces.Job import Job
from utils.Singleton import Singleton
import sqlite3

DEFAULT_DATABASE_FILE = Path("./db/db.sqlite3")


class DatabaseHelper(metaclass=Singleton):

    def __init__(self, database_file: Path = None) -> None:
        self._db_file = database_file or DEFAULT_DATABASE_FILE
        self._con = sqlite3.connect(self._db_file)
        self._cur = self._con.cursor()
        self._create_table()

    def _create_table(self) -> None:
        self._cur.execute('''CREATE TABLE IF NOT EXISTS jobs
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            scheduler TEXT NOT NULL,
            created_at DATETIME NOT NULL)''')
        self._con.commit()

    def _refresh_connection(self) -> None:
        self._con = sqlite3.connect(self._db_file)
        self._cur = self._con.cursor()

    def insert_job(self, job: Job) -> None:
        self._refresh_connection()
        self._cur.execute("INSERT INTO jobs (name, scheduler, created_at) VALUES (?, ?, ?)",
                          (job.name, job.scheduler.__str__(), job.created_at))
        self._con.commit()

    def get_jobs(self):
        self._refresh_connection()
        self._cur.execute("SELECT * FROM jobs")
        return self._cur.fetchall()
