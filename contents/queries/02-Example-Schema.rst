.. progress: 1.0  90% Austin

.. _query-example:

Example Schema
==============

The example schema below

.. python 1 start

.. code-block:: python

  @schema
  class Student (dj.Manual):
    definition = """
    student_id : int unsigned
    # university ID
    ---
    first_name      : varchar(40)
    last_name       : varchar(40)
    sex             : enum(’F’, ’M’, ’U’)
    date_of_birth   : date
    home_address    : varchar(200)
    # street address
    home_city       : varchar(30)
    home_state      : char(2)
    # two-letter abbreviation
    home_zipcode    : char(10)
    home_phone      : varchar(14)
    """

  @schema
  class Department (dj.Manual):
    definition = """
    dept : char(6)
    # abbreviated department name, e.g. BIOL
    ---
    dept_name    : varchar(200)
    # full department name
    dept_address : varchar(200)
    # mailing address
    dept_phone   : varchar(14)
    """

  @schema
  class StudentMajor (dj.Manual):
    definition = """
    -> Student
    ---
    -> Department
    declare_date :  date
    # when student declared her major
    """

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

File ``+university/Student.m``

.. code-block:: matlab

  %{
    student_id : int unsigned
    # university ID
    ---
    first_name      : varchar(40)
    last_name       : varchar(40)
    sex             : enum(’F’, ’M’, ’U’)
    date_of_birth   : date
    home_address    : varchar(200)
    # street address
    home_city       : varchar(30)
    home_state      : char(2)
    # two-letter abbreviation
    home_zipcode    : char(10)
    home_phone      : varchar(14)
  %}
  classdef Student < dj.Manual
  end

File ``+university/Department.m``

.. code-block:: matlab

  %{
    dept : char(6)
    # abbreviated department name, e.g. BIOL
    ---
    dept_name    : varchar(200)
    # full department name
    dept_address : varchar(200)
    # mailing address
    dept_phone   : varchar(14)
  %}
  classdef Department < dj.Manual
  end

File ``+university/StudentMajor.m``

.. code-block:: matlab

  %{
    -> Student
    ---
    -> Department
    declare_date :  date
    # when student declared her major
  %}
  classdef StudentMajor < dj.Manual
  end

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
