# Database Hosting

## Database access
This section describes the recommended practices and configurations for the database back end to the DataJoint. If you are working in or collaborating with a team who already use DataJoint, simply request your database credentials and skip this section.

## Hosting the database server
DataJoint relies on a MySQL-compatible database server (e.g. [MySQL](https://www.mysql.com/), [MariaDB](mariadb.org), [Amazon Aurora](https://aws.amazon.com/rds/aurora/)) for all its data operations. 

The first decision you need to make is where this server will be hosted and how it will be administered. The server may be hosted on your personal computer or on a dedicated machine in your lab. Increasingly, many teams make use of cloud-hosted database services such as [Amazon RDS](https://aws.amazon.com/rds/), which allow great flexibility and easy administration.

A cloud hosting option is provided by https://hub.datajoint.io.  The hub simplifies the setup for labs who wish to host their data pipelines in the cloud and allows sharing pipelines between multiple groups and locations.

## Docker
A docker image is available for a MySQL server configured to work with DataJoint: https://github.com/datajoint/mysql-docker

## Database server configuration
Typical default configurations of MySQL servers is not adequate and needs to be adjusted to allow for stricter data checks and larger data packet sizes.  For reference, please see the `my.cnf` used in our MySQL docker container: https://github.com/datajoint/mysql-docker

## User account and privileges

Create user accounts on the MySQL server. For example, if your username is `alice`, the SQL code for this step is

```sql
CREATE USER 'alice'@'%' IDENTIFIED BY 'alices-secret-password';
```

Teams that use DataJoint typically divide their data into schemas grouped together by common prefixes. For example, a lab may have a collection of schemas that begin with `common_`. Some common processing may be organized into several schemas that begin with `pipeline_`. Typically each user has all privileges to schemas that begin with her username.

For example, `alice` may have privileges to select and insert data from the common schemas (but not create new tables), and have all privileges to the pipeline schemas.

Then the SQL code to grant her priviges might look like

```sql
GRANT SELECT, INSERT ON `common\_%`.* TO 'alice'@'%';
GRANT ALL PRIVILEGES ON `pipeline\_%`.* TO 'alice'@'%';
GRANT ALL PRIVILEGES ON `alice\_%`.* TO 'alice'@'%';
```
