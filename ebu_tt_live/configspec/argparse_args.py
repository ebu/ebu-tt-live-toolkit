"""
This file is meant to keep our configurator compatible with the built-in python argparse package.
"""

import argparse


def get_ws_args(subparsers):
    ws_parser = subparsers.add_parser('websocket')
    ws_parser.add_argument('-u', '--websocket-url', dest='websocket_url',
                        help='URL for the websocket address to connect to',
                        default='ws://localhost:9000')
    ws_parser.add_argument('-s', '--websocket-channel', dest='websocket_channel',
                        help='Channel to connect to for websocket',
                        default='TestSequence1')


def get_proxy_args():
    pass


def get_ebuttd_conversion_args():
    pass


def get_segmentation_args():
    pass


def get_sequence_export_args():
    pass


def sequence_import_args():
    pass


def get_simple_producer_args():
    pass
