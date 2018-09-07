# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = DataJointDocumentation
# SOURCEDIR     = contents
SOURCEDIR     = contents
BUILDDIR      = _build
GH_PAGES_SOURCES = $(SOURCEDIR) Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile site

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

site:
	rm -rf site 
	make clean
	make html
	cp -r $(BUILDDIR)/html site
	@echo "Build finished. The HTML pages are in site/html."



