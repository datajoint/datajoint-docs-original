Distributed computing
=====================

Running ``populate`` on the same table on multiple computers, will causes them to attempt to compute the same data all at once.
This will not corrupt the data since DataJoint will reject any dupilication. 
One solution could be to cause the different computing nodes to populate the tables in random order.  This would reduce some collisions but not completely prevent them.

To allow efficient distributed computing, DataJoint provides a built-in job reservation process. 

|matlab|
In MATLAB, job reservations are activated by replacing ``populate`` calls with identical ``parpopulate`` calls.

|python|
In Python, job reservations are activated by setting the keyword argument ``reserve_jobs=True`` in ``populate`` calls.

.. important::
  Describe how to query the job reservation table

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
