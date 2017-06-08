External store
==============

DataJoint organizes most of its data in a relational database.  Relational databases are great for representing relationships between entities and storing structured data.
However, relational databases are not particularly well-suited for storing storing large, continuous chunks of data such as images, signals, and movies.  
An attribute of type `longblob` can contain an object up to 4 GB in size but storing many such large objects may hamper the performance of queries on that table.  A good rule of thumb is that if objects are over 10 MB in size, they probably should not be put in the relational database.
In addition, storing data in cloud-hosted relational databases is more expnensive than in cloud-hosted storage systems such as AWS S3, for example. 

DataJoint introduces a new datatype, ``external`` to store large data objects within its relational framework.  

Defining an attribute of type ``external`` is done using the same :doc:`Definition-syntax` and, to the user, the work the same way as a ``blob`` datatype.  However, internally, the data are stored in an external storage system.  
This can be a shared file system accessible to all team members with access to these objects or in cloud storage solutions such as the AWS S3 system.  

.. important::
   Desicribe configuration of external storage 

.. important:: 
   Describe the internal linkage between tuples in tables and external stored objects
