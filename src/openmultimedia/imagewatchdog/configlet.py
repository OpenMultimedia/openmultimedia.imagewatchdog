from zope.component import getUtility
from z3c.form import button
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from openmultimedia.imagewatchdog import _
from openmultimedia.imagewatchdog.migration import migrate_images
from openmultimedia.imagewatchdog.interfaces import IImageWatchDogSettings

from zope.i18nmessageid import MessageFactory
__ = MessageFactory('plone')


class ImageWatchDogEditForm(controlpanel.RegistryEditForm):
    schema = IImageWatchDogSettings
    label = _('Image WatchDog settings')
    description = _('Settings to configure Image WatchDog in Plone.')

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

    @button.buttonAndHandler(
        _(u"Save and Migrate"),
        name='migrate',
        condition=lambda enabled: bool(getUtility(IRegistry).forInterface(IImageWatchDogSettings).enabled))
    def handleMigrate(self, action):
        data, errors = self.extractData()
        self.applyChanges(data)
        migrate_images(self.context)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Migration done."),
            "info")
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(),
            self.control_panel_view))


class ImageWatchDogControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ImageWatchDogEditForm
