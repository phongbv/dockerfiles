###################################################################
###################################################################
# This script contains common utility methods used to configure
# a SOA profile in offline mode.
#
# These methods may be called by the SOA install, or could possibly
# be used by a WLST command for configuration of a SOA Profile in offline
# mode.
#
# NOTE: Any changes made to this file must also be ade to soaOfflineSetupProfileCommonCmd.py
#       These files are effectively the same with the exception that the soaOfflineSetupProfileCommonCmd.py file must import 
#       the wlstModule in order to work in command line mode, while this file (soaOfflineSetupProfileCommon.py)
#       is used as part of the server install and runns in a different context that does not support
#       importing modules since it is called from a final.py script.
#
###################################################################
###################################################################

def printDebug(debugMessage):
    print('SOA Offline Profile Common: ' + debugMessage + '\n')

import java.lang.Object as javaObject;
import java.lang.ClassLoader as javaClassLoader;
import java.lang.Class as javaClass;
from java.util import Properties;
from java.io import InputStream;
from java.io import FileInputStream;
from java.io import FileOutputStream;
from java.io import File;
from java.net import URL as javaURL;
from java.net import URLClassLoader;

# This method is a workaround for the classpath issues with WLST/Jython
def addJarToClassPath(pathToJar):
    jarURL = File(pathToJar).toURL()
    systemClassLoader = javaClassLoader.getSystemClassLoader()
    parametersArray = jarray.array([javaURL], javaClass)
    method = URLClassLoader.getDeclaredMethod('addURL', parametersArray)
    method.setAccessible(1)
    invokeParameters = jarray.array([jarURL], javaObject)
    method.invoke(systemClassLoader, invokeParameters)


# setup classpath prior to import statements
def setupFabricClasspath(mwHome):

    # setup paths to jars required for default profile mapping
    fabricRuntimeJarPath = mwHome + File.separatorChar + 'soa' + File.separatorChar + 'soa' + File.separatorChar + 'modules' + File.separatorChar + 'oracle.soa.fabric_11.1.1' + File.separatorChar + 'fabric-runtime.jar'

    digesterJarPath = mwHome + File.separatorChar + 'oracle_common' + File.separatorChar + 'modules' + File.separatorChar + 'org.apache.commons.digester_1.8.jar'

    soaMgmtJarPath = mwHome + File.separatorChar + 'soa' + File.separatorChar + 'soa' + File.separatorChar + 'modules' + File.separatorChar + 'oracle.soa.mgmt_11.1.1' + File.separatorChar + 'soa-infra-mgmt.jar'

    apacheLoggingJarPath = mwHome + File.separatorChar + 'oracle_common' + File.separatorChar + 'modules' + File.separatorChar + 'org.apache.commons.logging_1.1.1.jar'

    apacheLogging12JarPath = mwHome + File.separatorChar + 'oracle_common' + File.separatorChar + 'modules' + File.separatorChar + 'org.apache.commons.logging_1.2.jar'


    # PS3 uses this. Previous reference can be removed once this new
    # jar shows up and old one goes away - adding both for backward
    # compatibility during pickup
    beanUtilsJarPath = mwHome + File.separatorChar + 'oracle_common' + File.separatorChar + 'modules' + File.separatorChar + 'thirdparty'+ File.separatorChar+'commons-beanutils-1.9.3.jar'

    # Fix for bug-25808585 : NoClassDefFound error in soaOfflineSetupProfileCommon.py
    # Raj: I am totally unclear why we don’t have any issue now in our regular PS3 environments.
    # Robert: Because Mark’s environment is running the FMW LCM Framework with embedded WLST running from a custom classloader.
    #         AppToCloud uses this same framework but we are not applying templates to domains so we have not observed this problem.
    # Mark: Our code runs from FAPROV, against an FMWTOOLS shiphome.  We start up a WLST Interpreter in our code and issue commands to it.  
    #       We are not just running wlst.sh.  So any assumptions or happy accidents with respect to what is on the system classpath or any 
    #       other one when your script runs do not necessarily apply.  When we test this we run the code from a script, not from the full FAPROV, 
    #       but the test is as close as we can get to what they do without actually running the whole FAPROV process.  They run our code in the configure step.  
    #       Our tests run against an OH and DB that FA gave us from a backup taken right before they would run our code.
    collectionsJarPath = mwHome + File.separatorChar + 'oracle_common' + File.separatorChar + 'modules' + File.separatorChar + 'com.bea.core.apache.commons.collections.jar'
    xmlparserJarPath = mwHome + File.separatorChar + 'oracle_common' + File.separatorChar + 'modules' + File.separatorChar + 'oracle.xdk' + File.separatorChar + 'xmlparserv2_sans_jaxp_services.jar'
	
    # add fabric-runtime.jar to the classpath (not sure if appending this actually works?)
    sys.path.append(fabricRuntimeJarPath)
    sys.path.append(digesterJarPath)
    sys.path.append(soaMgmtJarPath)
    sys.path.append(apacheLoggingJarPath)
    sys.path.append(apacheLogging12JarPath)
    sys.path.append(beanUtilsJarPath)
    sys.path.append(collectionsJarPath)
    sys.path.append(xmlparserJarPath)
    
    # attempt this temporary workaround for now
    addJarToClassPath(fabricRuntimeJarPath)
    addJarToClassPath(digesterJarPath)
    addJarToClassPath(soaMgmtJarPath)
    addJarToClassPath(apacheLoggingJarPath)
    addJarToClassPath(apacheLogging12JarPath)
    addJarToClassPath(beanUtilsJarPath)
    addJarToClassPath(collectionsJarPath)
    addJarToClassPath(xmlparserJarPath)



# Common Utility Methods
def getDomainLocation():
    # attempt to get domain location using CIE setup
    domainLocation = retrieveObject('DOMAIN_DIRECTORY')
    return domainLocation


def getDomainConfigDirectory(domainLocation):
    return  domainLocation + File.separatorChar + 'config' + File.separatorChar + 'fmwconfig'


def getDefaultSOAProfileName(templateName):
    # create dictionary that maps template names to default profile names
    # any change to the default profile names should also modify this dictionary
    templateToProfileDictionary = {}
    templateToProfileDictionary['SOA'] = 'SOA FOUNDATION'
    templateToProfileDictionary['B2B'] = 'SOA FOUNDATION WITH B2B'
    templateToProfileDictionary['BPM'] = 'BPM BASIC'
    templateToProfileDictionary['HEALTHCARE'] = 'SOA FOUNDATION WITH HEALTHCARE'
    templateToProfileDictionary['SOA RECONFIG'] = 'SOA CLASSIC'
    templateToProfileDictionary['BPM RECONFIG'] = 'BPM CLASSIC'

    # query to see if mapping exists for passed-in template
    if templateToProfileDictionary.has_key(templateName):
        return templateToProfileDictionary[templateName]
    else:
        return None


def getCurrentProfileName(domainConfigurationDirectory):
    from oracle.fabric.profiles.impl import ProfileConstants;
    fileName = domainConfigurationDirectory + File.separatorChar + 'server-profile-mbean-config.xml'
    profileProperties = Properties()
    profileProperties.loadFromXML(FileInputStream(fileName))
    return profileProperties.getProperty(ProfileConstants.CURRENT_SOA_PROFILE_PROPERTY_NAME)


# save the new profile name back to the domain-level configuration file
def persistNewProfileName(domainConfigurationDirectory, profileName):
    from oracle.fabric.profiles.impl import ProfileConstants;
    fileName = domainConfigurationDirectory + File.separatorChar + 'server-profile-mbean-config.xml'
    profileProperties = Properties()
    profileProperties.loadFromXML(FileInputStream(fileName))
    profileProperties.setProperty(ProfileConstants.CURRENT_SOA_PROFILE_PROPERTY_NAME, profileName)
    profileProperties.storeToXML(FileOutputStream(fileName), None)


# find a named SubDeployment in the app's list
def findSubDeployment(appDeployment, name):
    for subDeployment in appDeployment.getSubDeployments():
        if subDeployment.getName() == name:
            return subDeployment
    return None


def setupApplicationAndResourceAdapterTargeting(appList, defaultProfile, allInternalProfile, targetListForSoaInfra):
    # current directory is now the AppDeployment folder
    cd('AppDeployment')
    # expected applications and adapters for new profile
    expectedSetOfApplications = defaultProfile.getExternalApplicationNames();
    expectedSetOfResourceAdapters = defaultProfile.getResourceAdapterNames();

    # all SOA applications and adapters
    allSOAApplications = allInternalProfile.getExternalApplicationNames();
    allSOAResourceAdapters = allInternalProfile.getResourceAdapterNames();
    for applicationName in appList:
        if (expectedSetOfApplications.contains(applicationName) or expectedSetOfResourceAdapters.contains(applicationName)):
            # assign this application to the same targets that soa-infra is assigned to
            for target in targetListForSoaInfra:
                print('SOA profile is attempting to target ' + applicationName + ' to ' + target.getName())
                assign('AppDeployment', applicationName, 'Target', target.getName())

        else:
            if (allSOAApplications.contains(applicationName) or allSOAResourceAdapters.contains(applicationName)):
                cd(applicationName)
                targetList = get('Target')
                if(targetList != None):
                    # remove any targets from this application/adapter
                    for target in targetList:
                        print('SOA profile is attempting to untarget ' + applicationName + ' to ' + target.getName())
                        unassign("AppDeployment", applicationName, "Target", target.getName())
                # get back to AppDeployment folder
                cd('..')


def setupResourceAdapterTargeting(appList, defaultProfile, allInternalProfile, targetListForSoaInfra):
    # current directory is now the AppDeployment folder
    cd('AppDeployment')
    # expected adapters for new profile
    expectedSetOfResourceAdapters = defaultProfile.getResourceAdapterNames();

    # all SOA applications and adapters
    allSOAResourceAdapters = allInternalProfile.getResourceAdapterNames();
    for applicationName in appList:
        if (expectedSetOfResourceAdapters.contains(applicationName)):
            # assign this application to the same targets that soa-infra is assigned to
            for target in targetListForSoaInfra:
                print('SOA profile is attempting to target ' + applicationName + ' to ' + target.getName())
                assign('AppDeployment', applicationName, 'Target', target.getName())

        else:
            if (allSOAResourceAdapters.contains(applicationName)):
                cd(applicationName)
                targetList = get('Target')
                if(targetList != None):
                    # remove any targets from this application/adapter
                    for target in targetList:
                        print('SOA profile is attempting to un-target ' + applicationName + ' to ' + target.getName())
                        unassign("AppDeployment", applicationName, "Target", target.getName())
                # get back to AppDeployment folder
                cd('..')



# target internal modules for a given application
def setupModuleTargeting(applicationName, newProfileConfig, allInternalProfileConfig, targetListForSoaInfra):
    cd('AppDeployment/' + applicationName)
    for moduleName in allInternalProfileConfig.getSoaInfraInternalModuleNames():
        # create the SubDeployment for this module
        subDeployment = findSubDeployment(cmo, moduleName)
        if subDeployment == None:
            # create SubDeployment if not already in config.xml
            subDeployment = create(moduleName, 'SubDeployment')
            
        # target each module in soa-infra
        setOfExpectedModules = newProfileConfig.getSoaInfraInternalModuleNames()
        if setOfExpectedModules.contains(moduleName):
            # target this sub-deployment to same targets as soa-infra
            printDebug('SubDeployment ' + moduleName + ' is being targeted')
            for target in targetListForSoaInfra:
                printDebug('Target name = ' + target.getName())
            subDeployment.setTargets(targetListForSoaInfra)
        else:
            # list of targets for this sub-deployment should be the empty list
            # only set to None if not already using that value (causes some warnings with WLST Offline Commands)
            if (subDeployment.getTargets() != None):
                print('SubDeployment ' + moduleName + 'is being un-targeted')
                subDeployment.setTargets(None)


def setupSOAProfile(domainLocation, defaultProfileName, isUpgrade):
    # import Fabric classes needed for setup of default profile
    from oracle.fabric.profiles.impl import FileBasedProfileConfigService;
    from oracle.fabric.profiles.impl import ProfileConstants;

    if (isUpgrade == True):
        printDebug('Setting SOA profile for profile = ' + defaultProfileName + ' in an upgrade install.')
    else:
        printDebug('Setting SOA profile for profile = ' + defaultProfileName)

    # find soa-infra target list
    cd('AppDeployment/soa-infra')
    targetListForSoaInfra = get('Target')

    # back to top-level domain
    cd('../..')

    # get list of applications in this domain
    appList = ls('AppDeployment', returnMap='true', returnType='c')

    domainConfigDirectory = getDomainConfigDirectory(domainLocation)

    # read in profile definitions
    configService = FileBasedProfileConfigService(domainConfigDirectory)

    # profile that we're trying to switch to
    defaultProfile = configService.getProfileConfig(defaultProfileName)
    # internal profile that contains the names of all SOA components
    allInternalProfile = configService.getProfileConfig(ProfileConstants.ALL_PROFILE_NAME)

    # configure targeting for applications and resource adapters for this default profile
    if (isUpgrade == True):
        setupResourceAdapterTargeting(appList, defaultProfile, allInternalProfile, targetListForSoaInfra)
        printDebug("external applications setup are skipped in an upgrade install")
    else:        
        setupApplicationAndResourceAdapterTargeting(appList, defaultProfile, allInternalProfile, targetListForSoaInfra)
        printDebug("setup both external applications and resource adapters")

    # get back to top-level domain
    cd('..')

    # configure targeting for soa-infra.ear modules, based on the default profile
    setupModuleTargeting('soa-infra', defaultProfile, allInternalProfile, targetListForSoaInfra)
    # save new profile name back to domain-level file
    persistNewProfileName(domainConfigDirectory, defaultProfileName)
    printDebug('Default Profile Setup Completed for this install.')
    


# Top-level method to set the default SOA Profile from a SOA Install Template
def setupSOAProfileFromTemplate(domainLocation, mwHome, templateName): 
    printDebug('Setup SOA Profile is starting for templateName = ' + templateName);
    # add Fabric jars (and dependencies) to classpath
    setupFabricClasspath(mwHome)
    defaultProfileName = getDefaultSOAProfileName(templateName)
    currentProfileName = getCurrentProfileName(getDomainConfigDirectory(domainLocation))
    if currentProfileName == None:
        # initial case of empty profile string found, pass empty string
        currentProfileName = ''

    # setup upgrade flag
    if ((templateName == 'SOA RECONFIG') or (templateName == 'BPM RECONFIG')):
        isUpgrade = True
    else:
        isUpgrade = False

    from oracle.fabric.profiles.impl import ProfilePrecedenceManager
    profilePrecedenceManager = ProfilePrecedenceManager()
    # check to see if this template can overwrite the existing profile with this new default
    if profilePrecedenceManager.canNewProfileOverwrite(currentProfileName, defaultProfileName):
        setupSOAProfile(domainLocation, defaultProfileName, isUpgrade)
    else:
        printDebug('Setup SOA Profile from template was not able to override the current profile ' + currentProfileName + ' with the new default ' + defaultProfileName)
