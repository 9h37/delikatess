# -*- coding: utf-8 -*-

from django.db import models

class DatabaseEntry (models.Model):
     checksum = models.CharField (max_length = 64)
     path     = models.CharField (max_length = 256)
     sent     = models.DateTimeField ()

# vim: tabstop=4 shiftwidth=4 expandtab
