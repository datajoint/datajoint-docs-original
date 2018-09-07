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
            function makeTuples(self, key)
                img = fetch1(test.Image & key, 'image');
                key.filtered_image = myfilter(img);
                self.insert(key)
            end
        end
    end

.. |matlab| image:: ../_static/img/matlab-tiny.png
