from zope.component import getUtility
from z3c.form import button
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from openmultimedia.pngwatchdog import _
from openmultimedia.pngwatchdog.migration import migrate_images
from openmultimedia.pngwatchdog.interfaces import IPNGWatchDogSettings

from zope.i18nmessageid import MessageFactory
__ = MessageFactory('plone')


class PNGWatchDogEditForm(controlpanel.RegistryEditForm):
    schema = IPNGWatchDogSettings
    label = _('PNG WatchDog settings')
    description = _('Settings to configure PNG WatchDog in Plone.')

    @button.buttonAndHandler(__(u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes saved."),
            "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(__(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes canceled."),
            "info")
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(),
            self.control_panel_view))

    @button.buttonAndHandler(_(u"Migrate"), name='migrate',
        condition=lambda enabled: bool(getUtility(IRegistry).forInterface(IPNGWatchDogSettings).enabled))
    def handleMigrate(self, action):
        migrate_images(self.context)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Migration done."),
            "info")
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(),
            self.control_panel_view))


class PNGWatchDogControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PNGWatchDogEditForm
