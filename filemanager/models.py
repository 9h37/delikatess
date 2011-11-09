from django.db import models

class DatabaseEntry (models.Model):
    checksum = models.CharField (max_length = 64)
    path = models.CharField (max_length = 256)
    sent = models.BooleanField ()

    def is_sent (self):
        return self.sent

    def is_checksum_equal (self, sha256):
        return self.checksum == sha256

    def restore (self):
        pass


# vim: tabstop=4 shiftwidth=4 expandtab
