
from unittest import TestCase
from ebu_tt_live.documents import EBUTT3Document, EBUTT3DocumentSequence
from ebu_tt_live.bindings import ebuttdt
import gc
import os
from datetime import timedelta
from jinja2 import Environment, FileSystemLoader, Template
import weakref


raw_template = """<?xml version="1.0" ?>
<tt:tt
        ebuttp:sequenceIdentifier="test_memory_leak"
        ebuttp:sequenceNumber="{{ sequence_number }}"
        ttp:timeBase="media"
        tts:extent="800px 600px"
        xml:lang="en-GB"
        xmlns:ebuttm="urn:ebu:tt:metadata"
        xmlns:ebuttp="urn:ebu:tt:parameters"
        xmlns:tt="http://www.w3.org/ns/ttml"
        xmlns:ttp="http://www.w3.org/ns/ttml#parameter"
        xmlns:tts="http://www.w3.org/ns/ttml#styling"
        xmlns:xml="http://www.w3.org/XML/1998/namespace">
  <tt:head>
    <tt:metadata>
      <ebuttm:documentMetadata/>
    </tt:metadata>
    <tt:styling>
      <tt:style tts:fontSize="12px" xml:id="style1"/>
      <tt:style tts:fontSize="15px" xml:id="style2"/>
      <tt:style tts:color="red" tts:fontSize="12px" xml:id="style3"/>
    </tt:styling>
    <tt:layout>
      <tt:region style="style3" tts:extent="300px 150px" tts:origin="200px 450px" xml:id="region1"/>
    </tt:layout>
  </tt:head>
  <tt:body begin="{{ body_begin }}" style="style2">
    <tt:div region="region1" style="style1">
      <tt:p xml:id="ID005">
        <tt:span begin="00:00:01" end="00:00:02" xml:id="span1">Some example text...</tt:span>
        <tt:span begin="00:00:03" end="00:00:04" xml:id="span2">And another line</tt:span>
      </tt:p>
    </tt:div>
  </tt:body>
</tt:tt>
"""


class TestDocumentLeaks(TestCase):

    def setUp(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self._j2env = Environment(loader=FileSystemLoader(cur_dir))

    def _generate_document(self, sequence_number=1, offset=None):
        # offset is a timedelta object to help generate the timings
        if offset is None:
            offset = timedelta()

        # template_file = self._j2env.get_template('mem_prof_document.xml')
        template_file = Template(raw_template)
        temp_dict = {
            'sequence_number': sequence_number,
            'body_begin': ebuttdt.FullClockTimingType(offset)
        }

        doc = EBUTT3Document.create_from_xml(
            template_file.render(temp_dict)
        )
        # print 'doc id {} created'.format(id(doc))
        return doc

    def test_single_document_removed(self):

        gc.collect()

        doc = self._generate_document()

        doc.validate()
        doc.validate()
        doc.validate()
        doc.get_xml()
        doc.get_xml()
        doc.get_xml()
        doc.get_xml()
        gc.collect()
        doc.cleanup()
        wref = weakref.ref(doc)
        gc.collect()
        self.assertIsInstance(wref(), EBUTT3Document)
        del doc
        gc.collect()
        gc.collect()
        self.assertIsNone(wref())

    def test_many_documents_removed(self):

        doc_reserve = []
        doc_refs = []

        for number in xrange(1, 10):
            doc = self._generate_document(
                sequence_number=number,
                offset=timedelta(seconds=5*number)
            )
            doc.validate()
            doc.get_xml()
            doc_reserve.append(doc)
            doc_refs.append(weakref.ref(doc))
            del doc
        gc.collect()
        for item in doc_refs:
            self.assertIsInstance(item(), EBUTT3Document)
        del doc_reserve
        gc.collect()
        for item in doc_refs:
            self.assertIsNone(item())

    def test_documents_in_sequence(self):

        doc_refs = []
        doc1 = self._generate_document(
            sequence_number=1
        )
        doc_refs.append(weakref.ref(doc1))
        sequence = EBUTT3DocumentSequence.create_from_document(doc1)
        sequence.add_document(doc1)
        seq_ref = weakref.ref(sequence)
        del doc1
        for number in xrange(2, 10):
            doc = self._generate_document(
                sequence_number=number,
                offset=timedelta(seconds=5*number)
            )
            doc.validate()
            doc.get_xml()
            doc_refs.append(weakref.ref(doc))
            sequence.add_document(doc)
            del doc
        gc.collect()
        self.assertIsInstance(seq_ref(), EBUTT3DocumentSequence)
        for item in doc_refs:
            self.assertIsInstance(item(), EBUTT3Document)
        sequence.cleanup()
        del sequence
        gc.collect()
        self.assertIsNone(seq_ref())
        for item in doc_refs:
            self.assertIsNone(item())

    def test_discard_partial_sequence(self):

        doc1 = self._generate_document(sequence_number=1, offset=timedelta(seconds=0))
        doc2 = self._generate_document(sequence_number=2, offset=timedelta(seconds=5))
        doc3 = self._generate_document(sequence_number=3, offset=timedelta(seconds=10))

        doc_refs = [
            weakref.ref(doc1),
            weakref.ref(doc2),
            weakref.ref(doc3)
        ]

        sequence = EBUTT3DocumentSequence.create_from_document(doc1)
        seq_ref = weakref.ref(sequence)

        sequence.add_document(doc1)
        sequence.add_document(doc2)
        sequence.add_document(doc3)

        del doc1
        del doc2
        del doc3

        gc.collect()

        self.assertIsInstance(seq_ref(), EBUTT3DocumentSequence)
        for item in doc_refs:
            self.assertIsInstance(item(), EBUTT3Document)

        sequence.discard_before(doc_refs[1]())

        gc.collect()

        self.assertIsNone(doc_refs[0]())
        self.assertIsInstance(doc_refs[1](), EBUTT3Document)
        self.assertIsInstance(doc_refs[2](), EBUTT3Document)


