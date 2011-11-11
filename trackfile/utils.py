# -*- coding: utf-8 -*-

from models import DatabaseEntry
import os
import hashlib

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

    def __init__ (self, recipient, src, dest, nbackups = 5):
        """
            Object's constructor

            recipient: GPG Key used to encrypt files. (need to be generated before the execution)
            src: Directory in which files are stored
            dest: Directory where to put encrypted files
            nbackups: number of copies (default = 5)
        """

        self.recipient = recipient
        self.nbackups  = nbackups
        self.src  = src
        self.dest = dest

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

            if os.path.exists (ef) == False:
                os.system ("gpg --output " + ef + " --encrypt --recipient " + self.recipient + " " + f)
            else:
                for i in range (1, self.nbackups + 1):
                    ief = ef.replace (".gpg", "." + str (i) + ".gpg")

                    if os.path.exists (ief) == False:
                        os.system ("gpg --output " + ief + " --encrypt --recipient " + self.recipient + " " + f)
                        ef = ief
                        break

            ret.append ((f, ef))

        return ret

    def decrypt (self, filelist):
        """
            Decrypt files using GnuPG
        """

        pass

class FileManager:
    """ Object implementing all previously created objects. """

    def __init__ (self, recipient, src, dest, nbackups = 5):
        """
            Object's constructor

            See #FileEncrypt constructor for more details.
        """

        self.src = src
        self.fl  = FileListing ()
        self.fh  = FileChecksum ()
        self.fe  = FileEncrypt (recipient, src, dest, nbackups)

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
            encrypted = self.fe.encrypt (files)

            data = self._combinedata (checksums, encrypted)

            # Put all data in the database
            for _,filehash,encryptedpath in data:
                dbe = DatabaseEntry (checksum = filehash, path = encryptedpath, sent = 0)
                dbe.save ()

# vim: tabstop=4 shiftwidth=4 expandtab
