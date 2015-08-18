#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

# UpdateWorkItem

# tfsUrl from server object
# username from server object
# password from server object
# collectionName = input variable defined in synthetic
# teamProjectName = input variable defined in synthetic
# workItemId = input variable defined in synthetic
# workItemTitle = input variable defined in synthetic

import sys
import os
from java.lang import System
from com.microsoft.tfs.core.httpclient import UsernamePasswordCredentials
from com.microsoft.tfs.core.util import URIUtils
from com.microsoft.tfs.core import TFSTeamProjectCollection
from com.microsoft.tfs.core.clients.workitem import CoreFieldReferenceNames
from com.microsoft.tfs.core.clients.workitem import WorkItem
from com.microsoft.tfs.core.clients.workitem import WorkItemClient
from com.microsoft.tfs.core.clients.workitem.project import Project

if tfsServer is None:
  print "No server provided"
  sys.exit(1)

System.setProperty("com.microsoft.tfs.jni.native.base-directory", os.getcwd() + "/conf/native")

collectionUrl = tfsServer['url'] + "/" + collectionName

if username is None:
	username = tfsServer['username']
if password is None:
	password = tfsServer['password']
credentials = UsernamePasswordCredentials(username, password)

tpc = TFSTeamProjectCollection(URIUtils.newURI(collectionUrl), credentials)

project = tpc.getWorkItemClient().getProjects().get(teamProjectName)

workItemClient = project.getWorkItemClient()

workItem = workItemClient.getWorkItemByID(int(workItemId))

workItem.setTitle(workItemTitle)
workItem.save()
