# Insert

The `insert` method of DataJoint table objects inserts rows of data into the table.

## MATLAB
In MATLAB, the `insert` method inserts any number of tuples in the form of a structure array with field attributes corresponding to the attribute names.

For example,
```matlab
s.username = 'alice';
s.first_name = 'Alice';
s.last_name = 'Cooper';
insert(lab.Person, s)
```

For quck entry of multiple tuples, we can take advantage of MATLAB's cell array notation:
```matlab
insert(lab.Person, {
       'alice'   'Alice'   'Cooper'
       'bob'     'Bob'     'Dylan'
       'carol'   'Carol'   'Douglas'
})
```
In this case, the values must match the order of the attributes in the table. 

## Python
In Python, there is a separate method, `insert1` to insert one tuple at a time.  The tuple may have the form of a Python dictionary with key names matching the attribute names in the table:
```python
lab.Person().insert1(
       dict(username='alice', 
            first_name='Alice', 
            last_name='Cooper'))
```
or it may take the form of a sequence of values in the same order as the attributes in the table
```python
lab.Person().insert1(['alice', 'Alice', 'Cooper'])
```
The inserted tuple may also take the form of a [`numpy.record`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.record.html#numpy.record).

The `insert` method accepts a sequence or a generator of multiple tuples and is used to insert multiple tuples at once.

```python
lab.Person().insert([
       ['alice',   'Alice',   'Cooper'],
       ['bob',     'Bob',     'Dylan'],
       ['carol',   'Carol',   'Douglas']])
```


## Batched inserts 
Inserting a set of tuples in a single `insert` differs from inserting the same set of tuples one-by-one in a `for` loop in two ways:
1. Network overhead is reduced. Network overhead can be tens of milliseconds per query.  Inserting 1000 tuples in a single `insert` call may save a few seconds over inserting them individually.
2. The insert is performed as an all-or-nothing transaction.  Even if one insert fails because it violates any constraint, then none of the tuples in the set are inserted.

However, inserting too many tuples in a single query may run against buffer size or packet size limits of the database server.  Therefore, in some cases, when inserting very large numbers of tuples, it makes sense to break them up into batches of a few hundred, for example.