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
The key represents the partially filled tuple, usually already containing :doc:`../definition/07-Primary-Key` attributes.

Inside the callback, three things always happen:

1. :doc:`../queries/02-fetch` data from tables upstream in the pipeline using the ``key`` for :doc:`../queries/04-restriction`.
2. The missing attributes are computed and added to the fields allredy in ``key``.
3. The entire tuple is inserted into ``self``.

``make_tuples`` may populate multiple tuples in one call when ``key`` does not specify the entire primary key of the populated table.


.. |python| image:: ../_static/img/python-tiny.png
