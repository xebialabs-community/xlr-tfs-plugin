#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import com.xhaus.jyson.JysonCodec as json
from xlrhttp.HttpRequest import HttpRequest

print "Executing CreateWorkItem"

if tfsServer is None:
  print "No server provided"
  sys.exit(1)

contentType = 'application/json-patch+json'

request = HttpRequest(tfsServer, username, password, domain)
title_json = '{"path": "/fields/System.Title", "value": "%s", "op": "add"}' % workItemTitle
description_json = '{"path": "/fields/System.Description", "value": "%s", "op": "add"}' % workItemDescription
content = '[%s, %s]' % (title_json, description_json)
# define TFS Server url as http://server:port/tfs
response = request.patch('%s/%s/_apis/wit/workitems/$%s?api-version=1.0' % (collectionName, teamProjectName, workItemType), content, contentType=contentType)
httpStatusCode = response.status

if httpStatusCode == 200:
  workItemId = json.loads(response.response)['id']
  print "New work item id is %d" % workItemId
else:
  print "Error in creating Work Item. Return status %s" % httpStatusCode
  print response.response
  sys.exit(1)

