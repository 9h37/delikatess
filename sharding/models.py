from django.db import models

class Block (models.Model):
     blockid  = models.CharField (max_length = 256)
     blockurl = models.CharField (max_length = 256)

# vim: tabstop=4 shiftwidth=4 expandtab
