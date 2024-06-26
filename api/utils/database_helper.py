'''Database helper class.'''

import os
import sqlite3
from pathlib import Path
from typing import List
from api.constants.job_status import JobStatus
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler
from api.utils.singleton import Singleton
from api.interfaces.queue import Queue

DEFAULT_DATABASE_FILE = ''
if os.environ.get('TESTING'):
    DEFAULT_DATABASE_FILE = Path('./db/test_db.sqlite3')
else:
    DEFAULT_DATABASE_FILE = Path('./db/db.sqlite3')


class DatabaseHelper(metaclass=Singleton):
    '''Database helper class.

    This class is responsible for handling all database operations.

    Attributes:
        _db_file (Path): The path to the database file.
        _con (sqlite3.Connection): The connection to the database.
        _cur (sqlite3.Cursor): The cursor to the database.

    Methods:
        TODO AT THE END OF THE PROJECT
    '''

    def __init__(self, schedulers: List[Scheduler] = None, database_file: Path = None) -> None:
        '''Initializes the database helper.'''

        if os.environ.get('TESTING') == 'true':
            from api.classes.apache_hadoop import ApacheHadoop
            from api.classes.sge import SGE
            schedulers = []
            schedulers.append(ApacheHadoop())
            schedulers.append(SGE())
        if not schedulers:
            raise ValueError(
                'At least one scheduler must be provided in database initialization')
        self._db_file = database_file or DEFAULT_DATABASE_FILE
        self._con = sqlite3.connect(self._db_file)
        self._con.execute('PRAGMA foreign_keys = ON')
        self._cur = self._con.cursor()
        self._create_tables()
        self._insert_default_queues(schedulers)

    def _insert_default_queues(self, schedulers: List[Scheduler]) -> None:
        '''Inserts the default queues into the database.'''

        for scheduler in schedulers:
            self._cur.execute(
                'SELECT * FROM queues WHERE name = ?', (scheduler.name,))
            row = self._cur.fetchone()
            if row is None:
                self._cur.execute(
                    'INSERT INTO queues (name) VALUES (?)', (scheduler.name,))
                self._con.commit()

    def _create_tables(self) -> None:
        '''Creates the tables in the database.'''

        self._create_queues_table()
        self._create_jobs_table()

    def _create_queues_table(self) -> None:
        '''Creates the queues table in the database.'''

        self._cur.execute('''CREATE TABLE IF NOT EXISTS queues
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)''')
        self._con.commit()

    def _create_jobs_table(self) -> None:
        '''Creates the jobs table in the database.'''

        self._cur.execute('''CREATE TABLE IF NOT EXISTS jobs
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            queue_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            owner TEXT NOT NULL,
            status TEXT NOT NULL,
            path TEXT NOT NULL,
            options TEXT NOT NULL,
            scheduler_job_id INTEGER,
            pwd TEXT,
            FOREIGN KEY(queue_id) REFERENCES queues(id))''')
        self._con.commit()

    def _refresh_connection(self) -> None:
        '''Refreshes the connection to the database.'''

        self._con = sqlite3.connect(self._db_file)
        self._con.execute('PRAGMA foreign_keys = ON')
        self._cur = self._con.cursor()

    def reset_database_for_testing(self) -> None:
        '''Resets the database for testing purposes.'''

        self._refresh_connection()
        self._cur.execute('DROP TABLE IF EXISTS jobs')
        self._cur.execute('DROP TABLE IF EXISTS queues')
        self._con.commit()
        self._create_tables()
        from api.classes.apache_hadoop import ApacheHadoop
        from api.classes.sge import SGE
        self._insert_default_queues([ApacheHadoop(), SGE()])

    def insert_job(self, job: Job) -> None:
        '''Inserts a job into the database.'''

        try:
            self._refresh_connection()
            self._cur.execute('INSERT INTO jobs (queue_id, name, created_at, owner, status, path, options, scheduler_job_id, pwd) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?)',
                              (job.queue, job.name, job.created_at, job.owner,
                               job.status.value, str(job.path), job.options, str(job.pwd)))
            self._con.commit()
        except sqlite3.IntegrityError as e:
            raise Exception(f'Queue {job.queue} not found') from e

    def get_queue_id(self, queue_name: str) -> int:
        '''Gets the ID of a queue by its name.'''

        self._refresh_connection()
        self._cur.execute(
            'SELECT id FROM queues WHERE name = ?', (queue_name,))
        row = self._cur.fetchone()
        if row is None:
            raise Exception(f'Queue {queue_name} not found')
        return row[0]

    def get_jobs(self, status: JobStatus = None, queue: int = None, owner: str = None) -> List[Job]:
        '''Gets all jobs from the database that match the given criteria.'''

        self._refresh_connection()
        query = 'SELECT * FROM jobs'
        params = []
        if owner and owner != 'root':
            query += ' WHERE owner = ?'
            params.append(owner)
            if status:
                query += ' AND status = ?'
                params.append(status.value)
            if queue:
                query += ' AND queue_id = ?'
                params.append(queue)
        else:
            query += ' WHERE 1=1'
            if status:
                query += ' AND status = ?'
                params.append(status.value)
            if queue:
                query += ' AND queue_id = ?'
                params.append(queue)

        self._cur.execute(query, params)
        rows = self._cur.fetchall()
        return [Job(*row) for row in rows]

    def get_job(self, job_id: int, owner: str) -> Job:
        '''Gets a job by its ID.'''

        self._refresh_connection()
        self._cur.execute(
            'SELECT * FROM jobs WHERE id = ? AND owner = ?', (job_id, owner,))
        row = self._cur.fetchone()
        if row is None:
            raise Exception('Job not found')
        return Job(*row)

    def update_job(self, job_id: int, owner: str, job: Job) -> None:
        '''Updates a job in the database.'''

        self._refresh_connection()
        self._cur.execute(
            'UPDATE jobs SET name = ?, queue_id = ?, status = ?, path = ?, options = ? WHERE id = ? AND owner = ?', (job.name, job.queue, job.status.value, str(job.path), job.options, job_id, owner))
        self._con.commit()

    def delete_job(self, job_id: int, owner: str) -> None:
        '''Deletes a job from the database.'''

        self._refresh_connection()
        self._cur.execute(
            'DELETE FROM jobs WHERE id = ? AND owner = ?', (job_id, owner))
        self._con.commit()

    def get_queues(self) -> List[Queue]:
        '''Gets all queues from the database.'''

        self._refresh_connection()
        self._cur.execute('SELECT id, name FROM queues')
        rows = self._cur.fetchall()
        return [Queue(*row) for row in rows]

    def set_job_scheduler_id(self, job_id: int, owner: str, scheduler_job_id: int) -> None:
        '''Sets the scheduler job ID of a job.'''

        self._refresh_connection()
        self._cur.execute(
            'UPDATE jobs SET scheduler_job_id = ? WHERE id = ? AND owner = ?', (scheduler_job_id, job_id, owner))
        self._con.commit()
