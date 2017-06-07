# Delete

The `delete` (Python) and `del` (Matlab) method deletes tuples from a table and all dependent entries in dependent tables.  It is used in conjunction with the [[restriction]] operator to define the subset of tuples to delete.  Delete is performed as an atomic transaction so that partial deletes never occur.

## Examples
Delete the entire contents of the table `tuning.VonMises` and all its dependents:

```matlab
%matlab
del(tuning.VonMises)
```
```python
#matlab
tuning.VonMises().delete()
```

Delete the contents from the same table for mouse 1010:
```matlab
%matlab
del(tuning.VonMises & 'mouse=1010')
```
```python
#python
(tuning.VonMises() & 'mouse=1010').delete()
```

### Deleting from part tables
[[Part tables]] prohibit direct deletion. The only way to delete from a part table is to delete from its master.