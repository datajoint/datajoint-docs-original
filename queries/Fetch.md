# Fetch

Data queries in DataJoint comprise two distinct steps:

1. Construct the relation `rel` to express the required data -- described in [[Query basics]] and [[Operators]].
2. Fetch the data into the workspace of the host language -- described in this section.

Fetch works somewhat differently between MATLAB and Python.

Note that tuples returned by `fetch` methods are not guaranteed to be sorted in any particular order unless specifically requested. Furthermore, the order is not guaranteed to be the same in any two queries and, unless they are wrapped in a transaction, the contents of two identical queries may change between two sequential invocations.  Therefore, if you wish to fetch matching pairs of attributes, do so in one `fetch` call.

---

## MATLAB
### Fetch the primary key
Without any arguments, the fetch method retrieves the primary key values of the relation in the form of a column array of [`struct`](https://www.mathworks.com/help/matlab/ref/struct.html). 
```matlab
keys = rel.fetch;
```

### Fetch entire relation
The following command retrieves all data from the relation in the form of a column array of type [`struct`](https://www.mathworks.com/help/matlab/ref/struct.html).

```matlab
data = rel.fetch('*');
```

### As separate variables 
Two fetch methods are used to retrieve individual attributes `fetch1` and `fetchn`.  `rel.fetch1` is used when `rel` is known to contain exactly one tuple. Then the retrieved strings and blobs are retrieved unwrapped. `rel.fetchn` is used for an arbitrary number of tuples in `rel`.  In this case, strings and blobs are returned in the form of cell arrays.

```matlab
[name, img] = rel.fetch1('name', 'image')    % when rel has exactly one tuple

[names, imgs] = rel.fetch('name', 'image')    % when rel has any number of tuples
```

Note that in MATLAB the object can be passed as an argument into its method so that `rel.fetchn(...)` is equivalent to `fetchn(rel, ...)`.  When `rel` is an expression, only the latter syntax works. 

### Obtaining the primary key along with individual values
It is often convenient to know the primary key values corresponding to attribute values retrieved by `fetchn`.  This can be done by adding another output argument to receive the key values:
```matlab
% retrieve names, images, and corresponding primary key values
[names, imgs, keys] = fetchn1(rel, 'name', 'image')   
```
The resulting value of `keys` will be a column array of type `struct`.  This mechanism is only implemented for `fetchn`. 

### Rename and calculate
In DataJoint for MATLAB, all `fetch` methods have all the same capability as the [[proj]] operator.  

```matlab
[names, BMIs] = rel.fetchn('name', 'weight/height/height -> bmi')
```

See the [[proj]] operator for an in-depth description of projection.


### Sorting and limiting the results
To sort the result, add the additional `ORDER BY` argument in `fetch` and `fetchn` methods. 
```matlab
% retrieve field `notes` from experiment sessions 
% performed by Alice, sorted by session date
notes = fetchn(experiment.Session & 'operator="alice"', 'note', ...
     'ORDER BY session_date'
```

The ORDER BY argument is passed directly to SQL and follows the same syntax as the [ORDER BY clause](https://dev.mysql.com/doc/refman/5.7/en/order-by-optimization.html)

Similarly, the LIMIT and OFFSET clauses can be used to limit the result to a subset of tuples.  For example, to return the top most recent sessions, one could do the following:
```matlab
s = fetch(experiment.Session, '*', 'ORDER BY session_date DESC', 'LIMIT 5')
```

The limit clause is passed directly to SQL and follows the same [rules](https://dev.mysql.com/doc/refman/5.7/en/select.html)

----

## Python
### Entire relation
The following statement retrieves the entire relation as a [`numpy.recarray`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html)

```python
data = rel.fetch()
```

To retrieve the data as a list of `dict`:
```python
data = rel.fetch.as_dict()
```

Furthermore, the `fetch` object can be used as a generator for loops:
```python
for row in rel.fetch:
   # row is a dict
```

### As separate variables 

```
name, img = rel.fetch1('name', 'image')  # direct values when rel has exactly one tuple
name, img = rel.fetch('name', 'image')  # [name, ...] [image, ...]
```

### Primary key values

```
keydict = rel.fetch1(dj.key)  # single key dict when rel has exactly one tuple
keylist = rel.fetch(dj.key)  # list of key dictionaries [{}, ...]
```

