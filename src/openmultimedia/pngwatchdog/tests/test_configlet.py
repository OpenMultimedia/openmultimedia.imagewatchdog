import unittest2 as unittest

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from openmultimedia.pngwatchdog.configlet import IPNGWatchDogSettings
from openmultimedia.pngwatchdog.testing import \
    OPENMULTIMEDIA_PNGWATCHDOG_FUNCTIONAL_TESTING


class TestConfiglet(unittest.TestCase):

    layer = OPENMULTIMEDIA_PNGWATCHDOG_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_default_config(self):
        """ Validate the default values
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        self.assertEqual(settings.source_formats, ['JPEG', 'GIF'])
        self.assertFalse(settings.optimize)
        self.assertFalse(settings.enabled)

    def test_change_config(self):
        """ Validate the default values
        """
        browser = Browser(self.app)
        portalURL = self.portal.absolute_url()
        browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        browser.open(portalURL + '/@@overview-controlpanel')
        browser.getLink('PNG WatchDog settings').click()
        browser.getControl('Optimize PNG').selected = True
        browser.getControl('Enabled').selected = True
        browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        self.assertTrue(settings.optimize)
        self.assertTrue(settings.enabled)

    def test_cancel_config(self):
        """ Validate the default values
        """
        browser = Browser(self.app)
        portalURL = self.portal.absolute_url()
        browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        browser.open(portalURL + '/@@overview-controlpanel')
        browser.getLink('PNG WatchDog settings').click()
        browser.getControl('Optimize PNG').selected = True
        browser.getControl('Enabled').selected = True
        browser.getControl('Cancel').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        self.assertFalse(settings.optimize)
        self.assertFalse(settings.enabled)

    def test_migrate_button(self):
        """ Check for the migrate button
        """
        browser = Browser(self.app)
        portalURL = self.portal.absolute_url()
        browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        browser.open(portalURL + '/@@overview-controlpanel')
        browser.getLink('PNG WatchDog settings').click()
        browser.getControl('Enabled').selected = True
        browser.getControl('Save').click()

        # Now there is a migrate button
        browser.open(portalURL + '/@@overview-controlpanel')
        browser.getLink('PNG WatchDog settings').click()
        browser.getControl('Optimize PNG').selected = True
        browser.getControl('Migrate').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPNGWatchDogSettings)
        self.assertTrue(settings.optimize)
        self.assertTrue(settings.enabled)
