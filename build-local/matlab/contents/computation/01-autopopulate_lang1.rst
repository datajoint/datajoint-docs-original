
|matlab| MATLAB

.. code-block:: MATLAB

    %{
    # Filtered image
    -> test.Image
    ---
    filtered_image : longblob
    %}

    classdef FilteredImage < dj.Computed
        methods(Access=protected)
            function make(self, key)
                img = fetch1(test.Image & key, 'image');
                key.filtered_image = myfilter(img);
                self.insert(key)
            end
        end
    end
