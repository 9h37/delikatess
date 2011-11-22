from django.http import HttpResponse
from django.template import RequestContext, loader
from trackfile.models import DatabaseEntry

import os

def home (request):
    entries = DatabaseEntry.objects.all ()

    ## NOTE: Database structure will change in the future.

    # Create JSON tree
    json = {"children": []}

    for dbe in entries:
        folders = dbe.path.split (os.sep)
        d = json["children"]

        for name in folders:
            tmp = {}

            # Is it the end of the path ?
            if name == folders[-1]:
                tmp["name"] = str (name)
                tmp["hash"] = str (dbe.checksum)
                tmp["sent"] = dbe.sent
                d.append (tmp)
                break

            # Is it already in the tree ?
            alreadyin = False

            for child in d:
                if child["name"] == name:
                    alreadyin = True

                    # If already in, just go to the next level
                    if "children" in child:
                        d = child["children"]

                    break

            # If not already in, create it
            if alreadyin == False:
                tmp["name"] = str (name)
                tmp["children"] = []

                d.append (tmp)
                d = tmp["children"]

    # Create list for the table
    filelist = []

    for dbe in entries:
        f = {'name': os.path.basename (dbe.path), 'checksum': dbe.checksum, 'size': 'unknow', 'date': dbe.sent}
        filelist.append (f)

    # Load template
    t = loader.get_template ("index.html")
    c = RequestContext (request, {
        'filelist': filelist,
        'jsontree': json,
    })

    return HttpResponse (t.render (c))

# vim: tabstop=4 shiftwidth=4 expandtab

