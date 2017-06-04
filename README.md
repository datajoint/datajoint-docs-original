# DataJoint Documentations

All DataJoint documentations are presented at [DataJoint documentation website](http://docs.datajoint.io/).
Documentations are generated using [Sphinx](http://www.sphinx-doc.org/en/stable/) with custom rendering theme 
largely based on the [Read The Doc theme](https://github.com/rtfd/sphinx_rtd_theme).

## Building locally

- Fork and clone the repository to your local machine.
- Install requirements using `pip3 install -r requirements.txt`
- Build the website by running `make html`. This will build and generate the static website in the `_build/html` directory.
- Some structural changes might require you to first clean the output directory by running `make clean` before generating the doc with `make html`.
