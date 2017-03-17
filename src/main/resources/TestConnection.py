#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys
from xlrhttp.HttpRequest import HttpRequest
import os
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
