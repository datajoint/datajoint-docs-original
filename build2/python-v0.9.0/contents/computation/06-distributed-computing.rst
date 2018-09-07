.. progress: 12.0 20% Dimitri

Distributed computing
=====================

Running ``populate`` on the same table on multiple computers, will causes them to attempt to compute the same data all at once.
This will not corrupt the data since DataJoint will reject any dupilication. 
One solution could be to cause the different computing nodes to populate the tables in random order.  This would reduce some collisions but not completely prevent them.

To allow efficient distributed computing, DataJoint provides a built-in job reservation process. When dj.Computed tables are auto-populated using job reservation, a record of each ongoing computation is kept in a schema-wide `jobs` table which is used internally by DataJoint to coordinate the auto-population effort among multiple computing processes.

.. include:: 06-distributed-computing_lang1.rst

