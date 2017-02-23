#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import com.xhaus.jyson.JysonCodec as json

print "Executing CreateWorkItem.py ver 2015Jun28-1"

if tfsServer is None:
  print "No server provided"
  sys.exit(1)

contentType = 'application/json-patch+json'

request = HttpRequest(tfsServer, username, password)
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

