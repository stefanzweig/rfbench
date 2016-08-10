from flask import current_app
from zweigdb import KeywordTable
from rfbench.version import __version__
from robot.utils.argumentparser import ArgFileParser
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
import tornado.ioloop
import argparse
import blueprints
import flask
import importlib
import inspect
import os
import robot.errors
import signal
import sys

class RobotBench(object):
    def __init__(self):

        self.args = self._parse_args()

        if self.args.version:
            print(__version__)
            sys.exit(0)

    def start(self):
    	pass

    def _parse_args(self):
    	print "parsing arguments!!"
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--library", action="append", default=[],
                            help="load the given LIBRARY (eg: -l DatabaseLibrary)")
        parser.add_argument("-i", "--interface", default="127.0.0.1",
                            help="use the given network interface (default=127.0.0.1)")
        parser.add_argument("-p", "--port", default=7070, type=int,
                            help="run on the given PORT (default=7070)")
        parser.add_argument("-A", "--argumentfile", action=ArgfileAction,
                            help="read arguments from the given file")
        parser.add_argument("-P", "--pythonpath", action=PythonPathAction,
                            help="additional locations to search for libraries.")
        parser.add_argument("-M", "--module", action=ModuleAction,
                            help="give the name of a module that exports one or more classes")
        parser.add_argument("-D", "--debug", action="store_true", default=False,
                            help="turn on debug mode")
        parser.add_argument("--no-installed-keywords", action="store_true", default=False,
                            help="do not load some common installed keyword libraries, such as BuiltIn")
        parser.add_argument("--poll", action="store_true", default=False,
                            help="use polling behavior instead of events to reload keywords on changes (useful in VMs)")
        parser.add_argument("--root", action="store", default="/dashboard",
                            help="Redirect root url (http://localhost:port/) to this url (eg: /dashboard, /doc)")
        parser.add_argument("--version", action="store_true", default=False,
                            help="Display version number and exit")
        parser.add_argument("path", nargs="*",
                            help="zero or more paths to folders, libraries or resource files")
        return parser.parse_args()

class ArgfileAction(argparse.Action):
    '''Called when the argument parser encounters --argumentfile'''
    def __call__ (self, parser, namespace, values, option_string = None):
        parser.parse_args(args, namespace)

class PythonPathAction(argparse.Action):
    """Add a path to PYTHONPATH"""
    def __call__(self, parser, namespace, arg, option_string = None):
        sys.path.insert(0, arg)

class ModuleAction(argparse.Action):
    '''Handle the -M / --module option

    This finds all class objects in the given module.  Since page
    objects are modules of , they will be appended to the "library"
    attribute of the namespace and eventually get processed like other
    libraries.

    Note: classes that set the class attribute
    '__show_in_rfhub' to False will not be included.

    This works by importing the module given as an argument to the
    option, and then looking for all members of the module that
    are classes

    For example, if you give the option "pages.MyApp", this will
    attempt to import the module "pages.MyApp", and search for the classes
    that are exported from that module. For each class it finds it will
    append "pages.MyApp.<class name>" (eg: pages.MyApp.ExamplePage) to
    the list of libraries that will eventually be processed.
    '''
    def __call__(self, parser, namespace, arg, option_string = None):
        try:
            module = importlib.import_module(name=arg)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    # Pay Attention! The attribute we're looking for
                    # takes advantage of name mangling, meaning that
                    # the attribute is unique to the class and won't
                    # be inherited (which is important!). See
                    # https://docs.python.org/2/tutorial/classes.html#private-variables-and-class-local-references

                    attr = "_%s__show_in_rfhub" % obj.__name__
                    if getattr(obj, attr, True):
                        libname = "%s.%s" % (module.__name__, name)
                        namespace.library.append(libname)

        except ImportError as e:
            print("unable to import '%s' : %s" % (arg,e))
