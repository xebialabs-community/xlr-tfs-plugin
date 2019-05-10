#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
