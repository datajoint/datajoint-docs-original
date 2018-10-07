.. progress: 10.0 75% Jake

.. _terminology:

Terminology
===========

DataJoint introduces a principled data model, which is described in detail in (`Yatsenko et al., 2018 <https://arxiv.org/abs/1807.11104>`_).
This data model is a conceptual refinement of the Relational Data Model and also draws on the Entity-Relationship Model (ERM).

The Relational Data Model was inspired by the concepts of *relations* in Set Theory.
When the formal relational data model was formulated it introduced additional terminology.
Practical programming languages such as SQL do not precisely follow the relational data model and introduce other terms to approximate relational concepts.
Subsequent data models (e.g. ERM) refined the relational data model and introduced their own terminology to describe analogous concepts.
As a result, similar concept may be described using different sets of terminologies, depending on the context and the speaker's background.

For example, what is known as a *relation* in the formal relational model is called a *table* in SQL; the analogous concept in ERM and DataJoint is called an *entity set*.

In the manual, we follow the terminology defined in `Yatsenko et al, 2018 <https://arxiv.org/abs/1807.11104>`_  except we replace  *entity set* with the more colloquial *table* or *query result* in most cases.

The table below summarizes the terms used for similar concepts across the related data models.

.. list-table:: Data model terminology
  :widths: 20 20 20 20 20
  :header-rows: 1

  * - Relational
    - ERM
    - SQL
    - DataJoint (formal)
    - This manual
  * - relation
    - entity set
    - table
    - entity set
    - table
  * - tuple
    - entity
    - row
    - entity
    - entity
  * - domain
    - value set
    - datatype
    - datatype
    - datatype
  * - attribute
    - attribute
    - column
    - attribute
    - attribute
  * - attribute value
    - attribute value
    - field value
    - attribute value
    - attribute value
  * - primary key
    - primary key
    - primary key
    - primary key
    - primary key
  * - foreign key
    - foreign key
    - foreign key
    - foreign key
    - foreign key
  * - schema
    - schema
    - schema or database
    - schema
    - schema
  * - relational expression
    - data query
    - ``SELECT`` statement
    - query expression
    - query expression


DataJoint: *databases*, *schemas*, *packages*, and *modules*
-------------------------------------------------------------

A **database** is collection of tables on the database server.
DataJoint users do not interact with it directly.

A **DataJoint schema** is

- a database on the database server containing tables with data *and*
- a collection of classes (in MATLAB or Python) associated with the database, one class for each table.

In MATLAB, the collection of classes is organized as a *package*, *i.e.* a file folder starting with a `+`.

In Python, the collection of classes is any set of classes decorated with the appropriate `schema` object.
Very commonly classes for tables in one database are organized as a distinct Python module.
Thus, typical DataJoint projects have one module per database.
However, this organization is up to the user's discretion.

*Base relations*
----------------

**Base relations** are tables in the database and we often refer to them as simply *tables*.
Base relations are distinguished from *derived relations*, which result from Relational :ref:`operators`.

*Relvars* and *relation values*
-------------------------------
In our early documentation we referred to the relation objects as **relvars** `<https://en.wikipedia.org/wiki/Relvar>`_.
This term  emphasizes the fact that relational variables and expressions do not contain actual data but are rather symbolic representations of data to be retrieved from the database.
The specific value of a relvar would then be referred to as the **relation value**.
The value of a relvar can change with changes in the state of the database.

In the more recent documentation, we have grown less pedantic and more often use the terms **relation** or **table** instead.

*Metadata*
----------
We avoid this term.

In data science, the term **metadata** commonly means "data about the data" rather than the data themselves.
For example, metadata could include data sizes, timestamps, data types, indexes, keywords.
In contrast,  neuroscientists often use the term to refer to conditions and annotations about experiments.
Such "metadata" are used to search and classify the data and are in fact an integral part of the actual **data**.

In DataJoint, all data other than blobs can be used in searches and categorization.
These fields may originate from manual annotations, preprocessing, or analysis.
Since *metadata* are not distinguished from simple *data*, we avoid this term.
Instead, we differentiate data into :ref:`data tiers <tiers>`.
