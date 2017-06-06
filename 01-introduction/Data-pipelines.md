# What Is a Data Pipeline?

DataJoint is a framework for creating scientific data pipelines from MATLAB and Python. 

A pipeline is a system that integrates data storage with data entry and computation.  In addition to all the functionality of an effective data repository, a data pipeline integrates mechanisms for the entry of manual data, automated data acquisition, automated importing from raw data storage, and automated processing and computation of various analyses.  

Data pipelines become the central tool for the operation of a data-intensive lab as it organizes the people with different roles and skills around a common framework.  Data sharing and publishing is no longer a separate step at the end of the project, it's an inherent feature of the process: to share data with other collaborators or to publish the data to the world, one only needs to set the access privileges. 


In DataJoint, a pipeline consists of nodes grouped into *schemas*. Each node is a table in a database as well as a class in MATLAB and Python that server as the interface to the table and implements computations for that node. Edges between nodes express dependencies between data as well as the direction of the workflow for the data.

The diagram below is an example of a pipeline used for multi-patching experiments. 
![](https://github.com/dimitri-yatsenko/andrew-multipatch/blob/master/erd.png)