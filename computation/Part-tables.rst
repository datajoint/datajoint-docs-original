Part Tables
===========

Often an entity in one relation is inseparably associated with a group of entities in another, forming a **master-part** relationship.  

Master-part relationships can form in any data tier but DataJoint observes them more strictly for auto-populated tables and become one of the most powerful data integrity principles in DataJoint, ensuring that all the parts of something appear all together or not at all.

The master-part relationship cannot be chained or nested: A master cannot be a part of another master.

As an example, imagine segmenting an image to identify regions of interest. The resulting segmentation is inseparable from the ROIs that it produces. 

In this case, the two tables might be called ``Segmentation`` and ``Segmentation.ROI``.

|python| Python
---------------

In Python, the master-part relationship is expressed by making the part a nested class of the master.  
The part is subclassed from ``dj.Part`` and does not need the schema decorator.


.. code-block:: python

    @schema
    class Segmentation(dj.Computed):
        definition = """  # image segmentation
        -> Image 
        """

        class ROI(dj.Part):
            definition = """  # Region of interest resulting from segmentation
            -> Segmentation 
            roi  : smallint   # roi number 
            ---
            roi_pixels  : longblob   #  indices of pixels
            roi_weights : longblob   #  weights of pixels
            """

        def _make_tuples(self, key):
            image = (Image() & key).fetch1['image']
            self.insert1(key)
            count = itertools.count()
            Segmentation.ROI().insert(
                    dict(key, roi=next(count), roi_pixel=roi_pixels, roi_weights=roi_weights)
                    for roi_pixels, roi_weights in mylib.segment(image))
                
|matlab| MATLAB
---------------
In MATLAB, the master and  part tables are declared in a separate ``classdef`` file.  
The name of the part table must begin with the name of the master table. 
The part table must declare the property ``master`` containing an object of the master.

``+test/Segmentation.m``

.. code-block:: matlab

    %{ 
    # image segmentation 
    -> test.Image 
    %}
    classdef Segmentation < dj.Computed
        methods(Access=protected)
            function makeTuples(self, key)
                self.insert(key)
                makeTuples(test.SegmentationRoi, key)
            end
        end
    end
    
``+test/Segmentation/ROI.m``

.. code-block:: matlab

    %{
    # Region of interest resulting from segmentation
    -> Segmentation
    roi  : smallint   # roi number
    ---
    roi_pixels  : longblob   #  indices of pixels
    roi_weights : longblob   #  weights of pixels
    %}

    classdef SegmentationROI < dj.Part
        properties
            master = test.Segmentation
        end
        methods 
            function makeTuples(self, key)
                image = fetch1(test.Image & key, 'image');
                [roi_pixels, roi_weighs] = mylib.segment(image);
                part = test.SegmentationROI;
                for roi=1:length(roi_pixels)
                    tuple = key;
                    tuple.roi_pixels = roi_pixels{i};
                    tuple.roi_weights = roi_weights{i};
                    self.insert(tuple)
                end
            end 
        end
    end

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
