#!/usr/bin/python
import os
import re
import sys
import getopt
oracleHome = "C:\Oracle\Middleware\Oracle_Home"
domainName = "test_domain"
password = "admin123"
hostName = None
listenPort = None


print('--> About creating compact_domain...')
if listenPort == None:
 listenPort = 8192
if hostName == None:
 hostName = 'localhost'
if domainName == None:
 domainName = 'compact_domain'
if password == None:
 password = 'weblogic1'
domainMode = 'Compact'
domainLocation = oracleHome + '/user_projects/domains/' + domainName
wlsTemplateJar = oracleHome + '/wlserver/common/templates/wls/wls.jar'
print('--> Create ' + domainLocation + " on listen port " + str(listenPort) + ".") 
readTemplate(wlsTemplateJar, domainMode)
print('--> Configure AdminServer for ' + domainLocation + ".")
cd('/Security/base_domain/User/weblogic')
cmo.setPassword(password)
cd('/Server/AdminServer')
cmo.setName('AdminServer')
cmo.setStuckThreadMaxTime(1800)
cmo.setListenPort(listenPort)
cmo.setListenAddress(hostName)
writeDomain(domainLocation)
closeTemplate()
dumpStack()
print('--> Extend domain ' + domainLocation + ".")
readDomain(domainLocation)
jrfTemplateJar = oracleHome + '/wlserver/common/templates/wls/wls_jrf.jar'
print('--> Extend domain ' + domainLocation + " with template " + jrfTemplateJar)
addTemplate(jrfTemplateJar)
soaTemplateJar = oracleHome + '/soa/common/templates/wls/oracle.soa_template.jar'
print('--> Extend domain ' + domainLocation + " with template " + soaTemplateJar)
addTemplate(soaTemplateJar)
osbTemplateJar = oracleHome + '/osb/common/templates/wls/oracle.osb_template.jar'
print('--> Extend domain ' + domainLocation + " with template " + osbTemplateJar)
addTemplate(osbTemplateJar)
updateDomain()
closeDomain()
dumpStack()
print('--> Domain' + domainLocation + " successfully created.")
exit()