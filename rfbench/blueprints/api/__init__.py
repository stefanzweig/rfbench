'''
API blueprint

This blueprint provides the /api interface.

'''

from flask import Blueprint
from . import keywords

blueprint = Blueprint('api', __name__)

endpoints = [
    keywords.ApiEndpoint(blueprint)
]

