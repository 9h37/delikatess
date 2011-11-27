from django.http import HttpResponse

def head (request, id_client):
     return HttpResponse ("")

def files (request, id_client, id_rev):
     return HttpResponse ("")

def blocks (request, id_client, id_rev):
     return HttpResponse ("")

# vim: tabstop=4 shiftwidth=4 expandtab
