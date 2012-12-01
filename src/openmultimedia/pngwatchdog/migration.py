import logging
import zope.event
#import time
from Products.CMFCore.utils import getToolByName
from zope.lifecycleevent import ObjectModifiedEvent


logger = logging.getLogger('openmultimedia.pngwatchdog')


def migrate_images(portal):
    catalog = getToolByName(portal, 'portal_catalog')
    query = {'portal_type': 'Image'}
    for brain in catalog.unrestrictedSearchResults(query):
        ob = brain._unrestrictedGetObject()
        logger.info('migrating %s' % brain.getPath())
        zope.event.notify(ObjectModifiedEvent(ob))
#        time.sleep(1)
