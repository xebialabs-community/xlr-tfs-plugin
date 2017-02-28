#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import com.xhaus.jyson.JysonCodec as json
from tempfile import mkdtemp
from xlrhttp.HttpRequest import HttpRequest

print "Executing GetTfsRepoArtifacts"

if tfsServer is None:
  print "No server provided"
  sys.exit(1)

request = HttpRequest(tfsServer, username, password, domain)
response = request.get('%s/_apis/git/repositories?api-version=1.0' % collectionName)

if not response.isSuccessful():
  raise Exception("Error in getting repositories. Server return [%s], with content [%s]" % (response.status, response.response))

repository_id = json.loads(response.response)['value'][0]['id']
print "Repository id is %s" % repository_id

response = request.get('%s/_apis/git/repositories/%s/items?api-version=1.0&scopepath=%s' % (collectionName, repository_id, scopePath))

if not response.isSuccessful():
    raise Exception("Error in getting repository item(s). Server return [%s], with content [%s]" % (response.status, response.response))

if artifactTempDir is None or artifactTempDir == "":
    artifactTempDir = mkdtemp()
temp_file = open (artifactTempDir + "/" + scopePath, "w")
temp_file.write(response.response)
temp_file.close()
print "Successful retrieval of %s to %s" % (scopePath, artifactTempDir)
