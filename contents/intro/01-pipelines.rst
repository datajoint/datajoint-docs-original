.. progress: 6 85% Dimitri

Data pipelines
==============

What is a data pipeline?
------------------------
A scientific *data pipeline* is a collections of processes and systems for organizing data, computations, and workflow used by a research group as they jointly perform complex sequences of data acquisition, processing, and analysis. 

A variety of tools can be used for supporting shared data pipelines: 

Data repository
  Research teams set up a shared *data repository*.  
  This minimal data management tool allows depositing and retrieving data and managing user access.

Database systems
  *Databases* are a form of data repositories that provide additional capabilities: 

    1) Allow defining, communicating, and enforcing structure in the stored data.
    2) Maintain data integrity: correct identification, consistent cross-references, dependencies, and groupings among the data.
    3) Support queries that retrieve various cross-sections and transformation of the deposited data.

Data Pipelines
  *Data Pipeline* frameworks may include all features of a database system but also provide additional capabilities: 

    1) A principled way to integrate computations to perform analysis and manage intermediate results 
    2) Support distributed computations without conflict
    3) Define, communicate, and enforce *workflow*, making clear the sequence of steps that must be performed for data entry, acquisition, and processing.

  Therefore, a full-featured data pipeline framework may also be described as a `scientific workflow system <https://en.wikipedia.org/wiki/Scientific_workflow_system>`_.

.. figure:: ../_static/img/pipeline-database.png
    :align: center
    :alt: data pipelines vs databases vs data repositories

    Major features of data management frameworks: data repositories, databases, and data pipelines.

What is DataJoint?
------------------
DataJoint is a free open-source framework for creating scientific data pipelines directly from MATLAB or Python (or any mixture of the two).
The data are stored in a language-independent way and other programming languages will be added in the future to work with the existing data.

In DataJoint, a data pipeline is a sequence of steps (more generally, a directed acyclic graph) with integrated data storage at each step. 
The pipeline may have some nodes requiring manual data entry or import from external sources. 
Experimenters and acquisition instruments feed data into nodes at the head of the pipeline. 
Downstream nodes perform automated computations for data processing and analysis.

.. figure:: ../_static/img/pipeline.png
    :width: 250px
    :align: center
    :alt: A data pipeline

    For example, this is the pipeline for a simple two-photon imaging experiment using mice as subjects.

In this example, the experimenter first enters information about the mouse information, then the imaging session information, then information for each scan.  
Then the automated portion of the pipeline takes over to perform image alignment to compensate for motion alignment, image segmentation to identify cells in the images and to extract calcium traces. 
Finally, the receptive field (RF) computation is performed by relating the calcium signals to the visual stimulus information.

When programming, users interact with these nodes in the form  MATLAB or Python objects that represent data and computations. 
Each object is associated with a separate table in a database. 
The data may be hosted locally or in the cloud.

.. image:: ../_static/img/high-level-pipeline.png
  :align: center 
  :alt: Data ecosystem

The data become immediately available to all participants of the project who have appropriate access privileges.  
Some of the "participants" may be computational agents that perform processing and analysis, including cloud computing solutions. 

DataJoint is designed for quick prototyping and continuous exploration as data pipelines continuously evolve.
New experiment designs and analysis methods can be added or removed.
Pipelines can grow large and complex while ever evolving,  reflecting the complexity of neuroscience experiments.  

DataJoint works well in combination with good code sharing (e.g. with `git <https://git-scm.com/>`_) and environment sharing (e.g. with `docker <https://www.docker.com/>`_)

Data pipelines become the central tool in the operations of a data-intensive lab or consortium as it organizes participants with different roles and skills around a common framework. 

With DataJoint, data sharing and publishing is no longer a separate step at the end of the project. Instead data sharing is an inherent feature of the process: to share data with other collaborators or to publish the data to the world, one only needs to set the access privileges. 

DataJoint uses a succinct data definition language, a powerful data query languages, and expressive visualizations of the pipeline. It also features a built-in distributed job management process to allow distributing analysis jobs between any number of computers.

A well-defined and principled approach to data organization and computation enables teams of scientists to work together efficiently.
