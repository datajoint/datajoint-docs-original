.. progress: 3.0 90% Dimitri

.. _normalization:

Entity Normalization
====================

DataJoint uses a uniform way of representing any data.
It does so in the form of **entity sets** -- unordered collections of entities of the same type. 
The term **entity normalization** describes the commitment to represent all data as well-formed entity sets.
Entity normalization is a conceptual refinement of the :ref:`relational data model <relational-model>` and the central principle of the DataJoint model (`Yatsenko et al., 2018 <https://arxiv.org/abs/1807.11104>`_).  Entity normalization leads to clear and logical database designs and easily comprehensible data queries.

Entity sets are a type of **relations** (from the :ref:`relational data model <relational-model>`) and are often visualized as *tables*. 
Hence the terms *relation*, *entity set*, and *table* can be used interchangeably when entity normalization is assumed.  

Criteria of a well-formed entity set 
------------------------------------
1. All elements of an entity set belong to the same well-defined and readily identified *entity type* from the model world.
2. All attributes of an entity set are applicable directly to each of its elements, although some attribute values may be missing (set to null).
3. All elements of an entity set must be distinguishable form each other by the same primary key.
4. Primary key attribute values cannot be missing, i.e. set to null.
5. All elements of an entity set participate in the same types of relationships with other entity sets.

Entity normalization in schema design 
-------------------------------------
Entity normalization applies to schema design where it is the designers' responsibility to identify the essential entity types in their model world and dependencies among them. 

The term entity normalization may also apply to a procedure for refactoring a schema design that does not meet the above criteria into one that does.
In some cases, this may require breaking up some entity sets into multiple entity sets, which may cause some entities to be represented across multiple entity sets.
In other cases, this may require converting attributes into their own entity sets.
Technically speaking, entity normalization entails compliance with the `Boyce-Codd normal form <https://en.wikipedia.org/wiki/Boyce%E2%80%93Codd_normal_form>`_ while lacking the representational power for the applicability of more complex normal forms (`Kent, 1983 <https://dl.acm.org/citation.cfm?id=358054>`_).
Adherence to entity normalization prevents redundancies in storage and anomalies ruing data manipulation anomalies. 
The same criteria originally motivated the formulation of the classical relational normal forms.

Entity normalization in data queries
------------------------------------
Entity normalization applies to data queries as well.
DataJoint's :ref:`query operators <operators>` are designed to preserve the entity normalization of its inputs.
For example, the output of operators :ref:`restriction`, :ref:`projection`, and :ref:`aggregation` retains the same entity type as the (first) input.
The :ref:`join` operator produces a new entity type comprising the pairing of the entity types of its inputs.
:ref:`Universal sets <universal-sets>` explicitly introduce virtual entity sets when necessary to accomplish a query.
