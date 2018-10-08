.. progress: 12.0 20% Dimitri

.. _auto:

Auto-populate
=============

Auto-populated tables are used to define, execute, and coordinate computations in a DataJoint pipeline.

Tables in the initial portions of the pipeline are populated from outside the pipeline.
In subsequent steps, computations are performed automatically by the DataJoint pipeline in auto-populated tables.

Computed tables belong to one of the two auto-populated :ref:`data tiers <tiers>`: ``dj.Imported`` and ``dj.Computed``.
DataJoint does not enforce the distinction between imported and computed tables: the difference is purely semantic, a convention for developers to follow.
If populating a table requires access to external files such as raw storage that is not part of the database, the table is designated as **imported**.
Otherwise it is **computed**.

Auto-populated tables are defined and queried exactly as other tables (See :ref:`example`).
Their data definition follows the same :ref:`definition syntax <definition-syntax>`.

Make
----
For auto-populated tables, data should never be entered using :ref:`insert <insert>` directly.
Instead these tables must define the callback method ``make(self, key)``.
The ``insert`` method then can only be called on ``self`` inside this callback method.

Imagine that there is a table ``test.Image`` that contains 2D grayscale images in its ``image`` attribute.
Let us define the computed table, ``test.FilteredImage`` that filters the image in some way and saves the result in its ``filtered_image`` attribute.

The class will be defined as follows.

.. matlab 1 start

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
            function make(self, key)
                img = fetch1(test.Image & key, 'image');
                key.filtered_image = myfilter(img);
                self.insert(key)
            end
        end
    end

.. matlab 1 end

.. python 1 start

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

        def make(self, key):
            img = (test.Image & key).fetch1['image']
            key['filtered_image'] = myfilter(img)
            self.insert(key)
.. python 1 end

The ``make`` method received one argument: the ``key`` of type ``struct`` in MATLAB and ``dict`` in Python.
The key represents the partially filled entity, usually already containing :ref:`primary key <primary-key>` attributes.

Inside the callback, three things always happen:

1. :ref:`fetch` data from tables upstream in the pipeline using the ``key`` for :ref:`restriction <restriction>`.
2. The missing attributes are computed and added to the fields already in ``key``.
3. The entire entity is inserted into ``self``.

``make`` may populate multiple entities in one call when ``key`` does not specify the entire primary key of the populated table.

Populate
--------
The inherited ``populate`` method of ``dj.Imported`` and ``dj.Computed`` automatically calls ``make`` for every key for which the auto-populated table is missing data.

The ``FilteredImage`` table can be populated as

.. python 2 start

|python| Python

.. code-block:: python

    FilteredImage.populate()

The progress of long-running calls to ``populate()`` in datajoint-python can be visualized by adding the ``display_progress=True`` argument to the populate call.
.. python 2 start

.. matlab 2 start

|matlab| MATLAB

.. code-block:: matlab

    populate(test.FilteredImage)
.. matlab 2 end

Note that it is not necessary to specify which data needs to be computed.
DataJoint will call ``make``, one-by-one, for every key in ``Image`` for which ``FilteredImage`` has not yet been computed.

Chains of auto-populated tables form computational pipelines in DataJoint.

The ``populate`` method accepts a number of optional arguments that provide more features and allow greater control over the method's behavior.

- ``restrictions`` - A list of restrictions, restricting as ``(tab.key_source & AndList(restrictions)) - tab.proj()``.
  Here ``target`` is the table to be populated, usually ``tab`` itself.
- ``suppress_errors`` - If ``True``, errors will not terminate execution of ``populate``.
  Error messages will be logged in the job reservation table (if ``reserve_jobs`` is ``True``) and returned as a list.
  See also ``return_exception_objects``.
  Defaults to ``False``.
- ``return_exception_objects`` - If ``True``, error objects are returned instead of error messages.
  This applies only when ``suppress_errors`` is ``True``.
  Defaults to ``False``.
- ``reserve_jobs`` - If ``True``, reserves job to populate asynchronously.
  Defaults to ``False``.
- ``order`` - The order of execution, either ``"original"``, ``"reverse"``, or ``"random"``.
  Defaults to ``"original"``.
- ``display_progress`` - If ``True``, displays a progress bar.
  Defaults to ``False``.
- ``limit`` - If not ``None``, checks at most this number of keys.
  Defaults to ``None``.
- ``max_calls`` - If not ``None``, populates at most this many keys.
  Defaults to ``None``, which means no limit.

Progress
--------

The method ``table.progress`` reports how many ``key_source`` entries have been populated and how many remain.
Two optional parameters allow more advanced use of the method.
A parameter of restriction conditions can be provided, specifying which entities to consider.
A Boolean parameter ``display`` (default is ``True``) allows disabling the output, such that the numbers of remaining and total entities are returned but not printed.

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
