Quickstart
==========

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

This guide assumes you are already familar with `Flask <http://flask.pocoo.org>`_ and that you have already install Flask and |project|. If that's not the case head toward :doc:`installation`


A Minimal Application
---------------------

A minimal |project| application looks something like this

.. code-block:: python

    from flask_assistant import Assisttant, SimpleResponse
    from flask import Flask


    app = Flask(__name__)
    ass = Assisttant(app, "/post")


    @ass.onIntent("Welcome")
    def welcome(args):
        return ass.say([SimpleResponse("Congrats!!", "Congrats !! You made it!!")])

    if __name__ == '__main__':
        app.run(debug=True)

So what did that code do?

1.  First, we imported the :class:`~flask_assistant.Assistant` and the :class:`~flask_assistant.SimpleResponse`. The instance of the :class:`~flask_assistant.SimpleResponse` will generate a simple response to your Google Assistant app
2.  Next we created an instance of the :class:`~flask_assistant.Assistant` which will handles webhooks and intent for us.
    The first parameter is an instance of Flask. The second one, is the endpoint our app will listen to.
3.  We then use the :meth:`~flask_assistant.Assistant.onIntent` decorator to tell our app
    what function to execute when the 'Welcome' intent is triggered.
4.  The function returns a list of SimpleResponse. This will display "Congrats" and say "Congrats !! You made it!!" out loud.

Save it as :file:`app.py` or something similar. Note that we’ve enabled Flask debugging mode to provide code reloading and better error messages.

.. code-block:: console

    $ python app.py
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

.. warning::

    Debug mode should never be used in a production environment!


Expose your application
-----------------------

To test this application we need to expose our Flask app. To do so, we use `Ngrok <https://ngrok.com/>`_
Once you installed it, run the following command

.. code-block:: console

    $ ngrok http 5000
     ngrok by @inconshreveable     (Ctrl+C to quit)

     Session Status                online
     Web Interface                 http://127.0.0.1:4040
     Forwarding                    http://e2a1794143e1.ngrok.io -> http://localhost:5000
     Forwarding                    https://e2a1794143e1.ngrok.io -> http://localhost:5000

     Connections                   ttl     opn     rt1     rt5     p50     p90
                                   0       0       0.00    0.00    0.00    0.00

Copy the https links and set it as your fulfillment url

.. attention::

    * Note that the argument following http must be the port of your flask app.
    * The fullliment url must be https


Now trigger the Welcome intent.
You sould hear and see something like this

.. figure:: _static/images/result_example.png
    :scale: 50 %
    :alt: Result

.. raw:: html

    <center>
      <audio controls="controls">
        <source src="_static/audio/example.mp3" type="audio/mp3">
          Your browser does not support the <code>audio</code> element.
       </audio>
    </center>

Handling intents
----------------

To handle intents you need to decorate your function with :meth:`~flask_assistant.Assistant.onIntent` like so

.. code-block:: python

    @ass.onIntent("intent 1")
    def something(args):
        ...

    @ass.onIntent("intent 2")
    def something(args):
        ...

    @ass.onIntent("intent 3")
    def something(args):
        ...


It is possible to handle intents how weren't registered. In this case, you need to decorate your function with :meth:`flask_assistant.Assistant.defaultIntent` like so

.. code-block:: python

    @ass.onIntent("intent 1")
    def something(args):
        ...

    @ass.defaultIntent
    def something(args):
        ...


RichResponses
-------------

You can use a rich response if you want to display visual elements to enhance user interactions with your app.
Rich responses can appear on screen-only or audio and screen experiences.

Simple responses
^^^^^^^^^^^^^^^^

Simple responses take the form of a chat bubble visually and use text-to-speech (TTS) or Speech Synthesis Markup Language (SSML) for sound.

.. code-block:: python

    from flask_asssistant import SimpleResponse

    ...

    @ass.onIntent("intentName")
    def welcome(args):
        return ass.say([SimpleResponse("Congrats !! You made it!!")])


Suggestion chips
^^^^^^^^^^^^^^^^

Suggestion chip take the form of a bubble at the bottom of the screen.

.. code-block:: python

    from flask_asssistant import SimpleResponse, SuggestionChip

    ...

    @ass.onIntent("intentName")
    def welcome(args):
        return ass.say(
            [SimpleResponse("Congrats !! You made it!!")],
            suggestions=[
                Suggestion("I am a chip"),
                Suggestion("Me too !"),
            ]
        )


.. warning::

    * Simple response is mandatory. It's not allowed to return Suggestion chips only.
    * If you don't provide a SimpleResponse, your app will crash
