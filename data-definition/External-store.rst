External store
==============

.. important:: This section serves as the feature specification.  The implementation of this feature is schedule for the upcoming release.

DataJoint organizes most of its data in a relational database.  Relational databases are great for representing relationships between entities and storing structured data.
However, relational databases are not particularly well-suited for storing storing large, continuous chunks of data such as images, signals, and movies.  
An attribute of type ``longblob`` can contain an object up to 4 GB in size but storing many such large objects may hamper the performance of queries on that table.  A good rule of thumb is that if objects are over 10 MB in size, they probably should not be put in the relational database.
In addition, storing data in cloud-hosted relational databases is more expensive than in cloud-hosted storage systems such as AWS S3, for example. 

DataJoint introduces a new datatype, ``external`` to store large data objects within its relational framework.  

Defining an attribute of type ``external`` is done using the same :doc:`Definition-syntax` and, to the user, the work the same way as a ``blob`` datatype.  However, internally, the data are stored in an external storage system.  
This can be a shared file system accessible to all team members with access to these objects or in cloud storage solutions such as the AWS S3 system.  

For example, in the following table defines the storage of motion-aligned two-photon movies.

.. code-block:: text

    # Motion aligned movies
    -> twophoton.Scan
    ---
    aligned_movie :  external  # motion-aligned movie


All :doc:`../data-manipulation/Insert` and :doc:`../queries/Fetch` operations work identically with ``external`` attributes as any other blob attributes with the same serialization protocol.  Similar to blobs, external attributes cannot be used in restriction conditions.


Configuration
-------------
The following steps must be performed to enable external storage:

1. Assign settings ``external-location``, ``external-account``, and ``external-token`` in DataJoint configuration.

  In Python this is performed using ``dj.config``.  
  In MATLAB, this is peformed using ``dj.set``.

  ``external-location`` specifies the root path to the external data for all schemas as well as the protocol in the prefix such as ``file://`` or ``s3:``.

  ``exteral-account`` and ``external-token`` specify the credentials for accessing the external location.

2. For each schema, specify the name of the folder or bucket for that schema.

   In Python, this can be done using the ``set_external_storage`` method of the schema object.

   In MATLAB, this can be done using the ``setExternalStorge`` method of the schema object.


Implementation details
----------------------

Schemas will contain an auxiliary table ``~external`` to represent external storage.  
This table is declared automatically when it's first needed.
Attributes of type external are effectively renamed foreign keys into ``~external``.

The  primary key of ``external`` is the base64 ASCII `SHA-256 <https://en.wikipedia.org/wiki/SHA-2>`_ hash of (the stored object, the primary key value of its entry,  and the name of the table from which it originates).  This scheme ensures that the same objects are 

.. list-table:: ~external
   :widths: 15 15 15
   :header-rows: 1

   * - HASH
     - status
     - timestamp
   * - 1GEqtEU6JYEOLS4sZHeHDxWQ3JJfLlHVZio1ga25vd2
     - stored
     - 2017-06-07 23:14:01
   * - wqsKbNB1LKSX7aLEV+ACKWGr-XcB6+h6x91Wrfh9uf7
     - deleted
     - 2017-06-07 22:47:58

Caching
-------
To reduce 
