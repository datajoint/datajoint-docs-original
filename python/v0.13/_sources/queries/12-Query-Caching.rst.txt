.. progress: 10.0 100% Raphael

.. _query-caching:

Query Caching
=============

Query caching allows avoiding repeated queries to the database by caching the results locally for faster retrieval.

To enable queries, set the query cache local path in ``dj.config``, create the directory, and activate the query caching.

.. include:: 12-Query-Caching_lang1.rst

The ``query_cache`` argument is an aribtrary string serving to differentiate cache states; setting a new value will effectively start a new cache, triggering retrieval of new values once.

To turn off query caching, use

.. include:: 12-Query-Caching_lang2.rst

While query caching is enabled, any insert or delete calls and any transactions are disabled and will raise an error. This ensures that stale data are not used for updating the database in violation of data integrity.

To clear and remove the query cache, use

.. include:: 12-Query-Caching_lang3.rst
