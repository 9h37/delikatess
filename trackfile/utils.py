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

     def __init__ (self, filelist):
          """
               Object's constructor

               filelist: List of files to hash (can be obtained with the FileListing object
          """
          self.filelist = filelist

     def checksum (self, block_size = 512):
          """
               Get checksum of each files

               block_size: Files are read by block of data, this param define the size in bytes of those block (default = 512)
               return: A list of tuples (filepath, filehash)
          """
          ret = []

          for f in self.filelist:
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
               return: List of tuples (filepath, encryptedfilepath)
          """

          ret = []
          gpg_argv = ["gpg", "--output", None, "--encrypt", "--recipient", self.recipient, None]

          for f in filelist:
               ef = f.replace (self.src, self.dest) + ".gpg"
               dirname = os.path.dirname (ef)

               if os.path.exists (dirname) == False:
                    os.makedirs (dirname)

               gpg_argv[6] = f

               if os.path.exists (ef) == False:
                    gpg_argv[2] = ef
                    os.execvp ("gpg", gpg_argv)
               else:
                    for i in range (1, self.nbackups + 1):
                         ief = ef.replace (".gpg", "." + str (i) + ".gpg")

                         if os.path.exists (ief) == False:
                              gpg_argv[2] = ef
                              os.execvp ("gpg", gpg_argv)
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

     def __init__ (self):
          pass

# vim: tabstop=4 shiftwidth=4 expandtab
