.. progress: 3.0 70% Dimitri

.. _normalization:

Entity Normalization
====================

In DataJoint, all data exist in the form of relations representing *entity sets*. As with any set, the order of elements in an entity set is never significant; elements cannot be addressed or identified by their position in the entity set. 
Since entity sets are relations, which are often visualized as tables, the terms relation, entity set, and table can be Entity normalization is a conceptual refinement of the relational data model and the central principle of the DataJoint model. 
Entity normalization is the requirement that all data must exist in the form of relations that meet the criteria of well-formed entity sets.

These criteria are:

1. All elements of an entity set belong to the same well-defined and readily identified entity type from the model world.
2. All attributes of an entity set are applicable directly to each of its elements, although some attribute values may be missing (set to null).
3. All elements of an entity set must be distinguishable form each other by the same primary key.
4. Primary key attribute values cannot be missing, i.e. set to null.
5. All elements of an entity set participate in the same types of relationships with other entity sets.

The term entity normalization refers to the procedure of refactoring a schema design that does not meet the above criteria into one that does. 
In some cases, this may require breaking up some entity sets into multiple entity sets, causing some entities to be represented across multiple entity sets. 
In other cases, this may require converting attributes into their own entity sets. 
Technically speaking, entity normalization entails compliance with the BoyceCoddnormal form while lacking the representational power for the applicability of more complex normal forms `[Kent, 1983] <https://dl.acm.org/citation.cfm?id=358054>`_. 
Thus adherence to entity normalization prevents redundancies and data manipulation anomalies that originally motivated the formulation of the classical relational normal forms.
