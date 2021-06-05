from flask import Flask, request, Response as ResponseFlask, _app_ctx_stack
from functools import wraps, partial
from inspect import getfullargspec
from json import dumps

from .RichResponses import SuggestionChip


class Assistant(object):
    """
    Flask Assistant helps linking your Google Assistant App with Flask via webhooks

    Args:
        app (Flask): a Flask application object
        route (str): Route at which your assistant will listen to.
        basic_auth_usr (str, optional): Username to use for basic auth
        basic_auth_pwd (str, optional): Password to use for basic auth
    """
    def __init__(self, app=None, route=None, basic_auth_usr=None, basic_auth_pwd=None):
        self._app = app
        self._route = route
        self._basic_auth_usr = basic_auth_usr
        self._basic_auth_pwd = basic_auth_pwd
        self._map_of_intents = {}
        self._default_view_func = None
        self._rr = self._clean_rr()

        if app is not None:
            self.init_app(app, route, basic_auth_usr, basic_auth_pwd)

    def init_app(self, app, route=None, basic_auth_usr=None, basic_auth_pwd=None):
        """
        Initialize the flask object

        Args:
            app (Flask): a Flask application object
            route (str): Route at which your assistant will listen to.
            basic_auth_usr (str, optional): Username to use for basic auth
            basic_auth_pwd (str, optional): Password to use for basic auth

        See Also:
            Why an init_app function? See: https://flask.palletsprojects.com/en/2.0.x/extensiondev/#flask-extension-development
        """
        self._route = route
        self._basic_auth_usr = basic_auth_usr
        self._basic_auth_pwd = basic_auth_pwd
        app.add_url_rule(self._route, view_func=self._flask_view_func, methods=["POST"])

    """@property
    def intent(self):
        return getattr(_app_ctx_stack.top, "_dialogflow_intent", [])

    @intent.setter
    def intent(self, value):
        _app_ctx_stack.top.dialogflow_intent = value"""

    @staticmethod
    def _clean_rr():
        return {
            "payload": {
                "google": {
                    "expectUserResponse": None,
                    "richResponse": {
                        "items": [],
                        "suggestions": [],
                        "linkOutSuggestion": {
                            "destinationName": "Suggestion Link",
                            "url": "https://assistant.google.com/"
                        }
                    }
                }
            }
        }

    def say(self, responses=None, suggestions=None, endConversation=False):
        """
        Generate the json response

        Args:
            responses (list): A list of rich responses
            suggestions (list[SuggestionChip], optional): A list of suggestion chips
            endConversation (bool, optional): Self explanatory

        Warnings:
            * If the 'responses' parameter is empty, the app will crash

        Returns:
            dict: An understandable response for the assistant
        """
        for response in responses:
            self._rr["payload"]["google"]["richResponse"]["items"].append(response.__dict__())
            self._rr["payload"]["google"]["expectUserResponse"] = not endConversation

        if suggestions is not None:
            for suggestion in suggestions:
                self._rr["payload"]["google"]["richResponse"]["suggestions"].append(suggestion.__dict__())

        rr = self._rr.copy()
        self._rr = self._clean_rr()
        return rr

    def _flask_view_func(self, *args, **kwargs):
        """
        This function is called every time the endpoint if triggerd.
        """
        is_basic_auth = self._basic_auth_usr is not None
        if is_basic_auth is True and request.authorization.username != self._basic_auth_usr or request.authorization.password != self._basic_auth_pwd:
            return "", 401

        # Ignore mimetype and ignore fails
        json_data = request.get_json(silent=True, force=True)

        print(json_data)

        intent = json_data["queryResult"]["intent"]["displayName"]
        try:
            view_func = self._map_of_intents[intent]
        except KeyError:
            if self._default_view_func:
                view_func = self._default_view_func
            else:
                raise NotImplementedError(f"The following intent: {intent} hasn't been mapped.")

        params = json_data['queryResult']['parameters']

        view_func_with_args = partial(view_func, params)

        response = view_func_with_args()

        if response is not None:
            jsonResponse = ResponseFlask(
                response=dumps(response),
                status=200,
                mimetype='application/json'
            )
            return jsonResponse
        return "", 400

    def onIntent(self, intentName):
        """
        Decorator which registers an actions's view function

        Args:
            intentName (str): The name of the intent to map to a function
        """
        def decorator(f):
            self._map_of_intents[intentName] = f

            @wraps(f)
            def wrapper(*args, **kwargs):
                self._flask_view_func(*args, **kwargs)
            return f
        return decorator

    def defaultResponse(self, f):
        """
        Register a default function which serve as a default response if no intent was mapped

        Args:
            f (function): A function
        """

        self._default_view_func = f

        @wraps(f)
        def wrapper(*args, **kwargs):
            self._flask_view_func(*args, **kwargs)
        return f
