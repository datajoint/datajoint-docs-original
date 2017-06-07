# Lookup Tables

Lookup tables contain basic facts that are not specific to an experiment and are fairly persistent. Their contents are typically small.  In GUIs, the are often used for pull-down menus. In computed tables, they are often used to specify alternative methods for computations.  Lookup tables are commonly populated from their `contents` property. In [[ERD]]s they are shown in gray. The decision which tables are Lookup and which tables are Manual can be somewhat arbitrary.

The table below is declared as a lookup table with the contents property to fill its contents.

![](../_static/img/python-tiny.png)

```python
@schema
class User(dj.Lookup):
    definition = """
    # users in the lab
    username : varchar(20)   # user in the lab
    ---
    first_name  : varchar(20)   # user first name
    last_name   : varchar(20)   # user last name
    """
    contents = [
        ['cajal', 'Santiago', 'Cajal'],
        ['hubel', 'David', 'Hubel'],
        ['wiesel', 'Torsten', 'Wiesel']
]
```

![](../_static/img/matlab-tiny.png)

File `+lab/User.m`
```matlab
%{
    # users in the lab
    username : varchar(20)   # user in the lab
    ---
    first_name  : varchar(20)   # user first name
    last_name   : varchar(20)   # user last name
%}
classdef User < dj.Lookup
    properties
        contents = {
            'cajal'  'Santiago' 'Cajal'
            'hubel'  'David'    'Hubel'
            'wiesel' 'Torsten'  'Wiesel'
        }
    end
end
```
