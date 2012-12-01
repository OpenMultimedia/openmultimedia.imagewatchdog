import unittest2 as unittest
from StringIO import StringIO
from PIL import Image

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login, setRoles

from openmultimedia.pngwatchdog.configlet import IPNGWatchDogSettings
from openmultimedia.pngwatchdog.testing import \
    OPENMULTIMEDIA_PNGWATCHDOG_FUNCTIONAL_TESTING
from openmultimedia.pngwatchdog.testing import \
    generate_jpeg
from openmultimedia.pngwatchdog.migration import migrate_images


IMAGES_RANGE = 10


class TestConfiglet(unittest.TestCase):

    layer = OPENMULTIMEDIA_PNGWATCHDOG_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        jpeg = generate_jpeg(100, 100)
        for i in range(IMAGES_RANGE):
            self.portal.invokeFactory('Image', 'test_jpeg_image%s' % i)
            self.portal['test_jpeg_image%s' % i].setImage(jpeg)

    def test_enabled_notmigrated(self):
        """ Product doesn't auto-migrate on enable
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        settings.enabled = True

        # Images are still in the original format
        for i in range(IMAGES_RANGE):
            im = Image.open(StringIO(self.portal['test_jpeg_image%s' % i].getImage()))
            self.assertEqual(im.format, 'JPEG')

#    from profilehooks import timecall
#    @timecall
    def test_migration(self):
        """ Migrate images to PNG
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        settings.enabled = True

        migrate_images(self.portal)

        for i in range(IMAGES_RANGE):
            im = Image.open(StringIO(self.portal['test_jpeg_image%s' % i].getImage()))
            self.assertEqual(im.format, 'PNG')
