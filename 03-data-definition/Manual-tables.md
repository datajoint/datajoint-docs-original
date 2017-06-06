# Manual Tables

Manual tables are populated during experiments through a variety of interfaces.  Not all manual information is entered by typing.  Automated software can enter it directly into the database.  What makes a manual table manual is that it does not perform any computations within the pipeline.

The following code defines three manual tables `Animal`, `Session`, and `Scan`:

![](../_static/img/python-tiny.png)

```python
@schema
class Animal(dj.Manual):
    definition = """
    # information about animal 
    animal_id : int  # animal id assigned by the lab
    ---
    -> Species
    date_of_birth=null : date  # YYYY-MM-DD optional
    sex='' : enum('M', 'F', '')   # leave empty if unspecified
    """

@schema
class Session(dj.Manual):
    definition = """
    # Experiment Session
    -> Animal
    session  : smallint  # session number for the animal
    --- 
    session_date : date  # YYYY-MM-DD
    -> User
    -> Anesthesia
    -> Rig
    """

@schema 
class Scan(dj.Manual):
    definition = """
    # Two-photon imaging scan
    -> Session 
    scan : smallint  # scan number within the session
    ---
    -> Lens
    laser_wavelength : decimal(5,1)  # um
    laser_power      : decimal(4,1)  # mW    
    """
```

![](../_static/img/matlab-tiny.png)

Matlab  file `+experiment/Animal.m`
```matlab
%{
  # information about animal 
  animal_id : int  # animal id assigned by the lab
  ---
  -> experiment.Species
  date_of_birth=null : date  # YYYY-MM-DD optional
  sex='' : enum('M', 'F', '')   # leave empty if unspecified
%}
classdef Animal < dj.Manual
end
```
Matlab  file `+experiment/Session.m`
```matlab
%{
  # Experiment Session
  -> experiment.Animal
  session  : smallint  # session number for the animal
  --- 
  session_date : date  # YYYY-MM-DD
  -> experiment.User
  -> experiment.Anesthesia
  -> experiment.Rig
%}
classdef Session < dj.Manual
end
```

Matlab file `+experiment/Scan.m`
```matlab
%{
  # Two-photon imaging scan
  -> experiment.Session 
  scan : smallint  # scan number within the session
  ---
  -> experiment.Lens
  laser_wavelength : decimal(5,1)  # um
  laser_power      : decimal(4,1)  # mW    
%}
classdef Scan < dj.Manual
end
```
