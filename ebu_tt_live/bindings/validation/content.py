
from .timing import TimingValidationMixin
from .base import SemanticValidationMixin, IDMixin
from ebu_tt_live.errors import DiscardElement
from pyxb.binding.basis import NonElementContent


class ContentContainerMixin(object):

    def is_empty(self):
        """
        This check is made necessary by some splitting edge cases of content. To make empty containers are not included
        one should check if there really was anything useful in the container. This function is meant to be
        implemented by the subclasses of this class to make sure the container checks for the right constraints.
        :return:
        """
        raise NotImplementedError()

    def _assert_empty_container(self):
        if self.is_empty():
            raise DiscardElement()


class SubtitleContentContainer(
        ContentContainerMixin, IDMixin, TimingValidationMixin, SemanticValidationMixin):

    def contains_subtitles(self):
        if len(self.br):
            return True

        if len(self.span):
            return True

        for item in self.orderedContent():
            # Last resort check for text content
            if isinstance(item, NonElementContent):
                if not item.value.isspace():
                    return True

        return False

    def is_empty(self):
        return not self.contains_subtitles()
