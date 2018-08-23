.. progress: 6 30% Dimitri

What is a data pipeline?
========================

DataJoint is a free open-source framework for creating scientific data pipelines using MATLAB or Python (or any mixture of the two) with a relational database and non-relational store as the backend. 

A data pipeline is a sequence of steps (more generally a directed acyclic graph) with integrated storage at each step.  These steps may be thought of as nodes in a graph.

In the initial nodes of the pipeline, data are typed in by the experimenters or are entered by data acquisition software.
In the later nodes of the pipeline, data are automatically processed and computed. Such computed nodes bind together code and data.

For example, the figure below depicts the pipeline for a simple two-photon imaging experiment using mice as subjects.

.. image:: ../_static/img/pipeline.png
    :width: 250px
    :align: center
    :alt: A data pipeline

The experimenter first enters information about the mouse information, then the imaging session information, then information for each scan.  Then the automated portion of the pipeline takes over to perform image alignment to compensate for motion alignment, image segmentation to identify cells in the images and to extract calcium traces. Finally, the receptive field (RF) computation is performed by relating the calcium signals to the visual stimulus information.

To the user, each node appears as a MATLAB or Python object that represents data and computations but underneath each object is connected to its own table in a relational database, which can be hosted locally or in the cloud. 

.. image:: ../_static/img/high-level-pipeline.png
  :align: center 
  :alt: Data ecosystem

The data becomes immediately available to all participates of the project with appropriate access privileges.  
This may include computational units that perform processing and analysis, including cloud computing solutions. 

DataJoint is designed for quick prototyping and continuous exploration since data pipelines quickly evolve and adopt to new experiment prototypes.  It works best when the team already has good code sharing practices (e.g. with git) and even environment sharing (e.g. with  docker)

Data pipelines become the central tool for the operation of a data-intensive lab as it organizes the people with different roles and skills around a common framework. 

Data sharing and publishing is no longer a separate step at the end of the project. Instead data sharing is an inherent feature of the process: to share data with other collaborators or to publish the data to the world, one only needs to set the access privileges. 

DataJoint uses an succinct data definition language, a powerful data query languages, and expressive visualizations of the pipeline. It also features a built-in distributed job management process to allow distributing analysis jobs between any number of computers.

Pipelines can grow large and complex while ever evolving,  reflecting the complexity of neuroscience experiments.  
A well-defined and principled approach to data organization and computation enables teams of scientists to work together efficiently.
