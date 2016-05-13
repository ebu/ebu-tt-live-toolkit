
from ebu_tt_live.documents import EBUTT3Document


doc1 = EBUTT3Document(
    time_base='clock',
    clock_mode='local',
    lang='en-GB',
    sequence_identifier='seq1',
    sequence_number=1
)

doc2 = EBUTT3Document(
    time_base='clock',
    clock_mode='local',
    lang='en-GB',
    sequence_identifier='seq1',
    sequence_number=2
)

doc3 = EBUTT3Document(
    time_base='clock',
    clock_mode='local',
    lang='en-GB',
    sequence_identifier='seq2',
    sequence_number=2
)

print hex(id(doc1))

print doc1 < doc2

print sorted([doc2, doc1])

print doc1 < doc3
