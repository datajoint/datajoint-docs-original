.. progress: 12.0 20% Dimitri

.. _distributed:

Distributed computing
=====================

Running ``populate`` on the same table on multiple computers will causes them to attempt to compute the same data all at once.
This will not corrupt the data since DataJoint will reject any duplication.
One solution could be to cause the different computing nodes to populate the tables in random order.
This would reduce some collisions but not completely prevent them.

To allow efficient distributed computing, DataJoint provides a built-in job reservation process.
When ``dj.Computed`` tables are auto-populated using job reservation, a record of each ongoing computation is kept in a schema-wide ``jobs`` table, which is used internally by DataJoint to coordinate the auto-population effort among multiple computing processes.

.. include: 06-distributed-computing_lang1.rst


With job management enabled, the ``make`` method of each table class will also consult the ``jobs`` table for reserved jobs as part of determining the next record to compute and will create an entry in the ``jobs`` table as part of the attempt to compute the resulting record for that key.
If the operation is a success, the record is removed.
In the event of failure, the job reservation entry is updated to indicate the details of failure.
Using this simple mechanism, multiple processes can participate in the auto-population effort without duplicating computational effort, and any errors encountered during the course of the computation can be individually inspected to determine the cause of the issue.

As part of DataJoint, the jobs table can be queried using native DataJoint syntax. For example, to list the jobs currently being run:

.. todo? : provide example schema here or later?


.. include: 06-distributed-computing_lang2.rst

The above output shows that a record for the ``JobResults`` table is currently reserved for computation, along with various related details of the reservation, such as the MySQL connection ID, client user and host, process ID on the remote system, timestamp, and the key for the record that the job is using for its computation.
Since DataJoint table keys can be of varying types, the key is stored in a binary format to allow the table to store arbitrary types of record key data.
We will discuss querying the jobs table for key data in the sections which follow.

As mentioned above, jobs encountering errors during computation will leave their record reservations in place, and update the reservation record with details of the error.


.. include: 06-distributed-computing_lang3.rst

By leaving the job reservation record in place, the error can be inspected, and if necessary the corresponding ``dj.Computed`` update logic can be corrected.
From there the jobs entry can be cleared, and the computation can then be resumed.
In the meantime, the presence of the job reservation will prevent this particular record from being processed during subsequent auto-population calls.
Inspecting the job record for failure details can proceed much like any other DataJoint query.


.. todo?: might be 'interesting' to rerun a given error job -
   however this requires reconverting the ndarray back to a dict before
   calling add tuples in the Python case.. so this would probably be
   best provided by in a library utility function..

.. include: 06-distributed-computing_lang4.rst

After any system or code errors have been resolved, the table can simply be cleaned of errors and the computation rerun.


.. include: 06-distributed-computing_lang5.rst

.. todo: how to make the 'dj-jobs.py' example script available? listing?


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
