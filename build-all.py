import os
from os import path
import json
import glob
import shutil
import subprocess
import platform
from collections import defaultdict
from util import get_newest_tag 
from util import copy_contents

# default values in case the build config file is missing
git_urls = {
    'common': "https://github.com/datajoint/datajoint-docs.git",
    'matlab': "https://github.com/datajoint/datajoint-matlab.git",
    'python': "https://github.com/datajoint/datajoint-python.git"
}

def create_build_folders(lang): 
    """
    Prepares the necessary parts for full-versioned documentation site building by 
    cloning and checking out appropriate tags from the `lang` respective repositories. 
    Prepared parts will be inside `build-all` directory 
    """
    raw_tags = subprocess.Popen(["git", "tag"], cwd= path.join("build-all", "datajoint-" + lang), stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()

    with open("build_versions.json") as f:
        print(f)
        min_tags = json.load(f)

    tags = [get_newest_tag(t, raw_tags) for t in min_tags[lang]]

    for tag in tags:
        subprocess.Popen(["git", "checkout", tag],
                         cwd=path.join("build-all", "datajoint-" + lang), stdout=subprocess.PIPE).wait()
        dsrc_lang = path.join("build-all", "datajoint-" + lang, "docs-parts")
        dst_build_folder = path.join("build-all", lang + "-" + tag)
        dst_main = path.join(dst_build_folder, "contents")
        dst_temp = path.join(dst_main, "comm")

        if path.exists(dst_build_folder):
            shutil.rmtree(dst_build_folder)

        # copy over the lang source doc contents into the build folder 
        shutil.copytree(dsrc_lang, dst_main)

        # grab which version of the common folder the lang doc needs to be merged with
        with open(path.join(dsrc_lang, "version_common.json")) as f:
            # expected in this format { "comm_version" : "v0.0"}
            version_info = json.load(f)

        raw_tags_comm = subprocess.Popen(["git", "tag"], cwd=path.join("build-all", "datajoint-docs"), stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
        comm_to_build = get_newest_tag(version_info['comm_version'], raw_tags_comm)

        subprocess.Popen(["git", "checkout", comm_to_build],cwd=path.join("build-all", "datajoint-docs"), stdout=subprocess.PIPE).wait()
        dsrc_comm = path.join("build-all", "datajoint-docs", "contents")
        # copy over the cmmon source doc contents into the build folder 
        shutil.copytree(dsrc_comm, dst_temp)

        # unpacking the content of common into lang-specific build folder
        copy_contents(dst_temp, dst_main)

        # removing the temporary comm folder because that shouldn't get build
        shutil.rmtree(dst_temp)

        # copy the datajoint_theme folder, conf.py and makefile for individual lang-ver folder building
        shutil.copytree("datajoint_theme", path.join(dst_build_folder, "datajoint_theme"))
        shutil.copy2("Makefile", path.join(dst_build_folder, "Makefile"))
        shutil.copy2(path.join("contents", "conf.py"), path.join(dst_build_folder, "contents", "conf.py"))
        shutil.copy2("report.txt", path.join(dst_build_folder, "report.txt"))

        # add current_version <p> tag into the datajoint_theme folder 
        with open(path.join(dst_build_folder, 'datajoint_theme', 'this_version.html'), 'w+') as f:
            f.write('<p class="thisVersion">' + lang + "-" + ".".join(tag.split(".")[:-1]) + '</p>')

        # add current_version as release into the conf.py file (for pdf generation)
        with open(path.join(dst_build_folder, "contents", "conf.py"), 'a+') as f:
            f.write('release = "' + lang + "-" + ".".join(tag.split(".")[:-1]) + '"')


# generate site folder with all contents using the above build folders
def make_full_site():
    """
    Builds the full-versioned site using the `build-all` directory and puts the resulting html/pdf into `full_site` directory.
    """

    if path.exists('full_site'):
        shutil.rmtree('full_site')
    os.makedirs('full_site')
    
    # build individual lang-ver folder
    to_make = [folder for folder in glob.glob(path.join('build-all', '**')) if not path.basename(folder).startswith('datajoint')]

    with open("build_versions.json") as f:
        min_tags = json.load(f)
    # min_tags look like this {'python': ['v0.9'], 'matlab': ['v3.2']}

    # create full version-menu listing using the built folders from above
    with open(path.join('datajoint_theme', 'version-menu.html'), 'w+') as f:
        for lang in min_tags:
            for ver in min_tags[lang]:
                # f.write('<li class="version-menu"><a href="/' + lang + "/" + ver + '">' + lang + "-" + ver + '</a></li>\n')
                f.write('<li class="version-menu"><a href="/{lang}/{ver}">{lang}-{ver}</a></li>\n'.format(lang=lang, ver=ver))
       
    # copy over the full version-menu listing to datajoint_theme FIRST, 
    # then build individual folders, and copy to full_site folder 

    for folder in to_make:
        shutil.copy2(path.join('datajoint_theme', 'version-menu.html'), path.join(folder, "datajoint_theme", "version-menu.html"))
        if platform.system() == "Windows":
            subprocess.Popen(["sphinx-build", ".", "..\_build\html"], cwd=path.join(folder, "contents")).wait() # builds html by default
            subprocess.Popen(["sphinx-build", "-b", "latex", ".", "..\_build\latex"], cwd=path.join(folder, "contents")).wait()
            if path.exists(path.join(folder, "site")):
                shutil.rmtree(path.join(folder, "site"))
            os.makedirs(path.join(folder, "site"))
            copy_contents(path.join(folder, "_build", "html"), path.join(folder, "site"))
        else:
            subprocess.Popen(["make", "site"], cwd=folder).wait()

        #making pdf out of the latex directory only if pdflatex runs
        try:
            subprocess.Popen(["pdflatex", "DataJointDocs.tex"], cwd=path.join(folder, '_build', 'latex')).wait()
            subprocess.Popen(["pdflatex", "DataJointDocs.tex"], cwd=path.join(folder, '_build', 'latex')).wait()
        except:
            print("Latex environment not set up - no pdf will be generated")

        lang_version = folder.split(os.sep)[1]  # 'matlab-v3.2.2'
        lang, version = lang_version.split("-")   # e.g. 'matlab',  'v3.2.2'
        abbr_ver = '.'.join(version.split('.')[:-1])  # e.g. 'v3.2'
        abbr_lang_ver = lang + '-' + abbr_ver

        shutil.copytree(path.join(folder, "site"), path.join('full_site', lang_version.split("-")[0], abbr_ver))

        if path.exists(path.join(folder, '_build', 'latex', 'DataJointDocs.pdf')):
            os.rename(path.join(folder, '_build', 'latex', 'DataJointDocs.pdf'), path.join(folder, '_build', 'latex', 'DataJointDocs_{}.pdf'.format(abbr_lang_ver)))
            shutil.copy2(path.join(folder, '_build', 'latex', 'DataJointDocs_{}.pdf'.format(abbr_lang_ver)), path.join('full_site', lang_version.split("-")[0], abbr_ver))

    for lang in min_tags:
        available_vers= defaultdict(list)
        for to_sort in glob.glob(path.join('full_site', lang, '**')):
            version = path.basename(to_sort).strip("v")
            major_v, minor_v = version.split(".")
            major_v = int(major_v)
            minor_v = int(minor_v)
            # example: available_vers = {3: [0, 1, 2], 4: [1, 2, 3]}
            available_vers[major_v].append(minor_v)

        # get the latest of the major version, then get the latest minor version within the latest major version
        newest_ver_maj = max(available_vers)
        newest_ver_min = max(available_vers[newest_ver_maj])
  
        newest_ver = "v{maj}.{min}".format(maj=str(newest_ver_maj), min=str(newest_ver_min))

        src_path = path.join('full_site', lang, newest_ver)
        # make the latest version of each language available by default
        copy_contents(src_path, path.join('full_site', lang))

    copy_contents('dj_root_theme', 'full_site')
    copy_contents(path.join('full_site', 'python', '_static'), path.join('full_site', '_static'))


##########################################################
####====== begin building full version doc here ======####
if __name__ == "__main__":
    # if build_config file exists, override the default git_url values with config values
    try:
        import build_config as config
        git_urls = dict(git_urls, **config.config_urls)
    except:
        print("build_config.py file missing - will use default values for git repo")

    # ensure build folder is clean before the build
    if path.exists('build-all'):
        shutil.rmtree('build-all')
    os.makedirs('build-all')

    subprocess.Popen(
        ["git", "clone", git_urls['common'], "datajoint-docs"], cwd="build-all").wait()

    subprocess.Popen(
        ["git", "clone", git_urls['matlab'], "datajoint-matlab"], cwd="build-all").wait()

    subprocess.Popen(
        ["git", "clone", git_urls['python'], "datajoint-python"], cwd="build-all").wait()

    create_build_folders("matlab")
    create_build_folders("python")
    make_full_site()
