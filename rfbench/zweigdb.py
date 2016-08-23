import sqlite3
import os
from robot.libdocpkg import LibraryDocumentation
import robot.libraries
import logging
import json
import re
import sys

from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import PatternMatchingEventHandler

class WatchdogHandler(PatternMatchingEventHandler):
    patterns = ["*.robot", "*.txt", "*.py", "*.tsv"]
    def __init__(self, tsdb, path):
        PatternMatchingEventHandler.__init__(self)
        self.tsdb = tsdb
        self.path = path

    def on_created(self, event):
        # monitor=False because we're already monitoring
        # ancestor of the file that was created. Duh.
        self.tsdb.add(event.src_path, monitor=False)

    def on_deleted(self, event):
        # FIXME: need to implement this
        pass

    def on_modified(self, event):
        self.tsdb.on_change(event.src_path, event.event_type)



class SuiteTable(object):
    def __init__(self, dbfile=":memory:", poll=False):
        self.db = sqlite3.connect(dbfile, check_same_thread=False)
        self.log = logging.getLogger(__name__)
        self._create_db()

        # set up watchdog observer to monitor changes to
        # keyword files (or more correctly, to directories
        # of keyword files)
        self.observer =  PollingObserver() if poll else Observer()
        self.observer.start()

    def _create_db(self):

        if not self._table_exists("collection_table"):
            self.db.execute("""
                CREATE TABLE collection_table
                (collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name          TEXT COLLATE NOCASE,
                 type          COLLATE NOCASE,
                 version       TEXT,
                 scope         TEXT,
                 namedargs     TEXT,
                 path          TEXT,
                 doc           TEXT,
                 doc_format    TEXT)
            """)
            self.db.execute("""
                CREATE INDEX collection_index
                ON collection_table (name)
            """)

        if not self._table_exists("keyword_table"):
            self.db.execute("""
                CREATE TABLE keyword_table
                (keyword_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                 name          TEXT COLLATE NOCASE,
                 collection_id INTEGER,
                 doc           TEXT,
                 args          TEXT)
            """)
            self.db.execute("""
                CREATE INDEX keyword_index
                ON keyword_table (name)
            """)

    def _table_exists(self, name):
        cursor = self.db.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='%s'
        """ % name)
        return len(cursor.fetchall()) > 0
