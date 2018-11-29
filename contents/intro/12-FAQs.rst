.. progress: 4 30% Dimitri

.. _faq:

FAQs
====

How do I use GUIs with DataJoint?
---------------------------------
It is common to enter data during experiments using a graphical user interface.


Does DataJoint support other programming languages?
---------------------------------------------------
DataJoint was originally developed to support MATLAB, followed by Python.
DataJoint's data model and data representation are largely language independent, which means that any language with a DataJoint client can work with a data pipeline defined in any other language.
DataJoint clients for other programming languages will be implemented based on demand.
All languages must comply to the same data model and computation approach as defined in `DataJoint: a simpler relational data model <https://arxiv.org/abs/1807.11104>`_.

Is DataJoint another ORM?
-------------------------
Programmers are familiar with object-relational mappings (ORM) in various programming languages.
Python in particular has several popular ORMs such as `SQLAlchemy <https://www.sqlalchemy.org/>`_ and `Django ORM <https://tutorial.djangogirls.org/en/django_orm/>`_.
The purpose of ORMs is to allow representations and manipulations of objects from the host programming language as data in a relational database.
ORMs allow making objects persistent between program executions.
ORMs create a bridge or a **mapping** between the object model used by the host language and the relational model allowed by the database.
The result is always a compromise, usually toward the object model.
ORMs usually forgo key concepts, features, and capabilities of the relational model for the sake of convenient programming constructs in the language.

In contrast, DataJoint implements a data model that is a refinement of the relational data model and that adheres to it faithfully without compromising its principles.
DataJoint supports data integrity (entity integrity, referential integrity, and group integrity) and provides a fully capable relational query language.
DataJoint remains absolutely data-centric, with the primary focus on the structure and integrity of the data pipeline.
Other ORMs are more application-centric, primarily focusing on the application design while the database plays a secondary role supporting the application with object persistence and sharing.

How can I use DataJoint with a LIMS?
------------------------------------
Lab Information Management Systems (LIMS)

What is the difference between DataJoint and Alyx?
--------------------------------------------------
`Alyx <https://github.com/cortex-lab/alyx>`_ is an experiment management database application developed in Kenneth Harris' lab at UCL.

Alyx is an application with a fixed pipeline design with a nice graphical user interface.
In contrast, DataJoint is a general-purpose library for designing and building data processing pipelines.

Alyx is geared towards ease of data entry and tracking for a specific workflow (e.g. mouse colony information and some pre-specified experiments) and data types.
DataJoint could be used as a more general purposes tool to design, implement, and execute processing on such workflows/pipelines from scratch, and DataJoint focuses on flexibility, data integrity, and ease of data analysis.
The purposes are partly overlapping and complementary.
The `International Brain Lab project <https://internationalbrainlab.com>`_ is developing a bridge from Alyx to DataJoint, hosted as an `open-source project <https://github.com/vathes/ibl-pipeline>`_.
It implements a DataJoint schema that replicates the major features of the Alyx application and a synchronization script from an existing Alyx database to its DataJoint counterpart.
