****************************
openmultimedia.imagewatchdog
****************************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A package to convert every image stored and uploaded to a Plone site to PNG
format.

If you are concerned about images format patent issues this package is for
you.

Patent issues
^^^^^^^^^^^^^

`Portable Network Graphics`_ (PNG) is a bitmapped image format that employs
lossless data compression. PNG was created to improve upon and replace GIF
(Graphics Interchange Format) as an image-file format not requiring a patent
license.

Even as the `JPEG`_ compression used in various image file formats has been
subject to a number of patent issues by well-known patent trolls of the
industry for many years, there is currently no patent-free alternative for
these formats (`WebP`_ has been available for some time, but is currently only
supported by Google Chrome and Opera web browsers).

Don't Panic
-----------

Configure
^^^^^^^^^

- Go to 'Site Setup'.
- Select 'Image WatchDog'.
- Select the files formats that should be converted to PNG.
- You can choose to optimize the PNG file checking the 'Optimize PNG'
  checkbox.
- 'Migration delay (milliseconds)' and 'Transaction threshold' are only used
  for migration.
- Activate the on-fly convertion checking the 'Enabled' checkbox.

Migrate images
^^^^^^^^^^^^^^

- First `Configure`_.
- Now in the `'Image WatchDog' control panel`_ you can set:
    - 'Migration delay (milliseconds)', this parameter indicates a delay
      between every processed image. 0 means no delay, more fast, but CPU
      intensive, bigger values are nicer with the CPU but will slow down the
      process.
    - 'Transaction threshold', this parameter is the number of images
      processed in a single transaction. 0 means one single transaction, more
      fast, but RAM intensive, small values are nicer with the RAM but will
      slow down the process.
- Click on 'Save & Migrate' button to start the migration process.
- Get your prefered caffeinated beverage because this could take some time,
  you could check your logs to see the progress of migration process.

Script to migrate images
^^^^^^^^^^^^^^^^^^^^^^^^

The package includes a handy method to migrate images, sometimes prefered for
running long processes.

- From your command line run: instance run <path_to_openmultimedia.imagewatchdog_package>/openmultimedia/imagewatchdog/script/install_and_migrate.py <plone_site_name>
- This will install de product in the Plone site and migrate the images to PNG.
- Get your prefered caffeinated beverage because this could take some time,
  you will see the progress of migration process in your console.

Screenshots
-----------

'Image WatchDog' control panel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: https://github.com/OpenMultimedia/openmultimedia.imagewatchdog/raw/master/control_panel.png
    :align: center
    :height: 384px
    :width: 683px

Comparison to other file formats
--------------------------------

Here is a small resume including just the downsides of PNG against GIF and
JPEG; you can find the complete comparison in the `Wikipedia`_:

GIF
^^^

- On small images, GIF can achieve greater compression than PNG.
- GIF intrinsically supports animated images. PNG supports animation only via
  unofficial extensions.

JPEG
^^^^

- JPEG formats can produce smaller files than PNG for photographic (and
  photo-like) images, since JPEG uses a lossy encoding method specifically
  designed for photographic image data.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/OpenMultimedia/openmultimedia.imagewatchdog.png
    :target: http://travis-ci.org/OpenMultimedia/openmultimedia.imagewatchdog

Have an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`Portable Network Graphics`: https://en.wikipedia.org/wiki/Portable_Network_Graphics
.. _`Graphics Interchange Format`: https://en.wikipedia.org/wiki/Graphics_Interchange_Format
.. _`JPEG`: https://en.wikipedia.org/wiki/JPEG
.. _`WebP`: https://en.wikipedia.org/wiki/WebP
.. _`Wikipedia`: https://en.wikipedia.org/wiki/Portable_Network_Graphics#Comparison_to_other_file_formats
.. _`opening a support ticket`: https://github.com/OpenMultimedia/openmultimedia.imagewatchdog/issues
