from subprocess import Popen, DEVNULL
from inspect import getsourcefile
from os.path import abspath
import time

class Server():
    def __init__(self):
        jar_path = abspath(getsourcefile(lambda:0))
        self.cmd = jar_path[:jar_path.find('java_server.py')] + 'EntryPoint.jar'
        """Output is suppressed to hide
        'WARN  on.impl.AbstractLexerBasedConverter  - Only terminal rules are supported by lexer based converters but got ID which is an instance of ParserRule' messages. 
        """
        self.proc = Popen(['java', '-jar', self.cmd], stdout=DEVNULL, stderr=DEVNULL)
        # Wait briefly so the MCNP gateway can get started properly.
        time.sleep(1)
        print('MCNP Gateway Server Started')

    def restart(self):
        self.proc = Popen(['java', '-jar', self.cmd], stdout=DEVNULL, stderr=DEVNULL)
        time.sleep(1)
        print('MCNP Gateway Server Started')

    def kill(self):
        Popen.kill(self.proc)
        print('MCNP Gateway Server Killed')