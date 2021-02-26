# DataJoint Technical Reference
This repository contains the source for comprehensive technical reference documentation for the DataJoint framework. 

All DataJoint documentations are presented at [DataJoint documentation website](http://docs.datajoint.io/).
Documentation is generated using [Sphinx](http://www.sphinx-doc.org/en/stable/) with custom rendering theme 
largely based on the [Read The Doc theme](https://github.com/rtfd/sphinx_rtd_theme).

# Developing Locally
It is recommended to use any of the 2 available docker environments for developing: `build` and `dev`. Ensure that you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed following the specific instructions for your operating system. For details regarding each environment, see the respective `*.docker-compose.yaml` files which contain a header comment at the top which indicate:

1. The recommended command to run the environment.
2. The intended usage for the environment along with other important notes.

Read on for more details on running the docs natively and writing style guidelines.

# License
The documentation can be distributed for free use under the [Creative Commons Attribution-ShareAlike 4.0 International Public License](https://creativecommons.org/licenses/by-sa/4.0/).  Any copy or derivation of the documentation must include attribution to "DataJoint contributors" and include the URL reference https://docs.datajoint.io


# Building All Versions (Full Site)
1. Clone the repository to your local machine.
2. The default setting will build using `datajoint/datajoint-docs.git`, `datajoint/datajoint-matlab.git` and `datajoint/datajoint-python.git` repo. If you'd like to change the repo that the build points to, modify the content of the `build_config_template.py` and rename the file to `build_config.py` (follow the instruction inside the template file for further instructions) 
3. Build the website by running `python build-all.py`. This will build and generate the static website in the `full_site` directory.
- Note for Windows users: Please manually remove the `build-all` folder before running `python build-all.py` for building second time and on... 
4. Move inside the `full_site` folder and run the following command to launch a local web server:
    ```bash
    $ python3 -m http.server
    ```
    This should launch a HTTP server locally serving files from the `full_site` directory.
5. Finally open up a web browser and navigate to `http://localhost:8000` - you should see the built documentation page. The port (i.e. the number after the colon `:`) may differ - refer to the output of the command from the step above for the actual port to use.
6. If you made changes to the documentation source but you're not seeing the changes reflected, that is because this command builds from contents that are already pushed and tagged in the git repository. Please build locally to test, and then push with updated version numbers to see the changes in the full_site building.
7. To stop the server, hit `Ctrl+C` in the terminal window that's running the server.

# Building Locally/Partially 
1. Fork and clone the repository to your local machine. Note: datajoint-docs now only contains the common documentions. If you are writing for a specific language, you also need to clone the datajoint-matlab or datajoint-python repository and make sure they are placed on the same level as the datajoint-docs folder. 
2. If you have the Python/MATLAB repository for local development/building and the folders aren't named `datajoint-python`/`datajoint-matlab` or have them somewhere other than on the same level as the `datajoint-docs` folder, open the `build_config_template.py` and set the new path inside, then rename the config file to `build_config.py` (follow the instruction inside the template file for further instructions)
3. Build the website by running `python build-local.py`. This will build and generate the static website in the `loc_built_site` directory. 

- Note for Windows users: Please manually remove the `build-local` folder before running `python build-local.py` for building second time and on...
- Note 1: `python build-local.py` defaults to building the most updated local common documentation. If you have both `datajoint-matlab` or `datajoint-python` folder locally on the same level, then this will build using those local folders (check and edit the `build-config.py` to make sure the local language folders are correctly placed). If you don't have a local language-specific folder, then it will still build using the most current lang-specific documentation on its respective git repository.
- Note 2: If you want to test-build a specific language version locally, then add `python/matlab_tag=(version)` after the `python build-local.py`. For example, `python build-local.py matlab_tag=v3.2.5` or `python build-local.py python_tag=v0.9.4` and this should automatically grab the matching common version for building. Make sure you are specifying the full version tag (and not the abbreviated v3.2 in this case).
Note 3: If for some reason, you don't want to build using the local common version, you can also build using the most updated common version on the git repository by running `python build-local.py False` or `python build-local.py loc_comm=False`. This is mostly likely not going to work well if you already have a pre-existing local language-specific folder. 
4. Move inside the `loc_built_site` folder and run the following command to launch a local web server:
    ```bash
    $ python3 -m http.server
    ```
    This should launch a HTTP server locally serving files from the `loc_built_site` directory.
5. Finally open up a web browser and navigate to `http://localhost:8000` - you should see the built documentation page. The port (i.e. the number after the colon `:`) may differ - refer to the output of the command from the step above for the actual port to use.
6. To stop the server, hit `Ctrl+C` in the terminal window that's running the server.

# Notes on Tagging
1. Before you tag anything, please `git tag` to make sure you see the current tag status.
2. In the `datajoint-docs` folder, `build-version.json` specifies which language versions to build in the build-all/full-build-mode. If you specify v3.2 in matlab, then the site will be built using the most recent tag (ex. v3.2.5 will be used to build, not v3.2.4). 
3. In the language-specific folder, all documentation contents are inside the `/docs-parts` directory. Inside, you will see a `_version_common.json` file, which should only contain one corresponding common version tag for this language folder to be build alongside. This file specifies the version (ex. v0.0) for the common version. Similar to the build process described above, if v0.0 is specified in the `_version_common.json`, then the most recent tag, for example v0.0.5 instead of v0.0.4 will be grabbed for the build.
4. - to add a doc specific tag to `datajoint-python` or `datajoint-matlab` repo, make sure to add the `-doc#` ending: `git tag -a v3.2.5-doc1 -m "some message"`. The # should be an integer.
   - to add a common doc tag to `datajoint-docs` repo, no special ending is necessary: `git tag -a v0.0.1 -m "some message`
   - to delete local tag: `git tag -d v3.2.5-doc1`
   - to delete already-pushed tag: `git push origin :refs/tags/v3.2.5-doc1`
   - to push with tag `git push origin v0.0.3`


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
- For referring to a language-specific content, use `.. include:: [FILENAME OF COMMON]_lang[#].rst` 

    - For example, if you are editing the RST file `01-autopopulate.rst` inside of `contents/computation` then you would refer to language specific parts with `.. include:: 01-autopopulate_lang1.rst` and `.. include:: 01-autopopulate_lang2.rst` if you have 2 sections. 
    
    - Then inside the language specific contents inside `docs-parts` folder in `datajoint-matlab`/`datajoint-python`, make sure to add a RST file with the same format as `[FILENAME OF COMMON]_lang[#].rst`. Following the previous example - inside of `datajoint-matlab/docs-parts` folder, you should put `01-autopopulate_lang1.rst` and `01-autopopulate_lang2.rst` inside the computation folder and do the same in inside the `datajoint-python`. For organization purposes, if one language has more includes than the other, it is recommended that you still keep an empty rst file as a placeholder inside the language that has less includes. 


# References
[Sphinx restructured text reference](http://www.sphinx-doc.org/en/master/usage/restructuredtext/)
