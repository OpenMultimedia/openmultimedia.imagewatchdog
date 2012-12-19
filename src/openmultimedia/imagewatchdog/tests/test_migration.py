import unittest2 as unittest
from StringIO import StringIO
from PIL import Image

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login, setRoles
from Products.CMFCore.utils import getToolByName

from openmultimedia.imagewatchdog.configlet import IImageWatchDogSettings
from openmultimedia.imagewatchdog.testing import \
    OPENMULTIMEDIA_IMAGEWATCHDOG_FUNCTIONAL_TESTING
from openmultimedia.imagewatchdog.testing import \
    generate_jpeg
from openmultimedia.imagewatchdog.migration import migrate_images, install_and_migrate


IMAGES_RANGE = 10


class TestConfiglet(unittest.TestCase):

    layer = OPENMULTIMEDIA_IMAGEWATCHDOG_FUNCTIONAL_TESTING

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
        settings = registry.forInterface(IImageWatchDogSettings)
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
        settings = registry.forInterface(IImageWatchDogSettings)
        settings.enabled = True

        migrate_images(self.portal)

        for i in range(IMAGES_RANGE):
            im = Image.open(StringIO(self.portal['test_jpeg_image%s' % i].getImage()))
            self.assertEqual(im.format, 'PNG')

#    from profilehooks import timecall
#    @timecall
    def test_migration_with_threshold(self):
        """ Migrate images to PNG
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IImageWatchDogSettings)
        settings.enabled = True
        settings.threshold = 1

        migrate_images(self.portal)

        for i in range(IMAGES_RANGE):
            im = Image.open(StringIO(self.portal['test_jpeg_image%s' % i].getImage()))
            self.assertEqual(im.format, 'PNG')

    def test_install_and_migrate(self):
        """ Migrate images to PNG
        """
        qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        qi_tool.uninstallProducts(['openmultimedia.imagewatchdog'])

        install_and_migrate(self.portal)

        for i in range(IMAGES_RANGE):
            im = Image.open(StringIO(self.portal['test_jpeg_image%s' % i].getImage()))
            self.assertEqual(im.format, 'PNG')
