# xlr-tfs-plugin

This plugin offers an interface from XL Release to Team Foundation Server to create, update and retrieve Work Items. 

Various APIs are supported:  Team Foundation Power Tools, TFS REST API, and the TFS SDK.

## Team Foundation Power Tools
The following actions are supported:

### CreateWorkItem
The CreateWorkItem.py script creates a new Work Item by executing a remote Windows batch wrapper script, CreateWorkItems.bat.  Input parameters are Project, Type, Collection, Title, AssignedTo, and Description; the script returns the number of the Work Item created.  

![screenshot of createWorkItem](screenshots/xlr-tfs2013-plugin-2.png)

### GetWorkItem
The GetWorkItem.py script retrieves a Work Item given its number and collection using the GetWorkItem.bat wrapper script.  Input parameters are workItemNumber and collection.

![screenshot of getWorkItem](screenshots/xlr-tfs2013-plugin-3.png)

### UpdateWorkItem
The UpdateWorkItem.py script updates a Work Item given its number, collection, and set of update fields and values in the format `fieldname1=value1;fieldname2=value2`.  See an example of setting `State=Done` at the end of this document.

![screenshot of updateWorkItem](screenshots/xlr-tfs2013-plugin-4.png)

### Notes:  
The TFS machine must have Microsoft Visual Studio Team Foundation Server 2013 Update 2 Power Tools installed.  

The CreateWorkItem.bat, GetWorkItem.bat, and UpdateWorkItem.bat scripts must be placed in a location on the TFS machine.  The default location is C:\xlr-tfs2013-plugin.

A field is provided for the Windows CIFS port (default is 445) to allow overriding a blocked port.

The functionality will be enhanced as specific needs materialize.

### Example configuration

Here is a basic workflow of four items to create a Work Item, then retrieve it, update it, and retrieve it again to see the modification.

![screenshot of release template](screenshots/xlr-tfs2013-plugin-1.png)

The variables appearing in the above screenshots are set in this manner:

![screenshot of release variables](screenshots/xlr-tfs2013-plugin-5.png)

Note that workItemNumber is set as an output variable by the createWorkItem task.

Successful execution of the release results in the following output:

**Create Work Item**

![screenshot of createWorkItem output](screenshots/xlr-tfs2013-plugin-6.png)

**Get Work Item, note State=New**

![screenshot of createWorkItem output](screenshots/xlr-tfs2013-plugin-7.png)

**Update Work Item**

![screenshot of createWorkItem output](screenshots/xlr-tfs2013-plugin-8.png)

**Get Work Item, note State=Done**

![screenshot of createWorkItem output](screenshots/xlr-tfs2013-plugin-9.png)

## TFS REST API

This plugin offers an interface from XL Release to Team Foundation Server via the REST API valid for work items in TFS 2015.  It provides a createWorkItem.py script that creates a Work Item given Collection, Project, Type and Title parameters.

The functionality will be enriched with additional Work Item fields as specific needs materialize.

Note:  HttpRequest.py in older versions of XL Release must be enhanced to support the HTTP PATCH method.  See https://github.com/droberts2013/xl-release/server/src/main/resources/pythonutil/HttpRequest.py if necessary.  Place this custom file in <xl-release-server>/ext/pythonutil.

## TFS SDK

The TFS SDK depends on the following configuration changes in XL Release:

1.  Script.policy file — confirm these lines:

permission  java.util.PropertyPermission "\*", "read, write";
permission java.lang.RuntimePermission "shutdownHooks";
permission java.io.FilePermission "conf/\*", "read";
permission java.io.FilePermission "lib/\*", "read";
permission java.io.FilePermission "plugins/\*", "read";
permission java.security.AllPermission;

2. Add the library com.microsoft.tfs.sdk-11.0.0.jar to /lib.

3.  Unzip native.zip in the <xl-release-server>/conf directory. 