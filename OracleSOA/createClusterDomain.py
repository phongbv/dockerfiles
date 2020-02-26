# Domain Configurations 

adminUser = weblogic
adminPassword = Welcome1
adminURL =http://localhost:7001
domainsHome = /u01/oracle/soa/domains
domainName = dev_domain
serverStartMode = dev

# Admin Server 

AdminServer.listenAddress = localhost
AdminServer.port = 8001
AdminServer.SSLEnabled = true
AdminServer.SSLPort = 8001

ADM_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1532m -Dweblogic.Stdout='+LOG_FOLDER+'AdminServer.out -Dweblogic.Stderr='+LOG_FOLDER+'AdminServer_err.out'
OSB_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1024m '
SOA_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=1024m -Xms1024m -Xmx2048m '


DB_CONNECTION_URL = 'jdbc:oracle:thin:@ora12c:1521/orcl'
SCHEMA_PREFIX  = 'PHONG'
DBPASSWORD     = 'phong#2020'

#Machine
total.machine.count = 1
machine.1.name=server1
machine.1.listenerAddress=localhost
machine.1.nodemanagerPort=5556
                

# ManageServers
total.ms.count = 4

ms.1.name = OsbServer1
ms.1.ListenPort = 8011
ms.1.ListenAddress = localhost
ms.1.machine = server1

ms.2.name = OsbServer2
ms.2.ListenPort = 8012
ms.2.ListenAddress = localhost
ms.2.machine = server1

ms.3.name = SoaServer1
ms.3.ListenPort = 8001
ms.3.ListenAddress = localhost
ms.3.machine = server1

ms.4.name = SoaServer2
ms.4.ListenPort = 8002
ms.4.ListenAddress = localhost
ms.4.machine = server1

#Cluster
total.cluster.count = 2

cluster.1.name=SoaCluster
cluster.1.clusterMessagingMode=unicast
cluster.1.ms=SoaServer1,SoaServer2

cluster.2.name=OsbCluster
cluster.2.clusterMessagingMode=unicast

cluster.2.ms=OsbServer1,OsbServer2