.. progress: 14.0 10% Dimitri

.. _restriction:

Restriction
===========

Restriction operators ``&`` and ``-``
-------------------------------------

The restriction operator ``A & cond`` selects the subset of entities from ``A`` that meet the condition ``cond``.
The exclusion operator ``A - cond`` selects the complement of restriction, i.e. the subset of entities from  ``A`` that do not meet the condition ``cond``.

.. figure:: ../_static/img/op-restrict.png
    :align: center
    :alt: Restriction and exclusion

    Restriction and exclusion

The condition ``cond`` may be one of the following:

.. matlab 1 start

* another table
* a mapping, or ``struct``
* an expression in a character string
* a collection of conditions as a ``struct`` or cell array
* a boolean expression (``true`` or ``false``)

.. matlab 1 end

.. python 1 start

* another table
* a mapping, e.g. ``dict``
* an expression in a character string
* a collection of conditions, e.g. a ``list``
* a boolean expression (``True`` or ``False``)
* an ``AndList``

.. python 1 end

As the restriction and exclusion operators are complementary, queries can be constructed using both operators that will return the same results.
For example, the queries ``A & cond`` and ``A - Not(cond)`` will return the same entities.

Restriction with a table
~~~~~~~~~~~~~~~~~~~~~~~~

When restricting table ``A`` with another table ``A & B``, the two relations must be **join-compatible**.
The result will contain all entities from ``A`` for which there exist a matching entity in ``B``.

Restriction with another table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: ../_static/img/restrict-example1.png
   :alt: Restriction with another table

   Restriction with another table

Difference |Difference from another table|

Restriction with a table with no common attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: ../_static/img/restrict-example2.png
   :alt: Restriction with a table with no common attributes

   Restriction with a table with no common attributes

Difference |Difference from another table with no common attributes|

Restriction with an empty table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|Restriction with an empty table| Difference |Difference from an empty table|

.. |Difference from another table| image:: ../_static/img/diff-example1.png
.. |Difference from another table with no common attributes| image:: ../_static/img/diff-example2.png
.. |Restriction with an empty table| image:: ../_static/img/restrict-example3.png
.. |Difference from an empty table| image:: ../_static/img/diff-example3.png
