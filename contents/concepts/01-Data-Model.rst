.. progress: 12.0 50% Jake

.. _model:

Data Model
==========

What is a data model?
---------------------

By a *data model*, we refer to a conceptual framework for thinking about data and operations on data.
A data model defines the mental toolbox of the data scientist and has less to do with the *architecture* of the data systems.

For example, the most widely used and commonly familiar data model is a model based on files and folders, or more technically, a "hierarchical file system". In this model, data of any kind can be lumped together into a file, files are collected together into folders, and folders can be nested within other folders to create a folder hierarchy. Another familiar data model is the two-dimensional representation of data in a "spreadsheet", where items are listed in rows, and attributes of each item are stored in columns. The "object model" for data is used in object-oriented programming, where data is stored in properties of a class along with the methods that operate on it.

The "relational model" is a way of thinking about data as sets and operations on sets. Formalized almost a half-century ago[1]_, The relational data model provides the most rigorous approach to structured data storage and the most precise approach to querying data. The model is defined by the principles of data representation, domain constraints, uniqueness constraints, referential constraints, and declarative queries as summarised in Table 1. From a practical point of view, the relational model has many advantages over the both hierarchical file systems and spreadsheets in terms of maintaining data integrity, building analysis workflows, and providing flexible access to interesting subsets of the data.

Popular implementations of the relational data model rely on the Structured Query Language (SQL). SQL comprises distinct sublanguages for schema definition, data manipulation, and data queries. SQL thoroughly dominates in the space of relational databases and is often
conflated with the relational data model in casual discourse. Various terminologies are used to describe related concepts
from the relational data model. Similar to spreadsheets, relations are often visualized as *tables* with attributes corresponding to *columns* and tuples corresponding to *rows*. In particular, SQL uses the terms *table*, *column*, and *row*.

Core Principles of the relational data model
        **Data representation.** Data are represented and manipulated in the form of relations. A relation is a set (i.e. an unordered collection) of tuples of values for each of the respective named attributes of the relation. Base relations represent stored data while derived relations are formed from base relations through query expressions. A collection of base relations with their attributes, domain constraints, uniqueness constraints, and referential constraints is called a schema.

        **Domain constraints.** Attribute values are drawn from corresponding attribute domains, i.e. predefined sets of values. Attribute domains may not include relations, keeping data model flat, free of nested structures.

        **Uniqueness constraints.** Tuples within relations are addressed by values of their attributes. To identify and relate data elements, uniqueness constraints are imposed on subsets of attributes, then referred to as keys. One key in a relation is designated as the primary key used for referencing its elements.

        **Referential constraints.** Associations among data are established by means of referential constraints with the help of foreign keys. A referential constraint on relation A referencing relation B allows only those tuples in A whose foreign key attributes match the key attributes of a tuple in B.

        **Declarative queries.** Data queries are formulated through declarative, as opposed to imperative, specifications of sought results. This means that query expressions convey the logic for the result rather than the procedure for obtaining it. Formal languages for query expressions include relational algebra, relational calculus, and SQL.

DataJoint is a Refinement of the Relational Data Model
------------------------------------------------------

We introduce DataJoint as a conceptual refinement of the relational data model offering a more expressive and rigorous framework for database programming. The DataJoint model facilitates clear conceptual modeling, efficient schema design, and precise and flexible data queries. The model has emerged over a decade of continuous development of complex data pipelines for neuroscience experiments
[Yatsenko et al., 2015]. DataJoint has allowed researchers with no prior knowledge of databases to collaborate effectively on common data pipelines sustaining data integrity and supporting flexible access. DataJoint is currently implemented as client libraries in MATLAB and Python. These libraries work by transpiling DataJoint queries into SQL before passing them on to conventional
relational database systems serving as the backend.

DataJoint comprises
 * a schema definition language (link)
 * a data manipulation language (link)
 * a data query language (link)
 * diagramming notation for visualizing relationships between modeled entities (link).

**Entity Normalization**

In DataJoint, all data exist in the form of relations representing *entity sets*. As with any set, the order of elements
in an entity set is never significant; elements cannot be addressed or identified by their position in the entity set. Since entity sets are relations, which are often visualized as tables, the terms relation, entity set, and table can be Entity normalization is a conceptual refinement of the relational data model and the central principle of the DataJoint model. Entity normalization is the requirement that all data must exist in the form of relations that meet the criteria of well-formed entity sets.
These criteria are:

1. All elements of an entity set belong to the same well-defined and readily identified entity type from the model world.
2. All attributes of an entity set are applicable directly to each of its elements, although some attribute values may be missing (set to null).
3. All elements of an entity set must be distinguishable form each other by the same primary key.
4. Primary key attribute values cannot be missing, i.e. set to null.
5. All elements of an entity set participate in the same types of relationships with other entity sets.

The term entity normalization refers to the procedure of refactoring a schema design that does not meet the above criteria into one that does. In some cases, this may require breaking up some entity sets into multiple entity sets, causing some entities to be represented across multiple entity sets. In other cases, this may require converting attributes into their own entity sets. Technically speaking, entity normalization entails compliance with the BoyceCoddnormal form while lacking the representational power for the applicability of more complex normal forms [Kent, 1983]. Thus adherence to entity normalization prevents redundancies and data manipulation anomalies
that originally motivated the formulation of the classical relational normal forms.

**Adherence to entity normalization is the common thread unifying DataJoint’s data definition, data manipulation, and data queries.**
