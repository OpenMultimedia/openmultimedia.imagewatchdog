from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig


class OpenmultimediapngwatchdogLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import openmultimedia.pngwatchdog
        xmlconfig.file('configure.zcml', openmultimedia.pngwatchdog, context=configurationContext)

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'openmultimedia.pngwatchdog:default')

OPENMULTIMEDIA_PNGWATCHDOG_FIXTURE = OpenmultimediapngwatchdogLayer()
OPENMULTIMEDIA_PNGWATCHDOG_INTEGRATION_TESTING = IntegrationTesting(bases=(OPENMULTIMEDIA_PNGWATCHDOG_FIXTURE,), name="OpenmultimediapngwatchdogLayer:Integration")
