#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
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
