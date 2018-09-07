import os
import sys
import glob
import shutil

import subprocess


matlab_dir = "../datajoint-matlab/"
python_dir = "../datajoint-python/"



if not os.path.exists('build2'):
    os.makedirs('build2')
    subprocess.Popen(["git", "clone", "git@github.com:datajoint/datajoint-docs.git"], cwd="build2") # for now, copy over the manually created "common" contents after this step

srcComm = "build2/datajoint-docs/contents"
srcMat = "../datajoint-matlab/docs/"
srcPy = "../datajoint-python/docs/"

def create_build_folders(dsrc_common, dsrc_lang, lang):
    tags = subprocess.Popen(["git", "tag"], cwd="../datajoint-" + lang,
                            stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
    # for t in tags:
    dst_build_folder = "build2/" + lang + "-" + tags[-1] # build for latest version for now
    dst_main = dst_build_folder + "/contents"
    dst_temp = dst_main + "/comm"

    if os.path.exists(dst_build_folder):
        shutil.rmtree(dst_build_folder)

    # copy over the source doc contents into the build folder 
    shutil.copytree(dsrc_lang, dst_main)
    shutil.copytree(dsrc_common, dst_temp)

    # copying and merging all of the folders from lang-specific repo to build folder
    for root, dirs, filename in os.walk(dst_temp):
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
    shutil.copy2(dst_temp + "/" + "index.rst", dst_main + "/" + "index.rst")

    # removing the temporary comm folder because that shouldn't get build
    shutil.rmtree(dst_temp)

    # copy the datajoint_theme folder, conf.py and makefile for individual lang-ver folder building
    shutil.copytree("datajoint_theme", dst_build_folder + "/datajoint_theme")
    shutil.copy2("Makefile", dst_build_folder + "/Makefile")
    shutil.copy2("contents/conf.py", dst_build_folder + "/contents/" + "conf.py")


    # build individual lang-ver folder
    subprocess.Popen(["make", "site"], cwd=dst_build_folder)

create_build_folders(srcComm, srcMat, "matlab")
create_build_folders(srcComm, srcPy, "python")

# tags = subprocess.Popen(["git", "tag"], cwd="../datajoint-matlab/", stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
# print(tags)

# dst_build_folder = "build2/matlab-" + tags[-1]


# #dst1 for example would look like `build2/matlab-v3.2.0/content`
# dst1 = dst_build_folder + "/contents"
# dst2 = dst1 + "/comm"

# if os.path.exists(dst_build_folder):
#     shutil.rmtree(dst_build_folder)

# shutil.copytree(srcMat, dst1)
# shutil.copytree(srcComm, dst2)



# # copying and merging all of the folders from lang-specific repo to build folder
# for root, dirs, filename in os.walk(dst2):
#     print("root: " + root),
#     print("dirs"),
#     print(dirs),
#     print("filenames"),
#     print(filename),
#     print("+++++++++++++++++++++++++++++++++"),
#     for f in filename:
#         fullpath = os.path.join(root, f)
#         print(fullpath)
#         if len(dirs) == 0:
#             root_path, new_path = root.split("comm/")
#             shutil.copy2(fullpath, root_path + new_path)
#     print("-------------------------------")

# # copying the toc tree and the config files
# shutil.copy2(dst2 + "/" + "index.rst", dst1 + "/" + "index.rst")
# # shutil.copy2(dst2 + "/" + "conf.py", dst1 + "/" + "conf.py")

# # removing the comm folder because that shouldn't get build
# shutil.rmtree(dst2)

# # copy the datajoint_theme folder, conf.py and makefile for individual lang-ver folder building
# shutil.copytree("datajoint_theme", dst_build_folder + "/datajoint_theme")
# shutil.copy2("Makefile", dst_build_folder + "/Makefile")
# shutil.copy2("contents/conf.py", dst_build_folder + "/contents/" + "conf.py")

# # build individual lang-ver folder
# subprocess.Popen(["make", "site"], cwd=dst_build_folder)
