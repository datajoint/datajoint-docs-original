Auto-populate
=============

Tables in the initial portions of the pipeline are populated from outside the pipeline.  
In subsequent steps, computations are performed automatically by the DataJoint pipeline.

Computed tables belong to one of the two auto-populated :doc:`../data-definition/Data-tiers`: ``dj.Imported`` and ``dj.Computed``.
DataJoint does not enforce the distinction between imported and compputed tables: the difference is purely semantic, a convention for developers to follow.
If populating a table requires access to external files such as raw storage that is not part of the database, the table is designated as *imported*. Otherwise, it is *computed*.

Make-tuples
-----------
Auto-populated tables are defined and queried exactly as other tables such as :doc:`../data-definition/Manual-tables`, for example. 
Their data definition follows the same :doc:`../data-definition/Definition-syntax`.

For auto-populated tables, data should never be entered using :doc:`../data-manipulation/Insert` directly.  Instead, these tables must define the callback method ``makeTuples(self, key)`` in MATLAB   ``_make_tuples(self, key)``.  The ``insert`` method then can only be called on ``self`` inside this callback method.

Consider the following example:  

Imagine that there is a table ``test.Image`` that contains 2D grayscale images in its ``image`` attribute.  
Let us define the computed table, ``test.FilteredImage`` that filters the image in some way and saves the result in its ``filtered_image`` attribute. 

The class will be defined as follows. 

|matlab| MATLAB

.. code-block:: MATLAB

    %{
    # Filtered image 
    -> test.Image
    ---
    filtered_image : longblob 
    %}

    classdef FilteredImage < dj.Computed
        methods(Access=protected)
            function makeTuples(self, key)
                img = fetch1(test.Image & key, 'image');
                key.filtered_image = myfilter(img);
                self.insert(key)
            end
        end
    end 

|python| Python

.. code-block:: python

    @schema 
    class FilteredImage(dj.Computed):
        definition = """
        # Filtered image 
        -> Image
        ---
        filtered_image : longblob 
        """

        def _make_tuples(self, key):
            img = (test.Image() & key).fetch1['image']
            key['filtered_image'] = myfilter(img)
            self.insert(key)

The ``make_tuples`` method received one argument: the ``key`` of type ``struct`` in MATLAB and ``dict`` in Python.  
The key represents the partially filled tuple, usually already containing :doc:`../data-definition/Primary-key` attributes. 

Inside the callback, three things always happen:

1. :doc:`../queries/Fetch` data from tables upstream in the pipeline using the ``key`` for :doc:`../queries/Restriction`.  
2. The missing attributes are computed and added to the fields allredy in ``key``.
3. The entire tuple is inserted into ``self``.

``make_tuples`` may populate multiple tuples in one call when ``key`` does not specify the entire primary key of the populated table.

Populate
--------
The inherited ``populate`` method of ``dj.Imported`` and ``dj.Computed`` automatically calls ``make_tuples`` for every key for which the auto-populated table is missing data.

The ``FilteredImage`` table can be populated as

|python| Python

.. code-block:: python

    FilteredImage().populate()

|matlab| MATLAB

.. code-block:: matlab

    populate(test.FilteredImage)

Note that it is not necessary which data needs to be computed.  DataJoint will call ``make_tuples``, one-by-one, for every key in ``Image`` for which ``FilteredImage`` has not yet been computed.

Chains of auto-populated tables form computational pipelines in DataJoint.  


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
