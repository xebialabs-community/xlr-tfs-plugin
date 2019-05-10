#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import re
import sys
from com.xebialabs.xlrelease.plugin.overthere import WinrmRemoteScript
from com.xebialabs.overthere.cifs import CifsConnectionBuilder

class WinrmRemoteScript2(WinrmRemoteScript):
    def __init__(self, username, password, address, remotePath, script, timeout, cifsPort):
        WinrmRemoteScript.__init__(self, username, password, address, remotePath, script, timeout)
        self.cifsPort = cifsPort

    def customize(self, options):
        self.super__customize(options)
        options.set(CifsConnectionBuilder.CIFS_PORT, cifsPort)

script = WinrmRemoteScript2(username, password, address, remotePath, script, timeout, cifsPort)
exitCode = script.execute()

output = script.getStdout()
err = script.getStderr()

if (exitCode == 0):
    print output
    (str,) = re.search('Work item ([0-9]+) created', output).groups()
    workItemNumber = int(str)
else:
    print "Exit code "
    print exitCode
    print
    print "#### Output:"
    print output

    print "#### Error stream:"
    print err
    print
    print "----"

    sys.exit(exitCode)
