from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from openmultimedia.imagewatchdog import _

image_formats = SimpleVocabulary(
    [SimpleTerm(value=u'JPEG', title=_(u'.jpg images')),
     SimpleTerm(value=u'GIF', title=_(u'.gif images'))]
)


class IImageWatchDogSettings(Interface):
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
            vocabulary=image_formats),
    )

    optimize = schema.Bool(
        title=_(u"Optimize PNG"),
        description=_(
            u"Instructs the PNG writer to make the output file as small as "
            u"possible. This includes extra processing in order to find "
            u"optimal encoder settings."
        ),
        required=False,
    )

    sleep = schema.Int(
        title=_(u"Migration delay (milliseconds)"),
        description=_(
            u"Migrating images to PNG is an expensive process, this "
            u"parameter indicates a delay between every processed image. 0 "
            u"means no delay, more fast, but CPU intensive, bigger values "
            u"are nicer with the CPU but will slow down the process."
        ),
        required=False,
        default=0,
    )

    threshold = schema.Int(
        title=_(u"Transaction threshold"),
        description=_(
            u"Migrating images in one single transaction could be a RAM "
            u"intensive process. This parameter is the number of images "
            u"processed in a single transaction. 0 means one single "
            u"transaction, more fast, but RAM intensive, small values are "
            u"nicer with the RAM but will slow down the process."
        ),
        required=False,
        default=0,
    )
