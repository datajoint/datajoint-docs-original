# Relational Data Model

The relational data model relies on a few basic concepts.  These concepts may be rather dry and abstract at this point so you might like to come back to review these after trying some examples.  
Note that these definitions are given as implemented in DataJoint and may differ from other descriptions. 

1. All data are represented as collections of simple tables (also called *relations*).  A relation represents a distinct class of entities in the real world or a class of relationships between entities.  This distinction is subtle since relationships may also be thought of as entities. 
1. Relations have unique rows (also called *tuples*).
1. Tuples in a given relation are independent of each other and represent distinct real-world *entities* or a *relationships* between entities.
1. Relations have named columns (also called *attributes*) with a fixed data type. All tuples in the same relation have the same sets of attributes.
1. Attribute values are *atomic*, i.e. the database does not break them up into further parts --- some deviations from this principle are allowed in DataJoint.
1. Some relations are *base relations*, i.e. they represent stored data and have names.
1. Related base relations are organized into named groups called *schemas*.
1. Other relations are *derived relations*: they are formed by applying *relational operators* to other relations.
1. Each relation (whether base or derived) has a primary key: a subset of its attributes that uniquely distinguish tuples in the relation. Relational operators respect the primary key.
1. *Referential constraints* (also known as *foreign keys*) define and enforce relationships between entities across base relations.