.. progress: 10.0 30% Austin

.. _definition-syntax:

Definition Syntax
=================

The table definition consists of one or more lines.
Each line can be one of the following:

* The optional first line starting with a ``#`` provides a description of the table's purpose.
  It may also be thought of as the table's long title.
* A new attribute definition in any of the following forms (see :ref:`datatypes` for valid datatypes):

  - ``name : datatype``
  - ``name : datatype # comment``
  - ``name = default : datatype``
  - ``name = default : datatype  # comment``
* The divider ``---`` (at least three hyphens) separating primary key attributes above from secondary attributes below.
* A foreign key in the format ``-> ReferencedTable``.
  (See :ref:`Dependencies`.)

For example, the table for Persons may have the following definition:

.. code-block:: text

	# Persons in the lab
	username :  varchar(16)   #  username in the database
	---
	full_name  : varchar(255)
	start_date :  date   # date when joined the lab


This will define the table with attributes ``username``, ``full_name``, and ``start_date``, in which ``username`` is the :ref:`primary key <primary-key>`.

Attribute names
---------------
Attribute names must be in lowercase and must start with a letter.
They can only contain alphanumerical characters and underscores.
The attribute name cannot exceed 64 characters.

Valid attribute names
   ``first_name``, ``two_photon_scan``, ``scan_2p``, ``two_photon_scan_``

Invalid attribute names
   ``firstName``, ``first name``, ``2photon_scan``, ``two-photon_scan``, ``TwoPhotonScan``

Default values
--------------

Non-primary attributes can be given default values.
A default value will be used for an attribute if no other value is given at the time the entity is :ref:`inserted <insert>` into the table.
Note that default values can only be used when inserting as a mapping.
Primary key attributes cannot have default values (with the exception of ``auto_increment`` and ``CURRENT_TIMESTAMP`` attributes; see :ref:`primary-key`).
