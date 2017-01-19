
import re
import argparse
import os
import shutil
import sys

_subito_log_xml_regex = re.compile(
    r'^(?P<datetime_stamp>\[[0-9]{4}/[0-9]{2}/[0-9]{2}-(?P<time_stamp>[0-9:\-/.]*?)\])  '
    r'(?P<xml_data>[<][?]xml .*?sequenceIdentifier="(?P<seq_id>.*?)".*?'
    r'sequenceNumber="(?P<seq_no>.*?)".*?[<]/tt:tt[>]$)+',
    flags=re.DOTALL | re.MULTILINE
)

parser = argparse.ArgumentParser(
    description='Convert Subito log file to filesystem carriage spec'
)
parser.add_argument(dest='log_file', type=argparse.FileType('r'), metavar='LOG_FILE')
parser.add_argument('-o', '--output-dir', dest='output_dir', metavar='DIR', default=None)
parser.add_argument('-f', '--force', dest='force', action='store_true', default=False)


def main():
    args = parser.parse_args()
    log_content = args.log_file.read()
    results = _subito_log_xml_regex.finditer(log_content)
    export = False
    manifest_lines = []

    if args.output_dir is not None:
        # Doing the export
        output_path = os.path.abspath(args.output_dir)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            export = True
        elif args.force is True:
            shutil.rmtree(output_path)
            os.makedirs(output_path)
            export = True
        else:
            print 'Directory exists already'
            sys.exit(-1)

    for item in results:
        print item.group('time_stamp'), item.group('seq_id'), item.group('seq_no')
        if export is True:
            filename = '{}_{}.xml'.format(item.group('seq_id').replace(' ', '_'), item.group('seq_no'))
            with open(
                os.path.join(output_path, filename),
                'w'
            ) as xml_file:
                xml_file.write(item.group('xml_data'))
                manifest_lines.append(
                    '{},{}'.format(item.group('time_stamp'), filename)
                )

    if export is True:
        with open(
            os.path.join(output_path, 'manifest.txt'),
            'w'
        ) as manifest_file:
            manifest_file.write('\n'.join(manifest_lines))


if __name__ == '__main__':
    main()
