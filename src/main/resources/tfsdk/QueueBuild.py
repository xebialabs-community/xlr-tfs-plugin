#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import os, sys, string, time
from com.microsoft.tfs.core import TFSTeamProjectCollection
from com.microsoft.tfs.core.clients.build.flags import BuildStatus, QueueStatus, QueryOptions
from com.microsoft.tfs.core.httpclient import UsernamePasswordCredentials
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
