.. progress: 1.0  90% Austin

.. _query-example:

Example Schema
==============

.. python 1 start

.. code-block:: python

  @schema
  class Course (dj.Manual):
    definition = """
    -> Department
    course      : int unsigned
    # course number, e.g. 1010
    ---
    course_name : varchar(200)
    # e.g. "Cell Biology"
    credits     : decimal(3,1)
    # number of credits earned by completing the course
    """

  @schema
  class Term (dj.Manual):
    definition = """
    term_year : year
    term      : enum(’Spring’, ’Summer’, ’Fall’)
    """

  @schema
  class Section (dj.Manual):
    definition = """
    -> Course
    -> Term
    section : char(1)
    ---
    room  :  varchar(12)
    # building and room code
    """

  @schema
  class CurrentTerm (dj.Manual):
    definition = """
    ---
    -> Term
    """

  @schema
  class Enroll (dj.Manual):
    definition = """
    -> Section
    -> Student
    """

  @schema
  class LetterGrade (dj.Manual):
    definition = """
    grade : char(2)
    ---
    points : decimal(3,2)
    """

  @schema
  class Grade (dj.Manual):
    definition = """
    -> Enroll
    ---
    -> LetterGrade
    """

.. python 1 end

.. matlab 1 start

File ``+university/Course.m``

.. code-block:: matlab

  %{
    -> Department
    course      : int unsigned
    # course number, e.g. 1010
    ---
    course_name : varchar(200)
    # e.g. "Cell Biology"
    credits     : decimal(3,1)
    # number of credits earned by completing the course
  %}
  classdef Course < dj.Manual
  end

File ``+university/Term.m``

.. code-block:: matlab

  %{
    term_year : year
    term      : enum(’Spring’, ’Summer’, ’Fall’)
  %}
  classdef Term < dj.Manual
  end

File ``+university/Section.m``

.. code-block:: matlab

  %{
    -> Course
    -> Term
    section : char(1)
    ---
    room  :  varchar(12)
    # building and room code
  %}
  classdef Section < dj.Manual
  end

File ``+university/CurrentTerm.m``

.. code-block:: matlab

  %{
    ---
    -> Term
  %}
  classdef CurrentTerm < dj.Manual
  end

File ``+university/Enroll.m``

.. code-block:: matlab

  %{
    -> Section
    -> Student
  %}
  classdef Enroll < dj.Manual
  end

File ``+university/LetterGrade.m``

.. code-block:: matlab

  %{
    grade : char(2)
    ---
    points : decimal(3,2)
  %}
  classdef LetterGrade < dj.Manual
  end

File ``+university/Grade.m``

.. code-block:: matlab

  %{
    -> Enroll
    ---
    -> LetterGrade
  %}
  classdef Grade < dj.Manual
  end

.. matlab 1 end
