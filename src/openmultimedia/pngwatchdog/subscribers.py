from StringIO import StringIO
from PIL import Image
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from openmultimedia.pngwatchdog.configlet import IPNGWatchDogSettings


def image_convert(context, event):
    """
    """
    orig = str(context.getImage())
    if not orig:
        return
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IPNGWatchDogSettings, None)
    if not settings:
        return
    if not settings.enabled:
        return
    im = Image.open(StringIO(orig))
    if im.format == 'PNG' or \
       im.format not in settings.source_formats:
        return
    output = StringIO()
    im.save(output, format='PNG', optimize=settings.optimize)
    context.setImage(output.getvalue())
