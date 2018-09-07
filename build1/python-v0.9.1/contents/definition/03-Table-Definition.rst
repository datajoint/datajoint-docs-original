.. progress: 16 30% Austin

Table Definition
================

Defining a table means to define the columns of the table (their names and datatypes) and constraints to be applied to them.

Both MATLAB and Python use the same syntax define tables.
In Python, the table definition is contained in the ``definition`` property of the class.
In MATLAB, the table definition is contained in the first block comment in the class definition file.
Note that although it looks like a mere comment, the table definition in MATLAB is parsed by DataJoint.
This solution thought to be convenient since MATLAB does not provide convenient syntax for multiline strings.

Tables have rows and columns.
Each column has a name and a datatype.
Rows don't have names or numbers and can only be identified by their contents.

For example, the following code in MATLAB and Python defines the same table, ``User`` that contains users of the database:


