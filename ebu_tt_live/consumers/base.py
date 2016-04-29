

class AbstractConsumer(object):
    _input_stream = None
    _output_stream = None

    def __init__(self, input_stream, output_stream=None):
        self._input_stream = input_stream
        self._output_stream = output_stream

    def start(self):
        raise NotImplementedError()

    def process_events(self):
        raise NotImplementedError()
