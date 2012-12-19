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


class OpenmultimediaimagewatchdogLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import openmultimedia.imagewatchdog
        xmlconfig.file('configure.zcml', openmultimedia.imagewatchdog, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'openmultimedia.imagewatchdog:default')


class OpenmultimediaimagewatchdogUnistalledLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import openmultimedia.imagewatchdog
        xmlconfig.file('configure.zcml', openmultimedia.imagewatchdog, context=configurationContext)

    def setUpPloneSite(self, portal):
        pass


OPENMULTIMEDIA_IMAGEWATCHDOG_FIXTURE = OpenmultimediaimagewatchdogLayer()
OPENMULTIMEDIA_IMAGEWATCHDOG_UNINSTALLED_FIXTURE = OpenmultimediaimagewatchdogUnistalledLayer()
OPENMULTIMEDIA_IMAGEWATCHDOG_INTEGRATION_TESTING = IntegrationTesting(
    bases=(OPENMULTIMEDIA_IMAGEWATCHDOG_FIXTURE,),
    name="OpenmultimediaimagewatchdogLayer:Integration")
OPENMULTIMEDIA_IMAGEWATCHDOG_UNINSTALLED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(OPENMULTIMEDIA_IMAGEWATCHDOG_UNINSTALLED_FIXTURE,),
    name="OpenmultimediaimagewatchdogLayer:UninstalledIntegration")
OPENMULTIMEDIA_IMAGEWATCHDOG_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(OPENMULTIMEDIA_IMAGEWATCHDOG_FIXTURE,),
    name="OpenmultimediaimagewatchdogLayer:Functional")
