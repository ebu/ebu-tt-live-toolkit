
import collections
import threading
import Queue
import os


class ComparableMixin(object):
    """
    This mixin is meant to make implementing the comparison interface easier without having to clutter up
    custom class implementations that would only like to delegate their comparison to comparable a member.
    This class is Python3 compatible.
    NOTE: This is a slightly modified version of the one suggested by the following blog:
    https://regebro.wordpress.com/2010/12/13/python-implementing-rich-comparison-the-correct-way/
    """
    def _compare(self, other, method):
        self._cmp_checks(other)
        try:
            return method(self._cmp_key(), other._cmp_key())
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or return different type,
            # so I can't compare with "other".
            return NotImplemented

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)

    def _cmp_key(self):
        """
        Implement the delegation method.
        :return: comparable member
        """
        raise NotImplementedError()

    def _cmp_checks(self, other):
        """
        Extra checks that need to be fulfilled in order for the comparison to make sense.
        Any custom exceptions thrown here are preserved and propagated in original form.
        :param other:
        :return:
        """
        pass


class RingBufferWithCallback(collections.deque):
    """
    This class calls a callback when an item is falling out of the buffer due to removal.
    On manual removal it does not. That is the user's responsibility.
    """

    _callback = None

    def __init__(self, iterable=(), maxlen=None, callback = None):
        if callback is not None  and not callable(callback):
            raise ValueError('Callback: {} is not callable'.format(callback))
        self._callback = callback
        super(RingBufferWithCallback, self).__init__(iterable, maxlen)

    def append(self, item):
        if len(self) >= self.maxlen:
            self._callback(self.popleft())
        super(RingBufferWithCallback, self).append(item)


class RotatingFileBuffer(RingBufferWithCallback):
    """
    This class holds the given number of file names and when they are pushed out of the buffer it deletes
    them asynchronously. Preferably just the names and not open file handles.
    """

    _deletion_thread = None
    _deletion_queue = None

    def __init__(self, maxlen):
        super(RotatingFileBuffer, self).__init__(maxlen=maxlen, callback=self.delete_file)
        # In this case threads make sense since it is I/O we are going to be waiting for and that is releasing the GIL.
        # Deletion is the means for us to send down files for deletion to the other thread(maybe process later)....
        self._deletion_queue = Queue.Queue()
        self._deletion_thread = threading.Thread(
            target=self._delete_thread_loop,
            kwargs={'q': self._deletion_queue}
        )
        # Ensuring the thread will not leave us hanging
        self._deletion_thread.daemon = True
        self._deletion_thread.start()

    @classmethod
    def _delete_thread_loop(cls, q):
        files_waiting = []
        default_wait = 0.2
        while True:
            if files_waiting:
                try:
                    # We got work to retry so we only try a little bit...
                    files_waiting.append(q.get(timeout=default_wait))
                except Queue.Empty:
                    pass
            else:
                # No pending files in our buffer we can wait for the next item
                try:
                    files_waiting.append(q.get())
                except Queue.Empty:
                    pass

            failed_files = []
            # Now we can try to see if we have anything to delete
            while files_waiting:
                item = files_waiting.pop()
                full_path = os.path.abspath(item)
                if os.path.exists(item):
                    # File is still there try to delete it
                    # If not we do nothing. The loop discards the name
                    try:
                        os.remove(full_path)
                    except IOError:
                        # Horrible! Quick, put it back... NEXT
                        failed_files.append(item)

            files_waiting = failed_files

    def delete_file(self, item):
        """
        This function hands the file down to our worker thread to deal with it.
        :param item:
        :return:
        """
        self._deletion_queue.put(item)
