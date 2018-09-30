.. progress: 8.0 5% Dimitri

.. _aggr:

Aggr
====

Aggregation is a special form of ``proj`` with the additional feature of allowing aggregation calculations on another table.
It has the form ``tab.aggr(other, ...)`` where ``other`` is another table.
Without the argument ``other``, ``aggr`` and ``proj`` are exactly equivalent.
Aggregation allows adding calculated attributes to each entity in ``tab`` based on aggregation functions over attributes in the :ref:`matching <matching>` entities of ``other``.

Aggregation functions include ``count``, ``sum``, ``min``, ``max``, ``avg``, ``median``, ``percentile``, ``stdev``, ``var``, and others.
Aggregation functions can only be used in the definitions of new attributes within the ``aggr`` operator.

As with ``proj``, the output of ``aggr`` has the same entity class, the same primary key, and the same number of elements as ``tab``.
Primary key attributes are always included in the output and may be renamed, just like in ``proj``.

Examples
--------

.. matlab 1 start

.. code-block:: matlab

  % Number of students in each course section
  university.Section.aggr(university.Enroll, n: count())
  % Average grade in each course
  university.Course.aggr(university.Grade * university.LetterGrade, avg_grade: avg(points))

.. matlab 1 end

.. python 1 start

.. code-block:: python

# Number of students in each course section
Section.aggr(Enroll, n: count())
# Average grade in each course
Course.aggr(Grade * LetterGrade, avg_grade: avg(points))

.. python 1 end
