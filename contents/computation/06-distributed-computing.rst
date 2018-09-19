.. progress: 12.0 20% Dimitri

Distributed computing
=====================

Running ``populate`` on the same table on multiple computers will causes them to attempt to compute the same data all at once.
This will not corrupt the data since DataJoint will reject any duplication.
One solution could be to cause the different computing nodes to populate the tables in random order.
This would reduce some collisions but not completely prevent them.

To allow efficient distributed computing, DataJoint provides a built-in job reservation process.
When ``dj.Computed`` tables are auto-populated using job reservation, a record of each ongoing computation is kept in a schema-wide ``jobs`` table, which is used internally by DataJoint to coordinate the auto-population effort among multiple computing processes.

.. matlab 1 start
|matlab|
In MATLAB job reservations are activated by replacing ``populate`` calls with identical ``parpopulate`` calls.
.. matlab 1 end

.. python 1 start
|python|
In Python job reservations are activated by setting the keyword argument ``reserve_jobs=True`` in ``populate`` calls.
.. python 1 end

With job management enabled, the ``_make_tuples`` method of each table class will also consult the ``jobs`` table for reserved jobs as part of determining the next record to compute and will create an entry in the ``jobs`` table as part of the attempt to compute the resulting record for that key.
If the operation is a success, the record is removed.
In the event of failure, the job reservation entry is updated to indicate the details of failure.
Using this simple mechanism, multiple processes can participate in the auto-population effort without duplicating computational effort, and any errors encountered during the course of the computation can be individually inspected to determine the cause of the issue.

As part of DataJoint, the jobs table can be queried using native DataJoint syntax. For example, to list the jobs currently being run:

.. todo? : provide example schema here or later?

.. python 2 start
.. code-block:: text

    In [1]: schema.jobs
    Out[1]:
    *table_name    *key_hash      status       error_message  user           host           pid       connection_id  timestamp      key        error_stack
    +------------+ +------------+ +----------+ +------------+ +------------+ +------------+ +-------+ +------------+ +------------+ +--------+ +------------+
    __job_results  e4da3b7fbbce23 reserved                    datajoint@localhos localhost     15571     59             2017-09-04 14: <BLOB>     <BLOB>
     (2 tuples)

.. python 2 end

.. matlab 2 start
.. todo: matlab
.. matlab 2 end

The above output shows that a record for the ``JobResults`` table is currently reserved for computation, along with various related details of the reservation, such as the MySQL connection ID, client user and host, process ID on the remote system, timestamp, and the key for the record that the job is using for its computation.
Since DataJoint table keys can be of varying types, the key is stored in a binary format to allow the table to store arbitrary types of record key data.
We will discuss querying the jobs table for key data in the sections which follow.

As mentioned above, jobs encountering errors during computation will leave their record reservations in place, and update the reservation record with details of the error.

.. python 3 start
For example, if a Python process is interrupted via the keyboard, a Python KeyboardError will be logged to the database as follows:

.. code-block:: text

    In [2]: schema.jobs
    Out[2]:
    *table_name    *key_hash      status     error_message  user           host           pid       connection_id  timestamp      key        error_stack
    +------------+ +------------+ +--------+ +------------+ +------------+ +------------+ +-------+ +------------+ +------------+ +--------+ +------------+
    __job_results  3416a75f4cea91 error      KeyboardInterr datajoint@localhos localhost     15571     59             2017-09-04 14: <BLOB>     <BLOB>
     (1 tuples)

.. python 3 end

.. matlab 3 start
.. todo: similarly, in matlab (blah)
.. matlab 3 end

By leaving the job reservation record in place, the error can be inspected, and if necessary the corresponding ``dj.Computed`` update logic can be corrected.
From there the jobs entry can be cleared, and the computation can then be resumed.
In the meantime, the presence of the job reservation will prevent this particular record from being processed during subsequent auto-population calls.
Inspecting the job record for failure details can proceed much like any other DataJoint query.

.. python 4 start
For example, given the above table, errors can be inspected in Python as follows:

.. code-block:: text

    In [3]: (schema.jobs & 'status="error"' ).fetch(as_dict=True)
    Out[3]:
    [OrderedDict([('table_name', '__job_results'),
                  ('key_hash', 'c81e728d9d4c2f636f067f89cc14862c'),
                  ('status', 'error'),
                  ('key', rec.array([(2,)],
                             dtype=[('id', 'O')])),
                  ('error_message', 'KeyboardInterrupt'),
                  ('error_stack', None),
                  ('user', 'datajoint@localhost'),
                  ('host', 'localhost'),
                  ('pid', 15571),
                  ('connection_id', 59),
                  ('timestamp', datetime.datetime(2017, 9, 4, 15, 3, 53))])]


This particular error occurred when processing the record with ID ``2``, resulted from a `KeyboardInterrupt`, and has no additional
error trace.
.. python 4 end

.. todo?: might be 'interesting' to rerun a given error job -
   however this requires reconverting the ndarray back to a dict before
   calling add tuples in the Python case.. so this would probably be
   best provided by in a library utility function..

.. matlab 4 start
.. todo: similarly, in matlab (blah)
.. matlab 4 end

After any system or code errors have been resolved, the table can simply be cleaned of errors and the computation rerun.

.. python 5 start
For example, in Python:

.. code-block:: text

   In [4]: (schema.jobs & 'status="error"' ).delete()

.. python 5 end

.. matlab 5 start
.. todo: similarly, in matlab (blah)
.. matlab 5 end

.. todo: how to make the 'dj-jobs.py' example script available? listing?


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
