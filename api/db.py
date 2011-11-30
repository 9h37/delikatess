from utils import openlock
import os

def AssertPathExists (path):
    if not os.path.exists (path):
        raise IOError ("Path doesn't exists : {}".format (path))

class Manifest:
    def __init__ (self, associated_file, diffs = 5):
        self.file = associated_file
        self.diffs = diffs
        self.paths = []

        AssertPathExists (self.file.path)

        for m in os.listdir (self.file.path):
            self.paths.append (os.path.join (self.file.path, m))

        self.paths.sort ()

    def checksum_in_db (self, checksum):
        for path in self.paths:
            m = openlock (path)
            d = eval (m.read ())

            for rev in d:
                if rev == checksum:
                    continue

                for blockid in d[rev]:
                    if checksum == d[rev][blockid]:
                        return (rev, blockid, checksum)

        return None

    def add_block (self, block):
        rev      = block[0]
        blockid  = block[1]
        checksum = block[2]

        mid = rev / self.diffs

        if mid >= len (self.paths):
            self.paths.append (os.path.join (self.file.path, "Manifest.{}".format (mid)))

            # Manifest.HEAD = Manifest.mid

        m = openlock (self.paths[mid], "rw")
        d = eval (m.read ())

        if rev not in d:
            d[rev] = {}

            # Manifest.HEAD : d["HEAD"] = rev

        d[rev][blockid] = checksum

        # empty file
        m.write (str (d))
        m.closeunlock ()

    def del_block (self, block):
        pass

class File:
    def __init__ (self, rev, info):
        self.name = info["name"]
        self.hash = info["hash"]
        self.blocksize = info["blocksize"]
        #...

        self.rev  = rev
        self.path = os.path.join (rev.path, self.hash)

        self.manifest = Manifest (self)

    def get_info (self):
        pass

    def filecut (self):
        pass

class Revision:
    def __init__ (self, db, revid):
        self.path = os.path.join (db.path, "revs", revid)
        self.id = revid
        self.db = db

        AssertPathExists (self.path)

        f = openlock (os.path.join (self.path, "files"))
        json = eval (f.read ())
        f.closeunlock ()

        self.files = []

        for filename in json:
            json[filename]["name"] = filename
            self.files.append (File (self, json[filename]))

    def get_files (self):
        pass

    def add_file (self, f):
        pass

    def del_file (self, f):
        pass

class Database:
    def __init__ (self, path, id_client):
        self.id_client = id_client
        self.path = os.path.join (path, id_client)
        self.revs = []

        AssertPathExists (self.path)

        for r in os.listdir (self.path):
            self.revs.append (Revision (self, r))

    def get_revs (self):
        pass

    def add_rev (self, revid):
        pass

    def del_rev (self, revid):
        pass

# vim: tabstop=4 shiftwidth=4 expandtab
