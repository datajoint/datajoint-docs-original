Database Hosting
================

Database access
---------------
This section describes the recommended practices and configurations for the database back end to the DataJoint. If you host your data on `<https://datajoint.io>`_ or are working with a team who already use DataJoint, simply request your database credentials and skip this section.

Hosting the database server
---------------------------
DataJoint relies on a MySQL-compatible database server (e.g. `MySQL <https://www.mysql.com/>`_, `MariaDB <http://mariadb.org>`_, `Amazon Aurora <https://aws.amazon.com/rds/aurora/>`_) for all its data operations. 

The first decision you need to make is where this server will be hosted and how it will be administered. The server may be hosted on your personal computer or on a dedicated machine in your lab. Increasingly, many teams make use of cloud-hosted database services such as `Amazon RDS <https://aws.amazon.com/rds/>`_, which allow great flexibility and easy administration.

A cloud hosting option is provided by `<https://hub.datajoint.io>`_.  The hub simplifies the setup for labs who wish to host their data pipelines in the cloud and allows sharing pipelines between multiple groups and locations.

Docker
------
A docker image is available for a MySQL server configured to work with DataJoint: `<https://github.com/datajoint/mysql-docker>`_.

Database server configuration
-----------------------------
Default configurations for MySQL servers are not adequate for scientific data pipelines and need to be adjusted for stricter data checks and for large data packet sizes.  For reference, please see the ``my.cnf`` file used in our MySQL docker container: `<https://github.com/datajoint/mysql-docker>`_.

User accounts and privileges
----------------------------

Create user accounts on the MySQL server. For example, if your username is ``alice``, the SQL code for this step is

.. code-block:: mysql

    CREATE USER 'alice'@'%' IDENTIFIED BY 'alices-secret-password';

Teams that use DataJoint typically divide their data into schemas grouped together by common prefixes. For example, a lab may have a collection of schemas that begin with ``common_``. Some common processing may be organized into several schemas that begin with ``pipeline_``. Typically each user has all privileges to schemas that begin with her username.

For example, ``alice`` may have privileges to select and insert data from the common schemas (but not create new tables), and have all privileges to the pipeline schemas.

Then the SQL code to grant her privileges might look like

.. code-block:: mysql

    GRANT SELECT, INSERT ON `common\_%`.* TO 'alice'@'%';
    GRANT ALL PRIVILEGES ON `pipeline\_%`.* TO 'alice'@'%';
    GRANT ALL PRIVILEGES ON `alice\_%`.* TO 'alice'@'%';

