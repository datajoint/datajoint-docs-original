# Query Basics

DataJoint allows manipulating and previewing data in the form of *relation objects* without retrieving any of the data into the workspace of the host language.

In the simplest case, `rel` is a *base relation* representing a table in the database. 
For example, we can instantiate the `experiment.Session` base relation as
```matlab
% matlab
rel = experiment.Session;       % in Matlab, constructors do not require parentheses ()
```
```python
# matlab or python
rel = experiment.Session() 
```
More generally, `rel` may be a *derived relation* constructed as an expression using [relational operators](Operators).

For example, the following relation contains information about all experiments and scans for mouse 102 (excluding experiments with no scans):
```matlab
% matlab
rel = experiment.Session * experiment.Scan & 'animal_id = 102';
```

```python
# python or matlab
rel = experiment.Session() * experiment.Scan() & 'animal_id = 102'
```
In python, querying via attribute dictionaries is also permitted:

```
# python 
rel = experiment.Session() * experiment.Scan() & {'animal_id': 102}
```

You can preview the contents of the relation in Python, Jupyter Notebook, or MATLAB by simply display the object:

<< FIGURE >>


To "fetch" means to transfer the data represented by the relation object into the workspace of the host language.  

All queries have the form `rel.fetch()` where `rel` is a relation object and `fetch` is one of several variants of fetch methods, which are described in [[Fetching]].
