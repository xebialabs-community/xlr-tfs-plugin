#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
from xlrhttp.HttpRequest import HttpRequest

if tfsServer is None:
  print "No server provided"
  sys.exit(1)

request = HttpRequest(tfsServer, username, password, domain)
url = "%s/%s/_apis/tfvc/changesets?api-version=1.0" % (collection,project) 

response = request.get(url)

if not response.isSuccessful():
  raise Exception("Error in getting repositories. Server return [%s], with content [%s]" % (response.status, response.response))

json_object = json.loads(response.response)

commits = json_object["value"]
latest_commit = commits[0]
changesetId = latest_commit["changesetId"]

triggerState = str(changesetId)
