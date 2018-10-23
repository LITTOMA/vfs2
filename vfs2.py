import struct


class VFS2(object):

    class Folder(object):
        def __init__(self, fs):
            (self.unk1, self.id, 
            self.unk2, self.unk3, 
            self.file_id_start) = struct.unpack('iiiii', fs.read(struct.calcsize('iiiii')))
            self.files = []

    class File(object):
        def __init__(self, fs):
            (self.unk1, self.id, 
            self.compress_type, self.folder_id, 
            self.data_offset, self.data_size) = struct.unpack('iiiiii', fs.read(struct.calcsize('iiiiii')))

    def __init__(self, fp=None):
        if fp:
            self.load_vfs2(fp)
        else:
            #Create a vfs2 object if no file input. (Default)
            self.create_vfs2()

    #Pass a 'file' object as 'fp' here is recommended.
    def load_vfs2(self, fp):
        if isinstance(fp, str):
            fp = open(fp, 'rb')
        if not isinstance(fp, file):
            raise TypeError('No file input.')
        
        sig = fp.read(4)
        if sig != 'VFS2':
            raise TypeError("Signature error. Except: VFS2, actual: %s"%sig)

        folder_count ,= struct.unpack('i', fp.read(4))
        self.folders = []
        for i in range(folder_count):
            self.folders.append(VFS2.Folder(fp))

        file_count ,= struct.unpack('i', fp.read(4))
        self.files = []
        for i in range(file_count):
            self.files.append(VFS2.File(fp))

    def create_vfs2(self):
        pass
    
    def add_file(self, folder, file_path):
        pass
    
    def create_folder(self, folder, name):
        pass
    
    def exists(self, path):
        pass
    
    def extract(self, out_dir):
        pass
    
    def list(self):
        pass

    def save(self, path):
        pass


if '__main__' == __name__:
    vfs = VFS2('data.vfs')
    print vfs