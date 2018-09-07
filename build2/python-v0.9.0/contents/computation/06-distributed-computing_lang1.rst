|python|
In Python, job reservations are activated by setting the keyword argument ``reserve_jobs=True`` in ``populate`` calls.

With job managment enabled, the ``_make_tuples`` method of each table class will also consult the `jobs` table for reserved jobs as part of determining the next record to compute, and create an entry in the `jobs` table as part of the attempt to compute the resulting record for that key. If the operation is a success, the record is removed, or, in the event of failure, the job reservation entry is updated to indicate the details of failure. Using this simple mechanism, multiple processes can participate in the auto-population effort without duplicating computational effort, and any errors encountered during the course of the computation can be individually inspected to determine the cause of the issue.

As part of the DataJoint, the jobs table can be queried using `native` DataJoint syntax. For example, to list the jobs currently being run:

.. todo? : provide example schema here or later?

.. code-block:: text

    In [1]: schema.jobs
    Out[1]:
    *table_name    *key_hash      status       error_message  user           host           pid       connection_id  timestamp      key        error_stack   
    +------------+ +------------+ +----------+ +------------+ +------------+ +------------+ +-------+ +------------+ +------------+ +--------+ +------------+
    __job_results  e4da3b7fbbce23 reserved                    datajoint@localhos localhost     15571     59             2017-09-04 14: <BLOB>     <BLOB>        
     (2 tuples)



.. |python| image:: ../_static/img/python-tiny.png
