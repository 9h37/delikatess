"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import utils
import os

GPG_KEY = "linkdd@goldorak"

class TestFileManager (TestCase):
    def setUp (self):
        self.src  = "/home/linkdd/devel/9h37/tests/src/"
        self.dest = "/home/linkdd/devel/9h37/tests/dest/"
        self.nbackups = 7


        # Data for test_01_readdir
        self.fl = utils.FileListing ()
        self.files     = [ self.src + "oops", self.src + "test", self.src + "try/subdir" ]

        # Data for test_02_checksum
        self.fh = utils.FileChecksum ()
        self.checksums = [
            (self.src + "oops",       "fe19778cf1ce280658154f2b9c01ffbccd825a23460141dcf3794e7a2c0eb629"),
            (self.src + "test",       "f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2"),
            (self.src + "try/subdir", "455ac1a4cc8343055b41a27005077fa934b95a0090676f1111cc1fbf1d4d2091")
        ]

        # Data for test_03_gpg
        self.fe = utils.FileEncrypt (GPG_KEY, self.src, self.dest, nbackups = self.nbackups)
        self.encrypted = [
            (self.src + "oops", self.dest + "oops.gpg"),
            (self.src + "test", self.dest + "test.gpg"),
            (self.src + "try/subdir", self.dest + "try/subdir.gpg")
        ]

        for i in range (1, self.nbackups + 1):
            self.encrypted = self.encrypted + [
                (self.src + "oops", self.dest + "oops." + str (i) + ".gpg"),
                (self.src + "test", self.dest + "test." + str (i) + ".gpg"),
                (self.src + "try/subdir", self.dest + "try/subdir." + str (i) + ".gpg")
            ]

    # Test #FileListing object
    def test_01_readdir (self):
        filelist = self.fl.readdir (self.src)

        for f in filelist:
            self.assertTrue (f in self.files, f)

    # Test #FileChecksum object
    def test_02_checksum (self):
        checksums = self.fh.checksum (self.files)

        for c in checksums:
            self.assertTrue (c in self.checksums, c)

    # Test #FileEncrypt object
    def test_03_gpg (self):
        encrypted = self.fe.encrypt (self.files)

        for i in range (1, self.nbackups + 1):
            encrypted = encrypted + self.fe.encrypt (self.files)

        for e in encrypted:
            self.assertTrue (e in self.encrypted, e)
            self.assertTrue (os.path.exists (e[1]), e[1])


# vim: tabstop=4 shiftwidth=4 expandtab

