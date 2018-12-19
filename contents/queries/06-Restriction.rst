.. progress: 14.0 50% Austin

.. _restriction:

Restriction
===========

Restriction operators ``&`` and ``-``
-------------------------------------

The restriction operator ``A & cond`` selects the subset of entities from ``A`` that meet the condition ``cond``.
The exclusion operator ``A - cond`` selects the complement of restriction, i.e. the subset of entities from  ``A`` that do not meet the condition ``cond``.

.. figure:: ../_static/img/op-restrict.png
    :width: 400px
    :align: center
    :alt: Restriction and exclusion

    Restriction and exclusion.

The condition ``cond`` may be one of the following:

.. include:: 06-Restriction_lang1.rst

As the restriction and exclusion operators are complementary, queries can be constructed using both operators that will return the same results.
For example, the queries ``A & cond`` and ``A - Not(cond)`` will return the same entities.

Restriction by a table
----------------------

When restricting table ``A`` with another table, written ``A & B``, the two tables must be **join-compatible** (see :ref:`join-compatible`).
The result will contain all entities from ``A`` for which there exist a matching entity in ``B``.
Exclusion of table ``A`` with table ``B``, or ``A - B``, will contain all entities from ``A`` for which there are no matching entities in ``B``.

.. only:: html

    .. figure:: ../_static/img/restrict-example1.png
        :width: 546px
        :align: center
        :alt: Restriction by another table

        Restriction by another table.

    .. figure:: ../_static/img/diff-example1.png
        :width: 539px
        :align: center
        :alt: Exclusion by another table

        Exclusion by another table.

.. only:: latex

    .. figure:: ../_static/img/restrict-example1.png
        :align: center
        :alt: Restriction by another table

        Restriction by another table.

    .. figure:: ../_static/img/diff-example1.png
        :align: center
        :alt: Exclusion by another table

        Exclusion by another table.

Restriction by a table with no common attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Restriction of table ``A`` with another table ``B`` having none of the same attributes as ``A`` will simply return all entities in ``A``, unless ``B`` is empty as described below.
Exclusion of table ``A`` with ``B`` having no common attributes will return no entities, unless ``B`` is empty as described below.

.. only:: html

    .. figure:: ../_static/img/restrict-example2.png
        :width: 571px
        :align: center
        :alt: Restriction by a table with no common attributes

        Restriction by a table having no common attributes.

    .. figure:: ../_static/img/diff-example2.png
        :width: 571px
        :align: center
        :alt: Exclusion by a table having no common attributes

        Exclusion by a table having no common attributes.

.. only:: latex

    .. figure:: ../_static/img/restrict-example2.png
        :align: center
        :alt: Restriction by a table with no common attributes

        Restriction by a table having no common attributes.

    .. figure:: ../_static/img/diff-example2.png
        :align: center
        :alt: Exclusion by a table having no common attributes

        Exclusion by a table having no common attributes.


Restriction by an empty table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Restriction of table ``A`` with an empty table will return no entities regardless of whether there are any matching attributes.
Exclusion of table ``A`` with an empty table will return all entities in ``A``.

.. only:: html

    .. figure:: ../_static/img/restrict-example3.png
        :width: 563px
        :align: center
        :alt: Restriction by an empty table

        Restriction by an empty table.

    .. figure:: ../_static/img/diff-example3.png
        :width: 571px
        :align: center
        :alt: Exclusion by an empty table

        Exclusion by an empty table.

.. only:: latex

    .. figure:: ../_static/img/restrict-example3.png
        :align: center
        :alt: Restriction by an empty table

        Restriction by an empty table.

    .. figure:: ../_static/img/diff-example3.png
        :align: center
        :alt: Exclusion by an empty table

        Exclusion by an empty table.

Restriction by a mapping
------------------------

A key-value mapping may be used as an operand in restriction.
For each key that is an attribute in ``A``, the paired value is treated as part of an equality condition.
Any key-value pairs without corresponding attributes in ``A`` are ignored.

Restriction by an empty mapping or by a mapping with no keys matching the attributes in ``A`` will return all the entities in ``A``.
Exclusion by an empty mapping or by a mapping with no matches will return no entities.

For example, let's say that table ``Session`` has the attribute ``session_date`` of :ref:`datatype <datatypes>` ``datetime``.
You are interested in sessions from January 1st, 2018, so you write the following restriction query using a mapping.

.. include:: 06-Restriction_lang2.rst


Our mapping contains a typo omitting the final ``e`` from ``session_date``, so no keys in our mapping will match any attribute in ``Session``.
As such, our query will return all of the entities of ``Session``.

Restriction by a string
-----------------------

Restriction can be performed when ``cond`` is an explicit condition on attribute values, expressed as a string.
Such conditions may include arithmetic operations, functions, range tests, etc.
Restriction of table ``A`` by a string containing an attribute not found in table ``A`` produces an error.

.. include:: 06-Restriction_lang3.rst

Restriction by a collection
---------------------------

.. include:: 06-Restriction_lang4.rst


When ``cond`` is a collection of conditions, the conditions are applied by logical disjunction (logical OR).
Thus, restriction of table ``A`` by a collection will return all entities in ``A`` that meet *any* of the conditions in the collection.
For example, if you restrict the ``Student`` table by a collection containing two conditions, one for a first and one for a last name, your query will return any students with a matching first name *or* a matching last name.

.. include:: 06-Restriction_lang5.rst


Restriction by an empty collection returns no entities.
Exclusion of table ``A`` by an empty collection returns all the entities of ``A``.

Restriction by a Boolean expression
-----------------------------------

.. include:: 06-Restriction_lang6.rst


.. include:: 06-Restriction_lang7.rst

Restriction by a query
----------------------

Restriction by a query object is a generalization of restriction by a table (which is also a query object), because DataJoint queries always produce well-defined entity sets, as described in  :ref:`entity normalization <normalization>`.
As such, restriction by queries follows the same behavior as restriction by tables described above.

The example below creates a query object corresponding to all the sessions performed by the user Alice.
The ``Experiment`` table is then restricted by the query object, returning all the experiments that are part of sessions performed by Alice.

.. include:: 06-Restriction_lang8.rst
