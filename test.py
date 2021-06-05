from flask_assistant import Assistant, SimpleResponse, SuggestionChip
from flask import Flask


app = Flask(__name__)
ass = Assistant(app, "/post", basic_auth_usr="Shinyhero36", basic_auth_pwd="LoremIpsum")


@ass.onIntent("Welcome")
def welcome(args):
    return ass.say([SimpleResponse("Congrats!!", "Congrats !! You made it!!")])


@ass.onIntent("Welcome 2")
def welcome(args):
    return ass.say(
        responses=[
            SimpleResponse("Hello", "Hello I Love you too !!")
        ],
        suggestions=[SuggestionChip("Bonjour")],
        endConversation=False
    )


@ass.defaultResponse
def default(args):
    return ass.say(
        responses=[
            SimpleResponse("Je fais caca", "Je me chie dessus !!")
        ], endConversation=True
    )


if __name__ == '__main__':
    app.run(debug=True, port=5001)
