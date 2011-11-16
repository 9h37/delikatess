from django.http import HttpResponse
from django.template import Context, loader
from trackfile.models import DatabaseEntry

def home (request):
    filelist = DatabaseEntry.objects.all ()
    t = loader.get_template ('index.html')

    c = Context ({
        'filelist': filelist,
    })

    return HttpResponse (t.render (c))

# vim: tabstop=4 shiftwidth=4 expandtab

