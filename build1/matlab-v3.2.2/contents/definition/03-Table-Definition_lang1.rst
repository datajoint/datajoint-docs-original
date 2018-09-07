|matlab| MATLAB

.. code-block:: matlab

	%{
	# database users
	username : varchar(20)   # unique user name
	---
	first_name : varchar(30)
	last_name  : varchar(30)
	role : enum('admin', 'contributor', 'viewer')
	%}
	classdef User < dj.Manual
	end


