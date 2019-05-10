#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# GetWorkItem

# tfsUrl from server object
# username from server object
# password from server object
# collectionName = input variable defined in synthetic
# teamProjectName = input variable defined in synthetic
# workItemId = input variable defined in synthetic
# workItemTitle = output variable defined in synthetic

import sys
import os
from java.lang import System
from com.microsoft.tfs.core.httpclient import UsernamePasswordCredentials
from com.microsoft.tfs.core.httpclient import NTCredentials
from com.microsoft.tfs.core.util import URIUtils
from com.microsoft.tfs.core import TFSTeamProjectCollection

if tfsServer is None:
  print "No server provided"
  sys.exit(1)

System.setProperty("com.microsoft.tfs.jni.native.base-directory", os.getcwd() + "/conf/native")

collectionUrl = tfsServer['url'] + "/" + collectionName

if username is None:
    username = tfsServer['username']
if password is None:
    password = tfsServer['password']
if tfsServer['authenticationMethod'] == 'Ntlm':
    if domain is None:
        domain = tfsServer['domain']
    credentials = NTCredentials(username, domain, password)
else:
    credentials = UsernamePasswordCredentials(username, password)

tpc = TFSTeamProjectCollection(URIUtils.newURI(collectionUrl), credentials)

project = tpc.getWorkItemClient().getProjects().get(teamProjectName)

workItemClient = project.getWorkItemClient()

workItem = workItemClient.getWorkItemByID(int(workItemId))

workItemTitle = str(workItem.getTitle())
print ("Work item " + workItemId + " " + workItemTitle)
