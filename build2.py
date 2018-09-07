import os
import sys
import glob
import shutil

import subprocess


matlab_dir = "../datajoint-matlab/"
python_dir = "../datajoint-python/"



if not os.path.exists('build1'):
    os.makedirs('build1')
    subprocess.Popen(
        ["git", "clone", "git@github.com:mahos/testDocMain.git", "datajoint-docs"], cwd="build1")
    
    subprocess.Popen(
        ["git", "clone", "git@github.com:mahos/testDocMatlab.git", "datajoint-matlab"], cwd="build1")
    
    subprocess.Popen(
        ["git", "clone", "git@github.com:mahos/testDocPython.git", "datajoint-python"], cwd="build1").wait()
    

srcComm = "build1/datajoint-docs/contents"
srcMat = "build1/datajoint-matlab/docs/"
srcPy = "build1/datajoint-python/docs/"
# srcMat = "../datajoint-matlab/docs/"
# srcPy = "../datajoint-python/docs/"

def create_build_folders(dsrc_common, dsrc_lang, lang):
    # tags = subprocess.Popen(["git", "tag"], cwd="build1/datajoint-" + lang, stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()

    tags2 = {"python": [
                        # "v0.9.0",
                        "v0.9.1"],
             "matlab": [
                        # "v3.2.0",
                        "v3.2.1",
                        "v3.2.2"]
             }
    for tag in tags2[lang]:
    # for tag in tags:
        subprocess.Popen(["git", "checkout", tag],
                         cwd="build1/datajoint-" + lang, stdout=subprocess.PIPE).wait()
        dsrc_lang2 = "build1/datajoint-" + lang + "/docs"
        dst_build_folder = "build1/" + lang + "-" + tag 
        dst_main = dst_build_folder + "/contents"
        dst_temp = dst_main + "/comm"

        if os.path.exists(dst_build_folder):
            shutil.rmtree(dst_build_folder)

        # copy over the source doc contents into the build folder 
        # shutil.copytree(dsrc_lang, dst_main)
        shutil.copytree(dsrc_lang2, dst_main)
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
        subprocess.Popen(["make", "site"], cwd=dst_build_folder).wait()

create_build_folders(srcComm, srcMat, "matlab")
create_build_folders(srcComm, srcPy, "python")

# tags = subprocess.Popen(["git", "tag"], cwd="../datajoint-matlab/", stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
# print(tags)

# dst_build_folder = "build1/matlab-" + tags[-1]


# #dst1 for example would look like `build1/matlab-v3.2.0/content`
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
