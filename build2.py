import os
import json
import glob
import shutil
import subprocess

import tagpicker


if os.path.exists('build1'):
    shutil.rmtree('build1')

os.makedirs('build1')
subprocess.Popen(
    ["git", "clone", "git@github.com:mahos/testDocMain.git", "datajoint-docs"], cwd="build1").wait()

subprocess.Popen(
    ["git", "clone", "git@github.com:mahos/testDocMatlab.git", "datajoint-matlab"], cwd="build1").wait()

subprocess.Popen(
    ["git", "clone", "git@github.com:mahos/testDocPython.git", "datajoint-python"], cwd="build1").wait()
    

def create_build_folders(lang): 
    raw_tags = subprocess.Popen(["git", "tag"], cwd="build1/datajoint-" + lang, stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
    git_tags = {}
    git_tags[lang] = raw_tags

    lv = open("build_versions2.json")
    buildver = lv.read()
    min_tags = json.loads(buildver)
    lv.close()

    tags = tagpicker.pick_tag(min_tags, git_tags, lang)

    # tags2 = {"python": [
    #                     # "v0.9.0",
    #                     "v0.9.1"],
    #          "matlab": [
    #                     # "v3.2.0",
    #                     # "v3.2.1",
    #                     "v3.2.2"]
    #          }
    # for tag in tags2[lang]:
    # for tag in tags[lang]:
    for tag in tags:
        subprocess.Popen(["git", "checkout", tag],
                         cwd="build1/datajoint-" + lang, stdout=subprocess.PIPE).wait()
        dsrc_lang2 = "build1/datajoint-" + lang + "/docs"
        dst_build_folder = "build1/" + lang + "-" + tag 
        dst_main = dst_build_folder + "/contents"
        dst_temp = dst_main + "/comm"

        if os.path.exists(dst_build_folder):
            shutil.rmtree(dst_build_folder)

        # copy over the lang source doc contents into the build folder 
        shutil.copytree(dsrc_lang2, dst_main)

        # grab which version of the common folder the lang doc needs to be merged with
        cv = open(dsrc_lang2 + "/_version_common.json")
        v = cv.read() # expected in this format { "comm_version" : "v0.0.0"}
        version_info = json.loads(v)
        cv.close
        subprocess.Popen(["git", "checkout", version_info['comm_version']],
                         cwd="build1/datajoint-docs", stdout=subprocess.PIPE).wait()
        dsrc_comm2 = "build1/datajoint-docs/contents"
        # copy over the cmmon source doc contents into the build folder 
        shutil.copytree(dsrc_comm2, dst_temp)

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

        # add current_version <p> tag into the datajoint_theme folder 
        f = open(dst_build_folder + '/datajoint_theme/this_version.html', 'w+')
        f.write('<p class="thisVersion">' + lang + "-" + ".".join(tag.split(".")[:-1]) + '</p>') 
        f.close()
        # add current_version as release into the conf.py file (for pdf generation)
        f = open(dst_build_folder + "/contents/" + "conf.py", 'a+')
        f.write('release = "' + lang + "-" + ".".join(tag.split(".")[:-1])+ '"')
        f.close()


create_build_folders("matlab")
create_build_folders("python")

# generate site folder with all contents using hte above build folders

def make_full_site():

    if os.path.exists('full_site'):
        shutil.rmtree('full_site')
        os.makedirs('full_site')
    else:
        os.makedirs('full_site')
    
    # build individual lang-ver folder
    to_make = [folder for folder in glob.glob('build1/**') if not os.path.basename(folder).startswith('datajoint')]
    # print(to_make)

    lv = open("build_versions2.json")
    buildver = lv.read()
    min_tags = json.loads(buildver)
    lv.close()
    # min_tags look like this {'python': ['v0.9'], 'matlab': ['v3.2']}

    # create full version-menu listing using the built folders from above
    f = open('datajoint_theme/version-menu.html', 'w+')
    for lang in min_tags:
        # print("lang is ")
        # print(lang)
        # print("versions are ")
        # print(min_tags[lang])

        for ver in min_tags[lang]:
        
            f.write('<li class="version-menu"><a href="/' + lang + "/" + ver + '">' + lang + "-" + ver + '</a></li>\n')

    
    # for folder in to_make:
    #     version = folder.split('/')[1] # 'matlab-v3.2.2'
    #     f.write('<li class="version-menu"><a href="/' + version.split("-")[0] + "/" + version.split("-")[1] + '">' + version + '</a></li>\n')
            
    f.close()
       
    # copy over the full version-menu listing to datajoint_theme FIRST, 
    # then build individual folders, and copy to full_site folder 

    for folder in to_make:
        shutil.copy2('datajoint_theme/version-menu.html', folder + "/datajoint_theme/version-menu.html") 
        subprocess.Popen(["make", "site"], cwd=folder).wait()
        subprocess.Popen(["pdflatex", "DataJointDocs.tex"], cwd=folder + '/_build/latex').wait()
        subprocess.Popen(["pdflatex", "DataJointDocs.tex"], cwd=folder + '/_build/latex').wait()

        lang_version = folder.split('/')[1] # 'matlab-v3.2.2'
        version = lang_version.split("-")[1].split(".")[:-1] #['v3', '2']
        abbr_ver = ".".join(version)  #v3.2
        abbr_lang_ver = ".".join(lang_version.split(".")[:-1])
        shutil.copytree(folder + "/site", 'full_site/' + lang_version.split("-")[0] + "/" + abbr_ver)
        os.rename(folder + '/_build/latex/DataJointDocs.pdf', folder + '/_build/latex/DataJointDocs_' + abbr_lang_ver + '.pdf')
        shutil.copy2(folder + '/_build/latex/DataJointDocs_' + abbr_lang_ver + '.pdf', 'full_site/' + lang_version.split("-")[0] + "/" + abbr_ver)

    for lang in ["matlab", "python"]:
        ver_list=[]
        for to_sort in glob.glob('full_site/' + lang + '/**'):
            ver_list.append(float((os.path.basename(to_sort).split("v")[1])))
        newest_ver = "v" + str(max(ver_list))
        src_path = 'full_site/' + lang + "/" + newest_ver
        copy_contents(src_path, os.path.join('full_site', lang))

    copy_contents('dj_root_theme', 'full_site')
    copy_contents('full_site/python/_static', 'full_site/_static')


def copy_contents(src_dir, dest_dir):
    """
    Copy the *contents* of `src_dir` into the `dest_dir` recursively. 
    Any empty directory will *not* be copied.
    """
    for root, dirnames, filenames in os.walk(src_dir):
        for fname in filenames:
            fpath = os.path.join(root, fname)
            rel_path = os.path.relpath(fpath, src_dir)
            dpath = os.path.join(dest_dir, rel_path)
            # print(fpath + " >>>>>> " + dpath)
            dir_name, _ = os.path.split(dpath)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            shutil.copy2(fpath, dpath)


make_full_site()
