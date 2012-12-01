from StringIO import StringIO
from PIL import Image
import unittest2 as unittest

import zope.event
from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login, setRoles

from openmultimedia.pngwatchdog.configlet import IPNGWatchDogSettings
from openmultimedia.pngwatchdog.testing import \
    OPENMULTIMEDIA_PNGWATCHDOG_INTEGRATION_TESTING
from openmultimedia.pngwatchdog.testing import \
    generate_jpeg, generate_gif


class TestConvert(unittest.TestCase):

    layer = OPENMULTIMEDIA_PNGWATCHDOG_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_disabled(self):
        """ Validate that our product doesn't modify images if disabled
        """
        login(self.portal, TEST_USER_NAME)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        self.assertFalse(settings.enabled)

        self.portal.invokeFactory('Image', 'test_jpeg_image')
        self.portal['test_jpeg_image'].setImage(generate_jpeg(100, 100))
        zope.event.notify(ObjectModifiedEvent(self.portal['test_jpeg_image']))
        self.portal.invokeFactory('Image', 'test_gif_image')
        self.portal['test_gif_image'].setImage(generate_gif(100, 100))
        zope.event.notify(ObjectModifiedEvent(self.portal['test_gif_image']))

        im = Image.open(StringIO(self.portal['test_jpeg_image'].getImage()))
        self.assertEqual(im.format, 'JPEG')

        im = Image.open(StringIO(self.portal['test_gif_image'].getImage()))
        self.assertEqual(im.format, 'GIF')

    def test_enabled(self):
        """ Validate that images are transformed to PNG if enabled
        """
        login(self.portal, TEST_USER_NAME)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        settings.enabled = True

        self.portal.invokeFactory('Image', 'test_jpeg_image')
        self.portal['test_jpeg_image'].setImage(generate_jpeg(100, 100))
        zope.event.notify(ObjectModifiedEvent(self.portal['test_jpeg_image']))
        self.portal.invokeFactory('Image', 'test_gif_image')
        self.portal['test_gif_image'].setImage(generate_gif(100, 100))
        zope.event.notify(ObjectModifiedEvent(self.portal['test_gif_image']))

        im = Image.open(StringIO(self.portal['test_jpeg_image'].getImage()))
        self.assertEqual(im.format, 'PNG')

        im = Image.open(StringIO(self.portal['test_gif_image'].getImage()))
        self.assertEqual(im.format, 'PNG')

    def test_only_jpeg(self):
        """ Validate that only configured image formats are transformed to PNG
        """
        login(self.portal, TEST_USER_NAME)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        settings.source_formats = ['JPEG']
        settings.enabled = True

        self.portal.invokeFactory('Image', 'test_jpeg_image')
        self.portal['test_jpeg_image'].setImage(generate_jpeg(100, 100))
        zope.event.notify(ObjectModifiedEvent(self.portal['test_jpeg_image']))
        self.portal.invokeFactory('Image', 'test_gif_image')
        self.portal['test_gif_image'].setImage(generate_gif(100, 100))
        zope.event.notify(ObjectModifiedEvent(self.portal['test_gif_image']))

        im = Image.open(StringIO(self.portal['test_jpeg_image'].getImage()))
        self.assertEqual(im.format, 'PNG')

        im = Image.open(StringIO(self.portal['test_gif_image'].getImage()))
        self.assertEqual(im.format, 'GIF')
