### for testing - sample of actual git tags
# git_tags = { "python": [
#                 "v0.8.7",

#                 "v0.9.0",
#                 "v0.9.1",
#                 "v0.9.5",

#                 "v0.10.0",
#                 "v0.10.3",

#                 "v1.0.1", 
#                 "v1.0.2", 

#                 "v1.1",
#                 "v1.1.3"
#                 ],
#           "matlab": [
#                 "v3.1.6",
#                 "v3.2.0",
#                 "v3.2.1",
#                 "v3.2.2",
#                 "v3.2.14",
#                 "v3.3.1",
#                 "v3.3.2-dev.5",
#                 "v3.3.3"
#                 ]
#         }

# # for testing: this will be specified in a file outside - this is the actual build that we want to see on the website
# to_make_tags = {
#     "python": [
#         "v0.9",
#         "v0.10",
#         "v1.0",
#         "v1.1"
#     ],
#     "matlab": [
#         "v3.2",
#         "v3.3"
#     ]
# }
import os
import os.path as path
import shutil

# returns the newest full tag (to the patch) given an abbreviated version (to minor version)
# get_newest_tag("v3.2", ["v3.1.6", "v3.2.0", "v3.2.1", "v3.2.2", "v3.2.14", "v3.3.1", "v3.3.2-dev.5","v3.3.3"])
# will return v3.2.14
def get_newest_tag(given_tag, raw_tags):
    to_sort = [rtag for rtag in raw_tags if rtag.startswith(given_tag)]
    patch_list = []
    for version in to_sort:
        try:
            vp = version.split('.', 2)[2]
        except IndexError: 
            vp = "0"

        if '-dev' in vp:
            print("invalid tag format: -dev in: " + version)
        else:
            patch_list.append(int(vp))
    if len(patch_list) > 0:
        newest_patch = max(patch_list)
        for ver in to_sort:
            if newest_patch == 0 and len(ver.split('.')) < 3:
                print("NOTICE: " + ver + " tag probably needs to be fixed to " + ver + ".0")
                return ver
            elif len(ver.split('.')) == 3 and ver.split('.', 2)[2] == str(newest_patch):
                # print("building version " + ver)
                return ver


def copy_contents(src_dir, dest_dir, skip_fpattern=None, skip_dpattern=None):
    for root, dirnames, filenames in os.walk(src_dir):
        if skip_dpattern is not None and skip_dpattern in root:
            continue
        inter_path = path.relpath(root, src_dir)
        dest_root = path.join(dest_dir, inter_path)
        if not path.exists(dest_root):
            os.makedirs(dest_root)
        for fname in filenames:
            if skip_fpattern is not None and skip_fpattern in fname:
                continue
            fpath = path.join(root, fname)
            dest_fpath = path.join(dest_root, fname)
            # print(fpath + " >>>>>> " + dest_fpath)
            shutil.copy2(fpath, dest_fpath)
