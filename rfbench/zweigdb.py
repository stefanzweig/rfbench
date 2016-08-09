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

class KeywordTable(object):
	pass