import urllib2
from StringIO import StringIO
from PIL import Image
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig


def generate_jpeg(width, height):
    url = 'http://lorempixel.com/%d/%d/' % (width, height)
    return urllib2.urlopen(url).read()


def generate_gif(width, height):
    jpeg = generate_jpeg(width, height)
    im = Image.open(StringIO(jpeg))
    output = StringIO()
    im.save(output, format='GIF')
    return output.getvalue()


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


class OpenmultimediapngwatchdogUnistalledLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import openmultimedia.pngwatchdog
        xmlconfig.file('configure.zcml', openmultimedia.pngwatchdog, context=configurationContext)

    def setUpPloneSite(self, portal):
        pass


OPENMULTIMEDIA_PNGWATCHDOG_FIXTURE = OpenmultimediapngwatchdogLayer()
OPENMULTIMEDIA_PNGWATCHDOG_UNINSTALLED_FIXTURE = OpenmultimediapngwatchdogUnistalledLayer()
OPENMULTIMEDIA_PNGWATCHDOG_INTEGRATION_TESTING = IntegrationTesting(bases=(OPENMULTIMEDIA_PNGWATCHDOG_FIXTURE,),
                                                                    name="OpenmultimediapngwatchdogLayer:Integration")
OPENMULTIMEDIA_PNGWATCHDOG_UNINSTALLED_INTEGRATION_TESTING = IntegrationTesting(bases=(OPENMULTIMEDIA_PNGWATCHDOG_UNINSTALLED_FIXTURE,),
                                                                                name="OpenmultimediapngwatchdogLayer:UninstalledIntegration")
OPENMULTIMEDIA_PNGWATCHDOG_FUNCTIONAL_TESTING = FunctionalTesting(bases=(OPENMULTIMEDIA_PNGWATCHDOG_FIXTURE,),
                                                                  name="OpenmultimediapngwatchdogLayer:Functional")
