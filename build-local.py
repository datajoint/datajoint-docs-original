import os
import json
import glob
import shutil
import subprocess
import datetime

matlab_dir = "../datajoint-matlab/"
python_dir = "../datajoint-python/"


if not os.path.exists('build-local'):
    os.makedirs('build-local')
    if os.path.exists(matlab_dir):
        print("local matlab doc exists - copying the folder over")
        shutil.copytree(matlab_dir, 'build-local/datajoint-matlab')
    else:
        print("local matlab doc not found - cloning from the git repo")
        subprocess.Popen(
            ["git", "clone", "git@github.com:mahos/testDocMatlab.git", "datajoint-matlab"], cwd="build-local").wait()
    if os.path.exists(python_dir):
        print("local python doc exists - copying the folder over")
        shutil.copytree(python_dir, 'build-local/datajoint-python')
    else:
        print("local python doc not found - cloning from the git repo")
        subprocess.Popen(
            ["git", "clone", "git@github.com:mahos/testDocPython.git", "datajoint-python"], cwd="build-local").wait()


def local_build(loc_comm=True, python_tag='', matlab_tag=''):
    if os.path.exists("build-local/datajoint-docs"):
            shutil.rmtree("build-local/datajoint-docs")
    if not loc_comm:
        print("local common folder build set to False - cloning from the git repo")
        subprocess.Popen(
            ["git", "clone", "git@github.com:mahos/testDocMain.git", "datajoint-docs"], cwd="build-local").wait()
    else:
        # Default - copy the local comm doc to the build folder
        print("local common folder found - copying over for build")
        # copy_contents("./", "build-local/datajoint-docs")
        
        shutil.copytree("./", "build-local/datajoint-docs", ignore=shutil.ignore_patterns('build-local'))

    to_build = { 'python' : python_tag, 'matlab' : matlab_tag }

    for lang, tag in to_build.items():
        print("lang, tag is " + lang + tag)
        if tag is not '':
            print('tag is not empty, tag is ' + tag)
            subprocess.Popen(["git", "checkout", tag],
                            cwd="build-local/datajoint-" + lang, stdout=subprocess.PIPE).wait()
            dst_build_folder = "build-local/" + lang + "-" + tag
        else:
            print("creating build folder for " + lang + "-" +tag)
            dst_build_folder = "build-local/" + lang

        dsrc_lang = "build-local/datajoint-" + lang + "/docs"
        dst_main = dst_build_folder + "/contents"
        dst_temp = dst_main + "/comm"

        if os.path.exists(dst_build_folder):
            shutil.rmtree(dst_build_folder)

        # copy over the lang source doc contents into the build folder
        shutil.copytree(dsrc_lang, dst_main)

        if tag:
            print("tag exists and it is tag-" + tag) 
            if os.path.exists(dsrc_lang + "/_version_common.json"):
                # grab which version of the common folder the lang doc needs to be merged with
                cv = open(dsrc_lang + "/_version_common.json")
                v = cv.read()  # expected in this format { "comm_version" : "v0.0.0"}
                version_info = json.loads(v)
                cv.close
                subprocess.Popen(["git", "checkout", version_info['comm_version']],
                                cwd="build-local/datajoint-docs", stdout=subprocess.PIPE).wait()
 
        dsrc_comm = "build-local/datajoint-docs/contents"
        # copy over the cmmon source doc contents into the build folder
        shutil.copytree(dsrc_comm, dst_temp)

        # copying and merging all of the folders from lang-specific repo to build folder
        for root, dirs, filename in os.walk(dst_temp):
            for f in filename:
                fullpath = os.path.join(root, f)
                print(fullpath)
                if len(dirs) == 0:
                    root_path, new_path = root.split("comm/")
                    shutil.copy2(fullpath, root_path + new_path)
            print("-------------------------------")

        # copying the toc tree and the config files
        shutil.copy2(dst_temp + "/" + "index.rst",
                     dst_main + "/" + "index.rst")

        # removing the temporary comm folder because that shouldn't get build
        shutil.rmtree(dst_temp)

        # copy the datajoint_theme folder, conf.py and makefile for individual lang-ver folder building
        shutil.copytree("datajoint_theme",
                        dst_build_folder + "/datajoint_theme")
        shutil.copy2("Makefile", dst_build_folder + "/Makefile")
        shutil.copy2("contents/conf.py", dst_build_folder +
                     "/contents/" + "conf.py")

        # add current_version <p> tag into the datajoint_theme folder
        f = open(dst_build_folder + '/datajoint_theme/this_version.html', 'w+')
        if tag:
            f.write('<p class="thisVersion">' + lang + "-" + tag + '</p>')
        else:
            f.write('<p class="thisVersion">' + lang + '</p>')
        f.close()
        # add current_version as release into the conf.py file (for pdf generation)
        f = open(dst_build_folder + "/contents/" + "conf.py", 'a+')
        if tag:
            f.write('release = "' + lang + "-" + tag + '"')
        else:
            f.write('release = "' + lang + '"')
        f.close()

# generate site folder with all contents using hte above build folders
    if os.path.exists('loc_built_site'):
        shutil.rmtree('loc_built_site')
        os.makedirs('loc_built_site')
    else:
        os.makedirs('loc_built_site')

    # build individual lang-ver folder - expect 2 for local build
    to_make = [folder for folder in glob.glob(
        'build-local/**') if not os.path.basename(folder).startswith('datajoint')]
    print(to_make)

    # create full version-menu listing using the built folders from above
    # refresher: to_build = {'python': python_tag, 'matlab': matlab_tag}
    f = open('datajoint_theme/version-menu.html', 'w+')
    for lang, tag in to_build.items():
        if tag:
            f.write('<li class="version-menu"><a href="/' + lang +
                        "/" + tag + '">' + lang + "-" + tag + '</a></li>\n')
        else:
            f.write('<li class="version-menu"><a href="/' + lang +
                    "/" '">' + lang + '</a></li>\n')
    f.close()

    # copy over the full version-menu listing to datajoint_theme FIRST,
    # then build individual folders, and copy to loc_built_site folder

    for folder in to_make:
        shutil.copy2('datajoint_theme/version-menu.html',
                     folder + "/datajoint_theme/version-menu.html")
        subprocess.Popen(["make", "site"], cwd=folder).wait()
        subprocess.Popen(["pdflatex", "DataJointDocs.tex"],
                         cwd=folder + '/_build/latex').wait()
        subprocess.Popen(["pdflatex", "DataJointDocs.tex"],
                         cwd=folder + '/_build/latex').wait()

        lang_version = folder.split('/')[1]  # 'matlab-v3.2.2'
        shutil.copytree(folder + "/site", 'loc_built_site/' + lang_version)
        os.rename(folder + '/_build/latex/DataJointDocs.pdf', folder +
                  '/_build/latex/DataJointDocs_' + lang_version + '.pdf')
        shutil.copy2(folder + '/_build/latex/DataJointDocs_' + lang_version +
                     '.pdf', 'loc_built_site/' + lang_version)
    #     # copy_contents('loc_built_site/' + lang_version,
    #     #               'loc_built_site/_static')


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



if __name__ == "__main__":
    import sys
    kwargs = {}

    for arg in sys.argv[1:]:
        if "=" in arg:
            arg_name, arg_value = arg.split('=')
            if arg_name == "loc_comm" and arg_value == "False":
                kwargs['loc_comm'] = ''
            else:
                kwargs[arg_name] = arg_value
        elif sys.argv[1:].index(arg) == 0:
            if arg == "False":
                kwargs['loc_comm'] = ''
            else:
                kwargs['loc_comm'] = arg
        elif sys.argv[1:].index(arg) == 1:
            kwargs['python_tag'] = arg
        elif sys.argv[1:].index(arg) == 2:
            kwargs['matlab_tag'] = arg
        else:
            local_build()
    local_build(**kwargs)



