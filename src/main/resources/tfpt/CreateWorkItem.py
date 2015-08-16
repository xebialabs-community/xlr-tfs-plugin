#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
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
