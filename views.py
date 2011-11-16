from django.http import HttpResponse
import bootstrap

def home (request):
     return HttpResponse ("<h1>It works!</h1>")
