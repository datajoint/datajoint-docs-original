#====== setting for where you get the documents from =====#
#=== used for build-all mode and in build-local when you don't have the folders locally set ===#

config_urls = {
    # common doc
    'common': "https://github.com/mahos/testDocMain.git",
    # MATLAB doc
    'matlab': "https://github.com/mahos/testDocMatlab.git",
    # Python doc
    'python': "https://github.com/mahos/testDocPython.git"
}


#====== setting for locally building the doc ======#
local_path = {
    'matlab': "../datajoint-matlab",
    'python': "../datajoint-python"
}



