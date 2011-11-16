# -*- coding: utf-8 -*-

from models import DatabaseEntry
import os
import hashlib
import re

class FileListing:
    """ Object use to list files recursively """

    def __init__ (self):
        pass

    def readdir (self, path):
        """
            List files recursively.

            path: Directory to list.
            return: List of files containned in @path and its subdirs.
        """
        ret = []

        for filename in os.listdir (path):
            abspath = os.path.join (path, filename)

            if os.path.isdir (abspath) == True:
                ret = ret + self.readdir (abspath)
            else:
                ret.append (abspath)

        return ret

class FileChecksum:
    """ Object used to get files' checksum. """

    def __init__ (self):
        pass

    def checksum (self, filelist, block_size = 512):
        """
            Get checksum of each files

            filelist: List of files to hash (can be obtained with the #FileListing object
            block_size: Files are read by block of data, this param define the size in bytes of those block (default = 512)
            return: A list of tuples (filepath, filehash)
        """
        ret = []

        for f in filelist:
            h = hashlib.sha256 ()

            try:
                fd = open (f, "rb")
            except IOError:
                print "Can't open :", f
            else:
                while True:
                    data = fd.read (block_size)

                    if not data:
                        break

                    h.update (data)

                fd.close ()
                ret.append ((f, h.hexdigest ()))

        return ret

class FileEncrypt:
    """ Object used to encrypt a list of files. """

    def __init__ (self, recipient, src, dest, nbackups = 5, extra_opts = ""):
        """
            Object's constructor

            recipient: GPG Key used to encrypt files. (need to be generated before the execution)
            src: Directory in which files are stored
            dest: Directory where to put encrypted files
            nbackups: number of copies (default = 5)
        """

        self.extra_opts = extra_opts
        self.recipient  = recipient
        self.nbackups   = nbackups
        self.src  = src
        self.dest = dest

        self.pattern = re.compile (r"(\.\d+)*.gpg")

    def _backup (self, path, iterate = 1):
        """
            Internal function which backup existant encrypted files.

            path: Path of the original file
            iterate: Internal param for the recursivity
        """

        npath = self.pattern.sub ("." + str (iterate) + ".gpg", path)

        if os.path.exists (npath) == True:
            self._backup (npath, iterate + 1)

        if iterate <= self.nbackups + 1:
            # Rename the file
            os.rename (path, npath)

            # Update the database
            try:
                dbe = DatabaseEntry.objects.get (path = path)
            except DatabaseEntry.DoesNotExist:
                pass
            else:
                dbe.path = npath
                dbe.save ()

    def encrypt (self, filelist):
        """
            Encrypt files using GnuPG

            filelist: List of files to encrypt (files stored in @self.src)
            return: List of tuples (filepath, encryptedpath)
        """

        ret = []

        for f in filelist:
            ef = f.replace (self.src, self.dest) + ".gpg"
            dirname = os.path.dirname (ef)

            if os.path.exists (dirname) == False:
                os.makedirs (dirname)

            if os.path.exists (ef):
                self._backup (ef)

            os.system ("gpg {0} --output {1} --encrypt --recipient {2} {3}".format (self.extra_opts, ef, self.recipient, f)
            ret.append ((f, ef))

        return ret

    def decrypt (self, filelist):
        """
            Decrypt files using GnuPG
        """

        pass

class FileManager:
    """ Object implementing all previously created objects. """

    def __init__ (self, recipient, src, dest, nbackups = 5, extra_gpg_opts = ""):
        """
            Object's constructor

            See #FileEncrypt constructor for more details.
        """

        self.src = src
        self.fl  = FileListing ()
        self.fh  = FileChecksum ()
        self.fe  = FileEncrypt (recipient, src, dest, nbackups, extra_gpg_opts)

    def _combinedata (self, checksums, encrypted):
        """
            Combine data in one list of tuples.

            checksums: List of tuples: (path, checksum) returned by #FileChecksum.checksum
            encrypted: List of tuples: (path, encrypted_path) returned by #FileEncrypt.encrypt
            return: List of tuples: (path, checksum, encrypted_path)
        """
        ret = []

        for path,checksum in checksums:
            for path2,encrypted_path in encrypted:
                if path == path2:
                    ret.append ((path, checksum, encrypted_path))
                    break

        return ret

    def run (self):
        """
            Do: Listing, hash and encryption.
        """

        try:
            if os.path.exists (self.src) == False:
                raise self.src + ": path doesn't exists."
        except Exception as e:
            print e
        else:
            files     = self.fl.readdir (self.src)
            checksums = self.fh.checksum (files)

            to_encrypt = files

            for dbe in DatabaseEntry.objects.all ():
                # Check if file's checksum is already in the database
                for f,h in checksums:
                    # If yes, don't need to encrypt it
                    if dbe.checksum == h:
                        to_encrypt.remove (f)
                        break

            # Now, delete unused checksums from the list
            for c in checksums:
                if c[0] not in to_encrypt:
                    checksums.remove (c)

            # Encrypt only files which are not in the database
            encrypted = self.fe.encrypt (to_encrypt)

            data = self._combinedata (checksums, encrypted)

            # Put all data in the database
            for _,filehash,encryptedpath in data:
                dbe = DatabaseEntry (checksum = filehash, path = encryptedpath, sent = 0)
                dbe.save ()

# vim: tabstop=4 shiftwidth=4 expandtab
