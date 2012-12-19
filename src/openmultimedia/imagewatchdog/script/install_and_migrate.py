# use with instance run
#
import sys
import logging
import transaction
from zope.app.component.hooks import setSite
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Testing.makerequest import makerequest
from Products.CMFCore.tests.base.security import (
    PermissiveSecurityPolicy,
    OmnipotentUser
)
from openmultimedia.imagewatchdog.migration import install_and_migrate


logger = logging.getLogger('openmultimedia.imagewatchdog')
logger.parent.setLevel(logging.INFO)
for h in logger.parent.handlers:
    h.setLevel(logging.INFO)


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
    if len(sys.argv) == 1:
        logger.error("missing portal name")
    else:
        app = spoofRequest(app)
        admin = app.acl_users.getUserById("admin")
        newSecurityManager(None, admin)
        portal = app.unrestrictedTraverse(sys.argv[1], None)
        if not portal:
            logger.error("portal not found")
        else:
            portal.setupCurrentSkin(app.REQUEST)
            setSite(portal)
            install_and_migrate(portal)
            transaction.commit()
