.. progress: 10.0 50% Austin

.. _universal-sets:

Universal Sets
==============

**Universal sets** are used in DataJoint to define virtual tables with arbitrary primary key structures for use in query expressions.
A universal set, defined using ``dj.U``, denotes the set of all possible entities with given attributes of any possible datatype.
Universal sets allow query expressions using virtual tables when no suitable base table exists.
Attributes of universal sets are allowed to be matched to any namesake attributes, even those that do not come from the same initial source.

For example, we may like to query the university database for the complete list of students' home cities, along with the number of students from each city.
The :ref:`schema <query-example>` for the university database does not have a table for cities and states.
A virtual table can fill the role of the nonexistent base table, allowing queries that would not be possible otherwise.

.. python 1 start

.. code-block:: python

  # All home cities of students
  dj.U('home_city', 'home_state') & Student
  # Total number of students from each city
  dj.U('home_city', 'home_state').aggr(Student, n: count())
  # Total number of students from each state
  U('home_state').aggr(Student, n: count())
  # Total number of students in the database
  U().aggr(Student, n: count())

.. python 1 end

.. matlab 1 start

.. code-block:: matlab

  % All home cities of students
  dj.U('home_city', 'home_state') & university.Student
  % Total number of students from each city
  dj.U('home_city', 'home_state').aggr(university.Student, n: count())
  % Total number of students from each state
  U('home_state').aggr(university.Student, n: count())
  % Total number of students in the database
  U().aggr(university.Student, n: count())

.. matlab 1 end

The result of aggregation on a universal set is restricted to the entities with matches in the aggregated table, such as ``Student`` in the example above.
In other words, ``X.aggr(A, ...)`` is interpreted as ``(X & A).aggr(A, ...)`` for universal set ``X``.
All attributes of a universal set are considered primary.

Universal sets should be used sparingly when no suitable base tables already exist.
In some cases, defining a new base table can make queries clearer and more semantically constrained.
