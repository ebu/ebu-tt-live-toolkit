import re
from argparse import ArgumentParser
import os
from xml.dom import minidom
import shutil
from ebu_tt_live.bindings import ebuttdt
from datetime import timedelta


parser = ArgumentParser()
parser.add_argument('-i', '--input-file', dest='input_file', type=unicode, required=True)
parser.add_argument('-o', '--output-folder', dest='output_folder', type=unicode, required=True)


xml_doc_regex = re.compile(r'(?:\[.*?-)(\d+:\d+:\d+(?:\.\d+)?)(?:\]  String message: )((?:<\?xml)(?:.*?)(?:</tt:tt>))', flags=re.DOTALL | re.MULTILINE)


def main():
    args = parser.parse_args()
    with open(os.path.abspath(args.input_file), 'r') as input_file:
        input_text = input_file.read()

    matches = xml_doc_regex.findall(input_text)

    time_adjustment = timedelta(hours=7)

    folder_path = os.path.abspath(args.output_folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    elif not os.path.isdir(folder_path):
        raise Exception('Output folder needs to be a folder')

    sequence_numbers = set()
    file_names = list()

    doc_counter = 1
    for availability, item in matches:
        adjusted_availability = ebuttdt.FullClockTimingType(
            ebuttdt.FullClockTimingType(availability).timedelta + time_adjustment
        )
        dom = minidom.parseString(item)
        seq_no = dom.documentElement.getAttribute('ebuttp:sequenceNumber')
        if seq_no not in sequence_numbers:
            sequence_numbers.add(seq_no)
            file_name = 'log_{}.xml'.format(str(doc_counter))
            with open(os.path.join(folder_path, file_name), 'w') as output_file:
                output_file.write(dom.toprettyxml(indent='  '))
            doc_counter += 1
            file_names.append((str(adjusted_availability), file_name))

    with open(os.path.join(folder_path, 'manifest.txt'), 'w') as manifest_file:
        for begin, item in file_names:
            manifest_file.write('{},{}\n'.format(begin, item))


if __name__ == '__main__':
    main()
