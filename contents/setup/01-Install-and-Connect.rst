.. progress: 8.0 80% Edgar

.. _install:

Install and Connect
===================

.. include:: 01-Install-and-Connect_lang1.rst


Other Configuration Settings
============================

If you are not using DataJoint on your own, or are setting up a DataJoint
system for other users, some additional configuraiton options may be required
to support :ref:`TLS <tls>` or :ref:`external storage <external>` .


.. _tls:

TLS Configuration
-----------------

Starting with v0.12 (Python) and v3.3.1 (MATLAB), DataJoint will by default
use TLS if it is available. TLS can be forced on or off with the boolean
`use_tls` in MATLAB, or `dj.config['database.use_tls']` in Python.

