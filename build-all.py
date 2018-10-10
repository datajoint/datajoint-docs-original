import os
from os import path
import json
import glob
import shutil
import subprocess
import platform
import build_config as config
import tagpicker


if path.exists('build-all'):
    shutil.rmtree('build-all')

os.makedirs('build-all')
subprocess.Popen(
    ["git", "clone", config.common_doc_url, "datajoint-docs"], cwd="build-all").wait()

subprocess.Popen(
    ["git", "clone", config.matlab_doc_url, "datajoint-matlab"], cwd="build-all").wait()

subprocess.Popen(
    ["git", "clone", config.python_doc_url, "datajoint-python"], cwd="build-all").wait()
    

def create_build_folders(lang): 
    raw_tags = subprocess.Popen(["git", "tag"], cwd= path.join("build-all", "datajoint-" + lang), stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
    git_tags = {}
    git_tags[lang] = raw_tags

    lv = open("build_versions.json")
    buildver = lv.read()
    min_tags = json.loads(buildver)
    lv.close()

    tags = tagpicker.pick_tag(min_tags, git_tags, lang)

    for tag in tags:
        subprocess.Popen(["git", "checkout", tag],
                         cwd=path.join("build-all", "datajoint-" + lang), stdout=subprocess.PIPE).wait()
        dsrc_lang2 = path.join("build-all", "datajoint-" + lang, "docs")
        dst_build_folder = path.join("build-all", lang + "-" + tag)
        dst_main = path.join(dst_build_folder, "contents")
        dst_temp = path.join(dst_main, "comm")

        if path.exists(dst_build_folder):
            shutil.rmtree(dst_build_folder)

        # copy over the lang source doc contents into the build folder 
        shutil.copytree(dsrc_lang2, dst_main)

        # grab which version of the common folder the lang doc needs to be merged with
        cv = open(path.join(dsrc_lang2, "_version_common.json"))
        v = cv.read() # expected in this format { "comm_version" : "v0.0.0"}
        version_info = json.loads(v)
        cv.close
        subprocess.Popen(["git", "checkout", version_info['comm_version']],cwd=path.join("build-all", "datajoint-docs"), stdout=subprocess.PIPE).wait()
        dsrc_comm2 = path.join("build-all", "datajoint-docs", "contents")
        # copy over the cmmon source doc contents into the build folder 
        shutil.copytree(dsrc_comm2, dst_temp)

        # copying and merging all of the folders from lang-specific repo to build folder
        for root, dirs, filename in os.walk(dst_temp):
            for f in filename:
                fullpath = path.join(root, f)
                print(fullpath) #
                if len(dirs) == 0:
                    root_path, new_path = root.split("comm")
                    shutil.copy2(fullpath, path.normpath(root_path + new_path)) # gets rid of the // resulting from the split
            print("-------------------------------")

        # copying the toc tree and the config files
        shutil.copy2(path.join(dst_temp, "index.rst"), path.join(dst_main, "index.rst"))

        # removing the temporary comm folder because that shouldn't get build
        shutil.rmtree(dst_temp)

        # copy the datajoint_theme folder, conf.py and makefile for individual lang-ver folder building
        shutil.copytree("datajoint_theme", path.join(dst_build_folder, "datajoint_theme"))
        shutil.copy2("Makefile", path.join(dst_build_folder, "Makefile"))
        shutil.copy2(path.join("contents", "conf.py"), path.join(dst_build_folder, "contents", "conf.py"))

        # add current_version <p> tag into the datajoint_theme folder 
        f = open(path.join(dst_build_folder, 'datajoint_theme', 'this_version.html'), 'w+')
        f.write('<p class="thisVersion">' + lang + "-" + ".".join(tag.split(".")[:-1]) + '</p>') 
        f.close()
        # add current_version as release into the conf.py file (for pdf generation)
        f = open(path.join(dst_build_folder, "contents", "conf.py"), 'a+')
        f.write('release = "' + lang + "-" + ".".join(tag.split(".")[:-1])+ '"')
        f.close()


create_build_folders("matlab")
create_build_folders("python")

# generate site folder with all contents using hte above build folders

def make_full_site():

    if path.exists('full_site'):
        shutil.rmtree('full_site')
        os.makedirs('full_site')
    else:
        os.makedirs('full_site')
    
    # build individual lang-ver folder
    to_make = [folder for folder in glob.glob(path.join('build-all', '**')) if not path.basename(folder).startswith('datajoint')]
    # print(to_make)

    lv = open("build_versions.json")
    buildver = lv.read()
    min_tags = json.loads(buildver)
    lv.close()
    # min_tags look like this {'python': ['v0.9'], 'matlab': ['v3.2']}

    # create full version-menu listing using the built folders from above
    f = open(path.join('datajoint_theme', 'version-menu.html'), 'w+')
    for lang in min_tags:

        for ver in min_tags[lang]:
        
            f.write('<li class="version-menu"><a href="/' + lang + "/" + ver + '">' + lang + "-" + ver + '</a></li>\n')
        
    f.close()
       
    # copy over the full version-menu listing to datajoint_theme FIRST, 
    # then build individual folders, and copy to full_site folder 

    for folder in to_make:
        shutil.copy2(path.join('datajoint_theme', 'version-menu.html'), path.join(folder, "datajoint_theme", "version-menu.html"))
        if platform.system() == "Windows":
            subprocess.Popen(["spinx-build", ".", "_build\html"], cwd="contents").wait() # builds html by default
            subprocess.Popen(["spinx-build", "latex", ".", "_build\latex"], cwd="contents").wait()
            copy_contents("_build\html", "site")
        else:
            subprocess.Popen(["make", "site"], cwd=folder).wait()

        # making pdf out of the latex directory only if pdflatex runs
        try:
            subprocess.Popen(["pdflatex", "DataJointDocs.tex"], cwd=path.join(folder, '_build', 'latex')).wait()
            subprocess.Popen(["pdflatex", "DataJointDocs.tex"], cwd=path.join(folder, '_build', 'latex')).wait()
        except Warning:
            print("Latex environment not set up - no pdf will be generated")

        lang_version = folder.split(os.sep)[1] # 'matlab-v3.2.2'
        version = lang_version.split("-")[1].split(".")[:-1] #['v3', '2']
        abbr_ver = ".".join(version)  #v3.2
        abbr_lang_ver = ".".join(lang_version.split(".")[:-1])
        shutil.copytree(path.join(folder, "site"), path.join('full_site', lang_version.split("-")[0], abbr_ver))
        
        if path.exists(path.join('_build', 'latex', 'DataJointDocs.pdf')):
            os.rename(path.join(folder, '_build', 'latex', 'DataJointDocs.pdf'), path.join(folder, '_build', 'latex', 'DataJointDocs_' + abbr_lang_ver + '.pdf'))
            shutil.copy2(path.join(folder, '_build', 'latex', 'DataJointDocs_' + abbr_lang_ver + '.pdf'), path.join('full_site', lang_version.split("-")[0], abbr_ver))

    for lang in ["matlab", "python"]:
        ver_list=[]
        for to_sort in glob.glob(path.join('full_site', lang, '**')):
            ver_list.append(float((path.basename(to_sort).split("v")[1])))
        newest_ver = "v" + str(max(ver_list))
        src_path = path.join('full_site', lang, newest_ver)
        copy_contents(src_path, path.join('full_site', lang))

    copy_contents('dj_root_theme', 'full_site')
    copy_contents(path.join('full_site', 'python', '_static'), path.join('full_site', '_static'))


def copy_contents(src_dir, dest_dir):
    """
    Copy the *contents* of `src_dir` into the `dest_dir` recursively. 
    Any empty directory will *not* be copied.
    """
    for root, dirnames, filenames in os.walk(src_dir):
        for fname in filenames:
            fpath = path.join(root, fname)
            rel_path = path.relpath(fpath, src_dir)
            dpath = path.join(dest_dir, rel_path)
            # print(fpath + " >>>>>> " + dpath)
            dir_name, _ = path.split(dpath)
            if not path.exists(dir_name):
                os.makedirs(dir_name)
            shutil.copy2(fpath, dpath)


make_full_site()
