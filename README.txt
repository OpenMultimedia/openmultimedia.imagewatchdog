**************************
openmultimedia.pngwatchdog
**************************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A package to convert every image uploaded to Plone to PNG format.

If you are concerned about images format license issues this package is for you.

Don't Panic
-----------

Configure
^^^^^^^^^

- Go to 'Site Setup'.
- Select 'PNG WatchDog'.
- Select the files formats that should be converted to PNG.
- You can choose to optimize the PNG file checking the 'Optimize PNG' checkbox.
- 'Migration delay (milliseconds)' and 'Transaction threshold' are only used for migration.
- Activate the on-fly convertion checking the 'Enabled' checkbox.

Migrate images
^^^^^^^^^^^^^^

- First `Configure`.
- Now in the 'PNG WatchDog' control panel you can set::
    - 'Migration delay (milliseconds)', this parameter indicates a delay between every processed image.
        0 means no delay, more fast, but CPU intensive,
        bigger values are nicer with the CPU but will slow down the process.

    - 'Transaction threshold', this parameter is the number of images processed in a single transaction.
        0 means one single transaction, more fast, but RAM intensive,
        small values are nicer with the RAM but will slow down the process.
- Click on 'Save & Migrate' button to start the migration process.
- Get your prefered caffeinated beverage because this could take some time, you could check your logs to see the progress of migration process.

Script to migrate images
^^^^^^^^^^^^^^^^^^^^^^^^

The package includes a handy method to migrate images, sometimes prefered for running long processes.

- From your command line run: instance run <path_to_openmultimedia.pngwatchdog_package>/openmultimedia/pngwatchdog/script/install_and_migrate.py <plone_site_name>
- This will install de product in the Plone site and migrate the images to PNG.
- Get your prefered caffeinated beverage because this could take some time, you will see the progress of migration process in your console.

Screenshots
-----------

.. figure:: https://github.com/OpenMultimedia/openmultimedia.pngwatchdog/raw/master/control_panel.png
    :align: center
    :height: 582px
    :width: 263px

    PNG WatchDog control panel.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/OpenMultimedia/openmultimedia.pngwatchdog.png
    :target: http://travis-ci.org/OpenMultimedia/openmultimedia.pngwatchdog

Have an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/OpenMultimedia/openmultimedia.pngwatchdog/issues
