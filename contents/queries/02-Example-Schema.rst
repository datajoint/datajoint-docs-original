.. progress: 1.0  90% Austin

.. _query-example:

Example Schema
==============

The example schema below contains data for a university enrollment system.
Information about students, departments, courses, etc. are organized in multiple tables.

.. python 1 start

.. warning::
  Empty primary keys, such as in the ``CurrentTerm`` table, are not yet supported by DataJoint.
  This feature will become available in a future release.
  See `Issue #113 <https://github.com/datajoint/datajoint-python/issues/113>`_ for more information.

.. code-block:: python

  @schema
  class Student (dj.Manual):
    definition = """
    student_id      : int unsigned # university ID
    ---
    first_name      : varchar(40)
    last_name       : varchar(40)
    sex             : enum('F', 'M', 'U')
    date_of_birth   : date
    home_address    : varchar(200) # street address
    home_city       : varchar(30)
    home_state      : char(2) # two-letter abbreviation
    home_zipcode    : char(10)
    home_phone      : varchar(14)
    """

  @schema
  class Department (dj.Manual):
    definition = """
    dept         : char(6) # abbreviated department name, e.g. BIOL
    ---
    dept_name    : varchar(200) # full department name
    dept_address : varchar(200) # mailing address
    dept_phone   : varchar(14)
    """

  @schema
  class StudentMajor (dj.Manual):
    definition = """
    -> Student
    ---
    -> Department
    declare_date :  date # when student declared her major
    """

  @schema
  class Course (dj.Manual):
    definition = """
    -> Department
    course      : int unsigned # course number, e.g. 1010
    ---
    course_name : varchar(200) # e.g. "Cell Biology"
    credits     : decimal(3,1) # number of credits earned by completing the course
    """

  @schema
  class Term (dj.Manual):
    definition = """
    term_year : year
    term      : enum('Spring', 'Summer', 'Fall')
    """

  @schema
  class Section (dj.Manual):
    definition = """
    -> Course
    -> Term
    section : char(1)
    ---
    room  :  varchar(12) # building and room code
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

.. warning::
  Empty primary keys, such as in the ``CurrentTerm`` table, are not yet supported by DataJoint.
  This feature will become available in a future release.
  See `Issue #127 <https://github.com/datajoint/datajoint-matlab/issues/127>`_ for more information.

File ``+university/Student.m``

.. code-block:: matlab

  %{
    student_id      : int unsigned # university ID
    ---
    first_name      : varchar(40)
    last_name       : varchar(40)
    sex             : enum('F', 'M', 'U')
    date_of_birth   : date
    home_address    : varchar(200) # street address
    home_city       : varchar(30)
    home_state      : char(2) # two-letter abbreviation
    home_zipcode    : char(10)
    home_phone      : varchar(14)
  %}
  classdef Student < dj.Manual
  end

File ``+university/Department.m``

.. code-block:: matlab

  %{
    dept         : char(6) # abbreviated department name, e.g. BIOL
    ---
    dept_name    : varchar(200) # full department name
    dept_address : varchar(200) # mailing address
    dept_phone   : varchar(14)
  %}
  classdef Department < dj.Manual
  end

File ``+university/StudentMajor.m``

.. code-block:: matlab

  %{
    -> university.Student
    ---
    -> university.Department
    declare_date :  date # when student declared her major
  %}
  classdef StudentMajor < dj.Manual
  end

File ``+university/Course.m``

.. code-block:: matlab

  %{
    -> university.Department
    course      : int unsigned # course number, e.g. 1010
    ---
    course_name : varchar(200) # e.g. "Cell Biology"
    credits     : decimal(3,1) # number of credits earned by completing the course
  %}
  classdef Course < dj.Manual
  end

File ``+university/Term.m``

.. code-block:: matlab

  %{
    term_year : year
    term      : enum('Spring', 'Summer', 'Fall')
  %}
  classdef Term < dj.Manual
  end

File ``+university/Section.m``

.. code-block:: matlab

  %{
    -> university.Course
    -> university.Term
    section : char(1)
    ---
    room  :  varchar(12) # building and room code
  %}
  classdef Section < dj.Manual
  end

File ``+university/CurrentTerm.m``

.. code-block:: matlab

  %{
    ---
    -> university.Term
  %}
  classdef CurrentTerm < dj.Manual
  end

File ``+university/Enroll.m``

.. code-block:: matlab

  %{
    -> university.Section
    -> university.Student
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
    -> university.Enroll
    ---
    -> university.LetterGrade
  %}
  classdef Grade < dj.Manual
  end

.. matlab 1 end

Example schema ERD
------------------

.. figure:: ../_static/img/queries_example_erd.png
    :align: center
    :alt: university example schema

    Example schema for a university database.
    Tables contain data on students, departments, courses, etc.
