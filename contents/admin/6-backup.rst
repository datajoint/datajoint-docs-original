.. progress: 8.0 50% Chris

Backups and Recovery 
====================

Backing up your DataJoint installation is critical to ensuring that
your work is safe and can be continued in the event of system
failures, and several mechanisms are available to use. 

Much like your live installation, your backup will consist of two portions:

  * Backup of the Relational Data
  * Backup of optional external bulk storage

This section primarily deals with backup of the relational data since
most of the optional bullk storage options use 'regular' flat-files
for storage and can be backed up via any 'normal' disk backup regieme.

There are many options to backup MySQL; subsequent sections discuss a
few options.

Cloud Hosted Backups
^^^^^^^^^^^^^^^^^^^^

In the case of cloud-hosted options, many cloud vendors provide
automated backup of your data, and some facility for downloading such
backups externally. Due to the wide variety of cloud-specific options,
we do not discuss these options here- however, since the cloud server
is also a MySQL server, other options listed here may work for your
situation.

Disk-Based Backup
^^^^^^^^^^^^^^^^^

The simplest option for many cases is to perform a disk-level backup
of your mysql installation using standard disk backup tools. It should
be noted that all database activity should be stopped for the duration
of the backup to prevent errors with the backed up data. This can be
done in one of two ways:

  * Stopping the mysql server program
  * Using database locks

These methods are required since mysql data operations can be ongoing
in the background even when no user activity is ongoing. To use a
database lock to perform a backup, the following commands can be used
as the mysql administrator:

.. code-block:: mysql

   FLUSH TABLES WITH READ LOCK;
   UNLOCK TABLES;
   
The backup should be peformed between the issuing of these two
commands, ensuring the database data is consistent on disk when it is
backed up.

MySQLDump
^^^^^^^^^

If disk based backups are not feasable for your installation, or your
database requires constant activity and so stopping it for backups is
not feasable, the simplest option for many cases is `MySQLDump <https://dev.mysql.com/doc/mysql-backup-excerpt/5.7/en/using-mysqldump.html>`__.
a command line tool which prints the contents of your database
contents in SQL form.

This tool is generally fine for most cases and is especially well
suited for smaller installations due to its simplicity/ease of
use.

For larger installations, the lower speed of mysqldump can be a
limitation since it has to convert the database contents to and from
SQL rather than dealing with the database files directly,
additionally, since backups are performed within a transaction, the
backup will be valid up to the time start of the backup rather than
it's completion, which can make ensuring the latest data is fully
backed up more difficult as the time it takes to run a backup grows.

Percona XTraBackup
^^^^^^^^^^^^^^^^^^

The percona `xtrabackup` tool provides near-realtime backup capability
of a mysql installation, with extended support for replicated
databases, and is a good tool for backing up larger databases.

However, This tool requires local disk access as well as reasonably
fast backup media, since it builds an ongoing transaction log in real
time to ensure that backups are valid up to the point of their
completion, failing if it cannot keep up with the write speed of the
database. Further, the backups it generates are in binary format and
include incomplete database transactions, which require careful
attention to detail when restoring.

As such, this solution is recommended only for advanced use cases or
larger databases where limitations of the other solutions may apply.

Locking and DDL Issues
^^^^^^^^^^^^^^^^^^^^^^

One important thing to note is that at the time of writing, MySQL's
transactional system is not `data definition language` aware, meaning
that changes to table structures occurring during some backup schemes
can result in corrupted backup copies. If schema changes will be
occuring during your backup window, it is a good idea to ensure that
appropriate locking mechanisms are used to prevent these changes
during critical steps of the backup process.

However, on on busy installations which cannot be stopped, the
use of locks in many backup utilities may cause issues if your
programs expect to write data to the database during the backup
window.

In such cases it might make sense to review the given backup tools for
locking related options or to use other mechanismis such as replicas
or alternate backup tools to prevent interaction of the database.

Replication and Snapshots for Backup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Larger databases consisting of many Terabytes of data may take many
hours or even days to backup and restore, and so downtime resulting
from system failure can create major impacts to ongoing work.

While not backup tools per-se, use of MySQL master-slave replication
and disk snapshots can be useful to assist in reducing the downtime
resulting from a full database outage.

Replicas can be configured so that one copy of the data is immediately
online in the event of server crash; when a server fails in this case,
users and programs simply restart and point to the new server before
resuming work.

Replicas can also reduce the system load generated by regular backup
procedures, since they can be backed up rather than the main server;
additionally they can allow more flexibility in a given backup scheme,
such as allowing for disk snapshots on a busy system which would not
otherwise be able to be stopped, since a replica copy can be stopped
temporarily and then resumed while a disk snapshot or other backup
operation occurs.
