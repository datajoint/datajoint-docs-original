User Management 
===============

Create user accounts on the MySQL server. For example, if your username is alice, the SQL code for this step is:

.. code-block:: mysql 

 CREATE USER 'alice'@'%' IDENTIFIED BY 'alices-secret-password';


Teams that use DataJoint typically divide their data into schemas grouped together by common prefixes. For example, a lab may have a collection of schemas that begin with ``common_``. Some common processing may be organized into several schemas that begin with ``pipeline_``. Typically each user has all privileges to schemas that begin with her username.

For example, alice may have privileges to select and insert data from the common schemas (but not create new tables), and have all privileges to the pipeline schemas.

Then the SQL code to grant her privileges might look like

.. code-block:: mysql

 GRANT SELECT, INSERT ON `common\_%`.* TO 'alice'@'%';
 GRANT ALL PRIVILEGES ON `pipeline\_%`.* TO 'alice'@'%';
 GRANT ALL PRIVILEGES ON `alice\_%`.* TO 'alice'@'%';

It may be more logical to prefix these categories of access with a category, to allow simpler wildcards to apply to all users; for example, the following equivalent convention:

.. code-block:: mysql

 GRANT ALL PRIVILEGES ON `user_alice\_%`.* TO 'alice'@'%';

Could then facilitate using a rule like:

.. code-block:: mysql

 GRANT SELECT ON `user\_%\_%`.* TO 'bob'@'%';

Which will enable ``bob`` to query all other users tables using the ``user_username_database`` convention without needing to explicitly give him access to ``alice\_%``, ``charlie\_%``, and so on.

