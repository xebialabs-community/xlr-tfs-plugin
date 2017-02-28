#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json, sys, time
from xlrhttp.HttpRequest import HttpRequest

print "Executing QueueBuild"

if tfsServer is None:
    print "No server provided"
    sys.exit(1)

contentType = 'application/json'

request = HttpRequest(tfsServer, username, password, domain)

response = request.get('%s/%s/_apis/build/definitions?api-version=2.0&name=%s' % (collectionName, teamProjectName, buildDefinitionName))

if not response.isSuccessful():
    raise Exception("Error fetching build definition. Server return [%s], with content [%s]" % (response.status, response.response))
print response.response
json_response = json.loads(response.getResponse())
if json_response["count"] != 1:
    raise Exception("Error fetching build definition. Server return [%s], with content [%s]" % (response.status, response.response))

build_definition_id = json.loads(response.getResponse())["value"][0]["id"]

# Queue build
content = '{"definition": { "id": %s }}' % build_definition_id
response = request.post('%s/%s/_apis/build/builds?api-version=2.0' % (collectionName, teamProjectName), content, contentType=contentType)

if not response.isSuccessful():
    raise Exception("Failed to queue build. Server return [%s], with content [%s]" % (response.status, response.response))

json_response = json.loads(response.getResponse())
build_id = json_response["id"]
build_number = json_response["buildNumber"]
build_status = json_response["status"]

while build_status != "completed":
    time.sleep(5)
    response = request.get('%s/%s/_apis/build/builds/%s?api-version=2.0' % (collectionName, teamProjectName, build_number))
    json_response = json.loads(response.getResponse())
    build_status = json_response["status"]

buildStatus = json_response["result"]
buildNumber = json_response["buildNumber"]

if buildStatus != "succeeded":
    raise Exception("Build failed with status [%s]" % buildStatus)



