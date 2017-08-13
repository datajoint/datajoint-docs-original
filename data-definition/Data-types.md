# Data Types

DataJoint supports the following datatypes. Use the smallest most restrictive datatype sufficient for your data.  

## Most common 
 * `tinyint`: an 8-bit integer number, ranging from -128 to 127.  
 * `tinyint unsigned`: an 8-bit positive integer number, ranging from 0 to 255.
 * `smallint`: a 16-bit integer number, ranging from -32,768 to 32,767.
 * `smallint unsigned`: a 16-bit positive integer, ranging from 0 to 65,535.
 * `int`: a 32-bit integer number, ranging from -2,147,483,648 to 2,147,483,647.  
 * `int unsigned`: a 32-bit positive integer, ranging from 0 to 4,294,967,295.
 * `enum`: one of several explicitly enumerated values specified as strings. Use this datatype instead of text strings to avoid spelling variations and to save storage space.  For example, for anesthesia, the datatype could be `enum("urethane", "isoflurane", "fentanyl")`.  Do not use enums in primary keys due to the difficulty of changing their definitions consistently in multiple tables.
 * `date`: date as `'YYYY-MM-DD'`.  
 * `time`: time as `'HH:MM:SS'`. 
 * `timestamp`: Date and time to the second as `'YYYY-MM-DD HH:MM:SS'`.  The default value may be set to `CURRENT_TIMESTAMP`.
 * `char(N)`:  a character string up to _N_ characters (but always takes the entire _N_ bytes to store).
 * `varchar(N)`:  a text string of arbitrary length up to *N* characters that takes *N+1* or *N+2* bytes of storage.
 * `float`:  a single-precision floating-point number.  Takes 4 bytes.  Single precision is sufficient for many measurements.  
 * `double`:  a double-precision floating-point number. Takes 8 bytes. Because equality comparisons are error-prone, neither `float` nor `double` should be used in primary keys. 
 * `decimal(N,F)`:  a fixed-point number with _N_ total decimal digits and _F_ fractional digits. This datatype is well suited to represent numbers whose magnitude is well defined and does not warrant the use of floating-point representation or requires precise decimal representations (e.g. dollars and cents). Because of its well-defined precision, `decimal` values can be used in equality comparison and be included in primary keys.
 * `longblob`: arbitrary MATLAB value (e.g. matrix, image, structure), up to 4  [GiB](http://en.wikipedia.org/wiki/Gibibyte) in size.  In Python, arbitrary numeric numpy array.  Numeric arrays are compatible between MATLAB and Python. 

## Less common (but supported)
 * `decimal(N,F) unsigned`: same as `decimal`, but limited to nonnegative values. 
 * `mediumint` a 24-bit integer number, ranging from -8,388,608 to 8,388,607.  
 * `mediumint unsigned`: a 24-bit positive integer, ranging from 0 to 16,777,216.
 * `mediumblob`: arbitrary MATLAB value, up to 16 [MiB](http://en.wikipedia.org/wiki/Mibibyte) 
 * `blob`: arbitrary MATLAB value, up to 64 [KiB](http://en.wikipedia.org/wiki/Kibibyte)
 * `tinyblob`: arbitrary MATLAB value, up to 256 bytes (actually smaller due to header info).

## Not (yet) supported
 * `binary`
 * `text`
 * `longtext`
 * `bit`

For additional information about these datatypes, see http://dev.mysql.com/doc/refman/5.6/en/data-types.html

## A note on fields and MySQL

Currently, DataJoint simply passes field declarations to MySQL without parsing it to restrict the use of SQL's modifiers such as `DEFAULT`, `NOT NULL`, and `UNIQUE`. However, DataJoint provides its way to implement each of these features in its own way and so it is best to use these features.

In DataJoint, there are three ways to impose a unique constraint.

 * Make it the primary key. We have seen some designs with a surrogate primary key with autoincrement and then a separate unique index on the natural attributes. In some cases, a better design is to use the unique fields as the primary key instead.

 * Use a `UNIQUE INDEX (...)` line in the declaration. This is documented in [definition syntax](Definition-syntax.html). It works the same way as in SQL, however it's more general than the UNIQUE modifier on a field since it can be applied to any number of attributes.

 * Use the unique option in the foreign key (datajoint >v0.8.1). This is documented in [foreign keys](Foreign-keys.html). This is the preferred way since it is consonant with the concept that DataJoint keeps the focus on entities rather than attributes.

