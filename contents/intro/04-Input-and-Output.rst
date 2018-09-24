.. progress: 5.0 30% Dimitri

.. _input-output:

Input and Output
================

Where do the data live?
-------------------------

The first question new users ask is "Where are my data?"

Typically users asking this question are coming from the perspective of thinking about **data repositories**, collections of files and folders, and a (usually separate) collection of metadata - information about how the files were collected and what they contain.
Lets address metadata first, since the answer there is easy: Everything goes in the database!
Any information about the experiment that would normally be stored in a lab notebook, in an Excel spreadsheet, or in a Word document is entered into tables in the database.
These tables can accomodate numbers, strings, dates, or numerical arrays.
The entry of metadata can be manual, or it can be an automated part of data acquisition (in this case the acquisition software itself is modified to enter information directly into the database).

Depending on their size and contents, raw data files can be stored in a number of ways.
In the simplest and most common scenario, raw data  continue to be stored in either a local filesystem or in the cloud as collections of files and folders.
The paths to these files are entered in the database (again, either manually or by automated processes).
This is the point at which the notion of a **data pipeline** begins.
Below these "manual tables" that contain metadata and file paths are a series of tables that load raw data from these files, process it in some way, and insert derived or summarized data directly into the database.
For example, in an imaging application, the very large raw .TIFF stacks would reside on the filesystem, but the extracted fluorescent trace timeseries for each cell in the image would be stored as a numerical array directly in the database.
Or the raw video used for animal tracking might be stored in a standard video format on the filesystem, but the computed X/Y positions of the animal would be stored in the database.
Storing these intermediate computations in the database makes them easily available for downstream analyses and queries.

Do I have to manually enter all my data into the database?
----------------------------------------------------------

No! While some of the data will be manually entered (the same way that it would be manually recorded in a lab notebook), the advantage of DataJoint is that standard downstream processing steps can be run automatically on all new data with a single command.
This is where the notion of a **data pipeline** comes into play.
When the workflow of cleaning and processing the data, extracting important features, and performing basic analyses is all implemented in a DataJoint pipeline, minimal effort is required to analyze newly-collected data.
Depending on the size of the raw files and the complexity of analysis, useful results may be available in a matter of minutes or hours.
Because these results are stored in the database, they can be made available to anyone who is given access credentials for additional downstream analyses.

Won't the database get too big if all my data is there?
-------------------------------------------------------

Typically, this is not a problem.
If you find that your database is getting larger than a few dozen TB, DataJoint provides transparent solutions for storing very large chunks of data (larger than the 4GB that can be natively stored as a LONGBLOB in MySQL).
However, in many use scenarios even long time series or images can be stored directly in the database with little effect on performance.

Why not just process the data and save it back to a file?
---------------------------------------------------------

There are two main advantages to storing results in the database.
The first is data integrity. Because the relationships between data are enforced by the structure of the database, DataJoint ensures that the metadata in the upstream nodes always correctly describes the computed results downstream in the pipeline.
If a specific experimental session is deleted, for example, all the data extracted from that session is automatically removed as well, so there is no chance of "orphaned" data.
Likewise, the database ensures that computations are atomic.
This means that any computation performed on a data set is performed in an "all or none" fashion.
Either all of the data is processed and inserted, or none at all.
This ensures that there are no incomplete data. Neither of these important features of data integrity can be guaranteed by a file system.

The second advantage of storing intermediate results in a data pipeline is flexible access.
Accessing arbitrarily complex subsets of the data can easily be acheived with DataJoints flexible query language.
This is unlike the case where data is stored in files, where collecting the desired data requires trawling through the file hierarchy, finding and loading the files of interest, and selecting the parts of the data stored there are interesting for analysis.
This brings us to the final important question:

How do I get my data out?
-------------------------

This is the fun part. See :ref:`queries` for details of the DataJoint query language.
