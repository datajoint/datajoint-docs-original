import os
import sys
import glob
import shutil

from subprocess import call

# srcComm = "contents/computation/01-autopopulate.rst"
srcComm = "contents/"
srcMat = "../datajoint-matlab/docs/"
# srcMat = "../datajoint-matlab/docs/computation/01-autopopulate_lang1.rst"
srcPy = "../datajoint-python/docs/computation/01-autopopulate_lang1.rst"

dst1 = "build/matlab-v3.2.0"
dst2 = "build/matlab-v3.2.0/comm"

if os.path.exists(dst1):
    shutil.rmtree(dst1)

shutil.copytree(srcMat, dst1)

shutil.copytree(srcComm, dst2)

# copying and merging all of the folders from lang-specific repo to build folder
for root, dirs, filename in os.walk(dst2):
    print("root: " + root),
    print("dirs"),
    print(dirs),
    print("filenames"),
    print(filename),
    print("+++++++++++++++++++++++++++++++++"),
    for f in filename:
        fullpath = os.path.join(root, f)
        print(fullpath)
        if len(dirs) == 0:
            root_path, new_path = root.split("comm/")
            shutil.copy2(fullpath, root_path + new_path)
    print("-------------------------------")
    
# copying the toc tree and the config files
shutil.copy2(dst2 + "/" + "index.rst", dst1 + "/" + "index.rst")
shutil.copy2(dst2 + "/" + "conf.py", dst1 + "/" + "conf.py")

# removing the comm folder because that shouldn't get build
shutil.rmtree(dst2)