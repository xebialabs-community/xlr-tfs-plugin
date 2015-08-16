#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import com.xhaus.jyson.JysonCodec as json

print "Executing CreateWorkItem.py ver 2015Jun28-1"

if tfs2015Server is None:
  print "No server provided"
  sys.exit(1)

contentType = 'application/json-patch+json'

request = HttpRequest(tfs2015Server)
content = '[{"path": "/fields/System.Title", "value": "%s", "op": "add"}]' % workItemTitle
response = request.patch('%s/%s/_apis/wit/workitems/$%s?api-version=1.0' % (collection, teamProject, workItemType), content, contentType=contentType)
httpStatusCode = response.status
print httpStatusCode
print response.response

if httpStatusCode == 200:
  print "New work item id is %d" % json.loads(response.response)['id']
else:
  print "Error in creating Work Item"
  sys.exit(1)
  
