#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import com.xhaus.jyson.JysonCodec as json
from tempfile import mkdtemp

print "Executing GetTfsRepoArtifacts.py"

if tfsServer is None:
  print "No server provided"
  sys.exit(1)

request = HttpRequest(tfsServer)
if username:
	request.username = username
if password:
  request.password = password

#contentType = "application/octet-stream"

response = request.get('%s/_apis/git/repositories?api-version=1.0' % collectionName)

httpStatusCode = response.status

if response.isSuccessful():
  repositoryId = json.loads(response.response)['value'][0]['id']
  print "Repository id is %s" % repositoryId
else:
  print "Error in getting repositories"
  sys.exit(1)

response = request.get('%s/_apis/git/repositories/%s/items?api-version=1.0&scopepath=%s' % (collectionName,repositoryId, scopePath))

if response.isSuccessful():
  if artifactTempDir is None or artifactTempDir == "":
    artifactTempDir = mkdtemp()
  tempFile = open (artifactTempDir + "/" + scopePath, "w")
  tempFile.write(response.response)
  tempFile.close()
  print "Successful retrieval of %s to %s" % (scopePath, artifactTempDir) 
else:
  print "Error in getting repository item(s)"
  sys.exit(1)
