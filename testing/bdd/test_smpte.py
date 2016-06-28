
from pytest_bdd import scenarios, given, then
import pytest
from .common import load_template
from ebu_tt_live.documents import EBUTT3Document

scenarios('features/validation/smpte_constraints.feature')

@given(
    'a xml file <xml_file>'
)
def template_file(xml_file):
    return load_template(xml_file)

@given(
    'it has timeBase <time_base>'
)
def time_base(time_base):
    return time_base

@given(
    'it has frameRate <frame_rate>'
)
def frame_rate(frame_rate):
    return frame_rate

@then(
    'document is valid'
)
def valid_doc(template_file, time_base, frame_rate=None):
    xml_file = template_file.render(time_base=time_base, frame_rate=frame_rate)
    document = EBUTT3Document.create_from_xml(xml_file)

@then(
    'document is invalid'
)
def invalid_doc(template_file, time_base, frame_rate=None):
    xml_file = template_file.render(time_base=time_base, frame_rate=frame_rate)
    # TODO: Standardize exception classes upon validation
    with pytest.raises(Exception):
        document = EBUTT3Document.create_from_xml(xml_file)
