.. progress: 6.0 75% Dimitri

.. _accounts:

User Management
===============

Create user accounts on the MySQL server. For example, if your
username is alice, the SQL code for this step is:

.. code-block:: mysql

 CREATE USER 'alice'@'%' IDENTIFIED BY 'alices-secret-password';

Teams that use DataJoint typically divide their data into schemas
grouped together by common prefixes. For example, a lab may have a
collection of schemas that begin with ``common_``. Some common
processing may be organized into several schemas that begin with
``pipeline_``. Typically each user has all privileges to schemas that
begin with her username.

For example, alice may have privileges to select and insert data from
the common schemas (but not create new tables), and have all
privileges to the pipeline schemas.

Then the SQL code to grant her privileges might look like

.. code-block:: mysql

 GRANT SELECT, INSERT ON `common\_%`.* TO 'alice'@'%';
 GRANT ALL PRIVILEGES ON `pipeline\_%`.* TO 'alice'@'%';
 GRANT ALL PRIVILEGES ON `alice\_%`.* TO 'alice'@'%';

To note, the :code:`ALL PRIVILEGES` option allows the user to create
and remove databases without administrator intervention.

Once created, grants for a user can be listed using the :code:`SHOW GRANTS`
statement.

.. code-block:: mysql

 SHOW GRANTS FOR 'alice'@'%';
 +--------------------------------------------------------------------------------------------------------+
 | Grants for alice@%                                                                                     |
 +--------------------------------------------------------------------------------------------------------+
 | GRANT USAGE ON *.* TO 'alice'@'%' IDENTIFIED BY PASSWORD '*EB6CE16739B46D0FA9FE919C15B2EA6B72F41CBE'   |
 | GRANT SELECT, INSERT ON `common\_%`.* TO 'alice'@'%'                                                   |
 | GRANT ALL PRIVILEGES ON `pipeline\_%`.* TO 'alice'@'%'                                                 |
 | GRANT ALL PRIVILEGES ON `alice\_%`.* TO 'alice'@'%'                                                    |
 +--------------------------------------------------------------------------------------------------------+
 4 rows in set (0.04 sec)

Grouping with Wildcards
-----------------------

Depending on the complexity of your installation, using additional
wildcards to group access rules together might make managing user
access rules simpler. For example, the following equivalent
convention:

.. code-block:: mysql

 GRANT ALL PRIVILEGES ON `user_alice\_%`.* TO 'alice'@'%';

Could then facilitate using a rule like:

.. code-block:: mysql

 GRANT SELECT ON `user\_%\_%`.* TO 'bob'@'%';

to enable ``bob`` to query all other users tables using the
``user_username_database`` convention without needing to explicitly
give him access to ``alice\_%``, ``charlie\_%``, and so on.

This convention can be further expanded to create notions of groups
and protected schemas for background proccesing, etc. For example:

.. code-block:: mysql

 GRANT ALL PRIVILEGES ON `group\_shared\_%`.* TO 'alice'@'%';
 GRANT ALL PRIVILEGES ON `group\_shared\_%`.* TO 'bob'@'%';

 GRANT ALL PRIVILEGES ON `group\_wonderland\_%`.* TO 'alice'@'%';
 GRANT SELECT ON `group\_wonderland\_%`.* TO 'alice'@'%';

could allow both bob an alice to read/write into the
:code:`group\_shared` databases, but in the case of the
:code:`group\_wonderland` databases, read write access is restricted
to alice.
