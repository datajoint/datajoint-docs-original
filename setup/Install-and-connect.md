# Install and Connect

## MATLAB 
1. Download the DataJoint Toolbox from the [Matlab Central FileExchange](https://www.mathworks.com/matlabcentral/fileexchange/63218-datajoint).
2. Open `DataJoint.mltbx` and follow installation instructions.
3. After installation, from MATLAB, verify that you have the latest version of datajoint (3.0.0 or above):
    ```
    >> dj.version
    
    DataJoint version 3.0.0
    ```
4. At the MATLAB command prompt, assign the environment variables with the database credentials.  For example, if you are connection to the server `alicelab.datajoint.io` with username `alice` and password `haha not my real password`, execute the following commands:
    ```matlab
    setenv DJ_USER alice
    setenv DJ_HOST alicelab.datajoint.io
    setenv DJ_PASS 'haha not my real password'
    ```

You will need to execute these commands at the beginning of each DataJoint work session.  To automate this process, you might like to use the [startup.m script](https://www.mathworks.com/help/matlab/ref/startup.html).

However, be careful not to share this file or commit it to a public directory (a common mistake).  If you are not sure, it is better not to set `DJ_PASS`, in which case DataJoint will prompt to enter the password when connecting to the database.

To change the database password, use the following command
```
>> dj.setPassword('my#cool!new*psswrd')
```
And update your credentials in your startup script for the next session.

---
## Python
DataJoint is implemented for Python 3.4+.  You may install it from [PyPI](https://pypi.python.org/pypi/datajoint):

```
pip3 install datajoint
```

or upgrade

```
pip3 install --upgrade datajoint
``` 

Next configure the connection through datajoint's `config` object:

```python
In [1]: import datajoint as dj
DataJoint 0.4.9 (February 1, 2017)
No configuration found. Use `dj.config` to configure and save the configuration. 
```

You may now set the database credentials:
```python
In [2]: dj.config['database.host'] = "alicelab.datajoint.io"
In [3]: dj.config['database.user'] = "alice"
In [4]: dj.config['database.password'] = "haha not my real password"
```
Skip setting the password to make datajoint prompt to enter the password every time. 

You may save the configuration in the local work directory with `dj.config.save_local()` or for all your projects in `dj.config.save_global()`.

You may leave the user or the password as `None`, in which case you will be prompted to enter them manually for every session.

Note that the system environment variables `DJ_HOST`, `DJ_USER`, and `DJ_PASS` will overwrite the settings in the config file.  You can use them to set the connection credentials instead of config files.

To change the password, the `dj.set_password` function will walk you through the process:
```
>>> dj.set_password()
```

After that, update the password in the configuration and save it as described above:
```python
dj.config['database.password'] = 'my#cool!new*psswrd'
dj.config.save_local()   # or dj.config.save_global()
```
If `dj.config['database.password']` is set to `NULL`, datajoint will prompt to enter the password interactive when connecting to the server. 
