from django.http import HttpResponse
from django.template import RequestContext, loader
from trackfile.models import DatabaseEntry

import os

def home (request):
    entries = DatabaseEntry.objects.all ()

    # Create JSON tree
    json = {}

    for dbe in entries:
        folders = dbe.path.split (os.sep)
        d = json

        for name in folders:
            # Is it the end of path ?
            if name == folders[-1]:
                d[name] = (dbe.checksum, dbe.sent)
            # If not in the tree, create it
            elif name not in d:
                d[name] = {}

            d = d[name]

    # Create list for the table
    filelist = []

    for dbe in entries:
        f = {'name': os.path.basename (dbe.path), 'checksum': dbe.checksum, 'size': 'unknow', 'date': dbe.sent}
        filelist.append (f)

    # Load template
    t = loader.get_template ("index.html")
    c = RequestContext (request, {
        'filelist': filelist,
        'json-tree': json,
    })

    return HttpResponse (t.render (c))

# vim: tabstop=4 shiftwidth=4 expandtab

