|matlab| MATLAB

.. code-block:: matlab

    populate(test.FilteredImage)

Note that it is not necessary which data needs to be computed.  DataJoint will call ``make_tuples``, one-by-one, for every key in ``Image`` for which ``FilteredImage`` has not yet been computed.

Chains of auto-populated tables form computational pipelines in DataJoint.

.. |matlab| image:: ../_static/img/matlab-tiny.png
