#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os, sys, string, time
from java.lang import System
from com.microsoft.tfs.core.httpclient import UsernamePasswordCredentials
from com.microsoft.tfs.core.httpclient import NTCredentials
from com.microsoft.tfs.core.util import URIUtils
from com.microsoft.tfs.core import TFSTeamProjectCollection
from com.microsoft.tfs.core.clients.workitem import CoreFieldReferenceNames

# load the <XL_RELEASE>/conf/native files
System.setProperty("com.microsoft.tfs.jni.native.base-directory", os.getcwd() + "/conf/native")

if tfsServer is None:
    print "No server provided."
    sys.exit(1)

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

tfsAPIUrl = tfsServer['url'] + "/" + collectionName
print "Generating Work Items in TFS instance via this REST API: %s\r" % (tfsAPIUrl)

# set up tfs
tpc = TFSTeamProjectCollection(URIUtils.newURI(tfsAPIUrl), credentials)

print "\r\rprojectName name: %s \r" % (projectName)
project = tpc.getWorkItemClient().getProjects().get(projectName)
print "\r\r created project object"

# Find the work item type matching the specified name.
bugWorkItemType = project.getWorkItemTypes().get(workItemType)   # e.g., get("Bug")

# Create a new work item of the specified type.
newWorkItem = project.getWorkItemClient().newWorkItem(bugWorkItemType)  # e.g., Bug

# Set the title on the work item.
newWorkItem.setTitle(workItemTitle)

# Add a comment as part of the change
newWorkItem.getFields().getField(CoreFieldReferenceNames.HISTORY).setValue("<p>%" + workItemComment + "</p>")

# Save the new work item to the server.
print "\r -- about to call newWorkItem.save() \r"
newWorkItem.save();
print "\r -- past newWorkItem save\r"

workItemId = str(newWorkItem.getID())
print "Created Work Item %s successfully created in TFS at %s.\r" % (workItemId, tfsAPIUrl)
