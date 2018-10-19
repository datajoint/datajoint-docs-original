import os
from os import path
import json
import glob
import shutil
import sys
import subprocess
import platform
import warnings
from util import get_newest_tag
from util import copy_contents

# default values in case the build config file is missing
git_urls = {
    'common': "https://github.com/datajoint/datajoint-docs.git",
    'matlab': "https://github.com/datajoint/datajoint-matlab.git",
    'python': "https://github.com/datajoint/datajoint-python.git"
}

# default path location for the language local folders unless otherwise specified in the build config
local_lang_path = {
    'matlab': "../datajoint-matlab",
    'python': "../datajoint-python"
}


def local_build(use_local_common=True, python_tag='', matlab_tag=''):
    """
    Builds the most recent version of locally placed documentation folder(s) by default. 
    If `use_local_common` set to False, then the most recent common documentation is cloned from the git repository.
    `python_tag` and `matlab_tag` may be set with full patch versions for specific language folder building.
    """

    if path.exists(path.join("build-local", "datajoint-docs")):
        shutil.rmtree(path.join("build-local", "datajoint-docs"))
    if not use_local_common:
        print("local common folder build set to False - cloning from the git repo")
        subprocess.Popen(
            ["git", "clone", git_urls['common'], "datajoint-docs"], cwd="build-local").wait()
    else:
        # Default - copy the local comm doc to the build folder
        print("using local common folder for build - copying over")
        
        shutil.copytree(".", path.join("build-local", "datajoint-docs"), ignore=shutil.ignore_patterns('build-local'))

    to_build = { 'python' : python_tag, 'matlab' : matlab_tag }

    for lang, tag in to_build.items():     
        if tag is not '':
            print("lang, tag is " + lang + ", " + tag)
            # issue warning when non-existent tag was specified. Build will keep on building with the latest lang content 
            proc = subprocess.Popen(["git", "checkout", tag], cwd=path.join("build-local", "datajoint-" + lang), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outs, errs = proc.communicate()
            if errs:
                print(errs.decode().strip())
                errmsg = "specified tag {tag} does not exist for the {lang} repo - will INSTEAD build using the most current version".format(tag=tag, lang=lang)
                warnings.warn(errmsg)

            dst_build_folder = path.join("build-local", lang + "-" + tag)
        else:
            print("creating build folder for " + lang)
            dst_build_folder = path.join("build-local", lang)

        dsrc_lang = path.join("build-local", "datajoint-" + lang, "docs-parts")
        dst_main = path.join(dst_build_folder, "contents")
        dst_temp = path.join(dst_main, "comm")

        if path.exists(dst_build_folder):
            shutil.rmtree(dst_build_folder)

        # copy over the lang source doc contents into the build folder
        # dst_main for example is "build-local/datajoint-matlab/docs-parts/contents/
        shutil.copytree(dsrc_lang, dst_main)

        if tag:
            print("tag {tag} was specified for {lang}".format(tag=tag ,lang=lang)) 
            if path.exists(path.join(dsrc_lang, "version_common.json")):
                # grab which version of the common folder the lang doc needs to be merged with
                with open(path.join(dsrc_lang, "version_common.json")) as f:
                    # expected in this format { "comm_version" : "v0.0"}
                    version_info = json.load(f)

                raw_tags_comm = subprocess.Popen(["git", "tag"], cwd=path.join("build-local", "datajoint-docs"), stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split()
                comm_to_build = get_newest_tag(version_info['comm_version'], raw_tags_comm)

                subprocess.Popen(["git", "checkout", comm_to_build],
                                cwd=path.join("build-local", "datajoint-docs"), stdout=subprocess.PIPE).wait()
 
        dsrc_comm = path.join("build-local", "datajoint-docs", "contents")
        # copy over the common source doc contents into the temporary subfolder in build folder 
        # dst_temp for example is "build-local/datajoint-matlab/docs-parts/contents/comm/"
        shutil.copytree(dsrc_comm, dst_temp)

        # unpacking the common content from the temporary dst_temp folder to the language build folder
        copy_contents(dst_temp, dst_main)

        # removing the temporary comm folder because that shouldn't get build
        shutil.rmtree(dst_temp)

        # copy the datajoint_theme folder, conf.py and makefile from the latest/local doc for individual lang-ver folder building
        shutil.copytree("datajoint_theme", path.join(dst_build_folder, "datajoint_theme"))
        shutil.copy2("Makefile", path.join(dst_build_folder, "Makefile"))
        shutil.copy2(path.join("contents", "conf.py"), path.join(dst_build_folder, "contents", "conf.py"))
        shutil.copy2("report.txt", path.join(dst_build_folder, "report.txt"))

        # add current_version <p> tag into the datajoint_theme folder
        with open(path.join(dst_build_folder, 'datajoint_theme', 'this_version.html'), 'w+') as f:
            if tag:
                f.write('<p class="thisVersion">{lang}-{tag}</p>'.format(lang=lang, tag=tag))
            else:
                f.write('<p class="thisVersion">{}</p>'.format(lang))

        # add current_version as release into the conf.py file (for pdf generation)
        with open(path.join(dst_build_folder, "contents", "conf.py"), 'a+') as f:
            if tag:
                f.write('release = "{lang}-{tag}"'.format(lang=lang, tag=tag))
            else:
                f.write('release = "{}"'.format(lang))

    # generate site folder with all contents using the above build folders
    if path.exists('loc_built_site'):
        shutil.rmtree('loc_built_site')        
    os.makedirs('loc_built_site')

    # build individual lang-ver folder - expect 2 for local build
    to_make = [folder for folder in glob.glob(path.join('build-local', '**')) if not path.basename(folder).startswith('datajoint')]
    print(to_make)

    # create full version-menu listing using the built folders from above
    # refresher: to_build = {'python': python_tag, 'matlab': matlab_tag}
    with open(path.join('datajoint_theme', 'version-menu.html'), 'w+') as f:
        for lang, tag in to_build.items():
            if tag:
                f.write('<li class="version-menu"><a href="/{lang}/{lang}-{tag}">{lang}-{tag}</a></li>\n'.format(lang=lang, tag=tag))
            else:
                f.write('<li class="version-menu"><a href="/{lang}">{lang}</a></li>\n'.format(lang=lang))


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

        # 'matlab' from `build-local/matlab/contents/...` or 'matlab-v3.2.4' from `build-local/matlab-v3.2.4/contents/...`
        lang_version = folder.split(os.sep)[1]
        lang = lang_version[:6] # workaround to make sure /matlab or /python exists for the pre-set dj_root_theme
        # dumping all contents of site/ inside something like 'loc_built_site/python/python-v0.10.0'
        shutil.copytree(path.join(folder, "site"), path.join('loc_built_site', lang, lang_version))        

        if path.exists(path.join(folder, '_build', 'latex', 'DataJointDocs.pdf')):
            os.rename(path.join(folder, '_build', 'latex', 'DataJointDocs.pdf'), path.join(folder, '_build', 'latex', 'DataJointDocs_{}.pdf'.format(lang_version)))
            shutil.copy2(path.join(folder, '_build', 'latex', 'DataJointDocs_{}.pdf'.format(lang_version)), path.join('loc_built_site', lang, lang_version))

        copy_contents('dj_root_theme', 'loc_built_site')
        copy_contents(path.join('loc_built_site', lang, lang_version), path.join('loc_built_site', lang))
        copy_contents(path.join('loc_built_site', 'python', '_static'), path.join('loc_built_site', '_static'))


##########################################################
####====== begin building local version doc here ======####
if __name__ == "__main__":
    # if build_config file exists, override the default git_url and/or local_lang_path values with config values
    try:
        import build_config as config
        git_urls = dict(git_urls, **config.config_urls)
        local_lang_path = dict(local_lang_path, **config.local_path)
    except:
        print("build_config.py file missing - will use default values")

    matlab_dir = local_lang_path['matlab']
    python_dir = local_lang_path['python']

    # ensure build folder is clean before the build
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


    # set up for arguments passed in for local_build()
    kwargs = {}

    for arg in sys.argv[1:]:
        if "=" in arg:
            arg_name, arg_value = arg.split('=')
            if arg_name == "use_local_common" and arg_value == "False":
                kwargs['use_local_common'] = ''
            else:
                kwargs[arg_name] = arg_value
        elif sys.argv[1:].index(arg) == 0:
            if arg == "False":
                kwargs['use_local_common'] = ''
            else:
                kwargs['use_local_common'] = arg
        elif sys.argv[1:].index(arg) == 1:
            kwargs['python_tag'] = arg
        elif sys.argv[1:].index(arg) == 2:
            kwargs['matlab_tag'] = arg
        else:
            local_build()
            
    local_build(**kwargs)




