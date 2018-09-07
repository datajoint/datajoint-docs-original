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
    
``+test/SegmentationROI.m``

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
               for roi=1:length(roi_pixels)
                   tuple = key;
                   tuple.roi_pixels = roi_pixels{roi};
                   tuple.roi_weights = roi_weights{roi};
                   self.insert(tuple)
               end
           end
       end
   end

.. |matlab| image:: ../_static/img/matlab-tiny.png
