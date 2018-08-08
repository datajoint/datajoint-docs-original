Primary Key
===========

Primary keys in DataJoint
~~~~~~~~~~~~~~~~~~~~~~~~~

In relations, tuples are neither named nor numbered. Questions of the
kind "What is the 10th element of this relation?" are foreign to the
relational mindset. Instead, tuples are distinguished and identified by
their values. Furthermore, the entire tuple is not required. In each
relation, a subset of its attributes is designated to be the *primary
key*; these attributes alone are sufficient to differentiate any tuple
from any other within the relation.

Each table must have exactly one `primary
key <http://en.wikipedia.org/wiki/Primary_key>`__: a subset of its
attributes that uniquely identify each tuple in the table. The database
uses the primary key to prevent duplicate entries, to relate data across
tables, and to accelerate data queries. The choice of the primary key
will determine how you identify tuples. Therefore, make the primary key
**short**, **expressive**, and **persistent**.

For example, mice in our lab are assigned unique IDs. The mouse ID
number ``animal_id`` of type ``smallint`` can serve as the primary key
for the table ``Mice``. An experiment performed on a mouse may be
identified by two attributes: ``animal_id`` and ``experiment_number``.

DataJoint takes the concept of primary keys somewhat more seriously than
other models and query languages. Even *derived relations*, i.e. those
produced through operations on *base relations* have a well-defined
primary key. All operator on relations are designed in such a way that
the result has a well-defined primary key.

In all representations of relations in DataJoint, the primary key
attributes always come first and are highlighted somehow (e.g. in a
**bold** font or marked with an asterisk \*)

Defining a primary key
~~~~~~~~~~~~~~~~~~~~~~

In table declarations, the primary key attributes always come first and
are separated from the rest with a line containing at least three
dashes. For example, the following is the definition of a table
containing database users where ``username`` is the primary key.

::

    ## database users
    username : varchar(20)   # unique user name
    ---
    first_name : varchar(30)  
    last_name  : varchar(30) 
    role : enum('admin', 'contributor', 'viewer')

Entity integrity
~~~~~~~~~~~~~~~~

The primary key defines and enforces the desired property of databases
known as *entity integrity*. In a proper relational design, each
relation represents a collection of discrete real-world entities of some
kind. Entity integrity states that the database must prevent any
confusion between entities such as duplication or misidentification.

To enforce entity integrity, DataJoint implements several rules: \*
Every table must have a primary key \* Primary key attributes cannot
have default values (with the exception of ``auto_increment`` and
``CURRENT_TIMESTAMP``; see below). \* Operators on relations are defined
with respect to the primary key and preserve a primary key in their
results.

Datatypes in primary keys
~~~~~~~~~~~~~~~~~~~~~~~~~

All integer types, dates, timestamps, and short character strings make
good primary key attributes. Character strings are somewhat less
suitable because they can be long and because they may have invisible
trailing spaces. Floating-point numbers should be avoided because
rounding errors may lead to misidentification of tuples. Enums are okay
as long as they do not need to be modified later when [[Foreign keys]]
are already created referencing the table. Finally, DataJoint does not
support blob types in primary keys.

The primary key may be composite, i.e. comprising several attributes. In
DataJoint, hierarchical designs often produce tables whose primary keys
comprise many attributes.

Natural primary keys
~~~~~~~~~~~~~~~~~~~~

A primary key comprising real-world attributes is a `natural primary
key <http://en.wikipedia.org/wiki/Natural_key>`__. Natural primary keys
are a good choice when such real-world attributes are already properly
assigned and their permanence is ensured. If no convenient natural key
exists, an artificial attribute may be created whose purpose is to
uniquely identify entities in the real world. An institutional process
must ensure the uniqueness and permanence of such an identifier. For
example, the U.S. government assigns every worker an identifying
attribute, the social security number, but the government must go to
great lengths to ensure that this primary key is assigned exactly once
by checking against other less convenient candidate keys (i.e. the
combination of name, parents' names, date of birth, place of birth,
etc.) Just like the SSN, well managed primary keys tend to get
institutionalized and find multiple uses.

Your lab must maintain a system for uniquely identifying important
entities. For example, experiment subjects and experiment protocols must
have unique IDs. Use these as the primary keys in the corresponding
tables in your DataJoint databases.

Surrogate primary keys
~~~~~~~~~~~~~~~~~~~~~~

There are cases when a special attribute may be added to play the role
of the primary key that is never used outside the database. These
primary keys are called *surrogate*. Below are some cases when surrogate
keys are appropriately used.

Using hashes as primary keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some relations include too many attributes in their primary keys. For
example, the stimulus condition in a psychophysics experiment may have a
dozen parameters such that a change in any one of them makes a different
valid stimulus condition: all the attributes would need to be included
in the primary key. However, long primary keys make it difficult to
reference individual tuples. To be most useful, primary keys need to be
relatively short.

This problem is effectively solved through the use of a hash of all the
identifying attributes as the surrogate primary key. For example, MD5 or
SHA-1 hash algorithms can be used for this purpose. To keep their
representations human-readable, they may be encoded in base-64 ASCII.
For example, the 128-bit MD5 hash can be represented by 21 base-64 ASCII
characters but for many applications, taking the first 8 to 12
characters is sufficient to avoid collisions.

``auto_increment``
^^^^^^^^^^^^^^^^^^

Some entities are created by the very action of being entered into the
database. The action of entering them into the database gives them their
identity. It is impossible to duplicate them since entering the same
thing twice still means creating two distinct entities.

In such cases, the use of an auto-incremented primary key is warranted.
These are declared by adding the word ``auto_increment`` after the data
type in the declaration. The datatype must be an integer. Then the
database will assign incrementing numbers at each insert.

The example definition below defines an auto\_incremented primary key

::

    ## log entries
    entry_id  :  smallint auto_increment   
    ---
    entry_text :  varchar(4000)  
    entry_time = CURRENT_TIMESTAMP : timestamp(3)  # automatic timestamp with millisecond precision

DataJoint passes ``auto_increment`` behavior to the underlying MySQL and
therefore it has the same limitations: it can only be used for tables
with a single attribute in the primary key.

If you need to auto-increment an attribute in a composite primary key,
you will need to do so programmatically within a transaction to avoid
collisions.

For example, let’s say that you want to auto-increment ``scan_idx`` in a
table called ``Scan`` whose primary key is
``(animal_id, session, scan_idx)``. You must already have the values for
``animal_id`` and ``session`` in the dictionary ``key``. Then you can do
the following.

.. code:: python

    key['scan_idx'] = (Scan() & key).proj(next='max(scan_idx)+1').fetch1['next']

.. code:: matlab

    key.scah_idx = fetch1(Scan & key, 'next=max(scan_idx)+1')

