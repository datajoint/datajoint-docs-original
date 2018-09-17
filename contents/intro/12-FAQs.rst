.. progress: 4 10% Dimitri

FAQs
====

GUIs?
-----


DataJoint vs ORMs
-----------------
What is the difference between DataJoint and established ORMs in Python such as SQLAlchemy and Django ORM, for example?

DataJoint and LIMS
------------------

DataJoint and Alyx
------------------
What is the difference between DataJoint and Alyx https://github.com/cortex-lab/alyx? 

Alyx is an experiment management database application developed in Kenneth Harris' lab at UCL. 

Alyx is an application with a more or less  fixed pipeline design with a nice graphical user interface to work with, whereas DataJoint is more of a general purpose library for designing and building such a processing pipeline. 
Alyx is more geared towards ease of data entry and tracking for a specific workflow (e.g. mouse colony information and some pre-specified experiments) and data types. 
DataJoint could be used as a more general purposes tool to design, implement, and also execute processing on such workflow/pipeline from scratch, and DataJoint focuses on flexibility, data integrity and ease of data analysis. 
The purposes are partly overlapping and complementary. 
We are actually working with IBL to make a bridge between the two systems. 
If you are interested in more features of DataJoint or have more questions, we also welcome you to our Slack group: datajoint.slack.com

