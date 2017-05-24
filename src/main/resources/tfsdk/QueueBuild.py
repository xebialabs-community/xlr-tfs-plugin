#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os, sys, string, time
from com.microsoft.tfs.core import TFSTeamProjectCollection
from com.microsoft.tfs.core.clients.build.flags import BuildStatus, QueueStatus, QueryOptions
from com.microsoft.tfs.core.httpclient import UsernamePasswordCredentials
from com.microsoft.tfs.core.httpclient import NTCredentials
from com.microsoft.tfs.core.util import URIUtils
from java.lang import System


# Wait for the build to finish.
def wait_for_queued_build_to_finish(queued_build_item):
    print "Waiting for build to finish"
    while queued_build_item.getBuild() is None or not queued_build_item.getBuild().isBuildFinished():
        time.sleep(5)
        print "."
        queued_build_item.refresh(QueryOptions.ALL)


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

tfs_api_url = tfsServer['url'] + "/" + collectionName
print "Queue build in TFS instance via this REST API: %s\r" % tfs_api_url

# set up tfs
tpc = TFSTeamProjectCollection(URIUtils.newURI(tfs_api_url), credentials)
build_server = tpc.getBuildServer()

print "Build server version: [%s]" % build_server.getBuildServerVersion()
buildDefinitions = build_server.queryBuildDefinitions(teamProjectName)
print "Found %s build definition(s)." % len(buildDefinitions)

build_definition = build_server.getBuildDefinition(teamProjectName, buildDefinitionName)
build_request = build_definition.createBuildRequest()

#queue build
queued_build = build_server.queueBuild(build_request)
print "Queued build with ID= %s" % queued_build.getID()

# Wait for the queued build to finish.
wait_for_queued_build_to_finish(queued_build)

if queued_build.getStatus().contains(QueueStatus.COMPLETED):
    # Display the status of the completed build.
    build_detail = queued_build.getBuild()
    build_status = build_detail.getStatus()
    buildNumber = build_detail.getBuildNumber()
    buildStatus = build_server.getDisplayText(build_status)
    print "Build [%s] completed with status [%s]" % (buildNumber, buildStatus)
    if build_status != BuildStatus.SUCCEEDED:
        raise Exception("Build failed.")
else:
    raise Exception("Build canceled or did not finish in time.")
