
filepath datatype
=================

filepath datatype configuration & usage
---------------------------------------

https://github.com/datajoint/datajoint-python/issues/481

The 'filepath' attribute type links datajoint records to files already
managed outside of datajoint. This can aid in sharing data with
other systems, such as allowing an image viewer application to
directly use files from a datajoint pipeline, or to allow downstream
tables to reference data which lives outside of the datajoint
pipeline.

To define a table using the 'filepath' datatype, an existing DataJoint
:ref:`store <external>` should be created and then referenced in the new
table definition. For example, given a simple store::

    dj.config['stores'] = {
      'data': {
        'protocol': 'file',
        'location': '/data',
        'stage': '/data'
      }
    }

we can define an ScanImages table as follows::

    @schema
    class ScanImages(dj.Manual):
        definition = """
        -> Session
        image_id:    int
        ---
        image_path:  filepath@data 
        """

This table can now be used for tracking paths within the '/data' area.
For example::

    >>> ScanImages.insert1((0, 0, '/data/images/image_0.tif'))
    >>> (ScanImages() & {'session_id': 0}).fetch1(as_dict=True)
    {'session_id': 0, 'image_id': 0, 'image_path': '/data/images/image_0.tif'}

As can be seen from the example, unlike 'blob' (FIXME docref) records, file
paths are managed as path locations to the underlying file.

filepath integrity notes
------------------------

Unlike other data in datajoint, data in 'filepath' records are
deliberately intended for shared use outside of datajoint.  To help
ensure integrity of filepath records, datajoint will record a
checksum of the file data on insert, and will verify this checksum
on fetch. However, since the underlying file data may be shared
with other applications, special care should be taken to ensure
records stored in 'filepath' attributes are not modified outside
of the pipeline, or, if they are, that records in the pipeline are
updated accordingly. A safe method of changing filepath data is
as follows:

  1) Delete filepath database record

     This will ensure that any downstream records in the pipeline depending
     on the 'filepath' record are purged from the database

  2) Modify filepath data

  3) Re-insert corresponding filepath record

     This will add the record back to DataJoint with an updated file checksum

  4) Compute any downstream dependencies, if needed

     This will ensure that downstream results dependent on the filepath
     record are updated to reflect the newer filepath contents.

.. TODO: purging filepath data

