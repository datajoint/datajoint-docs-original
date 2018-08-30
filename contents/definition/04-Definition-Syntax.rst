.. progress: 10.0 30% Austin

Definition Syntax
=================

The table definition consist of lines.
Each line can be one of the following:

* The optional first line starting with a ``#`` provides a description of the table's purpose.
  It may also be thought of as the table's long title.
* A new attribute definition in any of the following forms (see :doc:`06-Data-Types` for valid datatypes):

  - ``name : datatype``
  - ``name : datatype # comment``
  - ``name = default : datatype``
  - ``name = default : datatype  # comment``
* The divider ``---`` (at least three dashes) separating primary key attributes above from non-primary attributes below.
* A foreign key in the format ``-> ReferencedTable``.
  (See :doc:`10-dependencies`.)

For example, the table for Persons may have the following definition:

.. code-block:: text

	# Persons in the lab
	username :  varchar(16)   #  username in the database
	---
	full_name  : varchar(255)
	start_date :  date   # date when joined the lab


This will define the table with columns ``username``, ``full_name``, and ``start_date``, in which ``username`` is the :doc:`07-Primary-Key`.

Attribute names
---------------
Attribute names must be in lowercase and must start with a letter.
They can only contain alphanumerical characters and underscores.
The attribute name cannot exceed 64 characters.

Valid attribute names
   ``first_name``, ``two_photon_scan``, ``scan_2p``, ``two_photon_scan_``

Invalid attribute names
   ``firstName``, ``first name``, ``2photon_scan``, ``two-photon_scan``, ``TwoPhotonScan``
