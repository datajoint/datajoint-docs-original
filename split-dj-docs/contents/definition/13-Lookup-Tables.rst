.. progress: 8.0 50% Dimitri

.. _lookup:

Lookup Tables
=============

Lookup tables contain basic facts that are not specific to an experiment and are fairly persistent.
Their contents are typically small.
In GUIs, lookup tables are often used for drop-down menus or radio buttons.
In computed tables, they are often used to specify alternative methods for computations.
Lookup tables are commonly populated from their ``contents`` property.
In :ref:`erd` they are shown in gray.
The decision of which tables are lookup tables and which are manual can be somewhat arbitrary.

The table below is declared as a lookup table with its contents property provided to generate entities.

.. include:: 13-Lookup-Tables_lang1.rst

