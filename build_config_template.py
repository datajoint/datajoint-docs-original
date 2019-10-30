##====== setting for where you get the documents from =====##
##=== used for build-all mode and in build-local when you don't have the folders locally set ===##

## RENAME this file to build_config.py to start using non-default paths for getting the documents

## set the git repo 
config_repos = {
    ## common doc - default is preset to "https://github.com/datajoint/datajoint-docs.git"
    'common': "https://REPLACE-HERE-WITH-PATH-TO-COMMON-DOC.git",
    'common-branch': "REPLACE-HERE-WITH-COMMON-BRANCH",

    ## MATLAB doc - default is preset to "https://github.com/datajoint/datajoint-matlab.git"
    'matlab': "https://REPLACE-HERE-WITH-PATH-TO-MATLAB-DOC.git",
    'matlab-branch': "REPLACE-HERE-WITH-MATLAB-BRANCH",

    ## Python doc - default is preset to "https://github.com/datajoint/datajoint-python.git"
    'python': "https://REPLACE-HERE-WITH-PATH-TO-PYTHON-DOC.git",
    'python-branch': "REPLACE-HERE-WITH-PYTHON-BRANCH"
}


#====== setting for locally building the doc ======#
## set the path for locally placed language folders
local_path = {
    ## default is preset to 
    # 'matlab': "../datajoint-matlab",
    # 'python': "../datajoint-python"
    'matlab': "PATH-TO-LOCALLY-PLACED-MATLAB-FOLDER",
    'python': "PATH-TO-LOCALLY-PLACED-PYTHON-FOLDER"
}
 
