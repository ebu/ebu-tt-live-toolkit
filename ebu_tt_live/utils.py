
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
