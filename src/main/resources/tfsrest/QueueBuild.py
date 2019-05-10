#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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



