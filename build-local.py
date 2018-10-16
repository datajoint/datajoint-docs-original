import os
from os import path
import json
import glob
import shutil
import subprocess
import platform
import tagpicker


# default values in case the build config file is missing
git_urls = {
    'common': "https://github.com/datajoint/datajoint-docs.git",
    'matlab': "https://github.com/datajoint/datajoint-matlab.git",
    'python': "https://github.com/datajoint/datajoint-python.git"
}

# default path location for the language local folders
local_lang_path = {
    'matlab': "../datajoint-matlab",
    'python': "../datajoint-python"
}

try:
    import build_config as config
    git_urls = dict(git_urls, **config.config_urls)
    local_lang_path = dict(local_lang_path, **config.local_path)
except:
    print("build_config.py file missing - will use default values")

matlab_dir = local_lang_path['matlab']
python_dir = local_lang_path['python']

if path.exists('build-local'):
    shutil.rmtree('build-local')

os.makedirs('build-local')
if path.exists(matlab_dir):
    print("local matlab doc exists - copying the folder over")
    shutil.copytree(matlab_dir, path.join('build-local', 'datajoint-matlab'))
else:
    print("local matlab doc not found - cloning from the git repo")
    subprocess.Popen(
        ["git", "clone", git_urls['matlab'], "datajoint-matlab"], cwd="build-local").wait()
if path.exists(python_dir):
    print("local python doc exists - copying the folder over")
    shutil.copytree(python_dir, path.join('build-local', 'datajoint-python'))
else:
    print("local python doc not found - cloning from the git repo")
    subprocess.Popen(
        ["git", "clone", git_urls['python'], "datajoint-python"], cwd="build-local").wait()


def local_build(loc_comm=True, python_tag='', matlab_tag=''):
    if path.exists(path.join("build-local", "datajoint-docs")):
            shutil.rmtree(path.join("build-local", "datajoint-docs"))
    if not loc_comm:
        print("local common folder build set to False - cloning from the git repo")
        subprocess.Popen(
            ["git", "clone", git_urls['common'], "datajoint-docs"], cwd="build-local").wait()
    else:
        # Default - copy the local comm doc to the build folder
        print("using LOCAL common folder for build - copying over")
        
        shutil.copytree(".", path.join("build-local", "datajoint-docs"), ignore=shutil.ignore_patterns('build-local'))

    to_build = { 'python' : python_tag, 'matlab' : matlab_tag }

    for lang, tag in to_build.items():     
        if tag is not '':
            print("lang, tag is " + lang + ", " + tag)
            # TODO non-existent tag still keeps on building with the latest lang content - needs to throw an error
            subprocess.Popen(["git", "checkout", tag],
                            cwd=path.join("build-local", "datajoint-" + lang), stdout=subprocess.PIPE).wait()
            dst_build_folder = path.join("build-local", lang + "-" + tag)
        else:
            print("creating build folder for " + lang)
            dst_build_folder = path.join("build-local", lang)

        dsrc_lang = path.join("build-local", "datajoint-" + lang, "docs")
        dst_main = path.join(dst_build_folder, "contents")
        dst_temp = path.join(dst_main, "comm")

        if path.exists(dst_build_folder):
            shutil.rmtree(dst_build_folder)

        # copy over the lang source doc contents into the build folder
        # dst_main for example is "build-local/datajoint-matlab/docs/contents/
        shutil.copytree(dsrc_lang, dst_main)

        if tag:
            print("tag was specified. tag-" + tag) 
            if path.exists(path.join(dsrc_lang, "version_common.json")):
                # grab which version of the common folder the lang doc needs to be merged with
                cv = open(path.join(dsrc_lang, "version_common.json"))
                v = cv.read()  # expected in this format { "comm_version" : "v0.0"}
                version_info = json.loads(v)
                cv.close()

                raw_tags_comm = subprocess.Popen(["git", "tag"], cwd=path.join("build-local", "datajoint-docs"), stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
                comm_to_build = tagpicker.get_newest_tag(version_info['comm_version'], raw_tags_comm)

                subprocess.Popen(["git", "checkout", comm_to_build],
                                cwd=path.join("build-local", "datajoint-docs"), stdout=subprocess.PIPE).wait()
 
        dsrc_comm = path.join("build-local", "datajoint-docs", "contents")
        # copy over the common source doc contents into the temporary subfolder in build folder 
        # dst_temp for example is "build-local/datajoint-matlab/docs/contents/comm/"
        shutil.copytree(dsrc_comm, dst_temp)

        # unpacking the common content from the temporary dst_temp folder to the respective build folder
        for root, dirs, filenames in os.walk(dst_temp):
            for f in filenames:
                if f.endswith(".doctree"):
                    break
                fullpath = path.join(root, f)
                # root looks like "build-local/matlab/contents/comm/concepts"
                # fullpath looks like "build-local/matlab/contents/comm/concepts/01-Data-Model.rst"
                print("file: " + fullpath)
                # dirs is a list of all directories on the same level as the target file 
                # for example, when fullpath is "build-local/matlab/contents/comm/manipulation/Manipulation.rst"
                # the dirs list is [], however, when fullpath is "build-local/python/contents/comm/conf.py",
                # the dirs list is ['manipulation', 'intro', 'setup', 'admin', 'queries', '_static', 'computation', 'definition', 'concepts', 'existing']
                # the len(dirs) == 0 works because the target doc rst files are placed inside a folder with no other subdirectory inside
                if len(dirs) == 0:
                    root_path, new_dir = root.split("comm")
                    new_fullpath = root_path + new_dir
                    if not path.exists(path.normpath(new_fullpath)):
                        os.makedirs(path.normpath(new_fullpath))
                    
                    shutil.copy2(fullpath, path.normpath(new_fullpath))
            print("-------------------------------")

        # copying the toc tree and the contents of _static folder from the common build directory
        shutil.copy2(path.join(dst_temp, "index.rst"), path.join(dst_main, "index.rst"))
        copy_contents(path.join(dst_temp, "_static"), path.join(dst_main, "_static"))

        # removing the temporary comm folder because that shouldn't get build
        shutil.rmtree(dst_temp)

        # copy the datajoint_theme folder, conf.py and makefile from the latest/local doc for individual lang-ver folder building
        shutil.copytree("datajoint_theme", path.join(dst_build_folder, "datajoint_theme"))
        shutil.copy2("Makefile", path.join(dst_build_folder, "Makefile"))
        shutil.copy2(path.join("contents", "conf.py"), path.join(dst_build_folder, "contents", "conf.py"))
        shutil.copy2("report.txt", path.join(dst_build_folder, "report.txt"))

        # add current_version <p> tag into the datajoint_theme folder
        f = open(path.join(dst_build_folder, 'datajoint_theme', 'this_version.html'), 'w+')
        if tag:
            f.write('<p class="thisVersion">' + lang + "-" + tag + '</p>')
        else:
            f.write('<p class="thisVersion">' + lang + '</p>')
        f.close()
        # add current_version as release into the conf.py file (for pdf generation)
        f = open(path.join(dst_build_folder, "contents", "conf.py"), 'a+')
        if tag:
            f.write('release = "' + lang + "-" + tag + '"')
        else:
            f.write('release = "' + lang + '"')
        f.close()

# generate site folder with all contents using hte above build folders
    if path.exists('loc_built_site'):
        shutil.rmtree('loc_built_site')
        os.makedirs('loc_built_site')
    else:
        os.makedirs('loc_built_site')

    # build individual lang-ver folder - expect 2 for local build
    to_make = [folder for folder in glob.glob(path.join('build-local', '**')) if not path.basename(folder).startswith('datajoint')]
    print(to_make)

    # create full version-menu listing using the built folders from above
    # refresher: to_build = {'python': python_tag, 'matlab': matlab_tag}
    f = open(path.join('datajoint_theme', 'version-menu.html'), 'w+')
    for lang, tag in to_build.items():
        if tag:
            f.write('<li class="version-menu"><a href="/' + lang +
                        "-" + tag + '">' + lang + "-" + tag + '</a></li>\n')
        else:
            f.write('<li class="version-menu"><a href="/' + lang +
                    "/" '">' + lang + '</a></li>\n')
    f.close()

    # copy over the full version-menu listing to datajoint_theme FIRST,
    # then build individual folders, and copy to loc_built_site folder

    for folder in to_make:
        shutil.copy2(path.join('datajoint_theme', 'version-menu.html'), path.join(folder, "datajoint_theme", "version-menu.html"))
        if platform.system() == "Windows":
            subprocess.Popen(["sphinx-build", "-b", "html", ".", "..\_build\html"], cwd=path.join(folder, "contents")).wait()  
            subprocess.Popen(["sphinx-build", "-b", "latex", ".", "..\_build\latex"], cwd=path.join(folder, "contents")).wait()
            if path.exists(path.join(folder,"site")):
                shutil.rmtree(path.join(folder, "site"))
            os.makedirs(path.join(folder, "site"))
            copy_contents(path.join(folder, "_build", "html"), path.join(folder, "site"))
        else:
            subprocess.Popen(["make", "site"], cwd=folder).wait()

        try:
            subprocess.Popen(["pdflatex", "DataJointDocs.tex"], cwd=path.join(folder, '_build', 'latex')).wait()
            subprocess.Popen(["pdflatex", "DataJointDocs.tex"], cwd=path.join(folder, '_build', 'latex')).wait()
        except:
            print("Latex environment not set up - no pdf will be generated")

        lang_version = folder.split(os.sep)[1]  # 'matlab' from `build-local/matlab/contents/...`
        shutil.copytree(path.join(folder, "site"), path.join('loc_built_site', lang_version))

        if path.exists(path.join(folder, '_build', 'latex', 'DataJointDocs.pdf')):
            os.rename(path.join(folder, '_build', 'latex', 'DataJointDocs.pdf'), path.join(folder, '_build', 'latex', 'DataJointDocs_' + lang_version + '.pdf'))
            shutil.copy2(path.join(folder, '_build', 'latex', 'DataJointDocs_' + lang_version + '.pdf'), path.join('loc_built_site', lang_version))

        copy_contents('dj_root_theme', 'loc_built_site')
        copy_contents(path.join('loc_built_site', 'python', '_static'), path.join('loc_built_site', '_static'))
        

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



