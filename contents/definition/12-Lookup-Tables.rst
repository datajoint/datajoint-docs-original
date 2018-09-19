.. progress: 8.0 50% Dimitri


Lookup Tables
=============

Lookup tables contain basic facts that are not specific to an experiment and are fairly persistent.
Their contents are typically small.
In GUIs, lookup tables are often used for drop-down menus or radio buttons.
In computed tables, they are often used to specify alternative methods for computations.
Lookup tables are commonly populated from their ``contents`` property.
In :doc:`ERDs <../diagrams/01-ERD>` they are shown in gray.
The decision of which tables are lookup tables and which are manual can be somewhat arbitrary.

The table below is declared as a lookup table with its contents property provided to generate entities.

.. python 1 start
.. figure:: ../_static/img/python-tiny.png
   :alt:

.. code:: python

    @schema
    class User(dj.Lookup):
        definition = """
        # users in the lab
        username : varchar(20)   # user in the lab
        ---
        first_name  : varchar(20)   # user first name
        last_name   : varchar(20)   # user last name
        """
        contents = [
            ['cajal', 'Santiago', 'Cajal'],
            ['hubel', 'David', 'Hubel'],
            ['wiesel', 'Torsten', 'Wiesel']
    ]
.. python 1 end

.. matlab 1 start
.. figure:: ../_static/img/matlab-tiny.png
   :alt:

File ``+lab/User.m``

.. code:: matlab

    %{
        # users in the lab
        username : varchar(20)   # user in the lab
        ---
        first_name  : varchar(20)   # user first name
        last_name   : varchar(20)   # user last name
    %}
    classdef User < dj.Lookup
        properties
            contents = {
                'cajal'  'Santiago' 'Cajal'
                'hubel'  'David'    'Hubel'
                'wiesel' 'Torsten'  'Wiesel'
            }
        end
    end
.. matlab 1 end
