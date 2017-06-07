# Drop

The `drop` method completely removes the table from the database, including its definition.  It also removes all dependent tables, recursively.  DataJoint will first display the tables being dropped and the number of tuples in each before prompting the user to proceed.

The `drop` method is often used during the initial design to allow altered table definitions to take effect.

Examples:
```python
# python
Person().drop()   # drop the Person table and all its dependent tables
```

```matlab
% matlab
drop(lab.Person)  % drop the Person table and all its dependent tables
```