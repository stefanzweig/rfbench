'''
This provides the view functions for the /api/keywords endpoints
'''

import flask
from flask import current_app
from robot.libdocpkg.htmlwriter import DocToHtml

class ApiEndpoint(object):
    def __init__(self, blueprint):
        blueprint.add_url_rule("/keywords/", view_func = self.get_keywords)

    def get_keywords(self):
        # caller wants a list of keywords
        #collection_id = flask.request.args.get('collection_id', "")
        #return self.get_library_keywords(collection_id)
        d = {"hello":"world"}
        return flask.jsonify(d)