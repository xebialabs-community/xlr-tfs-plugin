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
from xlrhttp.HttpRequest import HttpRequest
import os;
from java.lang import System
from com.microsoft.tfs.core.httpclient import UsernamePasswordCredentials
from com.microsoft.tfs.core.httpclient import NTCredentials
from com.microsoft.tfs.core.util import URIUtils
from com.microsoft.tfs.core import TFSTeamProjectCollection


if configuration.preferredLibType == 'REST':

    # get the configuration properties from the UI
    params = { 'url': configuration.url, 'username' : configuration.username, 'password': configuration.password,  'proxyHost': configuration.proxyHost, 'proxyPort': configuration.proxyPort, 'domain': configuration.domain, 'authenticationMethod': configuration.authenticationMethod}

    # do an http request to the server
    response = HttpRequest(params).get('/_apis/projectcollections', contentType = 'application/json')
    
    print "Response from TFS: [%s]" % response.getResponse()
    print "Response status: [%s]" % response.status

    # check response status code, if is different than 200 exit with error code
    if response.status != 200:
        sys.exit(1)
elif configuration.preferredLibType == 'SDK':
    System.setProperty("com.microsoft.tfs.jni.native.base-directory", os.getcwd() + "/conf/native")

    collectionUrl = configuration.url + "/"
    if configuration.authenticationMethod == 'Ntlm':
        credentials = NTCredentials(configuration.username, configuration.domain, configuration.password)
    else:
        credentials = UsernamePasswordCredentials(configuration.username, configuration.password)

    tpc = TFSTeamProjectCollection(URIUtils.newURI(collectionUrl), credentials)
    workItemClient = tpc.getWorkItemClient()
