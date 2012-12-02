from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from openmultimedia.pngwatchdog import _


image_formats = SimpleVocabulary(
    [SimpleTerm(value=u'JPEG', title=_(u'.jpg images')),
     SimpleTerm(value=u'GIF', title=_(u'.gif images'))]
    )


class IPNGWatchDogSettings(Interface):
    """ Interface for the control panel form.
    """

    enabled = schema.Bool(
        title=_(u"Enabled"),
        description=_(u"Activate the convertion to PNG."),
        required=False,
        )

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
        description=_(u"Instructs the PNG writer to make the output " \
                       "file as small as possible. This includes extra " \
                       "processing in order to find optimal encoder settings."
                       ),
        required=False,
        )

    sleep = schema.Int(
        title=_(u"Migration delay (milliseconds)"),
        description=_(u"Migrating images to PNG is an expensive process, " \
                       "this parameter indicates a delay between every " \
                       "processed image. 0 means no delay, more fast, " \
                       "but CPU intensive, bigger values are nicer with " \
                       "the CPU but will slow down the process."
                       ),
        required=False,
        default=0,
        )

    threshold = schema.Int(
        title=_(u"Transaction threshold"),
        description=_(u"Migrating images in one single transaction could " \
                       "be a RAM intensive process. This value is the " \
                       "number of images processed in a single transaction. " \
                       "0 means one single transaction, more fast, " \
                       "but RAM intensive, small values are nicer with " \
                       "the RAM but will slow down the process."
                       ),
        required=False,
        default=0,
        )
