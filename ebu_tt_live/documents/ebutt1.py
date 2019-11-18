from ebu_tt_live import bindings
from ebu_tt_live.documents import SubtitleDocument
from ebu_tt_live.documents.base import EBUTTDocumentBase
from ebu_tt_live.documents.time_utils import TimelineUtilMixin
from .base import TimeBase
from pyxb import BIND

class EBUTT1Document(TimelineUtilMixin, SubtitleDocument, EBUTTDocumentBase):
    """
    This class wraps the binding object representation of the XML and provides the features the applications in the
    specification require.
    """

    # The XML binding holding the content of the document
    _ebutt1_content = None

    def _cmp_key(self):
        raise NotImplementedError()

    def __init__(self, time_base, lang, head, clock_mode=None,
                 frame_rate=None, frame_rate_multiplier=None,
                 drop_mode=None, marker_mode=None, active_area=None):
        self.load_types_for_document()
        if not clock_mode and time_base is TimeBase.CLOCK:
            clock_mode = 'local'
        if time_base is TimeBase.SMPTE:
            if not frame_rate:
                frame_rate = '30'
            if not frame_rate_multiplier:
                frame_rate_multiplier = '1 1'
            if not drop_mode:
                drop_mode = 'nonDrop'
            if not marker_mode:
                marker_mode = 'discontinuous'

        self._ebutt1_content = bindings.tt(
            timeBase=time_base,
            clockMode=clock_mode,
            frameRate=frame_rate,
            frameRateMultiplier=frame_rate_multiplier,
            dropMode=drop_mode,
            markerMode=marker_mode,
            lang=lang,
            activeArea=active_area,
            head=head,
            body=BIND()
        )
        self.validate()

    def validate(self):
        # Run validation

        result = self._ebutt1_content.validateBinding(
            availability_time=None,
            document=self
        )

    @classmethod
    def create_from_raw_binding(cls, binding):
        cls.load_types_for_document()
        instance = cls.__new__(cls)
        instance._ebutt1_content = binding
        instance.validate()
        return instance

    @classmethod
    def create_from_xml(cls, xml):
        cls.load_types_for_document()
        instance = cls.create_from_raw_binding(
            binding=bindings.CreateFromDocument(xml_text=xml))
        return instance

    @classmethod
    def load_types_for_document(cls):
        bindings.load_types_for_document('ebutt1')

    @property
    def lang(self):
        return self._ebutt1_content.lang

    @property
    def clock_mode(self):
        return self._ebutt1_content.clockMode

    def add_div(self, div):
        body = self._ebutt1_content.body
        body.append(div)

    def set_begin(self, begin):
        self._ebutt1_content.body.begin = begin

    def set_end(self, end):
        self._ebutt1_content.body.end = end

    @property
    def binding(self):
        return self._ebutt1_content

    def get_xml(self):
        return self._ebutt1_content.toxml()

    def get_dom(self):
        return self._ebutt1_content.toDOM()

    def get_element_by_id(self, elem_id, elem_type=None):
        return self.binding.get_element_by_id(
            elem_id=elem_id, elem_type=elem_type)
