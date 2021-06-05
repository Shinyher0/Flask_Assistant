class SimpleResponse(object):
    """
    Simple responses take the form of a chat bubble visually and use text-to-speech (TTS) or Speech Synthesis Markup Language (SSML) for sound.

    Args:
        tts (str): the text to say out loud
        displayText (str): the text to display

    Notes:
        TTS text is used as chat bubble content by default. If the visual aspect of that text meets your needs, you won't need to specify any display text for a chat bubble.
    """
    def __init__(self, tts=None, displayText=None):
        self._tts = tts
        if not displayText:
            self._disp = tts
        else:
            self._disp = displayText

    def __dict__(self):
        return {
            "simpleResponse": {
                "textToSpeech": self._tts,
                "displayText": self._disp
            }
        }


class SuggestionChip(object):
    """
    SuggestionChip takes the form of a bubble at the bottom of the screen.

    Args:
        text (str): The text to display on the chip
    """
    def __init__(self, text):
        self.txt = text

    def __dict__(self):
        return {
            "title": self.txt
        }
