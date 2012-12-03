import sys
import logging
import zope.event
import time
import transaction
from zope.app.component.hooks import setSite
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Testing.makerequest import makerequest
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
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


def spoofRequest(app):
    """
    Make REQUEST variable to be available on the Zope application server.

    This allows acquisition to work properly
    """
    _policy = PermissiveSecurityPolicy()
    setSecurityPolicy(_policy)
    newSecurityManager(None, OmnipotentUser().__of__(app.acl_users))
    return makerequest(app)


if 'app' in locals():
    # Enable Faux HTTP request object
    app = locals()['app']  # please pep8
    app = spoofRequest(app)
    admin = app.acl_users.getUserById("admin")
    newSecurityManager(None, admin)
    if len(sys.argv) == 1:
        logger.error("missing portal name")
    else:
        portal_name = sys.argv[1]
        portal = app.unrestrictedTraverse(portal_name, None)
        if not portal:
            logger.error("portal not found")
        else:
            portal.setupCurrentSkin(app.REQUEST)
            setSite(portal)
            qi_tool = getToolByName(portal, 'portal_quickinstaller')
            if not 'openmultimedia.pngwatchdog' in \
                [p['id'] for p in qi_tool.listInstalledProducts()]:
                qi_tool.installProduct('openmultimedia.pngwatchdog')
            getUtility(IRegistry).forInterface(IPNGWatchDogSettings).enabled = True
            migrate_images(portal)
            transaction.commit()
