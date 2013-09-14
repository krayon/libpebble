#!/usr/bin/env python2

import argparse
import logging
import pebble as libpebble
import code
import readline
import rlcompleter
import websocket
import sys
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.websocket import *
from pebble.EchoServerProtocol import *

def start_repl(pebble):
    readline.set_completer(rlcompleter.Completer(locals()).complete)
    readline.parse_and_bind('tab:complete')
    code.interact(local=locals())

logging.basicConfig(format='[%(levelname)-8s] %(message)s', level = logging.DEBUG)

parser = argparse.ArgumentParser(description='An interactive environment for libpebble.')
parser.add_argument('--pebble_id', metavar='PEBBLE_ID', type=str, help='the last 4 digits of the target Pebble\'s MAC address, or a complete MAC address')
parser.add_argument('-w', '--websocket', action="store_true", help='use WebSockets API')
parser.add_argument('--host', metavar='HOST', type=str, default=libpebble.DEFAULT_WEBSOCKET_HOST, help='the host of the WebSocket server to connect to when using the WebSockets API')
parser.add_argument('-b', '--lightblue', action="store_true", help='use LightBlue bluetooth API')
parser.add_argument('--pair', action="store_true", help='pair to the pebble from LightBlue bluetooth API before connecting.')
args = parser.parse_args()

pebble = libpebble.Pebble(args.pebble_id)

if args.websocket:
    echo_server_start(libpebble.DEFAULT_WEBSOCKET_PORT)
    pebble.connect_via_websocket(args.host)
elif args.lightblue:
    pebble.connect_via_lightblue(pair_first=args.pair)
else:
    pebble.connect_via_serial()

start_repl(pebble)
