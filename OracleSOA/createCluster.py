#!/usr/bin/python
# Author : Tim Hall
# Save Script as : create_cluster.py

import time
import getopt
import sys
import re

# Get location of the properties file.
properties = 'mv-dev.properties'
try:
   opts, args = getopt.getopt(sys.argv[1:],"p:h::",["properies="])
except getopt.GetoptError:
   print 'create_cluster.py -p <path-to-properties-file>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'create_cluster.py -p <path-to-properties-file>'
      sys.exit()
   elif opt in ("-p", "--properties"):
      properties = arg
print 'properties=', properties

# Load the properties from the properties file.
from java.io import FileInputStream
 
propInputStream = FileInputStream(properties)
configProps = Properties()
configProps.load(propInputStream)

# Set all variables from values in properties file.
adminUsername=configProps.get("admin.username")
adminPassword=configProps.get("admin.password")
adminURL=configProps.get("admin.url")
clusterName=configProps.get("cluster.name")
clusterAddress=configProps.get("cluster.address")

# Display the variable values.
print 'adminUsername=', adminUsername
print 'adminPassword=', adminPassword
print 'adminURL=', adminURL
print 'clusterName=', clusterName
print 'clusterAddress=', clusterAddress

# Connect to the AdminServer.
connect(adminUsername, adminPassword, adminURL)

edit()
startEdit()

# Create cluster.
cd('/')
cmo.createCluster(clusterName)

cd('/Clusters/' + clusterName)
cmo.setClusterMessagingMode('unicast')
cmo.setClusterBroadcastChannel('')
cmo.setClusterAddress(clusterAddress)

save()
activate()

disconnect()
exit()