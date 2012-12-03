import logging
import zope.event
import time
import transaction
from Products.CMFCore.utils import getToolByName
from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from openmultimedia.pngwatchdog.interfaces import IPNGWatchDogSettings


logger = logging.getLogger('openmultimedia.pngwatchdog')


def migrate_images(portal):
    catalog = getToolByName(portal, 'portal_catalog')
    query = {'portal_type': 'Image'}
    settings = getUtility(IRegistry).forInterface(IPNGWatchDogSettings)
    sleep = float(abs(settings.sleep)) / 1000
    threshold = abs(settings.threshold)
    counter = 0
    for brain in catalog.unrestrictedSearchResults(query):
        ob = brain._unrestrictedGetObject()
        logger.info('migrating %s' % brain.getPath())
        zope.event.notify(ObjectModifiedEvent(ob))
        time.sleep(sleep)
        counter += 1
        if(threshold and counter % threshold == 0):
            logger.info("commiting changes")
            transaction.commit()
            portal._p_jar.cacheMinimize()


def install_and_migrate(portal):
    """
    """
    qi_tool = getToolByName(portal, 'portal_quickinstaller')
    if not 'openmultimedia.pngwatchdog' in \
        [p['id'] for p in qi_tool.listInstalledProducts()]:
        qi_tool.installProduct('openmultimedia.pngwatchdog')
    getUtility(IRegistry).forInterface(IPNGWatchDogSettings).enabled = True
    migrate_images(portal)
