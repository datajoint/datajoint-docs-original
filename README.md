# DataJoint Technical Reference
This repository contains the source for comprehensive technical reference documentation for the DataJoint framework. 

All DataJoint documentations are presented at [DataJoint documentation website](http://docs.datajoint.io/).
Documentation is generated using [Sphinx](http://www.sphinx-doc.org/en/stable/) with custom rendering theme 
largely based on the [Read The Doc theme](https://github.com/rtfd/sphinx_rtd_theme).

# License
The documentation can be distributed for free use under the [Creative Commons Attribution-ShareAlike 4.0 International Public License](https://creativecommons.org/licenses/by-sa/4.0/).  Any copy or derivation of the documentation must include attribution to "DataJoint contributors" and include the URL reference https://docs.datajoint.io


# In-Development: Building All Versions (Full Site)
1. Clone the repository to your local machine.
2. Currently this will build using `testDocMain.git`, `testDocMatlab.git` and `testDocPython.git` repo. This will eventually need to be switched out to the actual official DJ documentation repositories. 
3. Build the website by running `python build-all.py`. This will build and generate the static website in the `full_site` directory. 
4. Move inside the `full_site` folder and run the following command to launch a local web server:
    ```bash
    $ python3 -m http.server
    ```
    This should launch a HTTP server locally serving files from the `full_site` directory.
5. Finally open up a web browser and navigate to `http://localhost:8000` - you should see the built documentation page. The port (i.e. the number after the color `:`) may differ - refer to the output of the command from the step above for the actual port to use.
6. If you made changes to the documentation source but you're not seeing the changes reflected, that is because this command builds from contents that are already pushed and tagged in the git repository. Please build locally to test, and then push with updated version numbers to see the changes in the full-site building.
7. To stop the server, hit `Ctrl+C` in the termianl window that's running the server.

# In-Development: Building Locally/Partially 
1. Fork and clone the repository to your local machine. Note: datajoint-docs now only contains the common documentions. If you are writing for specific language, you also need to clone the datajoint-matlab or datajoint-python repository and make sure they are place on the same level as the datajoint-docs folder.
2. Rename the cloned folder to `datajoint-docs`. If you cloned the python/matlab repository for local development/building, make sure to rename the folders to `datajoint-python` and `datajoint-matlab` respectively.
3. Build the website by running `python build-local.py`. This will build and generate the static website in the `loc_built_site` directory. 

- Note 1: `python build-local.py` defaults to building the most updated local common documentation. If you have both datajoint-matlab or datajoint-python folder locally on the same level, then this will build using those local folders (check/edit the `build-config.py` to make sure the local language folders are correctly placed. If you don't have a local language-specific folder, then it will still build using the most current lang-specific documentation on its respective git repository.
- Note 2: If you want to test-build a specific language version locally, then add `python/matlab_tag=(version)` after the `python build-local.py`. For example like, `python build-local.py matlab_tag=v3.2.5` and this should automatically grab the matching common version for building. Make sure you are specifying the full version tag (and not the abbreviated v3.2 in this case).
Note 3: If for some reason, you don't want to build using the local common version, you can also build using the most updated common version on the git repository by running `python build-local.py False` or `python build-local.py loc_comm=False`. This is mostly likely not going to work well if you already have a pre-existing local language-specific folder. 
4. Move inside the `loc_built_site` folder and run the following command to launch a local web server:
    ```bash
    $ python3 -m http.server
    ```
    This should launch a HTTP server locally serving files from the `loc_built_site` directory.
5. Finally open up a web browser and navigate to `http://localhost:8000` - you should see the built documentation page. The port (i.e. the number after the color `:`) may differ - refer to the output of the command from the step above for the actual port to use.
6. To stop the server, hit `Ctrl+C` in the termianl window that's running the server.

# Notes on Tagging
1. Before you tag anything, please `git tag` to make sure you see the current tag status.
2. In the datajoint-doc folder, `build-version.json` specifies which language versions to build in the full-build-mode. If you specify v3.2 in matlab, then the site will be build using the most recent tag (ex. v3.2.5 will be used to build, not v3.2.4). 
3. In the language-specific folder, all documentation contents are inside the `/docs` directory. Inside, you will see a `_version_common.json` file, which should only contain one corresponding common version tag for this language folder to be build alongside. Note that this file specifies the full-tag version (ex. v0.0.3) for the common version.
(Not sure about how we will coordinate this with the team yet: When you update content in the lang-specific documentation and you also have made changes in the common version to reflect the change, make sure you give a new tag to the common version, update this `_version_common.json` with the new tag, then also add a new tag (should we?) for the specific language version.)
4. to add a tag: `git tag -a v3.2.5 -m "some message"`
   to delete local tag: `git tag -d v3.2.5`
   to delete already-pushed tag: `git push origin :refs/tags/v3.2.5`
   to push with tag `git push origin v3.2.5`


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
