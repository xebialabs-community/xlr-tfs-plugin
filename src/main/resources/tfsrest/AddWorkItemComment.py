#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys

print "Executing CreateWorkItem.py ver 2015Jun28-1"

if tfsServer is None:
  print "No server provided"
  sys.exit(1)

contentType = 'application/json-patch+json'

request = HttpRequest(tfsServer, username, password)
comment_json = '{"path": "/fields/System.History", "value": "%s", "op": "add"}' % workItemComment
content = '[%s]' % (comment_json)
# define TFS Server url as http://server:port/tfs
response = request.patch('%s/_apis/wit/workitems/%s?api-version=1.0' % (collectionName, workItemId), content, contentType=contentType)
httpStatusCode = response.status

if httpStatusCode == 200:
  print "Comment updated."
else:
  print "Error in creating Work Item. Return status %s" % httpStatusCode
  print response.response
  sys.exit(1)

