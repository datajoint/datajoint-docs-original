import os
import sys
import glob
import shutil

import subprocess


# matlab_dir = "../datajoint-matlab/"
# python_dir = "../datajoint-python/"



if not os.path.exists('build1'):
    os.makedirs('build1')
    subprocess.Popen(
        ["git", "clone", "git@github.com:mahos/testDocMain.git", "datajoint-docs"], cwd="build1").wait()
    
    subprocess.Popen(
        ["git", "clone", "git@github.com:mahos/testDocMatlab.git", "datajoint-matlab"], cwd="build1").wait()
    
    subprocess.Popen(
        ["git", "clone", "git@github.com:mahos/testDocPython.git", "datajoint-python"], cwd="build1").wait()
    

srcComm = "build1/datajoint-docs/contents"
srcMat = "build1/datajoint-matlab/docs/"
srcPy = "build1/datajoint-python/docs/"
# srcMat = "../datajoint-matlab/docs/"
# srcPy = "../datajoint-python/docs/"

def create_build_folders(dsrc_common, dsrc_lang, lang): #TODO delete the dsrc_lang it's not getting used anymore
    # tags = subprocess.Popen(["git", "tag"], cwd="build1/datajoint-" + lang, stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
    # tags1 = {}
    # tags1[lang] = tags
    # print(tags1)

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
            # print("root: " + root),
            # print("dirs"),
            # print(dirs),
            # print("filenames"),
            # print(filename),
            # print("+++++++++++++++++++++++++++++++++"),
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

# generate site folder with all contents using hte above build folders

def make_full_site():
    if os.path.exists('full_site'):
        shutil.rmtree('full_site')
        os.makedirs('full_site')
    else:
        os.makedirs('full_site')
    
    # copies all of the lang-ver static sites into separate folder
    toMake = glob.glob('build1/**/site') #assuming the datajoint-docs folded pulled from the git repo doesn't have the site directory
    #returns something like ['build1/matlab-v3.2.1/site', 'build1/matlab-v3.2.2/site', 'build1/python-v0.9.1/site']
    print(toMake)
    # if not os.path.exists('version-menu.html'):
    #         subprocess.Popen(['touch', 'version-menu.html']).wait()
    # else:
    #     open('version-menu.html', 'w').close()
    f = open('full_site/version-menu.html', 'w+')

    for src_path in toMake:
        ver_path = src_path.split('/', 1)[1]
        shutil.copytree(src_path, 'full_site/' + ver_path)
        f.write('<li class="version-menu"><a href="' + ver_path + '">' + ver_path.split('/', 1)[0] + '</a></li>\n')
        
    f.close()

make_full_site()
    
