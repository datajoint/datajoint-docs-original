
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

# # this should probably be specified in a file outside - this is the actual build that we want to see on the website
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


def pick_tag(future_tags, raw_tags, lang):
    to_sort = []
    for tag in future_tags[lang]:
        tag_out = [rtag for rtag in raw_tags[lang] if rtag.startswith(tag)] # TODO swap out the raw_tags with actual git tags from repo
        to_sort.append(tag_out)
    print(to_sort)
    newest_version = []
    for versions in to_sort:
        ver_list = []
        for ver in versions:
            # print(ver)
            # choose the patch version i.e. 4 in v3.2.4
            try: 
                vp = ver.split('.', 2)[2]
            except IndexError: 
                vp = "0"
            if '-dev' in vp:
                print("-dev here!")
                break
            else:
                ver_list.append(int(vp)) 
        print(ver_list)
        if len(ver_list) > 0:
            newest_patch = max(ver_list)
            for ver in versions:
                if newest_patch == 0 and len(ver.split('.')) < 3:
                    newest_version.append(ver) 
                    print(ver + " tag probably needs to be fixed to " + ver + ".0")
                elif len(ver.split('.')) == 3 and ver.split('.', 2)[2] == str(newest_patch):
                    newest_version.append(ver)
    print(newest_version)
    return newest_version

# pick_tag(to_make_tags, git_tags,  "matlab")
