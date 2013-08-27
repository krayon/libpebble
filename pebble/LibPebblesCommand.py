import sh, os
import websocket
import time
from multiprocessing import Process
from autobahn.websocket import *
from PblCommand import PblCommand
import pebble as libpebble
from DebugServerPebble import *

def start_service():
  factory = WebSocketServerFactory("ws://localhost:9000")
  factory.protocol = EchoServerProtocol
  factory.setProtocolOptions(allowHixie76 = True)
  listenWS(factory)
  reactor.run()

class LibPebbleCommand(PblCommand):
  def configure_subparser(self, parser):
    pass

  def run(self, args):
    try:
      ws = websocket.create_connection("ws://localhost:9000")
      ws.close()
    except:
      print "Didn't find a websocket server. creating one... create a long running server with  \n\npython DebugServerPebble.py\n\n"
      p = Process(target=start_service, args=())
      p.daemon = True
      p.start()
      time.sleep(3)

    self.pebble = libpebble.Pebble(using_lightblue=False, pair_first=False, using_ws=True)


class PblPingCommand(LibPebbleCommand):
  name = 'ping'
  help = 'Ping your Pebble project to your watch'

  def configure_subparser(self, parser):
    PblCommand.configure_subparser(self, parser)

  def run(self, args):
    LibPebbleCommand.run(self, args)
    self.pebble.ping(cookie=0xDEADBEEF)


class PblInstallCommand(LibPebbleCommand):
  name = 'install'
  help = 'Install your Pebble project to your watch'

  def configure_subparser(self, parser):
    PblCommand.configure_subparser(self, parser)
    parser.add_argument('bundle', type=str)

  def run(self, args):
    LibPebbleCommand.run(self, args)
    self.pebble.install_app(args.bundle, True)
