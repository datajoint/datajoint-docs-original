# DataJoint Technical Reference
This repository contains the source for comprehensive technical reference documentation for the DataJoint framework. 

All DataJoint documentations are presented at [DataJoint documentation website](http://docs.datajoint.io/).
Documentation is generated using [Sphinx](http://www.sphinx-doc.org/en/stable/) with custom rendering theme 
largely based on the [Read The Doc theme](https://github.com/rtfd/sphinx_rtd_theme).

# License
The documentation can be distributed for free use under the [Creative Commons Attribution-ShareAlike 4.0 International Public License](https://creativecommons.org/licenses/by-sa/4.0/).  Any copy or derivation of the documentation must include attribution to "DataJoint contributors" and include the URL reference https://docs.datajoint.io

# Building locally
1. Fork and clone the repository to your local machine.
2. Install requirements using `pip3 install -r requirements.txt`
3. Build the website by running `make site`. This will build and generate the static website in the `site` directory. (Windows users should run `sphinx-build . _build` from the `contents` directory.)
4. Move inside the `site` folder (or the `_build` folder on Windows) and run the following command to launch a locally web server:
    ```bash
    $ python3 -m http.server
    ```
    This should launch a HTTP server locally serving files from the `site` directory.
5. Finally open up a web browser and navigate to `http://localhost:8000` - you should see the built documentation page. The port (i.e. the number after the color `:`) may differ - refer to the output of the command from the step above for the actual port to use.
6. If you made changes to the documentation source, rerun `make site` in a separate terminal window, and then refresh the page in the browser - you should see the changes reflected.
7. To stop the server, hit `Ctrl+C` in the termianl window that's running the server.

# Guidelines for Writing
- For inserting a SQL code-block, be sure to use `.. code-block:: mysql` (and NOT `SQL`)
- For inserting an image, make sure to put the image inside the `contents/_static/img` folder and refer to it using the `image` directive:
    ```rst
    .. image:: ../_static/img/pipeline.png
        :width: 250px
        :align: center
        :alt: A data pipeline
    ```
    Alternatively you can also use `figure` directive. For more information, refer to the documentation of [image](http://docutils.sourceforge.net/docs/ref/rst/directives.html#image) and/or [figure](http://docutils.sourceforge.net/docs/ref/rst/directives.html#figure) directives.

# References
[Sphinx restructured text reference](http://www.sphinx-doc.org/en/master/usage/restructuredtext/)
