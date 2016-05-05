

class TimeBase(object):
    SMPTE = 'smpte'
    MEDIA = 'media'
    CLOCK = 'clock'


class Subtitle(object):
    """
    This is a common base for a text fragment representation in
    the subtitle format. It is supposed to be a base for conversion
    between the different formats.
    """

    def __init__(self):
        raise NotImplementedError()

    def set_text(self, text):
        """
        Set the content as simple multi-line text.
        :param text:
        :return:
        """
        raise NotImplementedError()

    def get_text(self, text):
        """
        Get the content as simple multi-line text
        :param text:
        :return:
        """
        raise NotImplementedError()

    def validate(self):
        raise NotImplementedError()


class SubtitleDocument(object):

    def __init__(self):
        raise NotImplementedError('This is an abstract class')

    def validate(self):
        raise NotImplementedError()
