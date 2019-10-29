#!/usr/bin/env sh

git clone -b ${PY_BRANCH} --single-branch ${PY_REPO}
git clone -b ${M_BRANCH} --single-branch ${M_REPO}

cp datajoint-docs/build_config_template.py datajoint-docs/build_config.py
sed -i "s|https://REPLACE-HERE-WITH-PATH-TO-COMMON-DOC.git|${DOCS_REPO}|g" datajoint-docs/build_config.py
sed -i "s|https://REPLACE-HERE-WITH-PATH-TO-MATLAB-DOC.git|${M_REPO}|g" datajoint-docs/build_config.py
sed -i "s|https://REPLACE-HERE-WITH-PATH-TO-PYTHON-DOC.git|${PY_REPO}|g" datajoint-docs/build_config.py
sed -i 's|PATH-TO-LOCALLY-PLACED-MATLAB-FOLDER|../datajoint-matlab|g' datajoint-docs/build_config.py
sed -i 's|PATH-TO-LOCALLY-PLACED-PYTHON-FOLDER|../datajoint-python|g' datajoint-docs/build_config.py

cd datajoint-docs
# python3 build-all.py
# cd full_site
python3 build-local.py
cd loc_built_site
echo "Serving docs now..."
python3 -m http.server