.. progress: 3.0 90% Dimitri

.. _normalization:

Entity Normalization
====================

DataJoint uses a uniform way of representing any data.
It does so in the form of **entity sets**, unordered collections of entities of the same type.
The term **entity normalization** describes the commitment to represent all data as well-formed entity sets.
Entity normalization is a conceptual refinement of the :ref:`relational data model <relational-model>` and is the central principle of the DataJoint model (`Yatsenko et al., 2018 <https://arxiv.org/abs/1807.11104>`_).
Entity normalization leads to clear and logical database designs and to easily comprehensible data queries.

Entity sets are a type of **relation** (from the :ref:`relational data model <relational-model>`) and are often visualized as **tables**.
Hence the terms **relation**, **entity set**, and **table** can be used interchangeably when entity normalization is assumed.

Criteria of a well-formed entity set
------------------------------------
1. All elements of an entity set belong to the same well-defined and readily identified **entity type** from the model world.
2. All attributes of an entity set are applicable directly to each of its elements, although some attribute values may be missing (set to null).
3. All elements of an entity set must be distinguishable form each other by the same primary key.
4. Primary key attribute values cannot be missing, i.e. set to null.
5. All elements of an entity set participate in the same types of relationships with other entity sets.

Entity normalization in schema design
-------------------------------------
Entity normalization applies to schema design in that the designer is responsible for the identification of the essential entity types in their model world and of the dependencies among the entity types.

The term entity normalization may also apply to a procedure for refactoring a schema design that does not meet the above criteria into one that does.
In some cases, this may require breaking up some entity sets into multiple entity sets, which may cause some entities to be represented across multiple entity sets.
In other cases, this may require converting attributes into their own entity sets.
Technically speaking, entity normalization entails compliance with the `Boyce-Codd normal form <https://en.wikipedia.org/wiki/Boyce%E2%80%93Codd_normal_form>`_ while lacking the representational power for the applicability of more complex normal forms (`Kent, 1983 <https://dl.acm.org/citation.cfm?id=358054>`_).
Adherence to entity normalization prevents redundancies in storage and data manipulation anomalies.
The same criteria originally motivated the formulation of the classical relational normal forms.

Entity normalization in data queries
------------------------------------
Entity normalization applies to data queries as well.
DataJoint's :ref:`query operators <operators>` are designed to preserve the entity normalization of their inputs.
For example, the outputs of operators :ref:`restriction <restriction>`, :ref:`proj <proj>`, and :ref:`aggr <aggr>` retain the same entity type as the (first) input.
The :ref:`join <join>` operator produces a new entity type comprising the pairing of the entity types of its inputs.
:ref:`Universal sets <universal-sets>` explicitly introduce virtual entity sets when necessary to accomplish a query.

Examples of poor normalization
------------------------------

Design choices lacking entity normalization may lead to data inconsistencies or anomalies. 
Below are several examples of poorly normalized designs and improved alternatives.

Indirect attributes
^^^^^^^^^^^^^^^^^^^

All attributes should apply to the entity itself.
Avoid attributes that actually apply to one of the entity's other attributes.
For example, consider the table ``Author`` with attributes ``author_name``, ``institution``, and ``institution_address``.
The attribute ``institution_address`` should really be held in a separate ``Institution`` table that ``Author`` depends on.

Repeated attributes
^^^^^^^^^^^^^^^^^^^

Avoid tables with many attributes that are merely different instances of the same data.
A better solution is to create a separate table that depends on the first (often a :ref:`part table <master-part>`), with multiple individual entities rather than repeated attributes.
For example, consider the table ``Protocol`` that includes the attributes ``equipment1`, ``equipment2``, and ``equipment3``.
A better design would be to create a ``ProtocolEquipment`` table that links each entity in ``Protocol`` with multiple entities in ``Equipment`` through :ref:`dependencies <dependencies>`.

Optional attributes
^^^^^^^^^^^^^^^^^^^

All attributes should be relevant to every entity in a table.
Attributes that do not apply to all entities should be moved to another dependent table containing only the appropriate entities.
For example, a table ``Protocol`` should include the attribute ``stimulus`` only if all experiment protocols include stimulation.
If the not all entities in ``Protocol`` involve stimulation, then the ``stimulus`` attribute should be located in another table that depends on ``Protocol`` and references its entities as appropriate.

Transient attributes
^^^^^^^^^^^^^^^^^^^^

Attributes should be relevant to all entities in a table at all times.
Attributes that do not apply to all entities should be moved to another dependent table containing only the appropriate entities.
This principle also applies to attributes that have not yet become meaningful for some entities or that will not remain meaningful indefinitely.
For example, consider the table ``Mouse`` with attributes ``birth_date`` and ``death_date``, where ``death_date`` is set to ``NULL`` for living mice.
Since the ``death_date`` attribute is not meaningful for mice that are still living, the proper design would include a separate table ``DeceasedMouse`` that depends on ``Mouse``.
``DeceasedMouse`` would only contain entities for dead mice, which improves integrity and averts the need for :ref:`updates <update>`.
