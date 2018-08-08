Notes on Terminology
====================

Relational terminology 
----------------------
DataJoint is build on the foundation of the Relational Data Model.

The Relational Data Model was inspired by the concepts of *relations* in Set Theory.  Later, a formal relational data model was formulated, introducing additional terminology.  Later on, practical programming languages did not precisely follow the relational data model and used other terms to approximate relational concepts.  

For example, what is known as a *relation* in the formal relational model is called a *table* in SQL.  DataJoint closely adheres to the relational data model and the formal relational terminology is appropriate.  Hence, at different points we may refer to the same things using different terms.  Sometimes we may say "a row in the table" and on other occasions "a tuple in the relation" -- meaning the same thing. Please forgive us.  Various historical reasons have contributed to this mixture of terminologies and we will probably continue using them interchangeably. 

To help, here is a translation table:

=======================  ===========================================
Database Programming     Formal Relational Model   
=======================  ===========================================
*database*               *schema*  
*table*                  *relation*, *base relation*, *relvar* 
*query statement*        *derived relation*, *relational expression*
*column* or *field*      *attribute* 
*row*                    *tuple* 
=======================  ===========================================

DataJoint: *databases*, *schemas*, *packages*, and *modules*
-------------------------------------------------------------

A **database** is collection of tables on the database server.  DataJoint users do not interact with it directly.

A **DataJoint schema** is 

- a database on the database server containing tables with data *and* 
- a collection of classes (in MATLAB or Python) associated with the database, one class for each table.

In MATLAB, the collection of classes is organized as a *package*, *i.e.* a file folder starting with a `+`.

In Python, the collection of classes is any set of classes decorated with the appropriate `schema` object. 
Very commonly classes for tables in one database are organized as a distinct Python module.  Thus, typical DataJoint projects have one module per database.  However, this organization is up to the user's discretion. 

*Base relations*
----------------

**Base relations** are tables in the database and we often refer to them as simply *tables*.   Base relations are distinguished from *derived relations*, which result from Relational :doc:`../queries/Operators`.

*Relvars* and *relation values*
-------------------------------
In our early documentation we referred to the relation objects as **relvars** `<https://en.wikipedia.org/wiki/Relvar>`_.  This term  emphasizes the fact that relational variables and expressions do not contain actual data but are rather symbolic representations of data to be retrieved from the database.  The specific value of a relvar would then be referred to as the **relation value**. The value of a relvar can change with changes in the state of the database.  

In the more recent documentation, we have grown less pedantic and more often use the terms **relation** or **table** instead. 

*Metadata*
----------
We avoid this term.

In data science, the term **metadata** commonly means "data about the data" rather than the data themselves.  For example, metadata could include data sizes, timestamps, data types, indexes, keywords.  In contrast,  neuroscientists often use the term to refer to conditions and annotations about experiments.  Such "metadata" are used to search and classify the data and are in fact an integral part of the actual **data**.

In DataJoint, all data other than blobs can be used in searches and categorization.  These fields may originate from manual annotations, preprocessing, or analysis.  Since *metadata* are not distinguished from simply *data*, we avoid this term.  Instead, we differentiate data into :doc:`../definition/Data-tiers`.
