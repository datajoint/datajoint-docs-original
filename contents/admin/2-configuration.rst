.. progress: 8.0 75% Dimitri

Relational Database Server
==========================

Hardware Considerations
-----------------------

As in any computer system, CPU, RAM Memory, Disk Storage, and Network
Speed are important components of performance. The relational database
component of DataJoint is no exception to this rule. This section
discusses the various factors relating to selecting a server for your
DataJoint pipelines.

CPU
~~~

CPU Speed and Parallelism (number of Cores/Threads) will impact the
speed of queries and the number of simultaneous queries which can be
efficiently supported by the system. It is a good rule of thumb to
have enough cores to support the number of active users and background
tasks you expect to have running in during a typical 'busy' day of
usage. For example, a team of 10 people might want to have 8
cores to support a few active queries and background tasks.


RAM
~~~

The amount of RAM will impact the amount of DataJoint data kept in
memory, allowing for faster querying of data since the data can be
searched and returned to the user without needing to access the slower
disk drives. It is a good idea to get enough memory to fully store the
more important and frequently accessed portions of your dataset, with
room to spare, especially if in-database blob storage is used instead
of external :ref:`bulk-storage-systems`.

Disk
~~~~

The disk storage for a datajoint database server should have fast
random access, ideally with flash-based storage to eliminate the
rotational delay of mechanical hard drives.

Networking
~~~~~~~~~~

When network connections are used, network speed and latency are
important to ensure that large query results can be quickly
transferred across the network and that delays due to data entry/query
round-trip have minimal impact on the runtime of the program.


General Recommendations
~~~~~~~~~~~~~~~~~~~~~~~

Since DataJoint datasets can consist of many thousands or even
millions of records, generally speaking one would want to make sure
that the relational database system has sufficient CPU speed and
parallelism to support a typical number of concurrent users and search
through the records quickly, enough RAM to store the primary key
values of commonly used tables and and operating system caches, fast
enough disk storage to support quick loading and searching through the
data, and sufficient network bandwidth to support transferring user
records quickly.

Large-Scale Installations
--------------------------

If system downtime or precise database responsiveness is a concern,
use of database replication may be beneficial since this can allow for
easier coordination of maintenance activities, faster recovery in the
event of system problems, and distribution of the database workload
across server machines to increase throughput and responsiveness.

Master-Slave Replication
~~~~~~~~~~~~~~~~~~~~~~~~

Master/slave replication allows for creation of a read-only database
copy which which is updated in real time. This copy can be used for
backup or queries which are not time sensitive and then be upgrade
read-write usage in the event that the main database fails.

Multi-Master Replication
~~~~~~~~~~~~~~~~~~~~~~~~

Multi-master replication configurations allow for all replicas to be
used in a read/write fashion, with the workload being distributed
among all machines. However, multi-master replication is also more
complicated, requiring front-end machines to distribute the workload,
similar performance characteristics on all replicas to prevent
bottlenecks, and redundant network connections to ensure the
replicated machines are always in sync.

Recommendations
---------------

It is usually best to go with the simplest solution which can suit the
requirements of the installation, adjusting workloads where possible,
and adding complexity only as needs dictate.

As a general rule of thumb, and of course dependant on the data
collection and processing needs of the given pipeline, a reasonably
powerful workstation or small server should support the needs of a
small user group of a handful of users (2-10), a medium or large
server should support the needs of a larger user community (10-30),
and replicated or distributed setup of 2 or more medium or large
servers may be required in larger cases. These requirements can be
reduced through the use of external or cloud storage, which is
discussed in the following section.


.. list-table:: Recommendations
  :header-rows: 1

  * - Usage Scenario
    - DataJoint Database Computer
    - Hardware Recommendation
  * - Single User
    - Personal Laptop or Workstation
    - 4 Cores, 8-16GB or more of RAM, SSD or better storage
  * - Small Group (e.g. 2-10 Users)
    - Workstation or Small Server
    - 8 or more Cores, 16GB or more of RAM, SSD or better storage
  * - Medium Group (e.g. 10-30 Users)
    - Small to Medium Server
    - 8-16 or more Cores, 32GB or more of RAM, SSD/RAID or better storage
  * - Large Group/Department (e.g. 30-50+ Users)
    - Medium/Large Server or Multi-Server Replication
    - 16-32 or more Cores, 64GB or more of RAM, SSD Raid storage, multiple machines
  * - Multi-Location Collaboration (30+ users, Geographically Distributed)
    - Large Server, Advanced Replication
    - 16-32 or more Cores, 64GB or more of RAM, SSD Raid storage, multiple machines; potentially multiple machines in multiple locations


Docker
------

A docker image is available for a MySQL server configured to work with
DataJoint: https://github.com/datajoint/mysql-docker.
