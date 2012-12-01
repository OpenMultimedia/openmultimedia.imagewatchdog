from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from z3c.form import button
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from openmultimedia.pngwatchdog import _
from openmultimedia.pngwatchdog.migration import migrate_images

from zope.i18nmessageid import MessageFactory
__ = MessageFactory('plone')

image_formats = SimpleVocabulary(
    [SimpleTerm(value=u'JPEG', title=_(u'.jpg images')),
     SimpleTerm(value=u'GIF', title=_(u'.gif images'))]
    )


class IPNGWatchDogSettings(Interface):
    """ Interface for the control panel form.
    """

    source_formats = schema.List(
        title=_(u"Source formats"),
        description=_(u"Only image in these format will be converted to PNG."),
        required=False,
        default=['JPEG', 'GIF'],
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(
            vocabulary=image_formats),)

    optimize = schema.Bool(
        title=_(u"Optimize PNG"),
        description=_(u"Instructs the PNG writer to make the output file as small as possible. " \
                       "This includes extra processing in order to find optimal encoder settings."),
        required=False,
        )

    enabled = schema.Bool(
        title=_(u"Enabled"),
        description=_(u"Activate the convertion to PNG."),
        required=False,
        )


class PNGWatchDogEditForm(controlpanel.RegistryEditForm):
    schema = IPNGWatchDogSettings
    label = _('PNG WatchDog settings')
    description = _('Settings to configure PNG WatchDog in Plone.')
#    buttons = controlpanel.RegistryEditForm.buttons.copy()

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
