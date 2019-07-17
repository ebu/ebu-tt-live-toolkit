import abc
import collections
import threading
import Queue
import os
import time
import types

from nltk import BlanklineTokenizer, PunktSentenceTokenizer, WhitespaceTokenizer
from xml.dom.minidom import Node, parseString
import re


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

    def __init__(self, iterable=(), maxlen=None, callback=None):
        if callback is not None and not callable(callback):
            raise ValueError('Callback: {} is not callable'.format(callback))
        self._callback = callback
        super(RingBufferWithCallback, self).__init__(iterable, maxlen)

    def append(self, item):
        if len(self) >= self.maxlen:
            if self._callback is not None:
                self._callback(self.popleft())
        super(RingBufferWithCallback, self).append(item)


class StoppableThread(threading.Thread):
    """
    Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    """

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class RotatingFileBufferStopped(Exception):
    pass


class RotatingFileBuffer(RingBufferWithCallback):
    """
    This class holds the given number of file names and when they are pushed out of the buffer it deletes
    them asynchronously. Preferably just the names and not open file handles.
    """

    _deletion_thread = None
    _deletion_queue = None

    def __init__(self, maxlen, asynchronous=True):
        super(RotatingFileBuffer, self).__init__(maxlen=maxlen, callback=self.delete_file)
        # In this case threads make sense since it is I/O we are going to be waiting for and that is releasing the GIL.
        # Deletion is the means for us to send down files for deletion to the other thread(maybe process later)....
        self._deletion_queue = Queue.Queue()
        if asynchronous is True:
            self._deletion_thread = StoppableThread(
                target=self._delete_thread_loop,
                kwargs={'q': self._deletion_queue}
            )
            # Ensuring the thread will not leave us hanging
            self._deletion_thread.daemon = True
            self._deletion_thread.start()

    @classmethod
    def _do_delete(cls, files_waiting):
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

        return failed_files

    @classmethod
    def _do_consume(cls, q, files_waiting, default_wait):
        try:
            files_waiting.append(q.get(timeout=default_wait))
        except Queue.Empty:
            pass

        failed_files = cls._do_delete(files_waiting)
        return failed_files

    @classmethod
    def _delete_thread_loop(cls, q):
        files_waiting = []
        default_wait = 0.2
        while not threading.current_thread().stopped() or not q.empty():
            files_waiting = cls._do_consume(q=q, files_waiting=files_waiting, default_wait=default_wait)
            time.sleep(0.1)
        while files_waiting:
            files_waiting = cls._do_delete(files_waiting=files_waiting)
            time.sleep(0.1)

    def delete_file(self, item):
        """
        This function hands the file down to our worker thread to deal with it.
        :param item:
        :return:
        """
        self._deletion_queue.put(item)
        if self._deletion_thread is None:
            files_waiting = []
            default_wait = 0.1
            while files_waiting or not self._deletion_queue.empty():
                files_waiting = self._do_consume(
                    q=self._deletion_queue,
                    files_waiting=files_waiting,
                    default_wait=default_wait
                )

    def append(self, item):
        """
        This override makes sure that we don't add to an asynchronously managed buffer that is about to be shut down.
        :param item: The file name
        :return:
        """
        if self._deletion_thread is not None:
            if self._deletion_thread.stopped():
                raise RotatingFileBufferStopped('File deletion thread is stopped!')
        super(RotatingFileBuffer, self).append(item)


def tokenize_english_document(input_text):
    """
    This is a crude tokenizer for input conversations in English.
    :param input_text:
    :return:
    """
    end_list = []
    block_tokenizer = BlanklineTokenizer()
    sentence_tokenizer = PunktSentenceTokenizer()
    word_tokenizer = WhitespaceTokenizer()
    # using the 38 characters in one line rule from ITV subtitle guidelines
    characters_per_line = 38
    lines_per_subtitle = 2

    blocks = block_tokenizer.tokenize(input_text)
    for block in blocks:
        # We have one speaker
        sentences = sentence_tokenizer.tokenize(block)
        # We have the sentences
        for sentence in sentences:
            words = word_tokenizer.tokenize(sentence)
            reverse_words = words[::-1]

            lines = []
            current_line = ''
            line_full = False
            while reverse_words:
                word = reverse_words.pop()
                longer_line = ' '.join([current_line, word]).strip()
                if len(longer_line) > characters_per_line and len(current_line):
                    # The longer line is overreaching boundaries
                    reverse_words.append(word)
                    line_full = True
                elif len(word) >= characters_per_line:
                    # Very long words
                    current_line = longer_line
                    line_full = True
                else:
                    current_line = longer_line

                if line_full:
                    lines.append(current_line)
                    current_line = ''
                    line_full = False

                if len(lines) >= lines_per_subtitle:
                    end_list.append(lines)
                    lines = []
            if current_line:
                lines.append(current_line)
            if lines:
                end_list.append(lines)

    return end_list


def _assert_asm_is_defined(value, member_name, class_name):
    if value in (None, NotImplemented):
        raise TypeError(
            'Abstract static member: \`{}.{}\` does not match the criteria'.format(
                class_name,
                member_name
            )
        )


def validate_types_only(value, member_name, class_name):
    if not isinstance(value, tuple):
        value = (value,)
    for item in value:
        if not isinstance(item, (type, types.ClassType)) and item is not ANY:
            raise TypeError(
                'Abstract static member: \'{}.{}\' is not a type or class'.format(
                    class_name,
                    member_name
                )
            )


class AnyType(object):
    "A helper object that compares equal to everything."

    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return False

    def __repr__(self):
        return '<ANY>'

ANY = AnyType()


class AbstractStaticMember(object):
    """
    This allows me to require the subclasses to define some attributes using a customizeable
    validator. The idea is that all static members should be initialized to a value by the time
    abstract functions have all been implemented.
    """

    _validation_func = None

    def __init__(self, validation_func=None):
        if validation_func is None:
            self._validation_func = _assert_asm_is_defined
        else:
            self._validation_func = validation_func

    def validate(self, value, member_name, class_name):
        self._validation_func(value, member_name, class_name)


class AutoRegisteringABCMeta(abc.ABCMeta):
    """
    This metaclass gets us automatic class registration and cooperates with AbstractStaticMember.
    If none of the 2 features are needed it just provides the basic abc.ABCMeta functionality.
    For the auto registration an abstract class needs to implement the auto_register_impl classmethod.
    """

    def __new__(mcls, name, bases, namespace):
        cls = super(AutoRegisteringABCMeta, mcls).__new__(mcls, name, bases, namespace)
        abstract_members = set(name
                        for name, value in namespace.items()
                        if isinstance(value, AbstractStaticMember))

        abstracts = getattr(cls, "__abstractmethods__", set())

        if not abstracts:
            # This means the class is not abstract so we should not have any abstract static members
            validated_members = set()
            for base in bases:
                if isinstance(base, mcls):
                    for base_member in getattr(base, '_abc_static_members', set()):
                        if base_member in validated_members:
                            continue
                        value = getattr(cls, base_member, NotImplemented)
                        if isinstance(value, AbstractStaticMember) or value is NotImplemented:
                            abstract_members.add(base_member)
                        else:
                            getattr(base, base_member).validate(value, base_member, name)
                            validated_members.add(base_member)

                    base.auto_register_impl(cls)

            if abstract_members:
                raise TypeError('{} must implement abstract static members: [{}]'.format(
                    name,
                    ', '.join(abstract_members)
                ))
        if namespace.get('auto_register_impl') is None:
            cls.auto_register_impl = classmethod(lambda x, y: None)
        cls._abc_static_members = frozenset(abstract_members)
        cls._abc_interface = '__metaclass__' in namespace.keys()
        return cls

    def __call__(cls, *args, **kwargs):
        if cls._abc_interface is True:
            raise TypeError('Can\'t instantiate {} is an abstract base class.'.format(cls))
        instance = super(AutoRegisteringABCMeta, cls).__call__(*args, **kwargs)
        return instance

HTTPProxyConfig = collections.namedtuple('HTTPProxyConfig', ['host', 'port'])


# The following section is taken from https://github.com/django/django/blob/master/django/test/utils.py
# This is a relatively simple XML comparator implementation based on Python's minidom library.
# NOTE: different namespace aliases can break this code. The code superficial on namespaces. It ignores them
# In very rare cases when an element has 2 attributes with the same localName but their namespaces differ
# this implementation might say the document differs. It also avoids attribute sorting by comparing
# and attr_dict that it builds from minidom attributes.
#
# The Django Project is protected by the BSD Licence.


def strip_quotes(want, got):
    """
    Strip quotes of doctests output values:

    >>> strip_quotes("'foo'")
    "foo"
    >>> strip_quotes('"foo"')
    "foo"
    """
    def is_quoted_string(s):
        s = s.strip()
        return len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'")

    def is_quoted_unicode(s):
        s = s.strip()
        return len(s) >= 3 and s[0] == 'u' and s[1] == s[-1] and s[1] in ('"', "'")

    if is_quoted_string(want) and is_quoted_string(got):
        want = want.strip()[1:-1]
        got = got.strip()[1:-1]
    elif is_quoted_unicode(want) and is_quoted_unicode(got):
        want = want.strip()[2:-1]
        got = got.strip()[2:-1]
    return want, got


def compare_xml(want, got):
    """Tries to do a 'xml-comparison' of want and got.  Plain string
    comparison doesn't always work because, for example, attribute
    ordering should not be important. Comment nodes are not considered in the
    comparison. Leading and trailing whitespace is ignored on both chunks.

    Based on https://github.com/lxml/lxml/blob/master/src/lxml/doctestcompare.py

    This function is a close but not full implementation of fn:deep-equals.
    Possible scenario where this will yield a false positive result is where an element can have 2 arguments with
    the same name but different namespaces:

        i.e.: <elem ns1:myattr="1" /> != <elem ns2:myattr="1" /> if ns1 != ns2

    """
    _norm_whitespace_re = re.compile(r'[ \t\n][ \t\n]+')

    def norm_whitespace(v):
        return _norm_whitespace_re.sub(' ', v)

    def child_text(element):
        return ''.join(c.data for c in element.childNodes
                       if c.nodeType == Node.TEXT_NODE)

    def children(element):
        return [c for c in element.childNodes
                if c.nodeType == Node.ELEMENT_NODE]

    def norm_child_text(element):
        return norm_whitespace(child_text(element))

    def attrs_dict(element):
        return dict(element.attributes.items())

    def check_element(want_element, got_element):
        if want_element.tagName != got_element.tagName:
            return False
        if norm_child_text(want_element) != norm_child_text(got_element):
            return False
        if attrs_dict(want_element) != attrs_dict(got_element):
            return False
        want_children = children(want_element)
        got_children = children(got_element)
        if len(want_children) != len(got_children):
            return False
        for want, got in zip(want_children, got_children):
            if not check_element(want, got):
                return False
        return True

    def first_node(document):
        for node in document.childNodes:
            if node.nodeType != Node.COMMENT_NODE:
                return node

    want, got = strip_quotes(want, got)
    want = want.strip().replace('\\n', '\n')
    got = got.strip().replace('\\n', '\n')

    # If the string is not a complete xml document, we may need to add a
    # root element. This allow us to compare fragments, like "<foo/><bar/>"
    if not want.startswith('<?xml'):
        wrapper = '<root>%s</root>'
        want = wrapper % want
        got = wrapper % got

    # Parse the want and got strings, and compare the parsings.
    want_root = first_node(parseString(want))
    got_root = first_node(parseString(got))

    return check_element(want_root, got_root)